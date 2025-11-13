"""agent_logs_pipeline_50_email.py
Versão com envio automático de relatório por e-mail.

- Lê logs de logs_suspeitos_50.py
- Calcula score e classificação
- Gera Excel + PDF
- Envia o arquivo Excel e resumo para verdeazulemerald@gmail.com
"""

from datetime import datetime, time, timedelta
import pandas as pd
import numpy as np
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import smtplib
from email.message import EmailMessage

OUT_DIR = "./outputs"
os.makedirs(OUT_DIR, exist_ok=True)

NORMAL_START = time(7,0,0)
NORMAL_END = time(20,0,0)

WEIGHTS = {
    "hora_fora": 0.25,
    "pais_fora": 0.35,
    "tipo_critico": 0.25,
    "repeticao_mult_ips": 0.10
}
SCORE_MAX = 1.0

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
    "admin change","privilege escalation","reset password","alteração de senha",
    "excesso de tentativas","falha de autenticação","reset de senha","reset de password"
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

def generate_pdf_report(df, path, title="Relatório de Logs Suspeitos (Amostra 50)"):
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

def enviar_email(relatorio_excel, resumo_texto):
    remetente = "verdeazulemerald@gmail.com"
    destinatario = "verdeazulemerald@gmail.com"
    senha_app = "irwm gizn zpws immd"  

    msg = EmailMessage()
    msg["Subject"] = "Relatório de Logs Suspeitos - Amostra 50"
    msg["From"] = remetente
    msg["To"] = destinatario
    msg.set_content(f"Olá,\\n\\nSegue em anexo o relatório Excel e o resumo da análise:\\n\\n{resumo_texto}\\n\\nAtenciosamente,\\nAgente de Segurança Automatizado")

    with open(relatorio_excel, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=os.path.basename(relatorio_excel)
        )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remetente, senha_app)
            smtp.send_message(msg)
        print("📧 E-mail enviado com sucesso para", destinatario)
    except Exception as e:
        print("❌ Falha ao enviar e-mail:", e)

if __name__ == '__main__':
    try:
        import logs_suspeitos_50 as data_module
    except Exception as e:
        raise SystemExit(f"Não foi possível importar logs_suspeitos_50.py: {e}")

    logs = getattr(data_module, 'logs', None)
    if not logs:
        raise SystemExit("Variável 'logs' não encontrada em logs_suspeitos_50.py")

    df_raw = pd.DataFrame(logs)
    df = ensure_columns(df_raw)
    results = calculate_score_for_df(df)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    excel_path = os.path.join(OUT_DIR, f"relatorio_logs_50_{timestamp}.xlsx")
    pdf_path = os.path.join(OUT_DIR, f"relatorio_logs_50_{timestamp}.pdf")
    save_results_excel(results, excel_path)
    generate_pdf_report(results, pdf_path)
    print("Pipeline (50 amostras) executado com sucesso.")
    print(f"Planilha: {excel_path}")
    print(f"PDF: {pdf_path}")
    resumo = f"Total de eventos: {len(results)} | Suspeitos (score>0.3): {(results['score']>0.3).sum()} | Alta suspeita (score>0.8): {(results['score']>0.8).sum()}"
    enviar_email(excel_path, resumo)
