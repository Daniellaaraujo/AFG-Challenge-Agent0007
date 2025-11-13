"""agent_logs_pipeline_200.py
Leitura direta de logs_suspeitos_200.py (amostra de 200 logs) e execução da pipeline:
- normalização dos dados
- cálculo de score (0-1) conforme regras fornecidas
- classificação e ação recomendada
- geração de saída: Excel (.xlsx) e PDF (.pdf)
- impressão do resumo executivo no terminal
Execute: python agent_logs_pipeline_200.py
"""

from datetime import datetime, time, timedelta
import pandas as pd
import numpy as np
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Diretório de saída
OUT_DIR = "./outputs"
os.makedirs(OUT_DIR, exist_ok=True)

# Janela normal
NORMAL_START = time(7,0,0)
NORMAL_END = time(20,0,0)

# Pesos
WEIGHTS = {
    "hora_fora": 0.25,
    "pais_fora": 0.35,
    "tipo_critico": 0.25,
    "repeticao_mult_ips": 0.10
}
SCORE_MAX = 1.0

# Países das Américas (minusculas)
AMERICAS = set([c.lower() for c in [
    "United States","United States of America","USA","Canada","Mexico",
    "Guatemala","Belize","El Salvador","Honduras","Nicaragua","Costa Rica","Panama",
    "Cuba","Jamaica","Haiti","Dominican Republic","Puerto Rico",
    "Brazil","Argentina","Chile","Uruguay","Paraguay","Bolivia","Peru","Ecuador","Colombia","Venezuela","Guyana","Suriname"
]])

CRITICAL_KEYWORDS = [
    "failed login","failure","failed authentication","auth failure",
    "brute force","password change","alteração de credenciais",
    "credential change","unauthorized access","access denied",
    "admin change","privilege escalation","reset password","alteração de senha","excesso de tentativas","falha de autenticação","alteração de credenciais","reset de senha","reset de password"
]

SEQ_WINDOW_MINUTES = 60

def ensure_columns(df):
    df = df.rename(columns={
        "Data":"data","Hora":"hora","Nome":"nome","País":"pais","IP":"ip","Tipo de Log Suspeito":"tipo_de_log_suspeito"
    })
    required = ['data','hora','nome','pais','ip','tipo_de_log_suspeito']
    missing = [r for r in required if r not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias faltando: {missing}")
    # parse datetime
    df['datetime'] = pd.to_datetime(df['data'].astype(str) + ' ' + df['hora'].astype(str), errors='coerce')
    df['pais'] = df['pais'].astype(str).str.lower().str.strip()
    df['tipo_de_log_suspeito'] = df['tipo_de_log_suspeito'].astype(str).str.lower().str.strip()
    df['ip'] = df['ip'].astype(str).str.strip()
    df['nome'] = df['nome'].astype(str).str.strip()
    return df

def is_hour_out_of_range(dt):
    if pd.isna(dt): return False
    t = dt.time()
    return not (NORMAL_START <= t <= NORMAL_END)

def is_country_outside_americas(country):
    if not country or pd.isna(country):
        return True
    return country not in AMERICAS

def is_type_critical(tipo_text):
    if not tipo_text or pd.isna(tipo_text):
        return False
    txt = tipo_text.lower()
    for kw in CRITICAL_KEYWORDS:
        if kw in txt:
            return True
    return False

def detect_repetition_and_multi_ips(df):
    df_sorted = df.sort_values('datetime').copy()
    repeated = pd.Series(False, index=df_sorted.index)
    multi_ip = pd.Series(False, index=df_sorted.index)
    for user, g in df_sorted.groupby('nome'):
        if g['datetime'].isna().all():
            continue
        times = g['datetime']
        ips = g['ip']
        idxs = g.index.tolist()
        for i in range(len(times)):
            t0 = times.iloc[i]
            if pd.isna(t0):
                continue
            window_mask = (times >= t0) & (times <= t0 + timedelta(minutes=SEQ_WINDOW_MINUTES))
            if window_mask.sum() >= 2:
                repeated.iloc[idxs[i]] = True
            if ips[window_mask].nunique() >= 2:
                multi_ip.iloc[idxs[i]] = True
    repeated = repeated.reindex(df.index).fillna(False)
    multi_ip = multi_ip.reindex(df.index).fillna(False)
    return repeated, multi_ip

def calculate_score_for_df(df):
    df = df.copy()
    df['flag_hora_fora'] = df['datetime'].apply(is_hour_out_of_range)
    df['flag_pais_fora'] = df['pais'].apply(is_country_outside_americas)
    df['flag_tipo_critico'] = df['tipo_de_log_suspeito'].apply(is_type_critical)
    repeated, multi_ip = detect_repetition_and_multi_ips(df)
    df['flag_repeticao'] = repeated | multi_ip
    def compute(row):
        s = 0.0
        if row['flag_hora_fora']:
            s += WEIGHTS['hora_fora']
        if row['flag_pais_fora']:
            s += WEIGHTS['pais_fora']
        if row['flag_tipo_critico']:
            s += WEIGHTS['tipo_critico']
        if row['flag_repeticao']:
            s += WEIGHTS['repeticao_mult_ips']
        return min(s, SCORE_MAX)
    df['score'] = df.apply(compute, axis=1)
    def action_from_score(s):
        if s <= 0.30:
            return "Comportamento normal", "Nenhuma ação"
        elif s <= 0.60:
            return "Leve anomalia", "Exigir MFA"
        elif s <= 0.80:
            return "Potencial risco", "Gerar alerta para analistas"
        else:
            return "Alta suspeita", "Bloquear acesso automaticamente e notificar liderança"
    df[['classificacao','acao_aplicada']] = df['score'].apply(lambda s: pd.Series(action_from_score(s)))
    df['nivel_de_suspeita'] = df['score'].round(2)
    return df

def save_results_excel(df, path):
    cols = ['data','hora','nome','pais','ip','tipo_de_log_suspeito','nivel_de_suspeita','score','classificacao','acao_aplicada']
    if 'data' not in df.columns:
        df['data'] = df['datetime'].dt.date
    if 'hora' not in df.columns:
        df['hora'] = df['datetime'].dt.time
    df.to_excel(path, index=False, columns=cols)

def generate_pdf_report(df, path, title="Relatório de Logs Suspeitos"):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    margin = 40
    y = height - margin
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, title)
    y -= 20
    c.setFont("Helvetica", 10)
    total = len(df)
    high = (df['score'] > 0.8).sum()
    suspects = (df['score'] > 0.3).sum()
    countries = sorted(df.loc[df['score']>0.3, 'pais'].dropna().unique().tolist())
    df['hour_only'] = df['datetime'].dt.hour
    top_hours = df.loc[df['score']>0.3, 'hour_only'].value_counts().head(5).to_dict()
    c.drawString(margin, y, f"Data do relatório: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 15
    c.drawString(margin, y, f"Nº total de eventos: {total} | Eventos suspeitos (score>0.3): {suspects} | Alta suspeita (score>0.8): {high}")
    y -= 15
    c.drawString(margin, y, f"Países de origem (suspeitos): {', '.join(countries) if countries else 'Nenhum'}")
    y -= 15
    c.drawString(margin, y, f"Top horários (suspeitos): {top_hours if top_hours else 'Nenhum'}")
    y -= 25
    cols = ['data','hora','nome','pais','ip','tipo_de_log_suspeito','score','acao_aplicada']
    c.setFont("Helvetica-Bold", 9)
    x = margin
    for col in cols:
        c.drawString(x, y, col[:20])
        x += 80
    y -= 12
    c.setFont("Helvetica", 8)
    for i, row in df.head(30).iterrows():
        x = margin
        if y < margin + 50:
            c.showPage()
            y = height - margin
        for col in cols:
            val = row.get(col, "")
            txt = str(val)
            c.drawString(x, y, txt[:18])
            x += 80
        y -= 12
    c.save()

def compose_summary_email(df):
    total_sus = (df['score'] > 0.3).sum()
    high = (df['score'] > 0.8).sum()
    countries = sorted(df.loc[df['score']>0.3, 'pais'].dropna().unique().tolist())
    df['hour_only'] = df['datetime'].dt.hour
    hours = df.loc[df['score']>0.3, 'hour_only'].value_counts()
    hours_range = ', '.join([f"{h}:00 ({cnt})" for h,cnt in hours.head(5).items()])
    actions = df['acao_aplicada'].value_counts().to_dict()
    body = f"""
Prezados líderes e equipe de segurança,

Segue o resumo executivo da análise automatizada de logs (sistema): 

Principais Descobertas:
- Nº total de eventos analisados: {len(df)}
- Nº eventos com suspeita (score > 0.3): {total_sus}
- Eventos altamente suspeitos (score > 0.8): {high}
- Origem das conexões suspeitas (países): {', '.join(countries) if countries else 'Nenhum detectado'}
- Horários de maior incidência (hora: ocorrências): {hours_range if hours_range else 'Nenhum padrão claro'}
- Ações executadas (resumo): {actions}

Observações:
- A pontuação (0–1) foi calculada conforme regras predefinidas (hora fora, país fora das Américas, tipo crítico, repetição/multi IP).
- Eventos classificados como "Alta suspeita" tiveram a ação recomendada de bloqueio automático (se configurado).

Anexo: planilha detalhada com cada evento, score e ação aplicada.

Atenciosamente,
Agente de Análise Automatizada de Segurança
"""
    return body

if __name__ == '__main__':
    # importa os logs do módulo gerado pelo usuário
    try:
        import logs_suspeitos_200 as data_module
    except Exception as e:
        raise SystemExit(f"Não foi possível importar logs_suspeitos_200.py: {e}")
    logs = getattr(data_module, 'logs', None)
    if not logs:
        raise SystemExit("Variável 'logs' não encontrada em logs_suspeitos_200.py")
    df_raw = pd.DataFrame(logs)
    df = ensure_columns(df_raw)
    results = calculate_score_for_df(df)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    excel_path = os.path.join(OUT_DIR, f"relatorio_logs_{timestamp}.xlsx")
    pdf_path = os.path.join(OUT_DIR, f"relatorio_logs_{timestamp}.pdf")
    save_results_excel(results, excel_path)
    generate_pdf_report(results, pdf_path)
    print("Pipeline executado com sucesso.")
    print(f"Planilha: {excel_path}")
    print(f"PDF: {pdf_path}")
    print(compose_summary_email(results))
