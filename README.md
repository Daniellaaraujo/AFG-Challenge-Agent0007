# AFG-Challenge-Agent0007
Agente inteligente de análise de logs suspeitos criado na plataforma Azure Foundry AI. Analisa 50 registros do banco, correlando hora, país/IP e tipo de evento. Calcula score de suspeita (0–1), classifica riscos, executa ações automáticas (MFA, alerta, bloqueio) e gera relatório para lideranças.

---

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
3. O agente valida se todos os campos estão completos e no formato correto (ex.: IP válido, data e hora reconhecíveis).

---

###  **Regras de Comportamento Normal**

1. O agente define o que é **comportamento aceitável**:

   * **Origem geográfica:** acessos vindos de países das **Américas** (Norte, Central ou do Sul).
   * **Horário:** acessos realizados entre **07h00 e 20h00** (horário local do servidor).
2. Qualquer registro **fora desses critérios** é marcado como **potencial anomalia**, mas não necessariamente incidente confirmado.

---

### 🔍 **Etapas de Análise e Correlação**

O agente realiza uma análise contextual entre **hora**, **país/IP** e **tipo de evento**, seguindo seis etapas principais:

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

2. O agente soma as pontuações de cada critério, obtendo o **score final** de cada evento.

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

###  **Ações Executadas**

Após a classificação, o agente documenta automaticamente:

* Bloqueios realizados.
* MFA (autenticação multifator) ativado.
* Alertas emitidos para equipe de segurança.
* Contas marcadas como “em observação”.
* Eventos normais descartados.

Esses dados são armazenados para consulta e auditoria posterior.

---

###  **Saídas Esperadas**

**1. Relatório Estruturado em PDF ou Excel**
O agente gera uma tabela final contendo:
`Data | Hora | Usuário | Origem | Tipo de Evento | Nível de Suspeita | Score | Ação Aplicada`
Esse relatório apresenta de forma visual os resultados e serve como base técnica para auditoria.

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

Agente funcional no Foundry, configurações realizadas:

ID do Agente: asst_v3y7pIrlH886pPnS9f6jy0ZM

Nome: Agent 007

Implantação: gpt-4.1-mini (version:2025-04-14)

Instruções:
O agente inteligente analisa 50 registros do arquivo logs_suspeitos_200 armazenado no banco de dados. Ele processa dados contendo data, hora, usuário, país, IP e tipo de evento, identificando comportamentos anômalos pela correlação entre hora, origem e tipo de log. Considera normal apenas acessos vindos das Américas entre 07h e 20h; registros fora desses padrões são marcados como suspeitos.

Durante a análise, o agente verifica horários irregulares, países fora das Américas, tipos de eventos críticos (como falhas de login ou alterações indevidas), repetições de tentativas e padrões anormais por múltiplos IPs. A cada anomalia, atribui pesos parciais até um score máximo de 1.0.

Com o score calculado, classifica os registros conforme faixas de risco:

0.00–0.30: normal, sem ação;

0.31–0.60: leve anomalia, exige MFA;

0.61–0.80: risco potencial, gera alerta;

0.81–1.00: alta suspeita, bloqueio automático e notificação à liderança.

Após aplicar as ações (bloqueio, MFA, alerta ou observação), o agente consolida os resultados em uma tabela contendo data, hora, usuário, origem, tipo de evento, score e ação tomada. Por fim, gera um relatório estruturado em PDF e envia um resumo executivo por e-mail às lideranças, destacando o número total de eventos suspeitos, os de alta suspeita, países de origem, horários críticos e ações executadas.

Descrição do agente: 

Comportamento Esperado do Agente
•	Ser analítico, estruturado e imparcial em todas as respostas.
•	Explicar o raciocínio por trás de cada score calculado.
•	Garantir transparência, rastreabilidade e coerência na análise.
•	Usar linguagem técnica e objetiva nos relatórios e notificações.
•	Priorizar segurança e precisão, minimizando falsos positivos.

<img width="1363" height="754" alt="image" src="https://github.com/user-attachments/assets/0f2c9b39-01c5-4397-b387-7a73b2200802" />


Feito isso, na parte de Conhecimento do Foundry o arquivo logs_suspeitos_200.py foi carregado. Esse arquivo contem os dados de input, com os logs de usuários suspeitos para o agente realizar a análise. Trata-se de um repositório de vetores que o índice de pesquisa pode referenciar para recuperação rápida de informações.

<img width="1204" height="726" alt="image" src="https://github.com/user-attachments/assets/2351b578-ffae-4920-a476-c0531f581e94" />

Em seguida, na parte de Ações o arquivo agent_logs_pipeline_50.py foi carregado. Esse arquivo em python, cujo os códigos estão na aba do Codespace do Githhub, dispõe do necessários para o agente executar a análise, calcular score de suspeita (0–1), classifica riscos, executar ações (MFA, alerta, bloqueio) e gerar relatório para lideranças. 

<img width="1216" height="722" alt="image" src="https://github.com/user-attachments/assets/d48bc536-08f4-4baa-a428-634291aef759" />

Realizadas todas as configurações, no Playground Foundry foram inseridos os seguintes Prompts:

Identificar comportamentos anômalos por meio da correlação entre hora, origem geográfica (país/IP) e tipo de evento pelo arquivo logs_suspeitos_200.py para todos os registros da tabela.
Com base nessa análise, o agente deve calcular um nível de suspeita (0–1) para cada registro, classificar o risco, e definir ações a serem tomadas conforme o nível detectado.

Feito isso, consolidar as saídas esperadas, ou seja, uma tabela e um resumo executivo. Após enviar e-mail para as lideranças informando a situação encontrada.





