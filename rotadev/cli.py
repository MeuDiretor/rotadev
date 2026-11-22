"""Interface de linha de comando, com JSON para consultas e texto para documentos."""

import argparse
import json
from pathlib import Path
import sys

from .core import DomainError, catalogo, trilha, desafio, certificado


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0].startswith('/'):
        args[0] = args[0][1:]
    parser = argparse.ArgumentParser(prog='rotadev', description='Consulte trilhas e desafios de um catálogo fictício local.')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('catalogo', help='Listar as 30 trilhas fictícias.')
    track = commands.add_parser('trilha', help='Consultar módulos por tecnologia e nível.')
    track.add_argument('tecnologia')
    track.add_argument('--nivel', default='iniciante')
    challenge = commands.add_parser('desafio', help='Selecionar um desafio do catálogo.')
    challenge.add_argument('tecnologia')
    challenge.add_argument('nivel')
    challenge.add_argument('--seed', type=int, help='Semente opcional para reproduzir a escolha.')
    cert = commands.add_parser('certificado', help='Gerar documento fictício, sem validade oficial.')
    cert.add_argument('tecnologia')
    cert.add_argument('nivel')
    cert.add_argument('--nome', required=True)
    cert.add_argument('--concluidos', required=True, help='IDs dos módulos separados por vírgula: m1,m2,m3,m4.')
    cert.add_argument('--data', help='Data informada AAAA-MM-DD; padrão: hoje no sistema local.')
    cert.add_argument('--formato', choices=['md', 'html'], default='md')
    cert.add_argument('--saida', type=Path, help='Criar arquivo novo; não substitui um arquivo existente.')
    options = parser.parse_args(args)
    try:
        if options.command == 'catalogo':
            result = catalogo()
        elif options.command == 'trilha':
            result = trilha(options.tecnologia, options.nivel)
        elif options.command == 'desafio':
            result = desafio(options.tecnologia, options.nivel, options.seed)
        else:
            result = certificado(options.tecnologia, options.nivel, options.nome,
                                 [s.strip() for s in options.concluidos.split(',')],
                                 options.data, options.formato)
            if options.saida:
                with options.saida.open('x', encoding='utf-8') as file:
                    file.write(result['conteudo'])
                print(f'Documento demonstrativo criado: {options.saida}')
            else:
                print(result['conteudo'])
            return 0
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except DomainError as exc:
        print(f'Erro: {exc}', file=sys.stderr)
        return 2
    except OSError:
        print('Erro: não foi possível criar o arquivo. Confira o diretório e se o destino já existe.', file=sys.stderr)
        return 2
