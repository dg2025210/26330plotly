```python
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI 선호도 투표 결과",
    page_icon="🤖",
    layout="wide",
)

# ── 스타일 ───────────────────────────────────────────────────
st.markdown("""
<style>
    .title-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .title-box h1 { color: white; font-size: 2rem; margin: 0; }
    .title-box p  { color: rgba(255,255,255,0.85); margin: 0.4rem 0 0; font-size: 1rem; }
    .metric-card {
        background: #f8f9ff;
        border-left: 5px solid;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #4a4a6a;
        margin: 1.8rem 0 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ── 원본 데이터 ───────────────────────────────────────────────
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

AIs   = ["클로드", "제미나이", "챗지피티"]
SCORE = {0: 3, 1: 2, 2: 1}   # 인덱스(0=1등) → 점수
COLORS = {
    "클로드":   "#f59e42",
    "제미나이": "#4f8ef7",
    "챗지피티": "#34d399",
}
SCHOOL_COLORS = {"당곡고": "#818cf8", "수도여고": "#f472b6"}

# ── 전처리 ────────────────────────────────────────────────────
records = []
for r in RAW:
    for rank_i, ai in enumerate(r["ranks"]):
        records.append({
            "name": r["name"],
            "school": r["school"],
            "ai": ai,
            "rank": rank_i + 1,
            "score": SCORE[rank_i],
        })
df = pd.DataFrame(records)

# 전체 점수 집계
total_score = df.groupby("ai")["score"].sum().reindex(AIs)
rank_counts  = df.groupby(["ai", "rank"]).size().unstack(fill_value=0).reindex(AIs)

# 학교별 점수
school_score = (
    df.groupby(["school", "ai"])["score"]
    .sum()
    .unstack(fill_value=0)
    .reindex(columns=AIs)
)

# ── 헤더 ─────────────────────────────────────────────────────
st.markdown("""
<div class="title-box">
  <h1>🤖 AI 선호도 투표 결과</h1>
  <p>당곡고 · 수도여고 · 총 11명 응답 | 1등 3점 · 2등 2점 · 3등 1점</p>
</div>
""", unsafe_allow_html=True)

# ── 요약 메트릭 ───────────────────────────────────────────────
cols = st.columns(3)
medals = ["🥇", "🥈", "🥉"]
border_c = ["#f59e42", "#4f8ef7", "#34d399"]
ranked_ais = total_score.sort_values(ascending=False).index.tolist()

for i, ai in enumerate(ranked_ais):
    with cols[i]:
        first_cnt = rank_counts.loc[ai, 1] if 1 in rank_counts.columns else 0
        st.markdown(f"""
        <div class="metric-card" style="border-color:{border_c[i]}">
            <div style="font-size:2rem">{medals[i]}</div>
            <div style="font-size:1.4rem; font-weight:800; color:{COLORS[ai]}">{ai}</div>
            <div style="font-size:2rem; font-weight:900; color:#222">{int(total_score[ai])}점</div>
            <div style="color:#888; font-size:0.85rem">1위 선택 {int(first_cnt)}회</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Chart 1 : 총점 가로 바 차트 ───────────────────────────────
st.markdown('<div class="section-header">📊 총점 비교 (전체)</div>', unsafe_allow_html=True)

fig1 = go.Figure()
sorted_ais = total_score.sort_values().index.tolist()
for ai in sorted_ais:
    fig1.add_trace(go.Bar(
        x=[total_score[ai]],
        y=[ai],
        orientation="h",
        name=ai,
        marker_color=COLORS[ai],
        text=[f"<b>{int(total_score[ai])}점</b>"],
        textposition="inside",
        textfont=dict(size=16, color="white"),
        hovertemplate=f"<b>{ai}</b><br>총점: {int(total_score[ai])}점<extra></extra>",
    ))

fig1.update_layout(
    showlegend=False,
    height=260,
    margin=dict(l=10, r=40, t=20, b=20),
    plot_bgcolor="white",
    xaxis=dict(showgrid=True, gridcolor="#e5e7eb", range=[0, 36], title="점수"),
    yaxis=dict(tickfont=dict(size=15, family="Malgun Gothic, sans-serif")),
    bargap=0.35,
)
st.plotly_chart(fig1, use_container_width=True)

# ── Chart 2 : 순위별 누적 바 차트 ────────────────────────────
st.markdown('<div class="section-header">🏅 순위별 선택 횟수 (누적)</div>', unsafe_allow_html=True)

fig2 = go.Figure()
rank_labels = {1: "1등 (3점)", 2: "2등 (2점)", 3: "3등 (1점)"}
rank_colors  = {1: "#facc15", 2: "#94a3b8", 3: "#cd7c2f"}

for rank in [1, 2, 3]:
    counts = [rank_counts.loc[ai, rank] if rank in rank_counts.columns else 0 for ai in AIs]
    fig2.add_trace(go.Bar(
        name=rank_labels[rank],
        x=AIs,
        y=counts,
        marker_color=rank_colors[rank],
        text=[f"{c}명" if c > 0 else "" for c in counts],
        textposition="inside",
        textfont=dict(size=13, color="white"),
        hovertemplate="<b>%{x}</b><br>" + rank_labels[rank] + ": %{y}명<extra></extra>",
    ))

fig2.update_layout(
    barmode="stack",
    height=340,
    margin=dict(l=10, r=10, t=20, b=20),
    plot_bgcolor="white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    xaxis=dict(tickfont=dict(size=14, family="Malgun Gothic, sans-serif")),
    yaxis=dict(showgrid=True, gridcolor="#e5e7eb", title="선택 인원 수", dtick=1),
)
st.plotly_chart(fig2, use_container_width=True)

# ── Chart 3 : 학교별 비교 ────────────────────────────────────
st.markdown('<div class="section-header">🏫 학교별 AI 선호도 비교</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

for col, school in zip([col_a, col_b], ["당곡고", "수도여고"]):
    with col:
        n = sum(1 for r in RAW if r["school"] == school)
        sc = school_score.loc[school]
        max_possible = n * 3

        fig_s = go.Figure()
        for ai in AIs:
            pct = sc[ai] / max_possible * 100
            fig_s.add_trace(go.Bar(
                x=[ai],
                y=[sc[ai]],
                name=ai,
                marker_color=COLORS[ai],
                text=[f"<b>{int(sc[ai])}점</b><br>({pct:.0f}%)"],
                textposition="inside",
                textfont=dict(size=13, color="white"),
                hovertemplate=f"<b>{ai}</b><br>점수: {int(sc[ai])}점<br>비율: {pct:.1f}%<extra></extra>",
            ))

        fig_s.update_layout(
            title=dict(
                text=f"<b>{school}</b>  ({n}명)",
                font=dict(size=15, color=SCHOOL_COLORS[school]),
                x=0.5,
            ),
            showlegend=False,
            height=300,
            margin=dict(l=10, r=10, t=50, b=20),
            plot_bgcolor="white",
            xaxis=dict(tickfont=dict(size=13, family="Malgun Gothic, sans-serif")),
            yaxis=dict(showgrid=True, gridcolor="#e5e7eb", title="점수"),
            bargap=0.3,
        )
        st.plotly_chart(fig_s, use_container_width=True)

# ── 응답자 상세 테이블 ────────────────────────────────────────
st.markdown('<div class="section-header">📋 응답자 전체 목록</div>', unsafe_allow_html=True)

table_rows = []
for r in RAW:
    table_rows.append({
        "학교": r["school"],
        "이름": r["name"],
        "1위": r["ranks"][0],
        "2위": r["ranks"][1],
        "3위": r["ranks"][2],
    })

df_table = pd.DataFrame(table_rows)

def color_ai(val):
    colors_map = {"클로드": "#fff7ed", "제미나이": "#eff6ff", "챗지피티": "#f0fdf4"}
    return f"background-color: {colors_map.get(val, 'white')}"

styled = (
    df_table.style
    .applymap(color_ai, subset=["1위", "2위", "3위"])
    .set_properties(**{"text-align": "center"})
)
st.dataframe(styled, use_container_width=True, hide_index=True)

# ── 푸터 ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center style='color:#aaa; font-size:0.8rem'>당곡고 · 수도여고 AI 선호도 설문 | 2025</center>",
    unsafe_allow_html=True,
)
```

`requirements.txt`는 그대로예요:
```
streamlit>=1.32.0
plotly>=5.20.0
pandas>=2.0.0
```
