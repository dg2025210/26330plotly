import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI 선호도 조사",
    page_icon="🤖",
    layout="wide",
)

# ── 전역 CSS ─────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 10%, #1a0533 0%, #0a0a1a 45%, #001022 100%);
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"]  { background: transparent; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1200px; }

/* 노이즈 오버레이 */
[data-testid="stAppViewContainer"]::before {
    content: ""; position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    opacity: 0.4;
}

/* HERO */
.hero { text-align: center; padding: 3.5rem 1rem 2rem; }
.hero-badge {
    display: inline-block;
    background: linear-gradient(90deg,rgba(124,58,237,.18),rgba(14,165,233,.18));
    border: 1px solid rgba(124,58,237,.4); border-radius: 100px;
    padding: 5px 18px; font-size:.75rem; letter-spacing:.12em;
    text-transform: uppercase; color: #a78bfa; margin-bottom: 1.2rem;
}
.hero-title {
    font-family:'Syne',sans-serif; font-size:3.4rem; font-weight:800; line-height:1.1;
    background: linear-gradient(135deg,#fff 0%,#c4b5fd 40%,#38bdf8 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; margin:0 0 .6rem;
}
.hero-sub { color:rgba(255,255,255,.4); font-size:.95rem; letter-spacing:.04em; }

/* KPI 카드 */
.kpi-wrap { display:flex; gap:16px; margin-bottom:1.5rem; }
.kpi-card {
    flex:1; border-radius:20px; padding:28px 22px; text-align:center;
    position:relative; overflow:hidden; border:1px solid rgba(255,255,255,.1);
}
.kpi-card::before {
    content:""; position:absolute; inset:0; z-index:0; border-radius:20px;
    background: radial-gradient(circle at 50% -10%, var(--glow), transparent 65%);
    opacity:.25;
}
.kpi-card.claude  { background:linear-gradient(145deg,#1e0a00,#2d1200); border-color:rgba(217,119,87,.35); --glow:#D97757; }
.kpi-card.gemini  { background:linear-gradient(145deg,#00081e,#001433); border-color:rgba(66,133,244,.35);  --glow:#4285F4; }
.kpi-card.chatgpt { background:linear-gradient(145deg,#001810,#002a1c); border-color:rgba(16,163,127,.35); --glow:#10A37F; }
.kpi-medal  { font-size:2rem;   margin-bottom:6px;  position:relative; z-index:1; }
.kpi-name   { font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:700; position:relative; z-index:1; margin-bottom:4px; }
.kpi-score  { font-size:2.2rem; font-weight:700; position:relative; z-index:1; line-height:1; }
.kpi-score span { font-size:.85rem; font-weight:400; opacity:.6; }
.kpi-chips  { display:flex; gap:8px; justify-content:center; margin-top:12px; position:relative; z-index:1; }
.chip { background:rgba(255,255,255,.08); border-radius:100px; padding:3px 12px; font-size:.75rem; color:rgba(255,255,255,.65); }
.kpi-card.claude  .kpi-name { color:#FDBA74; } .kpi-card.claude  .kpi-score { color:#D97757; }
.kpi-card.gemini  .kpi-name { color:#93C5FD; } .kpi-card.gemini  .kpi-score { color:#4285F4; }
.kpi-card.chatgpt .kpi-name { color:#6EE7B7; } .kpi-card.chatgpt .kpi-score { color:#10A37F; }

/* 섹션 타이틀 */
.sec-title {
    font-family:'Syne',sans-serif; font-size:1.05rem; font-weight:700;
    color:rgba(255,255,255,.85); letter-spacing:.02em;
    margin-bottom:.3rem; display:flex; align-items:center; gap:8px;
}
[data-testid="stExpander"] {
    background:rgba(255,255,255,.03) !important;
    border:1px solid rgba(255,255,255,.08) !important;
    border-radius:16px !important;
}
hr { border-color:rgba(255,255,255,.08) !important; }
</style>
""", unsafe_allow_html=True)

# ── 데이터 ───────────────────────────────────────────────────
responses = [
    {"이름":"김한별","학교":"당곡고", "1위":"Claude","2위":"Gemini", "3위":"ChatGPT"},
    {"이름":"변시현","학교":"당곡고", "1위":"Claude","2위":"Gemini", "3위":"ChatGPT"},
    {"이름":"신연서","학교":"수도여고","1위":"Claude","2위":"ChatGPT","3위":"Gemini"},
    {"이름":"이마루","학교":"당곡고", "1위":"Gemini","2위":"Claude", "3위":"ChatGPT"},
    {"이름":"최윤영","학교":"수도여고","1위":"Gemini","2위":"Claude", "3위":"ChatGPT"},
    {"이름":"이지훈","학교":"당곡고", "1위":"Claude","2위":"Gemini", "3위":"ChatGPT"},
    {"이름":"조윤서","학교":"수도여고","1위":"Claude","2위":"Gemini", "3위":"ChatGPT"},
    {"이름":"김도연","학교":"당곡고", "1위":"Claude","2위":"Gemini", "3위":"ChatGPT"},
    {"이름":"이서영","학교":"수도여고","1위":"Claude","2위":"ChatGPT","3위":"Gemini"},
    {"이름":"이한규","학교":"당곡고", "1위":"Claude","2위":"Gemini", "3위":"ChatGPT"},
    {"이름":"김준영","학교":"당곡고", "1위":"Claude","2위":"Gemini", "3위":"ChatGPT"},
]
df = pd.DataFrame(responses)

AIs       = ["Claude","Gemini","ChatGPT"]
COLORS    = {"Claude":"#D97757","Gemini":"#4285F4","ChatGPT":"#10A37F"}
SCORE_MAP = {"1위":3,"2위":2,"3위":1}
AI_ICONS  = {"Claude":"🟠","Gemini":"🔵","ChatGPT":"🟢"}
CSS_CLS   = {"Claude":"claude","Gemini":"gemini","ChatGPT":"chatgpt"}
MEDALS    = ["🥇","🥈","🥉"]

score_data  = {ai:0 for ai in AIs}
rank_counts = {ai:{1:0,2:0,3:0} for ai in AIs}
for row in responses:
    for col,pts in SCORE_MAP.items():
        ai = row[col]; score_data[ai]+=pts; rank_counts[ai][int(col[0])]+=1

def rgba(hex_c:str, a:float)->str:
    h=hex_c.lstrip("#"); r,g,b=int(h[:2],16),int(h[2:4],16),int(h[4:],16)
    return f"rgba({r},{g},{b},{a})"

def dark_layout(**kw):
    base=dict(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
              font=dict(family="DM Sans",color="rgba(255,255,255,.7)"),
              margin=dict(t=30,b=20,l=30,r=20))
    base.update(kw); return base

GRID = dict(showgrid=True,gridcolor="rgba(255,255,255,.07)",zeroline=False)

rank_order = sorted(AIs, key=lambda a: score_data[a], reverse=True)

# ═══ HERO ════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-badge">📊 Student Survey · 2025</div>
  <h1 class="hero-title">AI 선호도 조사 결과</h1>
  <p class="hero-sub">당곡고 · 수도여고 학생 11명이 직접 선택한 AI 랭킹</p>
</div>
""", unsafe_allow_html=True)

# ═══ KPI 카드 ════════════════════════════════════════════════
chips = {ai: "".join([
    f'<div class="chip">🥇 {rank_counts[ai][1]}회</div>',
    f'<div class="chip">🥈 {rank_counts[ai][2]}회</div>',
    f'<div class="chip">🥉 {rank_counts[ai][3]}회</div>',
]) for ai in AIs}

cards_html = "".join([
    f'<div class="kpi-card {CSS_CLS[ai]}">'
    f'<div class="kpi-medal">{MEDALS[i]}</div>'
    f'<div class="kpi-name">{AI_ICONS[ai]} {ai}</div>'
    f'<div class="kpi-score">{score_data[ai]}<span> 점</span></div>'
    f'<div class="kpi-chips">{chips[ai]}</div>'
    f'</div>'
    for i,ai in enumerate(rank_order)
])
st.markdown(f'<div class="kpi-wrap">{cards_html}</div>', unsafe_allow_html=True)

# ═══ Row 1: 총점 막대 + 도넛 ════════════════════════════════
c1, c2 = st.columns([3,2], gap="medium")

with c1:
    st.markdown('<div class="sec-title">📊 가중 총점 비교</div>', unsafe_allow_html=True)
    st.caption("1위 3점 · 2위 2점 · 3위 1점")
    fig = go.Figure()
    for ai in rank_order:
        fig.add_trace(go.Bar(
            x=[ai], y=[score_data[ai]], name=ai,
            marker=dict(color=rgba(COLORS[ai],.85),
                        line=dict(color=COLORS[ai],width=2),
                        cornerradius=10),
            text=[f"<b>{score_data[ai]}점</b>"],
            textposition="outside", textfont=dict(size=17,color=COLORS[ai]),
            width=0.5,
        ))
    fig.update_layout(**dark_layout(
        showlegend=False, height=300, bargap=.35,
        yaxis=dict(range=[0,max(score_data.values())+8],**GRID,
                   tickfont=dict(color="rgba(255,255,255,.4)")),
        xaxis=dict(tickfont=dict(size=15,color="rgba(255,255,255,.85)")),
    ))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown('<div class="sec-title">🥇 1위 선택 비율</div>', unsafe_allow_html=True)
    st.caption(" ")
    fig2 = go.Figure(go.Pie(
        labels=AIs,
        values=[rank_counts[ai][1] for ai in AIs],
        hole=.6,
        marker=dict(colors=[COLORS[ai] for ai in AIs],
                    line=dict(color="#0a0a1a",width=3)),
        textinfo="label+percent", textfont=dict(size=13),
        pull=[0.06 if ai==rank_order[0] else 0 for ai in AIs],
        hovertemplate="%{label}: %{value}명 (%{percent})<extra></extra>",
    ))
    fig2.add_annotation(text=f"<b>{rank_order[0]}</b><br>압도적 1위",
                        x=.5,y=.5,showarrow=False,
                        font=dict(size=12,color=COLORS[rank_order[0]]))
    fig2.update_layout(**dark_layout(showlegend=False,height=300,
                                     margin=dict(t=10,b=10,l=10,r=10)))
    st.plotly_chart(fig2, use_container_width=True)

# ═══ Row 2: 스택 + 학교별 ═══════════════════════════════════
c3, c4 = st.columns([3,2], gap="medium")

with c3:
    st.markdown('<div class="sec-title">📈 순위별 득표 분포</div>', unsafe_allow_html=True)
    st.caption("각 AI를 1·2·3위로 선택한 학생 수")
    fig3 = go.Figure()
    for ri, (lbl, alpha) in enumerate(zip(["1위","2위","3위"],[.95,.6,.3]), start=1):
        fig3.add_trace(go.Bar(
            name=lbl, x=AIs,
            y=[rank_counts[ai][ri] for ai in AIs],
            marker=dict(
                color=[rgba(COLORS[ai],alpha) for ai in AIs],
                line=dict(color=[rgba(COLORS[ai],1) for ai in AIs],width=1.5),
            ),
            text=[f"{rank_counts[ai][ri]}명" for ai in AIs],
            textposition="inside", textfont=dict(size=13,color="white"),
            hovertemplate=f"{lbl}: %{{y}}명<extra></extra>",
        ))
    fig3.update_layout(**dark_layout(
        barmode="stack", height=280,
        yaxis=dict(title="응답 수(명)",**GRID,
                   tickfont=dict(color="rgba(255,255,255,.4)")),
        xaxis=dict(tickfont=dict(size=15,color="rgba(255,255,255,.85)")),
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,
                    font=dict(color="rgba(255,255,255,.6)")),
    ))
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.markdown('<div class="sec-title">🏫 학교별 평균 점수</div>', unsafe_allow_html=True)
    st.caption("당곡고 vs 수도여고")
    schools = ["당곡고","수도여고"]
    ss = {s:{ai:0 for ai in AIs} for s in schools}
    sc = {s:0 for s in schools}
    for row in responses:
        s=row["학교"]; sc[s]+=1
        for col in ["1위","2위","3위"]: ss[s][row[col]]+=SCORE_MAP[col]
    fig4 = go.Figure()
    for ai in AIs:
        fig4.add_trace(go.Bar(
            name=ai, x=schools,
            y=[ss[s][ai]/sc[s] for s in schools],
            marker=dict(color=rgba(COLORS[ai],.8),
                        line=dict(color=COLORS[ai],width=1.5),
                        cornerradius=8),
            text=[f"{ss[s][ai]/sc[s]:.1f}" for s in schools],
            textposition="outside", textfont=dict(size=13,color=COLORS[ai]),
        ))
    fig4.update_layout(**dark_layout(
        barmode="group", height=280,
        yaxis=dict(title="평균 점수",range=[0,4.3],**GRID,
                   tickfont=dict(color="rgba(255,255,255,.4)")),
        xaxis=dict(tickfont=dict(size=14,color="rgba(255,255,255,.85)")),
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,
                    font=dict(color="rgba(255,255,255,.6)")),
    ))
    st.plotly_chart(fig4, use_container_width=True)

# ═══ 히트맵 ════════════════════════════════════════════════════
st.markdown('<div class="sec-title">🗺️ 개인별 선택 히트맵</div>', unsafe_allow_html=True)
st.caption("각 학생이 어떤 AI를 몇 위로 선택했는지 한눈에")
hz, ht, hlabels = [], [], []
for row in responses:
    hlabels.append(f"{row['학교']}  {row['이름']}")
    rz, rt = [], []
    for ai in AIs:
        for col in ["1위","2위","3위"]:
            if row[col]==ai:
                rz.append(4-int(col[0])); rt.append(col); break
    hz.append(rz); ht.append(rt)

fig5 = go.Figure(go.Heatmap(
    z=hz, x=[f"{AI_ICONS[ai]} {ai}" for ai in AIs], y=hlabels,
    text=ht, texttemplate="<b>%{text}</b>",
    textfont=dict(size=13,color="white"),
    colorscale=[
        [0.0,  "rgba(20,10,5,1)"],
        [0.33, rgba(COLORS["ChatGPT"],.6)],
        [0.66, rgba(COLORS["Gemini"], .8)],
        [1.0,  rgba(COLORS["Claude"], 1.0)],
    ],
    showscale=False, xgap=5, ygap=5,
    hovertemplate="%{y}<br>%{x}: <b>%{text}</b><extra></extra>",
))
fig5.update_layout(**dark_layout(
    height=430,
    xaxis=dict(tickfont=dict(size=14,color="rgba(255,255,255,.85)"),side="top"),
    yaxis=dict(tickfont=dict(size=11,color="rgba(255,255,255,.6)"),autorange="reversed"),
    margin=dict(t=55,b=10,l=135,r=20),
))
st.plotly_chart(fig5, use_container_width=True)

# ═══ 원본 데이터 ════════════════════════════════════════════
with st.expander("📋 원본 응답 데이터 보기"):
    st.dataframe(df, use_container_width=True, hide_index=True)

# ═══ 푸터 ═══════════════════════════════════════════════════
st.markdown("""
<div style='text-align:center;padding:2.5rem 0 1rem;
            color:rgba(255,255,255,.18);font-size:.78rem;letter-spacing:.08em;'>
    STUDENT AI PREFERENCE SURVEY · 11 RESPONDENTS · 2025<br>
    가중점수제 — 1위 3점 · 2위 2점 · 3위 1점
</div>
""", unsafe_allow_html=True)
