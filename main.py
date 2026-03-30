import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="AI 선호도 투표 결과", page_icon="🏆", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@500;700;800;900&display=swap" rel="stylesheet">
<style>

/* ── 전체 배경 ── */
[data-testid="stAppViewContainer"] {
    background: #0d0d1a;
    font-family: 'Noto Sans KR', sans-serif;
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background:
        radial-gradient(ellipse 900px 700px at 15% 10%, rgba(99,60,255,0.22) 0%, transparent 60%),
        radial-gradient(ellipse 700px 600px at 85% 85%, rgba(236,60,180,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 600px 500px at 70% 5%,  rgba(0,180,255,0.14) 0%, transparent 60%);
}
[data-testid="stHeader"]       { background: transparent; }
[data-testid="block-container"] { padding-top: 1.8rem; position: relative; z-index: 1; }

/* ── 히어로 배너 ── */
.hero {
    background: linear-gradient(135deg,
        rgba(99,60,255,0.30) 0%,
        rgba(236,60,180,0.22) 50%,
        rgba(0,180,255,0.22) 100%);
    border: 1.5px solid rgba(255,255,255,0.22);
    backdrop-filter: blur(24px);
    border-radius: 28px;
    padding: 3rem 2rem 2.4rem;
    text-align: center;
    margin-bottom: 2rem;
    position: relative; overflow: hidden;
}
.hero::before {
    content:""; position:absolute; top:-80px; left:-80px;
    width:260px; height:260px; border-radius:50%;
    background: radial-gradient(circle, rgba(120,80,255,0.45) 0%, transparent 70%);
}
.hero::after {
    content:""; position:absolute; bottom:-60px; right:-60px;
    width:220px; height:220px; border-radius:50%;
    background: radial-gradient(circle, rgba(255,60,160,0.38) 0%, transparent 70%);
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 999px;
    padding: 0.3rem 1.1rem;
    font-size: 0.85rem;
    color: rgba(255,255,255,0.75);
    margin-bottom: 1rem;
    letter-spacing: 0.04em;
}
.hero h1 {
    font-size: 2.8rem; font-weight: 900; margin: 0 0 0.6rem;
    background: linear-gradient(90deg, #c4b5fd, #f9a8d4, #7dd3fc, #c4b5fd);
    background-size: 250%; -webkit-background-clip: text;
    -webkit-text-fill-color: transparent; background-clip: text;
    animation: shimmer 5s linear infinite;
    line-height: 1.2;
}
@keyframes shimmer { 0%{background-position:0%} 100%{background-position:250%} }
.hero-sub {
    color: #e2e8f0;
    font-size: 1rem; font-weight: 500; margin: 0;
    text-shadow: 0 1px 6px rgba(0,0,0,0.5);
}

/* ── 메트릭 카드 ── */
.metric-card {
    border-radius: 22px;
    padding: 2rem 1.2rem 1.8rem;
    text-align: center;
    backdrop-filter: blur(18px);
    border: 1.5px solid;
    height: 100%;
}
.mc-1 { background: linear-gradient(145deg, rgba(251,191,36,0.20), rgba(217,119,6,0.10));  border-color: rgba(251,191,36,0.50); }
.mc-2 { background: linear-gradient(145deg, rgba(203,213,225,0.18), rgba(100,116,139,0.10)); border-color: rgba(203,213,225,0.45); }
.mc-3 { background: linear-gradient(145deg, rgba(205,130,70,0.20), rgba(161,78,24,0.10));   border-color: rgba(205,130,70,0.45); }

.card-medal  { font-size: 3rem; display:block; margin-bottom:0.5rem; line-height:1; }
.card-rank   { font-size: 0.82rem; color: #94a3b8; font-weight: 600; letter-spacing:0.1em; text-transform:uppercase; }
.card-name   { font-size: 1.6rem; font-weight: 900; margin: 0.4rem 0 0.2rem; color: #f8fafc; }
.card-score  { font-size: 3.2rem; font-weight: 900; line-height: 1.1; margin: 0.3rem 0; }
.card-detail { font-size: 0.9rem; color: #94a3b8; margin-top: 0.5rem; }
.card-detail span { color: #e2e8f0; font-weight: 700; }

.score-claude  { background: linear-gradient(135deg,#ff7c3a,#fbbf24); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.score-gemini  { background: linear-gradient(135deg,#60a5fa,#a78bfa); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.score-chatgpt { background: linear-gradient(135deg,#34d399,#6ee7b7); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }

/* ── 섹션 헤더 ── */
.sec-hd {
    display: flex; align-items: center; gap: 0.75rem;
    margin: 2.4rem 0 1rem;
}
.sec-hd-icon {
    width: 42px; height: 42px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.25rem;
    flex-shrink: 0;
}
.sec-hd-text { font-size: 1.25rem; font-weight: 800; color: #f1f5f9; }
.sec-hd-sub  { font-size: 0.82rem; color: #94a3b8; font-weight: 500; margin-top:0.15rem; }

/* ── 차트 래퍼 ── */
.chart-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 1.2rem 0.6rem 0.6rem;
    margin-bottom: 0.5rem;
}

/* ── 테이블 ── */
[data-testid="stDataFrame"] { border-radius: 16px; overflow: hidden; }
[data-testid="stDataFrame"] table { font-size: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# ── 데이터 ──────────────────────────────────────────────────
RAW = [
    {"name": "김한별", "school": "당곡고",  "ranks": ["클로드","제미나이","챗지피티"]},
    {"name": "변시현", "school": "당곡고",  "ranks": ["클로드","제미나이","챗지피티"]},
    {"name": "신연서", "school": "수도여고","ranks": ["클로드","챗지피티","제미나이"]},
    {"name": "이마루", "school": "당곡고",  "ranks": ["제미나이","클로드","챗지피티"]},
    {"name": "최윤영", "school": "수도여고","ranks": ["제미나이","클로드","챗지피티"]},
    {"name": "이지훈", "school": "당곡고",  "ranks": ["클로드","제미나이","챗지피티"]},
    {"name": "조윤서", "school": "수도여고","ranks": ["클로드","제미나이","챗지피티"]},
    {"name": "김도연", "school": "당곡고",  "ranks": ["클로드","제미나이","챗지피티"]},
    {"name": "이서영", "school": "수도여고","ranks": ["클로드","챗지피티","제미나이"]},
    {"name": "이한규", "school": "당곡고",  "ranks": ["클로드","제미나이","챗지피티"]},
    {"name": "김준영", "school": "당곡고",  "ranks": ["클로드","제미나이","챗지피티"]},
]
AIs = ["클로드","제미나이","챗지피티"]
SCORE = {0:3, 1:2, 2:1}

# AI별 색·그라디언트
C = {
    "클로드":   {"hex":"#fb923c", "glow":"rgba(251,146,60,0.45)",  "grad":["#ff7c3a","#fbbf24"], "cls":"score-claude"},
    "제미나이": {"hex":"#60a5fa", "glow":"rgba(96,165,250,0.45)",  "grad":["#60a5fa","#a78bfa"], "cls":"score-gemini"},
    "챗지피티": {"hex":"#34d399", "glow":"rgba(52,211,153,0.45)",  "grad":["#34d399","#6ee7b7"], "cls":"score-chatgpt"},
}
AI_EMOJI = {"클로드":"🟠","제미나이":"🔷","챗지피티":"🟢"}

BG    = "rgba(0,0,0,0)"
BGPL  = "rgba(255,255,255,0.03)"
GRID  = "rgba(255,255,255,0.10)"
WHITE = "#f1f5f9"
GRAY  = "#94a3b8"
FONT  = "Noto Sans KR, sans-serif"

def base(h, **kw):
    return dict(paper_bgcolor=BG, plot_bgcolor=BGPL,
                font=dict(family=FONT, color=WHITE, size=14),
                height=h, margin=dict(l=12,r=12,t=36,b=12), **kw)

def xax(**kw):
    return dict(showgrid=True, gridcolor=GRID, zeroline=False,
                tickfont=dict(size=14, color=WHITE), linecolor=GRID, **kw)

def yax(**kw):
    return dict(showgrid=True, gridcolor=GRID, zeroline=False,
                tickfont=dict(size=14, color=WHITE), linecolor=GRID, **kw)

# ── 전처리 ──────────────────────────────────────────────────
recs = []
for r in RAW:
    for i, ai in enumerate(r["ranks"]):
        recs.append({"name":r["name"],"school":r["school"],"ai":ai,"rank":i+1,"score":SCORE[i]})
df = pd.DataFrame(recs)

total   = df.groupby("ai")["score"].sum().reindex(AIs)
rcounts = df.groupby(["ai","rank"]).size().unstack(fill_value=0).reindex(AIs)
scscore = df.groupby(["school","ai"])["score"].sum().unstack(fill_value=0).reindex(columns=AIs)
ranked  = total.sort_values(ascending=False).index.tolist()

# ══════════════════════════════════════════════════════════════
#  🏆 히어로
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-badge">📊 설문 결과 대시보드 · 2025</div>
  <h1>🤖 AI 선호도 투표 결과</h1>
  <p class="hero-sub">
    🏫 당곡고 &amp; 수도여고 &nbsp;·&nbsp;
    👥 총 11명 응답 &nbsp;·&nbsp;
    🥇 1등 3점 &nbsp;🥈 2등 2점 &nbsp;🥉 3등 1점
  </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  🎖️ 메트릭 카드
# ══════════════════════════════════════════════════════════════
medals = ["🥇","🥈","🥉"]
cls    = ["mc-1","mc-2","mc-3"]
ranks_label = ["1위","2위","3위"]
cols = st.columns(3, gap="medium")

for i, ai in enumerate(ranked):
    fc = int(rcounts.loc[ai, 1]) if 1 in rcounts.columns else 0
    total_pct = int(total[ai] / (11*3) * 100)
    with cols[i]:
        st.markdown(f"""
        <div class="metric-card {cls[i]}">
          <span class="card-medal">{medals[i]}</span>
          <div class="card-rank">overall {ranks_label[i]}</div>
          <div class="card-name">{AI_EMOJI[ai]} {ai}</div>
          <div class="card-score {C[ai]['cls']}">{int(total[ai])}점</div>
          <div class="card-detail">
            1위 선택 <span>{fc}회</span> &nbsp;·&nbsp; 점유율 <span>{total_pct}%</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  📊 Chart 1 · 총점 가로 바
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-hd">
  <div class="sec-hd-icon" style="background:linear-gradient(135deg,#f97316,#fbbf24)">📊</div>
  <div>
    <div class="sec-hd-text">총점 비교</div>
    <div class="sec-hd-sub">1등 3점 · 2등 2점 · 3등 1점 가중 합산 (최대 33점)</div>
  </div>
</div>
""", unsafe_allow_html=True)

fig1 = go.Figure()
for ai in total.sort_values().index:
    sc = int(total[ai])
    fig1.add_trace(go.Bar(
        x=[sc], y=[f"{AI_EMOJI[ai]}  {ai}"],
        orientation="h", name=ai,
        marker=dict(
            color=C[ai]["hex"],
            line=dict(width=0),
        ),
        text=[f"<b>{sc}점</b>"],
        textposition="inside",
        textfont=dict(size=20, color="white", family=FONT),
        hovertemplate=f"<b>{ai}</b>  총점 {sc}점<extra></extra>",
        showlegend=False,
    ))

fig1.update_layout(
    **base(280, bargap=0.38),
    xaxis=xax(title=dict(text="점수", font=dict(size=13,color=GRAY)),
               range=[0, int(total.max())+6],
               tickfont=dict(size=13, color=WHITE)),
    yaxis=dict(tickfont=dict(size=17, color=WHITE, family=FONT), linecolor=GRID),
)
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig1, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  🏅 Chart 2 · 순위별 누적 스택
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-hd">
  <div class="sec-hd-icon" style="background:linear-gradient(135deg,#8b5cf6,#c4b5fd)">🏅</div>
  <div>
    <div class="sec-hd-text">순위별 선택 횟수</div>
    <div class="sec-hd-sub">각 AI를 몇 명이 1·2·3위로 선택했는지 누적 표시</div>
  </div>
</div>
""", unsafe_allow_html=True)

rank_cfg = {
    1: ("🥇  1위 선택 (3점)", "#fbbf24"),
    2: ("🥈  2위 선택 (2점)", "#94a3b8"),
    3: ("🥉  3위 선택 (1점)", "#b45309"),
}
fig2 = go.Figure()
for rank in [3,2,1]:
    label, color = rank_cfg[rank]
    counts = [int(rcounts.loc[ai, rank]) if rank in rcounts.columns else 0 for ai in AIs]
    x_labels = [f"{AI_EMOJI[ai]}  {ai}" for ai in AIs]
    fig2.add_trace(go.Bar(
        name=label, x=x_labels, y=counts,
        marker=dict(color=color, line=dict(width=1.5, color="rgba(255,255,255,0.10)")),
        text=[f"<b>{c}명</b>" if c else "" for c in counts],
        textposition="inside",
        textfont=dict(size=16, color="white", family=FONT),
        hovertemplate="<b>%{x}</b><br>" + label + ": %{y}명<extra></extra>",
    ))

fig2.update_layout(
    **base(380, barmode="stack", bargap=0.38),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.04, xanchor="center", x=0.5,
        bgcolor="rgba(255,255,255,0.07)", bordercolor=GRID, borderwidth=1,
        font=dict(size=14, color=WHITE),
    ),
    xaxis=xax(tickfont=dict(size=16, color=WHITE, family=FONT)),
    yaxis=yax(title=dict(text="선택 인원", font=dict(size=13,color=GRAY)), dtick=1),
)
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig2, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  🏫 Chart 3 · 학교별 비교
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-hd">
  <div class="sec-hd-icon" style="background:linear-gradient(135deg,#ec4899,#f9a8d4)">🏫</div>
  <div>
    <div class="sec-hd-text">학교별 AI 선호도</div>
    <div class="sec-hd-sub">당곡고 7명 vs 수도여고 4명 — 학교별 가중 점수 비교</div>
  </div>
</div>
""", unsafe_allow_html=True)

school_style = {
    "당곡고":   {"n":7, "color":"#a78bfa", "icon":"🟣"},
    "수도여고": {"n":4, "color":"#f472b6", "icon":"🩷"},
}
col_a, col_b = st.columns(2, gap="medium")
for col, school in zip([col_a,col_b], ["당곡고","수도여고"]):
    with col:
        sc    = scscore.loc[school]
        ss    = school_style[school]
        maxp  = ss["n"] * 3
        x_lbl = [f"{AI_EMOJI[ai]}  {ai}" for ai in AIs]

        fig_s = go.Figure()
        for ai, xl in zip(AIs, x_lbl):
            pct = sc[ai] / maxp * 100
            fig_s.add_trace(go.Bar(
                x=[xl], y=[sc[ai]], name=ai,
                marker=dict(color=C[ai]["hex"],
                            line=dict(width=1.2, color="rgba(255,255,255,0.15)")),
                text=[f"<b>{int(sc[ai])}점</b><br>{pct:.0f}%"],
                textposition="inside",
                textfont=dict(size=15, color="white", family=FONT),
                hovertemplate=f"<b>{ai}</b><br>{int(sc[ai])}점 ({pct:.1f}%)<extra></extra>",
                showlegend=False,
            ))
        fig_s.update_layout(
            **base(330, bargap=0.38),
            title=dict(
                text=f"{ss['icon']} <b>{school}</b>  <span style='font-size:13px'>({ss['n']}명)</span>",
                font=dict(size=18, color=ss["color"], family=FONT), x=0.5,
            ),
            xaxis=xax(tickfont=dict(size=15, color=WHITE, family=FONT)),
            yaxis=yax(title=dict(text="점수", font=dict(size=13,color=GRAY)),
                      range=[0, maxp+2]),
        )
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_s, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  🎯 Chart 4 · 1위 선택 도넛
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-hd">
  <div class="sec-hd-icon" style="background:linear-gradient(135deg,#f59e0b,#fde68a)">🎯</div>
  <div>
    <div class="sec-hd-text">1위 선택 비율</div>
    <div class="sec-hd-sub">총 11명 중 각 AI를 1위로 선택한 인원 비율</div>
  </div>
</div>
""", unsafe_allow_html=True)

fc_vals  = [int(rcounts.loc[ai,1]) if 1 in rcounts.columns else 0 for ai in AIs]
fc_label = [f"{AI_EMOJI[ai]} {ai}" for ai in AIs]

fig_d = go.Figure(go.Pie(
    labels=fc_label,
    values=fc_vals,
    hole=0.60,
    marker=dict(
        colors=[C[ai]["hex"] for ai in AIs],
        line=dict(color="#0d0d1a", width=4),
    ),
    textfont=dict(size=15, color="white", family=FONT),
    texttemplate="<b>%{label}</b><br>%{value}명 · %{percent}",
    hovertemplate="<b>%{label}</b><br>1위 선택: %{value}명<br>비율: %{percent}<extra></extra>",
    pull=[0.06 if ai == ranked[0] else 0 for ai in AIs],
    rotation=100,
    insidetextorientation="horizontal",
))
fig_d.add_annotation(
    x=0.5, y=0.54, showarrow=False, align="center",
    text=f"<b style='font-size:26px'>🏆</b>",
    font=dict(size=26, color="white"),
)
fig_d.add_annotation(
    x=0.5, y=0.42, showarrow=False, align="center",
    text=f"<b>{ranked[0]}</b>",
    font=dict(size=18, color=C[ranked[0]]["hex"], family=FONT),
)
fig_d.add_annotation(
    x=0.5, y=0.31, showarrow=False, align="center",
    text="1위 최다 선택",
    font=dict(size=13, color=GRAY, family=FONT),
)
fig_d.update_layout(
    **base(400),
    showlegend=True,
    legend=dict(
        orientation="v", x=0.73, y=0.5, xanchor="left",
        bgcolor="rgba(255,255,255,0.06)", bordercolor=GRID, borderwidth=1,
        font=dict(size=15, color=WHITE, family=FONT),
    ),
)
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig_d, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  📋 응답자 목록 테이블
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-hd">
  <div class="sec-hd-icon" style="background:linear-gradient(135deg,#06b6d4,#67e8f9)">📋</div>
  <div>
    <div class="sec-hd-text">응답자 전체 목록</div>
    <div class="sec-hd-sub">11명의 개별 순위 응답 원본</div>
  </div>
</div>
""", unsafe_allow_html=True)

rows = []
school_icon = {"당곡고":"🏫","수도여고":"🏫"}
for r in RAW:
    rows.append({
        "학교": f"{school_icon[r['school']]} {r['school']}",
        "이름": f"👤 {r['name']}",
        "🥇 1위": f"{AI_EMOJI[r['ranks'][0]]} {r['ranks'][0]}",
        "🥈 2위": f"{AI_EMOJI[r['ranks'][1]]} {r['ranks'][1]}",
        "🥉 3위": f"{AI_EMOJI[r['ranks'][2]]} {r['ranks'][2]}",
    })

st.dataframe(
    pd.DataFrame(rows),
    use_container_width=True, hide_index=True, height=430,
)

# ══════════════════════════════════════════════════════════════
#  푸터
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center; margin-top:3rem; padding:1.6rem;
  background:rgba(255,255,255,0.04); border-radius:20px;
  border:1px solid rgba(255,255,255,0.10);">
  <div style="font-size:1.6rem; margin-bottom:0.4rem;">🤖 🏆 📊</div>
  <div style="color:#94a3b8; font-size:0.88rem; font-weight:500;">
    당곡고 · 수도여고 AI 선호도 설문 결과 &nbsp;|&nbsp; Powered by Streamlit &amp; Plotly
  </div>
</div>
""", unsafe_allow_html=True)
