# RotaDev

Consulta de trilhas de programação, seleção de desafios e geração de declarações demonstrativas, com interface de terminal e servidor MCP local.

Organizei o produto em um núcleo de regras compartilhado pelas duas interfaces. O catálogo contém 30 trilhas sintéticas: dez tecnologias em três níveis, com quatro módulos e dois desafios por trilha. Nenhum dado representa matrícula, presença ou certificação real.

## Instalação

Python 3.11 ou superior. A validação local foi executada em Python 3.14 no Windows. Não exige conta, serviço remoto ou chave de API.

```console
python -m venv .venv
.venv\Scripts\python -m pip install ".[test]"
```

Em Linux/macOS, use `.venv/bin/python` no lugar de `.venv\Scripts\python`.

## Comandos

```console
rotadev catalogo
rotadev trilha Python --nivel iniciante
rotadev desafio Python avancado --seed 7
rotadev certificado Python iniciante --nome "Pessoa Exemplo" --concluidos m1,m2,m3,m4 --data 2026-11-22
rotadev certificado Java iniciante --nome "Pessoa Exemplo" --concluidos m1,m2,m3,m4 --formato html --saida demonstracao.html
```

Após ativar o ambiente virtual, os comandos acima ficam disponíveis. Sem ativação, execute `.venv\Scripts\rotadev` ou `python -m rotadev` com o Python do ambiente.

Também são aceitos `/trilha`, `/desafio` e `/certificado` no terminal. Os arquivos em [commands](commands) documentam o contrato de cada comando para clientes de chat; a execução real depende da integração MCP do cliente.

As consultas retornam JSON. O desafio usa aleatoriedade local, ou seleção reproduzível quando recebe `--seed`. Tecnologias: Python, Java, JavaScript, TypeScript, SQL, Go, Rust, C#, Kotlin e Swift. Níveis: `iniciante`, `intermediario`, `avancado`. JavaScript/TypeScript aceitam `js`/`ts`.

O comando `certificado` exige os quatro IDs, sem repetição, e produz **documento fictício, sem validade acadêmica, profissional ou oficial**. A conclusão é autodeclarada; a referência hash não é validação institucional. O programa não comprova identidade, presença ou avaliação. `--saida` cria um arquivo novo e recusa sobrescrever um existente. Não envie nomes reais sem necessidade.

## MCP

```console
rotadev-mcp
```

O processo usa **stdio**: não abre uma porta HTTP. Seu stdout é reservado ao protocolo. Disponibiliza as ferramentas `consultar_trilha`, `gerar_desafio` e `gerar_certificado`, o recurso `rotadev://catalogo` e o prompt `planejar_trilha`. As ferramentas retornam dados e não executam shell, publicam conteúdo ou gravam arquivos. Consulte [configuração e chamadas](docs/mcp.md).

## Testes

```console
python -m coverage erase
python -m coverage run -m unittest discover -s tests -v
python -m coverage combine
python -m coverage report
```

Validação em 22/11/2026: **13 testes aprovados; cobertura de linhas e ramificações combinadas de 96%**. Inclui CLI em subprocessos, recusa de sobrescrita, escape de conteúdo e cliente MCP conectado por stdio a um processo real. O caminho de erro MCP por módulos incompletos é esperado e deve retornar `is_error`, com mensagem legível. [Detalhes e limites](docs/validacao.md).

## Estrutura e decisões

- `rotadev/core.py`: normalização, seleção, validação e documentos.
- `rotadev/data/catalogo.json`: catálogo sintético versionado.
- `rotadev/cli.py`: entrada e saída pelo terminal.
- `rotadev/server.py`: ferramentas, recurso e prompt MCP.
- `tests/`: contratos do domínio e integração das interfaces.

Mantive o domínio independente do SDK para compartilhar validações e evitar divergências entre terminal e MCP. A busca é linear em um catálogo pequeno e a leitura JSON usa cache; cada consulta devolve cópia independente. Não há persistência de progresso. [Arquitetura](docs/arquitetura.md).

## Próximos passos

Persistência opcional com consentimento, internacionalização e validação de desafios por execução isolada. Essas funcionalidades ainda não estão implementadas. O catálogo e as horas são referências fictícias, não métricas de uso.

Licença [MIT](LICENSE).
