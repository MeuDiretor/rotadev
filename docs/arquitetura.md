# Arquitetura

CLI e MCP chamam o mesmo domínio, que lê um catálogo JSON empacotado. Não há banco ou serviço externo. O domínio rejeita combinações ausentes, módulos duplicados/inventados, datas inválidas e nomes com caracteres de controle.

Os nomes são escapados em Markdown e HTML. O identificador determinístico do documento é uma referência de conteúdo, não assinatura digital ou prova de autenticidade. A CLI escreve somente quando `--saida` é fornecido e usa criação exclusiva. MCP retorna conteúdo sem escrever.

Decisões: catálogo estático para funcionamento offline; cópias independentes para impedir que um consumidor modifique consultas futuras; gerador com semente opcional para reproduzir desafios; funções de domínio separadas de I/O para facilitar testes. Não há autenticação porque não existe serviço de rede; expor o processo por outro transporte exigiria projeto e validação adicionais.

Limites: horas e trilhas sintéticas; nenhuma verificação de identidade ou aprendizado; nenhum executor de código ou acompanhamento persistente. Cobertura automatizada não prova segurança integral.
