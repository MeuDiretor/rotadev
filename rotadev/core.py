"""Regras de domínio compartilhadas pela CLI e pelo servidor MCP."""

from copy import deepcopy
from datetime import date
from functools import lru_cache
import hashlib
import html
import json
from pathlib import Path
import random
import re
import unicodedata


class DomainError(ValueError):
    """Entrada incompatível com o catálogo ou com o contrato do comando."""


def _normalizar(value: str) -> str:
    if not isinstance(value, str):
        raise DomainError('Informe tecnologia e nível como texto.')
    text = ''.join(c for c in unicodedata.normalize('NFKD', value.strip().lower()) if not unicodedata.combining(c))
    return {'js': 'javascript', 'ts': 'typescript', 'c#': 'csharp', 'golang': 'go'}.get(text, text)


@lru_cache(maxsize=1)
def _dados() -> list[dict]:
    return json.loads((Path(__file__).parent / 'data' / 'catalogo.json').read_text(encoding='utf-8'))


def catalogo() -> list[dict]:
    """Retorna uma cópia independente das trilhas fictícias."""
    return deepcopy(_dados())


def trilha(tecnologia: str, nivel: str = 'iniciante') -> dict:
    tech, level = _normalizar(tecnologia), _normalizar(nivel)
    for item in _dados():
        if item['id'] == f'{tech}-{level}':
            return deepcopy(item)
    raise DomainError('Trilha não encontrada. Consulte o catálogo e use iniciante, intermediario ou avancado.')


def desafio(tecnologia: str, nivel: str, seed: int | None = None) -> dict:
    """Seleciona um exercício; seed permite reproduzir a mesma seleção."""
    if seed is not None and (not isinstance(seed, int) or isinstance(seed, bool)):
        raise DomainError('A semente deve ser um número inteiro.')
    item = trilha(tecnologia, nivel)
    rng = random.SystemRandom() if seed is None else random.Random(seed)
    selected = deepcopy(rng.choice(item['desafios']))
    return {'trilha_id': item['id'], 'tecnologia': item['tecnologia'], 'nivel': item['nivel'], **selected}


def _nome(value: str) -> str:
    if not isinstance(value, str):
        raise DomainError('Informe um nome de 1 a 120 caracteres.')
    clean = value.strip()
    if not 1 <= len(clean) <= 120 or any(unicodedata.category(c).startswith('C') for c in clean):
        raise DomainError('Informe um nome de 1 a 120 caracteres, sem caracteres de controle.')
    return clean


def certificado(tecnologia: str, nivel: str, nome: str, concluidos: list[str],
                data: str | None = None, formato: str = 'md') -> dict:
    """Gera documento fictício com conclusão informada, sem comprovação oficial."""
    item, name = trilha(tecnologia, nivel), _nome(nome)
    expected = {m['id'] for m in item['modulos']}
    if (not isinstance(concluidos, list) or not all(isinstance(x, str) for x in concluidos)
            or len(concluidos) != len(expected) or set(concluidos) != expected):
        raise DomainError('Informe todos os IDs dos módulos uma única vez, sem IDs desconhecidos.')
    issued = date.today().isoformat() if data is None else data
    if not isinstance(issued, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', issued):
        raise DomainError('Use uma data válida no formato AAAA-MM-DD.')
    try:
        date.fromisoformat(issued)
    except ValueError as exc:
        raise DomainError('Use uma data válida no formato AAAA-MM-DD.') from exc
    if formato not in {'md', 'html'}:
        raise DomainError('Formato disponível: md ou html.')
    ident = hashlib.sha256(json.dumps([item['id'], name, sorted(expected), issued], ensure_ascii=False).encode()).hexdigest()[:16]
    disclaimer = 'Documento fictício e demonstrativo. SEM VALIDADE acadêmica, profissional ou oficial.'
    if formato == 'html':
        content = ('<!doctype html><html lang="pt-BR"><meta charset="utf-8">'
                   '<meta name="viewport" content="width=device-width,initial-scale=1">'
                   '<title>Declaração demonstrativa — RotaDev</title>'
                   '<style>body{font:18px system-ui;background:#f4f6f8;color:#162735;max-width:850px;margin:8vh auto;padding:32px}'
                   'main{border:3px solid #147d78;background:white;padding:40px}strong{color:#9a3412}</style>'
                   f'<main><h1>Declaração demonstrativa</h1><p><strong>{disclaimer}</strong></p>'
                   f'<p>{html.escape(name)} informou a conclusão dos módulos de <b>{html.escape(item["titulo"])}</b>.</p>'
                   f'<p>Data informada: {issued} · Referência local: {ident}</p>'
                   '<p>Conclusão autodeclarada; não verifica identidade, avaliação ou presença.</p></main></html>')
        mime = 'text/html'
    else:
        escaped = re.sub(r'([\\`*_{}\[\]()#+.!|>~-])', r'\\\1', html.escape(name))
        content = (f'# Declaração demonstrativa — RotaDev\n\n**{disclaimer}**\n\n'
                   f'{escaped} informou a conclusão dos módulos de **{item["titulo"]}**.\n\n'
                   f'Data informada: {issued}\n\nReferência local: `{ident}`\n\n'
                   'Conclusão autodeclarada; não verifica identidade, avaliação ou presença.\n')
        mime = 'text/markdown'
    return {'id': ident, 'trilha_id': item['id'], 'data': issued, 'mime_type': mime,
            'demonstrativo': True, 'conteudo': content}
