# AFG-Challenge- Agent 007
---

Este agente foi desenvolvido na plataforma Azure Foundry AI para realizar a análise de logs suspeitos armazenados no banco de dados. Ele correlaciona dados como hora, país/IP e tipo de evento para identificar padrões anômalos. O agente calcula uma pontuação de suspeita (variando de 0 a 1), classifica os riscos de acordo com essa pontuação e sugeri ações, como a aplicação de MFA, geração de alertas e bloqueios. Além disso, ele gera relatórios detalhados e resumos executivos para as lideranças, facilitando a tomada de decisões rápidas e informadas.

## Agente Inteligente de Análise de Logs Suspeitos — Passo a Passo Explicativo

---

###  **Entrada de Dados**

1. O agente acessa o banco de dados e lê **50 registros** do arquivo `logs_suspeitos_200`.
2. Cada registro contém as colunas:

   * **Data** → Quando o evento ocorreu.
   * **Hora** → O horário exato do evento.
   * **Nome** → Usuário ou ID responsável.
   * **País** → Localização geográfica do acesso.
   * **IP** → Endereço IP de origem.
   * **Tipo de Log Suspeito** → Breve descrição do tipo de evento (ex.: falha de login, alteração de senha etc.).

---

###  **Regras de Comportamento Normal**

1. O agente define o que é **comportamento aceitável**:

   * **Origem geográfica:** acessos vindos de países das **Américas** (Norte, Central ou do Sul).
   * **Horário:** acessos realizados entre **07h00 e 20h00** (horário local do servidor).
2. Qualquer registro **fora desses critérios** é marcado como **potencial anomalia**, mas não necessariamente incidente confirmado.

---

### 🔍 **Etapas de Análise e Correlação**

O 007 realiza uma análise contextual entre **hora**, **país/IP** e **tipo de evento**, seguindo seis etapas principais:

1. **Identificação temporal:**
   Detectar registros fora do horário normal (antes das 07h ou após as 20h).
2. **Validação geográfica:**
   Verificar se o país de origem está **fora das Américas**.
3. **Correlação de tipo de log:**
   Avaliar se o tipo de evento é **crítico ou incomum** (falha de autenticação, alteração de credencial etc.).
4. **Correlação sequencial:**
   Identificar **padrões repetitivos**, como múltiplas tentativas seguidas ou acessos de IPs diferentes pelo mesmo usuário.
5. **Análise comportamental:**
   Comparar com o **histórico de comportamento** do mesmo usuário (frequência e horário típicos).
6. **Atribuição de pesos:**
   A cada anomalia identificada, o agente soma uma **pontuação parcial** até o limite de **1.0**.

---

###  **Cálculo do Nível de Suspeita (Score 0–1)**

1. Cada registro recebe um **score de suspeita**, conforme as regras abaixo:

   | Critério                | Regra Aplicada                                            | Pontuação |
   | ----------------------- | --------------------------------------------------------- | --------- |
   | Horário fora de 07h–20h | Acesso fora do horário comercial                          | +0.25     |
   | País fora das Américas  | Origem geográfica atípica                                 | +0.35     |
   | Tipo de log crítico     | Falha de login, alteração indevida, acesso não autorizado | +0.25     |
   | Repetição/múltiplos IPs | Possível automação ou força bruta                         | +0.10     |
   | **Score máximo**        | Valor total limitado a 1.0                                | —         |

2. O 007 soma as pontuações de cada critério, obtendo o **score final** de cada evento.

---

###  **Interpretação e Ações Automáticas**

1. O agente classifica o registro de acordo com a faixa de score:

   | Faixa       | Interpretação        | Ação Automática                         |
   | ----------- | -------------------- | --------------------------------------- |
   | 0.00 – 0.30 | Comportamento normal | Nenhuma ação                            |
   | 0.31 – 0.60 | Leve anomalia        | Solicitar MFA (autenticação multifator) |
   | 0.61 – 0.80 | Potencial risco      | Gerar alerta aos analistas de segurança |
   | 0.81 – 1.00 | Alta suspeita        | Bloquear acesso e notificar lideranças  |

2. Cada decisão e ação executada é registrada para auditoria e rastreabilidade.

---

###  **Ações Sugeridas**

Após a classificação, sugere:

* Bloqueios.
* MFA (autenticação multifator).
* Alertas emitidos para equipe de segurança.
* Contas marcadas como “em observação”.
* Eventos normais descartados.


---

###  **Saídas Esperadas**

**1. Relatório Estruturado em PDF ou Excel**
O agente gera uma tabela final contendo:
`Data | Hora | Usuário | Origem | Tipo de Evento | Nível de Suspeita | Score | Ação Aplicada`
Esse relatório apresenta de forma visual os resultados e serve como base técnica para consulta.

**2. Resumo Executivo Automático (E-mail)**
O agente monta e envia automaticamente um e-mail corporativo às lideranças, contendo:

* Total de eventos suspeitos detectados.
* Quantos tiveram **score > 0,8**.
* Lista dos **países de origem** das conexões suspeitas.
* **Horários de maior incidência** de anomalias.
* Ações executadas (**bloqueios**, **MFA**, **alertas**).

---

Fluxo:
<img width="1011" height="1509" alt="image" src="https://github.com/user-attachments/assets/a5aed43b-8da9-4b44-9312-0ec84274f9dc" />


---

**Agente Funcional no Foundry – Configurações Realizadas**

**ID do Agente**: asst_v3y7pIrlH886pPnS9f6jy0ZM

**Nome**: Agent 007

**Implantação**: gpt-4.1-mini (versão: 2025-04-14)

**Instruções**:
O agente 007 foi configurado para analisar registros armazenados no arquivo `logs_suspeitos_200` presente no banco de dados. Ele processa dados como data, hora, usuário, país, IP e tipo de evento, identificando comportamentos anômalos através da correlação entre hora, origem e tipo de log. Considera como normal apenas acessos realizados dentro do horário entre 07h e 20h de países das Américas. Registros fora desses padrões são automaticamente marcados como suspeitos.

Durante a análise, verifica os seguintes fatores: horários irregulares, países fora das Américas, eventos críticos (como falhas de login ou alterações não autorizadas), tentativas repetidas e padrões anormais de múltiplos IPs. A cada anomalia identificada, um peso parcial é atribuído ao registro, resultando em um score final que varia de 0 a 1.

**Classificação de Riscos**:
O agente classifica os registros conforme o score calculado, adotando as seguintes faixas de risco:

* **0.00–0.30**: Normal, sem ação
* **0.31–0.60**: Leve anomalia, exige MFA
* **0.61–0.80**: Risco potencial, gera alerta
* **0.81–1.00**: Alta suspeita, bloqueio automático e notificação à liderança

Após a análise, consolida os resultados em uma tabela contendo: data, hora, usuário, origem, tipo de evento, score e ação tomada. Em seguida, gera um relatório estruturado em PDF e envia um resumo executivo por e-mail às lideranças, destacando o número total de eventos suspeitos, aqueles de alta suspeita, os países de origem, os horários críticos e as ações executadas.

**Comportamento Esperado do Agente 007**:

* Análise imparcial e estruturada em todas as respostas.
* Explicação clara do raciocínio por trás de cada score calculado.
* Garantir a transparência, rastreabilidade e coerência em toda análise.
* Uso de linguagem técnica e objetiva nos relatórios e notificações.
* Priorizar segurança e precisão, minimizando falsos positivos.

---

**Azure Foundry - Conhecimento**

O arquivo `logs_suspeitos_200.py` foi carregado, contendo os dados de entrada para análise dos logs de usuários suspeitos. Este recurso serve como um repositório de vetores, permitindo a recuperação rápida de informações através do índice de pesquisa.

**Ações Realizadas**

O arquivo `agent_logs_pipeline_50.py`, cujo código em python está na aba de Codespace do GitHub, foi carregado para permitir que o agente execute a análise, calcule o score de suspeita, classifique os riscos e execute as ações necessárias (MFA, alerta, bloqueio). O código também gera o relatório e envia e-mails para as lideranças.

---

**Respostas no Playground Foundry**
Foram inseridos os seguintes Prompts:

1. Identificar comportamentos anômalos por meio da correlação entre hora, origem geográfica (país/IP) e tipo de evento, com base nos registros no arquivo `logs_suspeitos_200.py`.
2. Calcular um nível de suspeita (0-1) para cada registro, classificar o risco e definir ações a serem tomadas conforme o nível detectado.
3. Consolidar os resultados em uma tabela e um resumo executivo, enviando um e-mail para as lideranças com o relatório e as ações executadas.

---

**Respostas do Agente 007**

O agente gerou as seguintes respostas durante o processo:

1. **Primeira resposta**: Iniciou as análises de log conforme solicitado.
   ![Primeira resposta](https://github.com/user-attachments/assets/88538ae7-0785-4e9a-a87b-1608254ddd3f)

2. **Segunda resposta**: Gerou um Resumo Executivo com as análises, detalhando o número total de eventos, os eventos suspeitos e de alta suspeita, países de origem, horários críticos e ações sugeridas, como bloqueio ou exigência de MFA.
   ![Segunda resposta](https://github.com/user-attachments/assets/f4256a5b-c215-4077-86eb-8d3adeef8cb2)

3. **Terceira resposta**: Preparou o escopo do e-mail para envio às lideranças, contendo o resumo e o arquivo gerado.
   ![Terceira resposta](https://github.com/user-attachments/assets/3e0522df-9b37-4dcf-99e6-eacd460b7cd1)

4. **Quarta resposta**: Disponibilizou os arquivos para download nos formatos PDF e CSV.
   ![Quarta resposta](https://github.com/user-attachments/assets/acc2d6f0-123f-4964-bcab-afdcdb716384)

Após solicitações de ajustes no formato, o relatório foi gerado, incluindo cada log de usuário com seu respectivo score, nível de suspeita e ação recomendada, além de um resumo da análise. O PDF final foi anexado ao Read.me.
![Relatório gerado](https://github.com/user-attachments/assets/16045c05-e655-4665-b7c7-5eb85cda6237)

---

**Conclusão**
Com a configuração do agente, as análises de comportamento suspeito foram realizadas, com relatórios detalhados e ações automatizadas para mitigar riscos de segurança. O resumo executivo e o relatório completo foram compartilhados com as lideranças, garantindo maior controle e tomada de decisão rápida.

---

Obrigada!!

Fim!!







