# Validação observada

Data: 22/11/2026. Ambiente local: Windows, Python 3.14.3, MCP 2.3.0, coverage 7.17.4.

13 testes passaram. Cobertura combinada de linhas/ramificações: 96% (152 instruções, três não percorridas; 36 ramificações, cinco parcialmente percorridas). Domínio 93%, CLI 99%, servidor 97%, inicializadores 100%.

Inclui integridade das 30 trilhas; normalização e isolamento de cópias; seleção reproduzível; rejeição de módulos incompletos, duplicados e desconhecidos; datas e nomes inválidos; escape HTML; CLI com códigos de saída e mensagens; escrita exclusiva sem sobrescrita; descoberta MCP, três chamadas válidas, erro de domínio, recurso JSON e prompt. O teste MCP inicia um processo real e troca mensagens pelo SDK, sem mock do protocolo.

O ambiente de cobertura é repassado explicitamente ao subprocesso MCP porque o SDK filtra variáveis de ambiente. Isso permite medir o código realmente executado, sem alterar as funções da aplicação.

O resultado não significa teste em todas as versões Python ou clientes MCP. A automação de CI é fornecida, mas só um resultado observado de execução remota confirma o estado da CI.
