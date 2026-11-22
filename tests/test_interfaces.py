import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from mcp import Client
from mcp.client.stdio import StdioServerParameters

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, '-m', 'rotadev', *args], cwd=ROOT,
                              capture_output=True, text=True, encoding='utf-8', timeout=10)

    def test_fluxo_trilha_desafio_certificado(self):
        result = self.run_cli('trilha', 'Java', '--nivel', 'iniciante')
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual('java-iniciante', json.loads(result.stdout)['id'])
        challenge = self.run_cli('desafio', 'Java', 'iniciante', '--seed', '4')
        self.assertEqual(0, challenge.returncode, challenge.stderr)
        self.assertTrue(json.loads(challenge.stdout)['criterios'])
        certificate = self.run_cli('certificado', 'Java', 'iniciante', '--nome', 'Pessoa Exemplo',
                                   '--concluidos', 'm1,m2,m3,m4', '--data', '2026-11-22')
        self.assertEqual(0, certificate.returncode, certificate.stderr)
        self.assertIn('fictício', certificate.stdout)

    def test_erros_legiveis_sem_traceback_e_nao_emitem_documento(self):
        for args in [('trilha', 'desconhecida'), ('certificado', 'Java', 'iniciante', '--nome', 'Pessoa', '--concluidos', 'm1')]:
            result = self.run_cli(*args)
            self.assertEqual(2, result.returncode)
            self.assertNotIn('Traceback', result.stderr)
            self.assertFalse(result.stdout)

    def test_alias_barra_e_catalogo(self):
        result = self.run_cli('/trilha', 'Python')
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(30, len(json.loads(self.run_cli('catalogo').stdout)))

    def test_saida_nova_e_recusa_sobrescrita(self):
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder) / 'documento.html'
            args = ('certificado', 'Python', 'iniciante', '--nome', 'Pessoa Exemplo',
                    '--concluidos', 'm1,m2,m3,m4', '--formato', 'html', '--saida', str(dest))
            self.assertEqual(0, self.run_cli(*args).returncode)
            original = dest.read_bytes()
            self.assertIn(b'SEM VALIDADE', original)
            self.assertEqual(2, self.run_cli(*args).returncode)
            self.assertEqual(original, dest.read_bytes())


class McpTests(unittest.IsolatedAsyncioTestCase):
    async def test_conexao_stdio_real_descoberta_chamadas_e_erro(self):
        coverage_env = {k: v for k, v in os.environ.items() if k.startswith('COVERAGE_')}
        params = StdioServerParameters(command=sys.executable, args=['-m', 'rotadev.server'], cwd=ROOT, env=coverage_env)
        async with Client(params, read_timeout_seconds=10) as client:
            tools = await client.list_tools()
            self.assertEqual({'consultar_trilha', 'gerar_desafio', 'gerar_certificado'}, {t.name for t in tools.tools})
            track = await client.call_tool('consultar_trilha', {'tecnologia': 'Python'})
            self.assertEqual('python-iniciante', track.structured_content['id'])
            challenge = await client.call_tool('gerar_desafio', {'tecnologia': 'Python', 'nivel': 'avancado', 'seed': 3})
            self.assertEqual('avancado', challenge.structured_content['nivel'])
            cert = await client.call_tool('gerar_certificado', {'tecnologia': 'Python', 'nivel': 'iniciante',
                'nome': 'Pessoa Exemplo', 'concluidos': ['m1', 'm2', 'm3', 'm4'], 'data': '2026-11-22'})
            self.assertTrue(cert.structured_content['demonstrativo'])
            bad = await client.call_tool('gerar_certificado', {'tecnologia': 'Python', 'nivel': 'iniciante',
                'nome': 'Pessoa Exemplo', 'concluidos': ['m1']})
            self.assertTrue(bad.is_error)
            self.assertIn('todos os IDs', bad.content[0].text)
            resource = await client.read_resource('rotadev://catalogo')
            self.assertEqual(30, len(json.loads(resource.contents[0].text)))
            prompts = await client.list_prompts()
            self.assertIn('planejar_trilha', {p.name for p in prompts.prompts})
            prompt = await client.get_prompt('planejar_trilha', {'tecnologia': 'Python', 'nivel': 'iniciante'})
            self.assertIn('Python', prompt.messages[0].content.text)


if __name__ == '__main__':
    unittest.main()
