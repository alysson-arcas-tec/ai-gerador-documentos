# Project Automatizacao Documentos

Projeto em Python para gerar documentos localmente a partir de `Escopo.docx`, sem depender de token para criar `.docx`, `.xlsx` ou `.png`.

Guia de chamada por linguagem natural para Cursor, Codex e Claude:

- [COMANDOS_IA.md](COMANDOS_IA.md)

## Objetivo

Este projeto foi criado para automatizar a geracao de documentos de projeto a partir de um arquivo de escopo. A ideia e permitir dois modos de uso:

- com apoio de uma IA, escrevendo um comando em linguagem natural
- com execucao direta em Python, chamando o runner local do projeto

Em ambos os casos, o comportamento esperado e o mesmo:

1. ler o `Escopo.docx`
2. reaproveitar os dados encontrados no escopo
3. perguntar somente o que estiver faltando
4. gerar o artefato final localmente, sem uso de token para montar os arquivos

## Formas de uso

### 1. Caso esteja usando uma IA

Caso esteja usando uma IA, use o comando:

```text
Use o agente <nome-do-agente-ou-documento> com base no Escopo.docx. Se faltar informacao, me pergunte antes de gerar. Gere o arquivo final no formato padrao do projeto.
```

Exemplos:

```text
Use o agente dicionario da eap com base no Escopo.docx. Se faltar informacao, me pergunte antes de gerar. Gere o documento final.
```

```text
Use o agente infraestrutura com base no Escopo.docx. Se faltar informacao, me pergunte antes de gerar. Gere o documento final.
```

```text
Use o agente backlog sprint 3 com base no Escopo.docx. Se faltar informacao, me pergunte antes de gerar. Gere a planilha final.
```

Para mais exemplos prontos, consulte:

- [COMANDOS_IA.md](COMANDOS_IA.md)

### 2. Executar diretamente em Python

Execute diretamente o conversor de dados em Python atraves do comando:

```powershell
python .\tools\cli.py list-agents
```

Esse comando lista todos os agentes disponiveis no projeto.

Para executar um agente de forma interativa:

```powershell
python .\tools\cli.py run <agent-id> --scope ..\Escopo.docx
```

Exemplo:

```powershell
python .\tools\cli.py run wbs-dictionary --scope ..\Escopo.docx
```

### 3. Exportar um template de respostas

Se voce quiser preencher os dados manualmente antes da geracao final, exporte um arquivo de respostas:

```powershell
python .\tools\cli.py export-template <agent-id> --scope ..\Escopo.docx --output .\respostas.json
```

Exemplo:

```powershell
python .\tools\cli.py export-template sprint-backlog --scope ..\Escopo.docx --output .\backlog_respostas.json
```

### 4. Gerar sem perguntas, usando respostas prontas

Quando ja existir um arquivo de respostas preenchido:

```powershell
python .\tools\cli.py run <agent-id> --scope ..\Escopo.docx --answers .\respostas.json --non-interactive
```

Exemplo:

```powershell
python .\tools\cli.py run infrastructure-sizing --scope ..\Escopo.docx --answers .\infra_respostas.json --non-interactive
```

## Como funciona internamente

1. O runner le o `Escopo.docx`.
2. O parser identifica nomes, objetivos, restricoes, equipe, datas e outros dados reutilizaveis.
3. Cada agente carrega seu prompt estruturado em `JSON`.
4. O sistema cruza o escopo com os campos obrigatorios do documento.
5. O que nao for encontrado e perguntado ao usuario ou preenchido no arquivo de respostas.
6. O builder gera o arquivo final localmente em Python.

## Fluxo recomendado

Para uso rapido:

```powershell
python .\tools\cli.py run <agent-id> --scope ..\Escopo.docx
```

Para uso mais controlado:

1. exporte o template com `export-template`
2. revise ou preencha o `.json`
3. execute com `run --answers --non-interactive`

## Agentes

`change-request`  
Documento: `Solicitacao de Mudanca de Escopo.docx`

```powershell
python .\tools\cli.py run change-request --scope ..\Escopo.docx
```

`status-report`  
Documento: `Status Report.docx`

```powershell
python .\tools\cli.py run status-report --scope ..\Escopo.docx
```

`acceptance-term`  
Documento: `Termo de Aceite - Sprint 3.docx`

```powershell
python .\tools\cli.py run acceptance-term --scope ..\Escopo.docx
```

`project-timeline`  
Documento: `Timeline_Projeto.png`

```powershell
python .\tools\cli.py run project-timeline --scope ..\Escopo.docx
```

`retrospective-minutes`  
Documento: `Ata de Retrospectiva.docx`

```powershell
python .\tools\cli.py run retrospective-minutes --scope ..\Escopo.docx
```

`kickoff-minutes`  
Documento: `Ata de Reuniao de Kick-off.docx`

```powershell
python .\tools\cli.py run kickoff-minutes --scope ..\Escopo.docx
```

`sprint-backlog`  
Documento: `Backlog Sprint 3.xlsx`

```powershell
python .\tools\cli.py run sprint-backlog --scope ..\Escopo.docx
```

Saida reforcada:
- aba `Resumo` com indicadores de tarefas, horas, custo e impacto de ausencias
- aba `Alocacao` com capacidade, horas alocadas, folga e utilizacao por colaborador
- aba `Backlog` com epico, impacto, mitigacao e criterio de aceite por item
- aba `Riscos` para registrar bloqueios e exposicoes da sprint
- grafico de alocacao para leitura rapida da carga da equipe

`cycle-details`  
Documento: `Detalhamento dos Ciclos.xlsx`

```powershell
python .\tools\cli.py run cycle-details --scope ..\Escopo.docx
```

`wbs-dictionary`  
Documento: `Dicionario da EAP.docx`

```powershell
python .\tools\cli.py run wbs-dictionary --scope ..\Escopo.docx
```

Saida reforcada:
- quadro inicial com metadados do projeto
- bloco de visao consolidada do documento
- tabela de pacotes de trabalho com codigo, entregavel, descricao e criterio de aceite
- secoes de premissas, fora do escopo e criterios globais
- preenchimento inicial derivado do escopo sempre que possivel

`infrastructure-sizing`  
Documento: `Dimensionamento de Infraestrutura e Arquitetura.docx`

```powershell
python .\tools\cli.py run infrastructure-sizing --scope ..\Escopo.docx
```

Saida reforcada:
- quadro inicial com dados de referencia do projeto
- bloco de escopo tecnico considerado
- tabela de ambientes previstos
- tabela de stack tecnologica
- secoes de integracoes, seguranca, backup, monitoramento e premissas operacionais
- preenchimento inicial derivado do escopo sempre que possivel

`team-directory`  
Documento: `Diretorio da Equipe.docx`

```powershell
python .\tools\cli.py run team-directory --scope ..\Escopo.docx
```

## Estrutura

`agents/`  
Definicao declarativa de cada agente.

`skills/`  
Capacidades reutilizaveis: parser do escopo, perguntas interativas e builders locais.

`tools/`  
CLI principal do projeto.

`workflows/`  
Orquestracao entre agente, escopo, respostas e geracao do arquivo.

`prompts/`  
Campos que cada agente precisa coletar.

`config/`  
Configuracao tecnica do runtime, estilos e defaults neutros.

`assets/`  
Mapas auxiliares usados pelo parser do escopo.

## Observacoes

- Nenhum template fixa nome de empresa, cliente ou responsavel dentro do codigo do agente. Esses dados vem do `Escopo.docx` ou sao perguntados ao usuario.
- Quando o escopo nao trouxer uma informacao necessaria, o agente pergunta campo por campo.
- Para fluxos maiores, o ideal e usar `export-template` e depois `run --answers`.
