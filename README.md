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
Agente funcional no Foundry, configurações realizadas:

ID do Agente: asst_v3y7pIrlH886pPnS9f6jy0ZM

Nome: Agent 007

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

Fluxo:




