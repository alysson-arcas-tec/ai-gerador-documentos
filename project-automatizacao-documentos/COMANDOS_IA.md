# Comandos para Cursor, Codex e Claude

Este guia serve para chamar os agentes por linguagem natural, sem precisar digitar o comando manualmente no PowerShell.

## Regra geral

Ao conversar com a IA dentro deste projeto, use comandos nesse formato:

```text
Use o agente <nome-do-agente-ou-documento> com base no arquivo Escopo.docx.
Se faltar informacao, me pergunte antes de gerar.
Gere o arquivo final no formato padrao do projeto.
```

O projeto agora aceita:
- `id` tecnico do agente
- nome do documento
- apelidos humanos como `dicionario da eap`, `infraestrutura`, `backlog sprint 3`, `status report`

## Comandos prontos

### Gerar documento

`Status Report`

```text
Use o agente status report com base no Escopo.docx. Se faltar informacao, me pergunte. Gere o Status Report.docx final.
```

`Solicitacao de Mudanca de Escopo`

```text
Use o agente solicitacao de mudanca de escopo com base no Escopo.docx. Se faltar informacao, me pergunte. Gere o documento final.
```

`Termo de Aceite - Sprint 3`

```text
Use o agente termo de aceite sprint 3 com base no Escopo.docx. Se faltar informacao, me pergunte. Gere o documento final.
```

`Ata de Reuniao de Kick-off`

```text
Use o agente kickoff com base no Escopo.docx. Se faltar informacao, me pergunte. Gere a ata final em .docx.
```

`Ata de Retrospectiva`

```text
Use o agente retrospectiva com base no Escopo.docx. Se faltar informacao, me pergunte. Gere a ata final em .docx.
```

`Timeline`

```text
Use o agente timeline com base no Escopo.docx. Gere a imagem final do cronograma do projeto.
```

`Backlog Sprint 3`

```text
Use o agente backlog sprint 3 com base no Escopo.docx. Se faltar informacao, me pergunte. Gere a planilha final com resumo, alocacao, backlog, ausencias e riscos.
```

`Detalhamento dos Ciclos`

```text
Use o agente detalhamento dos ciclos com base no Escopo.docx. Se faltar informacao, me pergunte. Gere a planilha final com sprints e graficos.
```

`Dicionario da EAP`

```text
Use o agente dicionario da eap com base no Escopo.docx. Se faltar informacao, me pergunte. Gere o documento final com pacotes de trabalho, premissas e criterios de aceite.
```

`Dimensionamento de Infraestrutura e Arquitetura`

```text
Use o agente infraestrutura com base no Escopo.docx. Se faltar informacao, me pergunte. Gere o documento final com ambientes, stack, integracoes, seguranca, backup e monitoramento.
```

`Diretorio da Equipe`

```text
Use o agente diretorio da equipe com base no Escopo.docx. Se faltar informacao, me pergunte. Gere o documento final em .docx.
```

## Comandos para template de respostas

Quando voce quiser que a IA monte primeiro o arquivo de respostas:

```text
Exporte o template de respostas do agente <nome-do-agente> com base no Escopo.docx. Nao gere o documento final ainda.
```

Exemplos:

```text
Exporte o template de respostas do agente backlog sprint 3 com base no Escopo.docx.
```

```text
Exporte o template de respostas do agente dicionario da eap com base no Escopo.docx.
```

```text
Exporte o template de respostas do agente infraestrutura com base no Escopo.docx.
```

## Comandos para gerar usando respostas prontas

Quando ja existir um JSON de respostas:

```text
Use o agente <nome-do-agente> com base no Escopo.docx e gere o documento usando o arquivo de respostas <arquivo.json>, sem me perguntar nada.
```

Exemplos:

```text
Use o agente backlog sprint 3 com base no Escopo.docx e gere o documento usando o arquivo de respostas backlog_answers.json, sem me perguntar nada.
```

```text
Use o agente status report com base no Escopo.docx e gere o documento usando o arquivo de respostas status_report_answers.json, sem me perguntar nada.
```

## Comando universal curto

Se quiser um comando padrao e simples para qualquer artefato:

```text
No projeto project-automatizacao-documentos, use o agente <nome-do-documento-ou-agente> com base no Escopo.docx. Se faltar dado, pergunte. Se existir arquivo de respostas, use-o. Gere o artefato final no formato padrao do projeto.
```

## Sobre JSON vs Markdown

### Recomendacao

Mantenha os arquivos estruturados dos agentes e prompts em `.json`.

### Motivo

O codigo Python atual usa esses arquivos como contrato de maquina para:
- registrar agentes
- carregar campos do questionario
- exportar templates de respostas
- executar geracao nao interativa

Hoje o projeto espera explicitamente:
- `agents/*.json`
- `prompts/*.json`
- arquivos de resposta em `.json`

### O que acontece se trocar para `.md`

Se voce renomear os arquivos para `.md` puro, o Python atual deixa de funcionar sem adaptacao, porque o loader usa leitura JSON direta.

### Melhor padrao para este projeto

Use:
- `.json` para configuracao e entrada estruturada da automacao
- `.md` para documentacao humana, exemplos de uso e guias para IA

Esse modelo ja deixa o projeto padronizado sem perder confiabilidade na execucao.
