import re
import unittest

from rotadev.core import catalogo, trilha, desafio, certificado, DomainError


class CatalogoTests(unittest.TestCase):
    def test_trinta_trilhas_unicas_com_desafios_por_nivel(self):
        items = catalogo()
        self.assertEqual(30, len(items))
        self.assertEqual(30, len({t['id'] for t in items}))
        for t in items:
            self.assertEqual(4, len(t['modulos']))
            self.assertGreaterEqual(len(t['desafios']), 2)
            self.assertTrue(all(m['objetivo'] for m in t['modulos']))

    def test_busca_normaliza_e_nao_modifica_catalogo(self):
        t = trilha('  PYTHON ', 'iniciante')
        self.assertEqual('python-iniciante', t['id'])
        t['modulos'].clear()
        self.assertEqual(4, len(trilha('Python', 'iniciante')['modulos']))

    def test_tecnologia_e_nivel_inexistentes(self):
        for tech, level in [('x', 'iniciante'), ('Python', 'mestre'), ('', 'iniciante')]:
            with self.subTest(tech=tech, level=level), self.assertRaises(DomainError):
                trilha(tech, level)

    def test_desafio_reprodutivel_do_nivel_solicitado(self):
        a = desafio('Java', 'avancado', seed=7)
        self.assertEqual(a, desafio('Java', 'avancado', seed=7))
        self.assertEqual('avancado', a['nivel'])
        self.assertIn(a['id'], {c['id'] for c in trilha('Java', 'avancado')['desafios']})
        self.assertTrue(a['criterios'])


class CertificadoTests(unittest.TestCase):
    def setUp(self):
        self.modules = [m['id'] for m in trilha('Python', 'iniciante')['modulos']]

    def test_requer_todos_modulos_sem_ids_inventados(self):
        for modules in [[], self.modules[:-1], self.modules + ['inventado'], self.modules + [self.modules[0]]]:
            with self.subTest(modules=modules), self.assertRaises(DomainError):
                certificado('Python', 'iniciante', 'Pessoa Exemplo', modules, '2026-11-22')

    def test_html_escapa_nome_e_identifica_demonstracao(self):
        output = certificado('Python', 'iniciante', '<script>alert(1)</script>', self.modules, '2026-11-22', 'html')
        self.assertNotIn('<script>', output['conteudo'])
        self.assertIn('&lt;script&gt;', output['conteudo'])
        self.assertIn('SEM VALIDADE', output['conteudo'])
        self.assertEqual('text/html', output['mime_type'])

    def test_markdown_deterministico_e_data_valida(self):
        args = ('Python', 'iniciante', 'Pessoa Exemplo', self.modules, '2026-11-22')
        first = certificado(*args)
        self.assertEqual(first, certificado(*args))
        self.assertIn('fictício', first['conteudo'])
        self.assertRegex(first['id'], r'^[a-f0-9]{16}$')
        for value in ['2026-02-30', 'ontem']:
            with self.assertRaises(DomainError):
                certificado('Python', 'iniciante', 'Pessoa Exemplo', self.modules, value)

    def test_rejeita_nome_vazio_controle_e_formato_invalido(self):
        for name in ['', '  ', 'A\x00B', 'x' * 121]:
            with self.assertRaises(DomainError):
                certificado('Python', 'iniciante', name, self.modules, '2026-11-22')
        with self.assertRaises(DomainError):
            certificado('Python', 'iniciante', 'Nome', self.modules, '2026-11-22', 'exe')


if __name__ == '__main__':
    unittest.main()
