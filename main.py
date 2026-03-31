import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI 선호도 조사 결과",
    page_icon="🤖",
    layout="wide",
)

# ── 데이터 ───────────────────────────────────────────────────
responses = [
    {"이름": "김한별", "학교": "당곡고", "1위": "Claude", "2위": "Gemini", "3위": "ChatGPT"},
    {"이름": "변시현", "학교": "당곡고", "1위": "Claude", "2위": "Gemini", "3위": "ChatGPT"},
    {"이름": "신연서", "학교": "수도여고", "1위": "Claude", "2위": "ChatGPT", "3위": "Gemini"},
    {"이름": "이마루", "학교": "당곡고", "1위": "Gemini", "2위": "Claude", "3위": "ChatGPT"},
    {"이름": "최윤영", "학교": "수도여고", "1위": "Gemini", "2위": "Claude", "3위": "ChatGPT"},
    {"이름": "이지훈", "학교": "당곡고", "1위": "Claude", "2위": "Gemini", "3위": "ChatGPT"},
    {"이름": "조윤서", "학교": "수도여고", "1위": "Claude", "2위": "Gemini", "3위": "ChatGPT"},
    {"이름": "김도연", "학교": "당곡고", "1위": "Claude", "2위": "Gemini", "3위": "ChatGPT"},
    {"이름": "이서영", "학교": "수도여고", "1위": "Claude", "2위": "ChatGPT", "3위": "Gemini"},
    {"이름": "이한규", "학교": "당곡고", "1위": "Claude", "2위": "Gemini", "3위": "ChatGPT"},
    {"이름": "김준영", "학교": "당곡고", "1위": "Claude", "2위": "Gemini", "3위": "ChatGPT"},
]
df = pd.DataFrame(responses)

AIs = ["Claude", "Gemini", "ChatGPT"]
COLORS = {
    "Claude":   "#D97757",   # 클로드 오렌지
    "Gemini":   "#4285F4",   # 구글 블루
    "ChatGPT":  "#10A37F",   # 오픈AI 그린
}
SCORE_MAP = {"1위": 3, "2위": 2, "3위": 1}

# 점수 계산
score_data = {ai: 0 for ai in AIs}
rank_counts = {ai: {1: 0, 2: 0, 3: 0} for ai in AIs}
for row in responses:
    for rank_col, pts in SCORE_MAP.items():
        ai = row[rank_col]
        score_data[ai] += pts
        rank_counts[ai][int(rank_col[0])] += 1

# ── 헤더 ────────────────────────────────────────────────────
st.markdown("""
<h1 style='text-align:center; font-size:2.4rem; margin-bottom:0'>
    🤖 AI 선호도 설문 결과
</h1>
<p style='text-align:center; color:gray; font-size:1rem; margin-top:4px'>
    당곡고 · 수도여고 학생 11명 대상 | 2025
</p>
""", unsafe_allow_html=True)

st.divider()

# ── 요약 KPI 카드 ────────────────────────────────────────────
kpi_cols = st.columns(3)
rank_order = sorted(AIs, key=lambda a: score_data[a], reverse=True)
medals = ["🥇", "🥈", "🥉"]
for i, ai in enumerate(rank_order):
    with kpi_cols[i]:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg,{COLORS[ai]}22,{COLORS[ai]}44);
            border: 2px solid {COLORS[ai]};
            border-radius: 16px;
            padding: 20px;
            text-align: center;
        '>
            <div style='font-size:2.2rem'>{medals[i]}</div>
            <div style='font-size:1.6rem; font-weight:700; color:{COLORS[ai]}'>{ai}</div>
            <div style='font-size:1.1rem; color:gray'>총점 <b>{score_data[ai]}점</b></div>
            <div style='font-size:0.85rem; color:gray'>
                1위 {rank_counts[ai][1]}회 &nbsp;|&nbsp;
                2위 {rank_counts[ai][2]}회 &nbsp;|&nbsp;
                3위 {rank_counts[ai][3]}회
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: 총점 막대 + 1위 도넛 ──────────────────────────────
col1, col2 = st.columns([1.4, 1])

with col1:
    st.subheader("📊 가중 총점 비교 (1위=3점 · 2위=2점 · 3위=1점)")
    fig_bar = go.Figure()
    for ai in AIs:
        fig_bar.add_trace(go.Bar(
            x=[ai], y=[score_data[ai]],
            name=ai,
            marker_color=COLORS[ai],
            text=[f"{score_data[ai]}점"],
            textposition="outside",
            textfont=dict(size=18, color=COLORS[ai]),
            width=0.45,
        ))
    fig_bar.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(range=[0, max(score_data.values()) + 6], showgrid=True,
                   gridcolor="rgba(200,200,200,0.3)", zeroline=False),
        xaxis=dict(tickfont=dict(size=16)),
        margin=dict(t=20, b=20, l=20, r=20),
        height=340,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("🥇 1위 선택 분포")
    first_counts = [rank_counts[ai][1] for ai in AIs]
    fig_pie = go.Figure(go.Pie(
        labels=AIs,
        values=first_counts,
        hole=0.52,
        marker_colors=[COLORS[ai] for ai in AIs],
        textinfo="label+value",
        textfont=dict(size=14),
        hovertemplate="%{label}: %{value}명 (%{percent})<extra></extra>",
    ))
    fig_pie.add_annotation(
        text="1위 투표",
        x=0.5, y=0.5,
        font=dict(size=14, color="gray"),
        showarrow=False,
    )
    fig_pie.update_layout(
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        height=340,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Row 2: 누적 막대 (순위별 분포) ──────────────────────────
st.subheader("📈 순위별 득표 분포 (스택)")
fig_stack = go.Figure()
rank_labels = ["1위", "2위", "3위"]
rank_colors_alpha = ["FF", "AA", "55"]
for ri, (rank_label, alpha) in enumerate(zip(rank_labels, rank_colors_alpha), start=1):
    fig_stack.add_trace(go.Bar(
        name=rank_label,
        x=AIs,
        y=[rank_counts[ai][ri] for ai in AIs],
        marker_color=[f"{COLORS[ai]}{alpha}" for ai in AIs],
        text=[f"{rank_counts[ai][ri]}명" for ai in AIs],
        textposition="inside",
        textfont=dict(size=14, color="white"),
        hovertemplate=f"{rank_label}: %{{y}}명<extra></extra>",
    ))
fig_stack.update_layout(
    barmode="stack",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(title="응답 수(명)", showgrid=True,
               gridcolor="rgba(200,200,200,0.3)", zeroline=False),
    xaxis=dict(tickfont=dict(size=16)),
    legend=dict(title="순위", orientation="h", yanchor="bottom",
                y=1.02, xanchor="right", x=1),
    margin=dict(t=40, b=20, l=40, r=20),
    height=320,
)
st.plotly_chart(fig_stack, use_container_width=True)

# ── Row 3: 개인별 히트맵 ────────────────────────────────────
st.subheader("🗺️ 개인별 선택 히트맵")

# 히트맵용 매트릭스 (행=학생, 열=AI, 값=순위)
heatmap_z = []
heatmap_text = []
student_labels = [f"{r['학교']} {r['이름']}" for r in responses]

for row in responses:
    ranks = [int(col[0]) for col in ["1위", "2위", "3위"]]
    row_z = []
    row_txt = []
    for ai in AIs:
        for col in ["1위", "2위", "3위"]:
            if row[col] == ai:
                row_z.append(4 - int(col[0]))   # 1위→3, 2위→2, 3위→1 (높을수록 밝게)
                row_txt.append(col)
                break
    heatmap_z.append(row_z)
    heatmap_text.append(row_txt)

fig_heat = go.Figure(go.Heatmap(
    z=heatmap_z,
    x=AIs,
    y=student_labels,
    text=heatmap_text,
    texttemplate="%{text}",
    textfont=dict(size=13, color="white"),
    colorscale=[
        [0.0, "#333333"],
        [0.33, COLORS["ChatGPT"]],
        [0.66, COLORS["Gemini"]],
        [1.0,  COLORS["Claude"]],
    ],
    showscale=False,
    hovertemplate="%{y} → %{x}: %{text}<extra></extra>",
))
fig_heat.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=12), autorange="reversed"),
    margin=dict(t=20, b=20, l=130, r=20),
    height=420,
)
st.plotly_chart(fig_heat, use_container_width=True)

# ── Row 4: 학교별 비교 ──────────────────────────────────────
st.subheader("🏫 학교별 AI 평균 순위")

schools = ["당곡고", "수도여고"]
school_score = {s: {ai: 0 for ai in AIs} for s in schools}
school_count = {s: 0 for s in schools}

for row in responses:
    s = row["학교"]
    school_count[s] += 1
    for col in ["1위", "2위", "3위"]:
        school_score[s][row[col]] += SCORE_MAP[col]

fig_school = go.Figure()
for ai in AIs:
    fig_school.add_trace(go.Bar(
        name=ai,
        x=schools,
        y=[school_score[s][ai] / school_count[s] for s in schools],
        marker_color=COLORS[ai],
        text=[f"{school_score[s][ai]/school_count[s]:.1f}" for s in schools],
        textposition="outside",
        textfont=dict(size=14),
    ))
fig_school.update_layout(
    barmode="group",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(title="평균 점수", range=[0, 4],
               showgrid=True, gridcolor="rgba(200,200,200,0.3)"),
    xaxis=dict(tickfont=dict(size=15)),
    legend=dict(orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1),
    margin=dict(t=40, b=20, l=40, r=20),
    height=320,
)
st.plotly_chart(fig_school, use_container_width=True)

# ── 원본 데이터 테이블 ───────────────────────────────────────
with st.expander("📋 원본 응답 데이터 보기"):
    st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("""
<hr>
<p style='text-align:center;color:gray;font-size:0.85rem'>
    데이터 수집: 2025 · 응답자 11명 · 가중점수제(1위 3점, 2위 2점, 3위 1점)
</p>
""", unsafe_allow_html=True)
