# AFG-Challenge-Agent 007
Agente Inteligente de Análise de Logs Suspeitos
---

Este agente foi desenvolvido na plataforma Azure Foundry AI para realizar a análise de logs suspeitos armazenados no banco de dados. Ele correlaciona dados como hora, país/IP e tipo de evento para identificar padrões anômalos. O agente calcula uma pontuação de suspeita (variando de 0 a 1), classifica os riscos de acordo com essa pontuação e sugere ações, como a aplicação de MFA, geração de alertas e bloqueios. Além disso, gera relatórios detalhados e resumos executivos para as lideranças, facilitando a tomada de decisões rápidas e informadas.

---


### **Índice de Tópicos Abordados **

– **AFG-Challenge - Agent 007**

– **Agente 007 — Passo a Passo Explicativo**

– **Etapas de Análise e Correlação**

* Identificação temporal
* Validação geográfica
* Correlação de tipo de log
* Correlação sequencial
* Análise comportamental
* Atribuição de pesos

– **Cálculo do Nível de Suspeita (Score 0–1)**

– **Interpretação e Ações Automáticas**

* Faixa do Score

– **Ações Sugeridas**

– **Saídas Esperadas**

* Relatório Estruturado
* Resumo Executivo

– **Agente Funcional no Foundry – Configurações Realizadas**

– **Comportamento Esperado do Agente 007**

– **Azure Foundry - Conhecimento**

– **Azure Foundry - Ações**

– **Respostas no Playground Foundry**

– **Conclusão**

---

## Passo a Passo Explicativo

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

### **Fluxo:**

<img width="399" height="603" alt="image" src="https://github.com/user-attachments/assets/3fc4eec0-2b44-470f-b2d0-7f75b3aac81d" />




---

### **Agente Funcional no Foundry – Configurações Realizadas**

### **ID do Agente**: asst_v3y7pIrlH886pPnS9f6jy0ZM

### **Nome**: Agent 007

### **Implantação**: gpt-4.1-mini (versão: 2025-04-14)

<img width="1288" height="615" alt="image" src="https://github.com/user-attachments/assets/b2eb065a-8a83-4d65-99fc-caa99893d553" />

### **Instruções**:
O agente 007 foi configurado para analisar registros armazenados no arquivo `logs_suspeitos_200` presente no banco de dados. Ele processa dados como data, hora, usuário, país, IP e tipo de evento, identificando comportamentos anômalos através da correlação entre hora, origem e tipo de log. Considera como normal apenas acessos realizados dentro do horário entre 07h e 20h de países das Américas. Registros fora desses padrões são automaticamente marcados como suspeitos.

Durante a análise, verifica os seguintes fatores: horários irregulares, países fora das Américas, eventos críticos (como falhas de login ou alterações não autorizadas), tentativas repetidas e padrões anormais de múltiplos IPs. A cada anomalia identificada, um peso parcial é atribuído ao registro, resultando em um score final que varia de 0 a 1.

### **Classificação de Riscos**:
O agente classifica os registros conforme o score calculado, adotando as seguintes faixas de risco:

* **0.00–0.30**: Normal, sem ação
* **0.31–0.60**: Leve anomalia, exige MFA
* **0.61–0.80**: Risco potencial, gera alerta
* **0.81–1.00**: Alta suspeita, bloqueio automático e notificação à liderança

Após a análise, consolida os resultados em uma tabela contendo: data, hora, usuário, origem, tipo de evento, score e ação tomada. Em seguida, gera um relatório estruturado em PDF e envia um resumo executivo por e-mail às lideranças, destacando o número total de eventos suspeitos, aqueles de alta suspeita, os países de origem, os horários críticos e as ações executadas.

### **Comportamento Esperado do Agente 007**:

* Análise imparcial e estruturada em todas as respostas.
* Explicação clara do raciocínio por trás de cada score calculado.
* Garantir a transparência, rastreabilidade e coerência em toda análise.
* Uso de linguagem técnica e objetiva nos relatórios e notificações.
* Priorizar segurança e precisão, minimizando falsos positivos.

---

### **Azure Foundry - Conhecimento**

O arquivo `logs_suspeitos_200.py` foi carregado, contendo os dados de entrada para análise dos logs de usuários suspeitos. Este recurso serve como um repositório de vetores, permitindo a recuperação rápida de informações através do índice de pesquisa.

<img width="2292" height="670" alt="image" src="https://github.com/user-attachments/assets/4934b568-7b9c-443d-8867-25e82fa3568f" />


** Azure Foundry -Ações **

O arquivo `agent_logs_pipeline_50.py`, cujo código em python está na aba de Codespace do GitHub, foi carregado para permitir que o agente execute a análise, calcule o score de suspeita, classifique os riscos e execute as ações necessárias (MFA, alerta, bloqueio). O código também gera o relatório e envia e-mails para as lideranças.

<img width="2251" height="678" alt="image" src="https://github.com/user-attachments/assets/15b480f8-6481-44f5-9205-03db75aca755" />


---

### **Respostas do Agent 007 no Playground Foundry**


Foram inseridos os seguintes Prompts:

1. Identificar comportamentos anômalos existentes nos registros do arquivo `logs_suspeitos_200.py essa análise deve ser feita por meio da correlação entre hora, origem geográfica (país/IP) e tipo de evento, `.
2. Calcular um nível de suspeita (0-1) para cada registro, classificar o risco e definir ações a serem tomadas conforme o nível detectado.
3. Consolidar os resultados em uma tabela e um resumo executivo, enviando um e-mail para as lideranças com o relatório e as ações executadas.

---

O agente gerou as seguintes respostas durante o processo:

1. **Primeira resposta**
    As imagens desta etapa representam a tela inicial do Agente 007, logo após ser acionado.
Elas exibem:

  * A confirmação de que o processo de análise dos logs foi iniciado.
  * Indicadoresmostrando que o agente está lendo os registros do banco de dados.
  * Mensagens do sistema sinalizando que os dados estão sendo processados para identificação de padrões anômalos.

Essa etapa demonstra que o agente iniciou corretamente a tarefa solicitada.

<img width="1095" height="632" alt="image" src="https://github.com/user-attachments/assets/ba788579-4779-475c-86a8-5fcdcd6489e9" />
<img width="1065" height="579" alt="image" src="https://github.com/user-attachments/assets/27ad5b1f-e5c8-4720-a47a-cf453641bb44" />
<img width="1091" height="588" alt="image" src="https://github.com/user-attachments/assets/6b9c6e2d-bf3c-4633-8c3b-ae97f499864b" />


2. **Segunda resposta**
    As imagens desta fase mostram a interface do agente apresentando o Resumo Executivo. Assim, é possível visualizar:

   * Um painel com o total de eventos analisados e quantos foram classificados como suspeitos ou altamente suspeitos.
   * A lista dos países de origem das tentativas suspeitas (ex.: Canadá, China, Alemanha etc.).
   * Indicadores de horários críticos em que houve maior incidência de eventos.
   * A distribuição das ações realizadas pelo agente (exigir MFA, bloquear e notificar liderança, ou nenhuma ação).

Essas imagens ajudam a entender rapidamente o panorama da investigação feita pelo agente.

<img width="1114" height="630" alt="image" src="https://github.com/user-attachments/assets/7f3378d7-ccc0-4ea9-8b47-f3ad7fc7ecdb" />

<img width="1036" height="578" alt="image" src="https://github.com/user-attachments/assets/0bf8f244-0747-4441-ad22-76250e7fcab2" />

<img width="1052" height="564" alt="image" src="https://github.com/user-attachments/assets/f5d5d963-a2dd-46f8-9c41-907593de0222" />

3. **Terceira resposta**
 As imagens desta etapa mostram:

   * A prévia do e-mail institucional preparado pelo Agente 007 para ser enviado às lideranças.
   * O texto formatado com assunto, destinatários, resumo executivo e descrição das ações tomadas.
   * A estrutura profissional do e-mail, com linguagem formal e orientada à gestão.

São telas demonstrando a automatização da comunicação com o time de liderança.


<img width="1046" height="582" alt="image" src="https://github.com/user-attachments/assets/11d0ef82-fbef-4498-a95f-ed562ab40f47" />

<img width="1076" height="658" alt="image" src="https://github.com/user-attachments/assets/a0cc3692-41e6-4dbe-b854-72df38af2675" />

  A seguir, o escopo do e-mail que foi gerado, na íntegra:

          Assunto: Relatório de Análise de Logs Suspeitos - Situação Atual e Ações Executadas
          Para: verdeazulemerald@gmail.com
          Cc: [Adicionar outros e-mails relevantes, se necessário]
           
          Prezados(as),
          
          Encaminho o relatório de análise dos últimos 200 registros de logs suspeitos, contendo a avaliação dos níveis de suspeita, classificação de riscos e as ações aplicadas.

          Resumo Executivo:
          
          • Nº total de eventos suspeitos detectados: 200
          • Eventos altamente suspeitos (score > 0,8): 34
          • Origem das conexões suspeitas: Canadá, China, Chile, Índia, EUA, França, Alemanha, Brasil, Japão, México
          • Horários de maior incidência: 06:30:33, 11:45:22, 04:08:48
          • Ações executadas: Exigir MFA: 152, Bloquear e notificar liderança: 34, Nenhuma ação: 14
          
          O relatório completo em anexo detalha cada evento com o respectivo nível de suspeita, score e ação recomendada ou executada.
          
          Solicito especial atenção aos eventos classificados como “Alta suspeita”, para que as equipes possam atuar prontamente onde necessário.
          
          Fico à disposição para esclarecimentos adicionais.
          
          Atenciosamente,
          [Seu Nome]
          Equipe de Segurança da Informação
           


4. **Quarta resposta**
 As imagens finais exibem o processo de:

   * Criação do relatório detalhado em PDF, contendo cada log analisado.
   * Ajustes de layout solicitados (fonte, espaçamento, organização e estrutura da tabela).
   * A versão final do PDF disponibilizada para download e anexada ao Read.me.

Essas imagens ilustram a entrega concluída do relatório contendo todos os eventos com seus respectivos scores, níveis de suspeita e ações recomendadas.
   
   
<img width="1072" height="592" alt="image" src="https://github.com/user-attachments/assets/31c5fbcb-3756-4dc8-b8c2-68eca8a33b9d" />

<img width="1079" height="660" alt="image" src="https://github.com/user-attachments/assets/59860e9b-5ed3-4e1f-a2ff-e86b12393bb4" />

<img width="1178" height="636" alt="image" src="https://github.com/user-attachments/assets/f0277256-d024-486e-816b-3731c4b29059" />

---

### **Conclusão**
Com a configuração do agente, as análises de comportamento suspeito foram realizadas, com relatórios detalhados e ações automatizadas para mitigar riscos de segurança. O resumo executivo e o relatório completo foram compartilhados com as lideranças, garantindo maior controle e tomada de decisão rápida.

---

Obrigada!!

Fim!!







