# Integração MCP

Dependência fixada: SDK Python `mcp==2.3.0`. O teste usa `mcp.Client` e `StdioServerParameters`, executando `python -m rotadev.server` em subprocesso. Compatibilidade foi verificada com esse cliente; não se presume compatibilidade com toda aplicação ou versão do protocolo.

Exemplo de configuração para um cliente que aceite `mcpServers`:

```json
{
  "mcpServers": {
    "rotadev": {
      "command": "/caminho/absoluto/.venv/bin/python",
      "args": ["-m", "rotadev.server"]
    }
  }
}
```

No Windows, substitua por `C:\\caminho\\.venv\\Scripts\\python.exe`. Instale o pacote nesse ambiente primeiro. O formato de configuração é um exemplo: confirme o formato exigido por seu cliente. Não inclua credenciais. O servidor funciona sem `cwd` quando instalado.

| Ferramenta | Entradas principais | Retorno |
| --- | --- | --- |
| consultar_trilha | tecnologia, nivel opcional | trilha com módulos e desafios |
| gerar_desafio | tecnologia, nivel, seed opcional | desafio e critérios |
| gerar_certificado | tecnologia, nivel, nome, concluidos; data/formato opcionais | conteúdo demonstrativo e metadados |

As saídas possuem `structured_content`. Entradas de domínio inválidas retornam erro de ferramenta, sem simular sucesso. O recurso `rotadev://catalogo` fornece JSON das 30 trilhas; o prompt `planejar_trilha` usa os módulos do catálogo e não atesta conclusão.

Exemplo de argumentos para `gerar_certificado`:

```json
{"tecnologia":"Python","nivel":"iniciante","nome":"Pessoa Exemplo","concluidos":["m1","m2","m3","m4"],"data":"2026-11-22","formato":"md"}
```

O transporte local não concede acesso ao sistema inteiro. Este servidor não expõe shell, rede, escrita de arquivos ou credenciais. Anotações MCP descrevem comportamento; não substituem revisão do código e permissões do processo. O cliente pode receber os nomes que informar: use dados de exemplo.

Referência de API: [SDK Python oficial](https://github.com/modelcontextprotocol/python-sdk).
