"""Servidor MCP stdio. Não executa shell nem grava arquivos."""

import json
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations

from .core import DomainError, catalogo, trilha, desafio, certificado

mcp = MCPServer('RotaDev')
READ_ONLY = ToolAnnotations(read_only_hint=True, destructive_hint=False, open_world_hint=False)


def _executar(func, *args):
    try:
        return func(*args)
    except DomainError as exc:
        raise ToolError(str(exc)) from exc


@mcp.tool(annotations=READ_ONLY)
def consultar_trilha(tecnologia: str, nivel: str = 'iniciante') -> dict[str, object]:
    """Consulte módulos de uma trilha fictícia. Níveis: iniciante, intermediario, avancado."""
    return _executar(trilha, tecnologia, nivel)


@mcp.tool(annotations=READ_ONLY)
def gerar_desafio(tecnologia: str, nivel: str, seed: int | None = None) -> dict[str, object]:
    """Selecione um desafio de código; seed permite uma seleção reproduzível."""
    return _executar(desafio, tecnologia, nivel, seed)


@mcp.tool(annotations=READ_ONLY)
def gerar_certificado(tecnologia: str, nivel: str, nome: str, concluidos: list[str],
                      data: str | None = None, formato: str = 'md') -> dict[str, object]:
    """Retorne documento fictício sem validade oficial. Exige todos os IDs dos módulos.

    Conclusão informada pelo usuário; não verifica identidade, avaliação ou presença.
    Retorna conteúdo; não cria arquivo nem publica dados.
    """
    return _executar(certificado, tecnologia, nivel, nome, concluidos, data, formato)


@mcp.resource('rotadev://catalogo', mime_type='application/json')
def consultar_catalogo() -> str:
    """Catálogo sintético de 30 trilhas e seus módulos e desafios."""
    return json.dumps(catalogo(), ensure_ascii=False)


@mcp.prompt()
def planejar_trilha(tecnologia: str, nivel: str = 'iniciante') -> str:
    """Prepare um plano a partir dos módulos reais do catálogo local."""
    selected = trilha(tecnologia, nivel)
    return ('Organize um plano para esta trilha fictícia. Preserve a ordem dos módulos, '
            'diferencie estimativa de horas de tempo realizado e não invente conclusão ou certificado oficial.\n'
            + json.dumps(selected, ensure_ascii=False))


def main() -> None:
    mcp.run(transport='stdio')


if __name__ == '__main__':
    main()
