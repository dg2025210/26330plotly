import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI 선호도 투표 결과",
    page_icon="🤖",
    layout="wide",
)

# ── 전체 CSS (글래스모피즘 + 네온 그라디언트) ────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a4e 35%, #24243e 65%, #0f0c29 100%);
    background-attachment: fixed;
    font-family: 'Noto Sans KR', sans-serif;
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 800px 600px at 20% 20%, rgba(120,80,255,0.18) 0%, transparent 70%),
        radial-gradient(ellipse 600px 500px at 80% 80%, rgba(255,80,160,0.15) 0%, transparent 70%),
        radial-gradient(ellipse 500px 400px at 60% 10%, rgba(0,200,255,0.12) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="block-container"] { padding-top: 2rem; position: relative; z-index: 1; }

.hero {
    background: linear-gradient(135deg,
        rgba(120,80,255,0.22) 0%,
        rgba(255,80,160,0.18) 50%,
        rgba(0,200,255,0.18) 100%);
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 2.8rem 2rem 2.2rem;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -60px; left: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(120,80,255,0.4) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: "";
    position: absolute;
    bottom: -50px; right: -50px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(255,80,160,0.35) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-icon { font-size: 3.5rem; display: block; margin-bottom: 0.5rem; filter: drop-shadow(0 0 20px rgba(120,80,255,0.8)); }
.hero h1 {
    font-size: 2.4rem; font-weight: 900;
    background: linear-gradient(90deg, #a78bfa, #f472b6, #38bdf8, #a78bfa);
    background-size: 300%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    animation: shimmer 4s linear infinite;
    margin: 0 0 0.5rem;
}
@keyframes shimmer { 0%{background-position:0%} 100%{background-position:300%} }
.hero p { color: rgba(255,255,255,0.65); font-size: 0.95rem; margin: 0; }

.metric-card {
    border-radius: 20px;
    padding: 1.6rem 1rem 1.4rem;
    text-align: center;
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.18);
    position: relative;
    overflow: hidden;
}
.mc-gold   { background: linear-gradient(145deg, rgba(251,191,36,0.22), rgba(245,158,66,0.12)); border-color: rgba(251,191,36,0.45); }
.mc-silver { background: linear-gradient(145deg, rgba(148,163,184,0.22), rgba(100,116,139,0.12)); border-color: rgba(148,163,184,0.45); }
.mc-bronze { background: linear-gradient(145deg, rgba(180,100,60,0.22), rgba(205,124,47,0.12)); border-color: rgba(180,100,60,0.38); }
.medal-emoji { font-size: 2.6rem; display:block; margin-bottom:0.3rem; filter: drop-shadow(0 0 12px rgba(255,200,50,0.7)); }
.ai-name  { font-size: 1.3rem; font-weight: 800; margin: 0.2rem 0; }
.ai-score { font-size: 2.8rem; font-weight: 900; line-height: 1.1; }
.ai-sub   { font-size: 0.82rem; color: rgba(255,255,255,0.5); margin-top: 0.5rem; }

.sec-header {
    display: flex; align-items: center; gap: 0.7rem;
    font-size: 1.1rem; font-weight: 800;
    color: rgba(255,255,255,0.9);
    margin: 2rem 0 0.8rem;
    padding-left: 0.6rem;
    border-left: 4px solid transparent;
    border-image: linear-gradient(180deg,#a78bfa,#f472b6) 1;
}
.sec-icon {
    width: 34px; height: 34px; border-radius: 10px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── 원본 데이터 ─────────────────────────────────────────────
RAW = [
    {"name": "김한별", "school": "당곡고", "ranks": ["클로드", "제미나이", "챗지피티"]},
    {"name": "변시현", "school": "당곡고", "ranks": ["클로드", "제미나이", "챗지피티"]},
    {"name": "신연서", "school": "수도여고", "ranks": ["클로드", "챗지피티", "제미나이"]},
    {"name": "이마루", "school": "당곡고", "ranks": ["제미나이", "클로드", "챗지피티"]},
    {"name": "최윤영", "school": "수도여고", "ranks": ["제미나이", "클로드", "챗지피티"]},
    {"name": "이지훈", "school": "당곡고", "ranks": ["클로드", "제미나이", "챗지피티"]},
    {"name": "조윤서", "school": "수도여고", "ranks": ["클로드", "제미나이", "챗지피티"]},
    {"name": "김도연", "school": "당곡고", "ranks": ["클로드", "제미나이", "챗지피티"]},
    {"name": "이서영", "school": "수도여고", "ranks": ["클로드", "챗지피티", "제미나이"]},
    {"name": "이한규", "school": "당곡고", "ranks": ["클로드", "제미나이", "챗지피티"]},
    {"name": "김준영", "school": "당곡고", "ranks": ["클로드", "제미나이", "챗지피티"]},
]

AIs = ["클로드", "제미나이", "챗지피티"]
SCORE = {0: 3, 1: 2, 2: 1}

AI_COLORS = {
    "클로드":   "#f97316",
    "제미나이": "#3b82f6",
    "챗지피티": "#10b981",
}
AI_GRADIENT = {
    "클로드":   ("#ff6b35", "#fb923c"),
    "제미나이": ("#1d4ed8", "#60a5fa"),
    "챗지피티": ("#059669", "#34d399"),
}

PLOTLY_PAPER = "rgba(0,0,0,0)"
PLOTLY_BG    = "rgba(255,255,255,0.03)"
AXIS_CLR     = "rgba(255,255,255,0.12)"
TXT_CLR      = "rgba(255,255,255,0.85)"

BASE_LAYOUT = dict(
    paper_bgcolor=PLOTLY_PAPER,
    plot_bgcolor=PLOTLY_BG,
    font=dict(family="Noto Sans KR, sans-serif", color=TXT_CLR),
    margin=dict(l=10, r=10, t=36, b=10),
)

def ax(title="", dtick=None, rng=None):
    d = dict(showgrid=True, gridcolor=AXIS_CLR, gridwidth=1,
             zeroline=False, tickfont=dict(size=13, color=TXT_CLR),
             linecolor=AXIS_CLR,
             title=dict(text=title, font=dict(size=11, color="rgba(255,255,255,0.45)")))
    if dtick: d["dtick"] = dtick
    if rng:   d["range"]  = rng
    return d

# ── 전처리 ──────────────────────────────────────────────────
records = []
for r in RAW:
    for i, ai in enumerate(r["ranks"]):
        records.append({"name": r["name"], "school": r["school"],
                        "ai": ai, "rank": i+1, "score": SCORE[i]})
df = pd.DataFrame(records)
total_score = df.groupby("ai")["score"].sum().reindex(AIs)
rank_counts  = df.groupby(["ai","rank"]).size().unstack(fill_value=0).reindex(AIs)
school_score = df.groupby(["school","ai"])["score"].sum().unstack(fill_value=0).reindex(columns=AIs)
ranked_ais   = total_score.sort_values(ascending=False).index.tolist()

# ══════════════════════════════ HERO ══════════════════════════
st.markdown("""
<div class="hero">
  <span class="hero-icon">🤖</span>
  <h1>AI 선호도 투표 결과</h1>
  <p>✦ 당곡고 · 수도여고 &nbsp;|&nbsp; 총 11명 응답 &nbsp;|&nbsp; 1등 3점 · 2등 2점 · 3등 1점 ✦</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════ 메트릭 카드 ═══════════════════
medals   = ["🥇","🥈","🥉"]
cls_list = ["mc-gold","mc-silver","mc-bronze"]
nm_clrs  = ["#fbbf24","#cbd5e1","#cd7c2f"]
grd = {
    "클로드":   "linear-gradient(135deg,#ff6b35,#fb923c)",
    "제미나이": "linear-gradient(135deg,#1d4ed8,#60a5fa)",
    "챗지피티": "linear-gradient(135deg,#059669,#34d399)",
}

cols = st.columns(3)
for i, ai in enumerate(ranked_ais):
    fc = int(rank_counts.loc[ai, 1]) if 1 in rank_counts.columns else 0
    with cols[i]:
        st.markdown(f"""
        <div class="metric-card {cls_list[i]}">
          <span class="medal-emoji">{medals[i]}</span>
          <div class="ai-name" style="color:{nm_clrs[i]}">{ai}</div>
          <div class="ai-score" style="
            background:{grd[ai]};
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;"
          >{int(total_score[ai])}점</div>
          <div class="ai-sub">🎯 1위 선택 {fc}회</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════ Chart 1: 총점 ════════════════
st.markdown("""
<div class="sec-header">
<span class="sec-icon" style="background:linear-gradient(135deg,#f97316,#fb923c)">📊</span>
총점 비교 (전체 11명 기준)
</div>""", unsafe_allow_html=True)

sorted_ais = total_score.sort_values().index.tolist()
fig1 = go.Figure()
for ai in sorted_ais:
    sc = int(total_score[ai])
    fig1.add_trace(go.Bar(
        x=[sc], y=[ai], orientation="h",
        marker=dict(
            color=AI_COLORS[ai],
            line=dict(width=0),
            opacity=0.92,
        ),
        text=[f" ◆ {sc}점"], textposition="inside",
        textfont=dict(size=17, color="white"),
        hovertemplate=f"<b>{ai}</b><br>총점: {sc}점<extra></extra>",
        showlegend=False,
    ))
fig1.update_layout(
    **BASE_LAYOUT, height=250, bargap=0.32,
    xaxis=ax("점수", rng=[0, int(total_score.max())+5]),
    yaxis=dict(tickfont=dict(size=15, color=TXT_CLR), linecolor=AXIS_CLR),
)
st.plotly_chart(fig1, use_container_width=True)

# ══════════════════════════════ Chart 2: 누적 순위 ════════════
st.markdown("""
<div class="sec-header">
<span class="sec-icon" style="background:linear-gradient(135deg,#8b5cf6,#a78bfa)">🏅</span>
순위별 선택 횟수 (누적 스택)
</div>""", unsafe_allow_html=True)

rank_meta = {
    1: {"label":"🥇 1등 (3점)", "color":"#fbbf24"},
    2: {"label":"🥈 2등 (2점)", "color":"#94a3b8"},
    3: {"label":"🥉 3등 (1점)", "color":"#b45309"},
}
fig2 = go.Figure()
for rank in [3, 2, 1]:
    m = rank_meta[rank]
    counts = [int(rank_counts.loc[ai, rank]) if rank in rank_counts.columns else 0 for ai in AIs]
    fig2.add_trace(go.Bar(
        name=m["label"], x=AIs, y=counts,
        marker=dict(color=m["color"], line=dict(width=1.5, color="rgba(255,255,255,0.12)")),
        text=[f"{c}명" if c else "" for c in counts],
        textposition="inside",
        textfont=dict(size=14, color="white"),
        hovertemplate="<b>%{x}</b><br>" + m["label"] + ": %{y}명<extra></extra>",
    ))
fig2.update_layout(
    **BASE_LAYOUT, height=360, barmode="stack", bargap=0.35,
    legend=dict(
        orientation="h", yanchor="bottom", y=1.04, xanchor="center", x=0.5,
        bgcolor="rgba(255,255,255,0.05)", bordercolor="rgba(255,255,255,0.1)",
        borderwidth=1, font=dict(size=12),
    ),
    xaxis=dict(tickfont=dict(size=15, color=TXT_CLR), linecolor=AXIS_CLR),
    yaxis=ax("선택 인원 수", dtick=1),
)
st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════ Chart 3: 학교별 ═══════════════
st.markdown("""
<div class="sec-header">
<span class="sec-icon" style="background:linear-gradient(135deg,#ec4899,#f472b6)">🏫</span>
학교별 AI 선호도 비교
</div>""", unsafe_allow_html=True)

school_cfg = {
    "당곡고":   {"n":7, "title_clr":"#818cf8"},
    "수도여고": {"n":4, "title_clr":"#f472b6"},
}
col_a, col_b = st.columns(2)
for col, school in zip([col_a, col_b], ["당곡고", "수도여고"]):
    with col:
        sc   = school_score.loc[school]
        cfg  = school_cfg[school]
        maxp = cfg["n"] * 3
        fig_s = go.Figure()
        for ai in AIs:
            pct = sc[ai] / maxp * 100
            fig_s.add_trace(go.Bar(
                x=[ai], y=[sc[ai]], name=ai,
                marker=dict(color=AI_COLORS[ai], line=dict(width=1, color="rgba(255,255,255,0.15)")),
                text=[f"<b>{int(sc[ai])}점</b><br>{pct:.0f}%"],
                textposition="inside",
                textfont=dict(size=13, color="white"),
                hovertemplate=f"<b>{ai}</b><br>{int(sc[ai])}점 ({pct:.1f}%)<extra></extra>",
                showlegend=False,
            ))
        fig_s.update_layout(
            **BASE_LAYOUT, height=310, bargap=0.35,
            title=dict(
                text=f"<b>{school}</b>  <span style='font-size:13px'>({cfg['n']}명)</span>",
                font=dict(size=16, color=cfg["title_clr"]), x=0.5,
            ),
            xaxis=dict(tickfont=dict(size=14, color=TXT_CLR), linecolor=AXIS_CLR),
            yaxis=ax("점수", rng=[0, maxp+2]),
        )
        st.plotly_chart(fig_s, use_container_width=True)

# ══════════════════════════════ 도넛 차트 ═════════════════════
st.markdown("""
<div class="sec-header">
<span class="sec-icon" style="background:linear-gradient(135deg,#f59e0b,#fbbf24)">🎯</span>
1위 선택 비율 (도넛 차트)
</div>""", unsafe_allow_html=True)

first_cnts = {ai: int(rank_counts.loc[ai, 1]) if 1 in rank_counts.columns else 0 for ai in AIs}
fig_d = go.Figure(go.Pie(
    labels=list(first_cnts.keys()),
    values=list(first_cnts.values()),
    hole=0.62,
    marker=dict(
        colors=[AI_COLORS[ai] for ai in AIs],
        line=dict(color="rgba(255,255,255,0.08)", width=3),
    ),
    textfont=dict(size=14, color="white"),
    texttemplate="<b>%{label}</b><br>%{value}명 (%{percent})",
    hovertemplate="<b>%{label}</b><br>1위 선택: %{value}명<br>비율: %{percent}<extra></extra>",
    pull=[0.05 if ai == ranked_ais[0] else 0 for ai in AIs],
    rotation=90,
))
fig_d.add_annotation(
    text=f"🏆<br><b>{ranked_ais[0]}</b><br><span>1위 최다</span>",
    x=0.5, y=0.5, showarrow=False,
    font=dict(size=15, color="white"), align="center",
)
fig_d.update_layout(
    **BASE_LAYOUT, height=380,
    legend=dict(
        orientation="v", x=0.75, y=0.5, xanchor="left",
        bgcolor="rgba(255,255,255,0.05)", bordercolor="rgba(255,255,255,0.1)",
        borderwidth=1, font=dict(size=13),
    ),
)
st.plotly_chart(fig_d, use_container_width=True)

# ══════════════════════════════ 테이블 ═══════════════════════
st.markdown("""
<div class="sec-header">
<span class="sec-icon" style="background:linear-gradient(135deg,#06b6d4,#0ea5e9)">📋</span>
응답자 전체 목록
</div>""", unsafe_allow_html=True)

AI_DOT = {"클로드":"🟠","제미나이":"🔵","챗지피티":"🟢"}
rows = []
for r in RAW:
    rows.append({
        "🏫 학교": r["school"],
        "👤 이름": r["name"],
        "🥇 1위": AI_DOT[r["ranks"][0]] + " " + r["ranks"][0],
        "🥈 2위": AI_DOT[r["ranks"][1]] + " " + r["ranks"][1],
        "🥉 3위": AI_DOT[r["ranks"][2]] + " " + r["ranks"][2],
    })
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True, height=420)

# ══════════════════════════════ 푸터 ══════════════════════════
st.markdown("""
<div style="text-align:center;margin-top:3rem;padding:1.4rem;
  background:rgba(255,255,255,0.04);border-radius:16px;
  border:1px solid rgba(255,255,255,0.08);">
  <span style="font-size:1.4rem">✨</span>
  <div style="color:rgba(255,255,255,0.4);font-size:0.82rem;margin-top:0.4rem;">
    당곡고 · 수도여고 AI 선호도 설문 결과 &nbsp;|&nbsp; Powered by Streamlit &amp; Plotly
  </div>
</div>
""", unsafe_allow_html=True)
