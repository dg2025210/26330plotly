import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ══════════════════════════════════════════════════════════════
#  Page Config
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="⚗️ 화학 시험 분석 대시보드",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
#  Global Style
# ══════════════════════════════════════════════════════════════
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

/* ── Header ── */
.dash-header {
    text-align: center;
    padding: 1.6rem 0 0.4rem;
}
.dash-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #4fc3f7 0%, #7c4dff 55%, #f06292 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.dash-header p {
    color: #8899aa;
    font-size: 0.92rem;
    margin-top: 0.35rem;
}

/* ── KPI Cards ── */
.kpi-wrap {
    display: flex;
    gap: 1rem;
    margin: 1rem 0 1.4rem;
}
.kpi-card {
    flex: 1;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #2d3555;
    border-radius: 14px;
    padding: 1.1rem 1rem;
    text-align: center;
}
.kpi-icon  { font-size: 1.5rem; }
.kpi-label { color: #7788aa; font-size: 0.72rem; letter-spacing: .06em;
             text-transform: uppercase; margin: .15rem 0; }
.kpi-val   { font-size: 1.9rem; font-weight: 700; color: #4fc3f7; line-height: 1.1; }
.kpi-sub   { color: #556; font-size: 0.75rem; margin-top: .2rem; }

/* ── Section title ── */
.sec-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #ccd6f6;
    margin: 1.5rem 0 .6rem;
    padding-left: .35rem;
    border-left: 3px solid #7c4dff;
}

/* ── Sidebar ── */
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1a 0%, #111827 100%);
}
div[data-testid="stSidebar"] .stMarkdown h3 {
    color: #7c4dff;
}
</style>
""",
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════
#  Palette & Template
# ══════════════════════════════════════════════════════════════
EXAM_COLORS = {
    "수능":        "#4fc3f7",
    "3월 모의고사": "#69f0ae",
    "6월 모의평가": "#ff6e40",
}
SUBJ_COLORS = {
    "화학 I":  "#7c4dff",
    "화학 II": "#f06292",
}
TPL  = "plotly_dark"
BGTR = "rgba(0,0,0,0)"


# ══════════════════════════════════════════════════════════════
#  Data Generation  (캐시)
# ══════════════════════════════════════════════════════════════
@st.cache_data
def build_dataset():
    rng   = np.random.default_rng(42)
    years = list(range(2015, 2025))

    # ── 연도별 수능 화학I·II 평균점수 (근사 실측치) ──
    c1_base = {
        2015: 51.2, 2016: 57.8, 2017: 54.3, 2018: 59.1, 2019: 53.7,
        2020: 49.8, 2021: 52.4, 2022: 47.6, 2023: 54.9, 2024: 56.8,
    }
    c2_base = {
        2015: 44.1, 2016: 50.3, 2017: 47.2, 2018: 52.4, 2019: 46.8,
        2020: 43.1, 2021: 45.9, 2022: 41.3, 2023: 48.6, 2024: 49.7,
    }
    exam_offset = {"수능": 0.0, "3월 모의고사": 5.5, "6월 모의평가": 2.5}

    # ── 점수 데이터 ──
    score_rows = []
    for yr in years:
        for exam, off in exam_offset.items():
            for subj, bmap in [("화학 I", c1_base), ("화학 II", c2_base)]:
                avg  = bmap[yr] + off + rng.normal(0, 1.2)
                cut1 = min(100, avg + rng.uniform(22, 30))
                score_rows.append({
                    "연도": yr, "시험": exam, "과목": subj,
                    "평균점수":  round(avg,  1),
                    "1등급컷":   round(cut1, 1),
                    "표준편차":  round(rng.uniform(10, 17), 1),
                    "응시인원":  int(rng.integers(30_000, 300_000)),
                    "난이도지수": round(100 - avg, 1),
                })
    df_s = pd.DataFrame(score_rows)

    # ── 단원 & 기본 빈도 ──
    U1 = ["화학의 언어", "원자의 세계", "화학 결합과 분자",
          "역동적인 화학 반응", "산화·환원", "산·염기와 중화"]
    U2 = ["물질의 세 가지 상태", "용액", "반응 엔탈피",
          "화학 평형", "산·염기 평형", "전기화학"]
    B1 = [3, 4, 5, 4, 2, 2]
    B2 = [3, 3, 3, 4, 4, 3]

    freq_rows = []
    for yr in years:
        for exam in exam_offset:
            for u, b in zip(U1, B1):
                freq_rows.append({
                    "연도": yr, "시험": exam, "과목": "화학 I",
                    "단원": u, "출제수": max(0, b + rng.integers(-1, 2)),
                })
            for u, b in zip(U2, B2):
                freq_rows.append({
                    "연도": yr, "시험": exam, "과목": "화학 II",
                    "단원": u, "출제수": max(0, b + rng.integers(-1, 2)),
                })
    df_f = pd.DataFrame(freq_rows)

    # ── 킬러·준킬러 문항 ──
    Q_TYPES = ["자료 해석", "계산", "추론·판단", "실험 설계"]
    base_cr = {"수능": 12, "3월 모의고사": 20, "6월 모의평가": 15}

    killer_rows = []
    for yr in years:
        for exam in exam_offset:
            cr_b = base_cr[exam]
            for subj, units in [("화학 I", U1), ("화학 II", U2)]:
                # 킬러 (18~20번)
                killer_rows.append({
                    "연도": yr, "시험": exam, "과목": subj,
                    "문항번호": int(rng.choice([18, 19, 20])),
                    "정답률(%)": round(max(2.0, cr_b + rng.normal(0, 4)), 1),
                    "배점": int(rng.choice([3, 4])),
                    "단원": str(rng.choice(units[-3:])),
                    "유형": str(rng.choice(Q_TYPES)),
                    "난이도구분": "킬러",
                })
                # 준킬러 (15~17번)
                killer_rows.append({
                    "연도": yr, "시험": exam, "과목": subj,
                    "문항번호": int(rng.choice([15, 16, 17])),
                    "정답률(%)": round(min(45.0, max(8.0, cr_b + rng.normal(10, 5))), 1),
                    "배점": int(rng.choice([2, 3])),
                    "단원": str(rng.choice(units)),
                    "유형": str(rng.choice(Q_TYPES)),
                    "난이도구분": "준킬러",
                })
    df_k = pd.DataFrame(killer_rows)

    return df_s, df_f, df_k, U1, U2


df_scores, df_freq, df_killer, UNITS1, UNITS2 = build_dataset()


# ══════════════════════════════════════════════════════════════
#  Sidebar — Filters
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚗️ 필터 설정")
    st.markdown("---")

    sel_subj = st.multiselect(
        "과목 선택",
        ["화학 I", "화학 II"],
        default=["화학 I", "화학 II"],
    )
    sel_exam = st.multiselect(
        "시험 유형",
        ["수능", "3월 모의고사", "6월 모의평가"],
        default=["수능", "3월 모의고사", "6월 모의평가"],
    )
    yr_min, yr_max = st.slider("연도 범위", 2015, 2024, (2015, 2024))

    st.markdown("---")
    st.markdown("#### 📌 데이터 안내")
    st.info(
        "수능·모의고사 출제 경향을 바탕으로 구성된 분석 데이터입니다.  "
        "실측 평균점수(수능)를 기준으로 모의고사 값을 추산하였으며,  "
        "일부 수치는 추정치를 포함합니다.",
        icon="ℹ️",
    )

# ── 기본값 방어 ──
if not sel_subj:
    sel_subj = ["화학 I"]
if not sel_exam:
    sel_exam = ["수능"]

# ── 필터 적용 ──
fs = df_scores[
    df_scores["과목"].isin(sel_subj)
    & df_scores["시험"].isin(sel_exam)
    & df_scores["연도"].between(yr_min, yr_max)
]
ff = df_freq[
    df_freq["과목"].isin(sel_subj)
    & df_freq["시험"].isin(sel_exam)
    & df_freq["연도"].between(yr_min, yr_max)
]
fk = df_killer[
    df_killer["과목"].isin(sel_subj)
    & df_killer["시험"].isin(sel_exam)
    & df_killer["연도"].between(yr_min, yr_max)
]


# ══════════════════════════════════════════════════════════════
#  Header
# ══════════════════════════════════════════════════════════════
st.markdown(
    """
<div class="dash-header">
  <h1>⚗️ 화학 수능 · 모의고사 분석 대시보드</h1>
  <p>화학 I · II &nbsp;|&nbsp; 수능 · 3월 모의고사 · 6월 모의평가 &nbsp;|&nbsp; 2015 – 2024</p>
</div>
""",
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════════════════════
#  KPI Cards
# ══════════════════════════════════════════════════════════════
avg_score  = fs["평균점수"].mean()
avg_cut1   = fs["1등급컷"].mean()
avg_diff   = fk[fk["난이도구분"] == "킬러"]["정답률(%)"].mean()
total_rec  = len(fs)

kpi_data = [
    ("🎯", "평균 점수",       f"{avg_score:.1f}점",  "전체 시험 기준"),
    ("🏆", "평균 1등급컷",    f"{avg_cut1:.1f}점",   "100점 만점 기준"),
    ("💥", "킬러 평균 정답률", f"{avg_diff:.1f}%",    "18~20번 문항"),
    ("📋", "분석 데이터",      f"{total_rec:,}건",    "필터 적용 후"),
]

cols = st.columns(4)
for col, (icon, label, val, sub) in zip(cols, kpi_data):
    col.markdown(
        f"""
<div class="kpi-card">
  <div class="kpi-icon">{icon}</div>
  <div class="kpi-label">{label}</div>
  <div class="kpi-val">{val}</div>
  <div class="kpi-sub">{sub}</div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown("")

# ══════════════════════════════════════════════════════════════
#  Tabs
# ══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs(
    ["📈 연도별 추이", "📊 단원별 빈도", "🎯 킬러문항 분석", "🔍 종합 비교"]
)

# ────────────────────────────────────────────────────────────
# TAB 1 ── 연도별 추이
# ────────────────────────────────────────────────────────────
with tab1:

    st.markdown('<p class="sec-title">연도별 평균 점수 & 1등급컷 추이</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        fig = px.line(
            fs, x="연도", y="평균점수",
            color="시험", line_dash="과목",
            markers=True,
            color_discrete_map=EXAM_COLORS,
            template=TPL,
            labels={"평균점수": "평균 점수 (점)", "연도": ""},
            title="연도별 평균 점수",
        )
        fig.update_traces(line_width=2.5, marker_size=7)
        fig.update_layout(
            plot_bgcolor=BGTR, paper_bgcolor=BGTR,
            legend=dict(orientation="h", y=-0.22, x=0),
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.line(
            fs, x="연도", y="1등급컷",
            color="시험", line_dash="과목",
            markers=True,
            color_discrete_map=EXAM_COLORS,
            template=TPL,
            labels={"1등급컷": "1등급컷 (점)", "연도": ""},
            title="연도별 1등급컷 추이",
        )
        fig2.update_traces(line_width=2.5, marker_size=7)
        fig2.update_layout(
            plot_bgcolor=BGTR, paper_bgcolor=BGTR,
            legend=dict(orientation="h", y=-0.22, x=0),
            height=380,
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── 난이도 지수 히트맵 ──
    st.markdown('<p class="sec-title">난이도 지수 히트맵 (높을수록 어려운 시험)</p>', unsafe_allow_html=True)

    piv_diff = (
        fs.pivot_table(
            index=["시험", "과목"], columns="연도",
            values="난이도지수", aggfunc="mean",
        )
        .round(1)
    )
    piv_diff.index = [f"{a} · {b}" for a, b in piv_diff.index]

    fig3 = go.Figure(
        go.Heatmap(
            z=piv_diff.values,
            x=[str(c) for c in piv_diff.columns],
            y=list(piv_diff.index),
            colorscale="RdYlBu_r",
            text=piv_diff.values.round(1),
            texttemplate="%{text}",
            colorbar=dict(title="난이도"),
            zmid=50,
        )
    )
    fig3.update_layout(
        template=TPL, plot_bgcolor=BGTR, paper_bgcolor=BGTR,
        height=290, margin=dict(l=180, r=20, t=20, b=50),
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ── 응시인원 추이 ──
    st.markdown('<p class="sec-title">연도별 평균 응시인원</p>', unsafe_allow_html=True)

    pop_df = (
        fs.groupby(["연도", "과목"])["응시인원"]
        .mean()
        .reset_index()
    )
    fig4 = px.area(
        pop_df, x="연도", y="응시인원", color="과목",
        color_discrete_map=SUBJ_COLORS,
        template=TPL,
        labels={"응시인원": "평균 응시인원 (명)", "연도": ""},
    )
    fig4.update_layout(
        plot_bgcolor=BGTR, paper_bgcolor=BGTR,
        legend=dict(orientation="h", y=-0.18),
        height=290,
    )
    st.plotly_chart(fig4, use_container_width=True)


# ────────────────────────────────────────────────────────────
# TAB 2 ── 단원별 출제 빈도
# ────────────────────────────────────────────────────────────
with tab2:

    st.markdown('<p class="sec-title">단원별 누적 출제 빈도 (전 기간)</p>', unsafe_allow_html=True)

    total_freq = ff.groupby(["과목", "단원"])["출제수"].sum().reset_index()
    fig5 = px.bar(
        total_freq,
        x="출제수", y="단원", color="과목",
        facet_col="과목",
        color_discrete_map=SUBJ_COLORS,
        orientation="h",
        template=TPL,
        labels={"출제수": "총 출제 수", "단원": ""},
    )
    fig5.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig5.update_layout(
        plot_bgcolor=BGTR, paper_bgcolor=BGTR,
        showlegend=False, height=350,
        margin=dict(l=150),
    )
    st.plotly_chart(fig5, use_container_width=True)

    # ── 단원 × 연도 히트맵 ──
    st.markdown('<p class="sec-title">단원 × 연도 히트맵</p>', unsafe_allow_html=True)

    hm_c1, hm_c2 = st.columns(2)

    def draw_heatmap(col_obj, subj, cscale):
        with col_obj:
            sub_ff = ff[ff["과목"] == subj]
            if sub_ff.empty:
                st.info(f"{subj} 데이터 없음")
                return
            piv = (
                sub_ff.groupby(["단원", "연도"])["출제수"]
                .sum()
                .unstack(fill_value=0)
            )
            figH = go.Figure(
                go.Heatmap(
                    z=piv.values,
                    x=[str(c) for c in piv.columns],
                    y=list(piv.index),
                    colorscale=cscale,
                    text=piv.values,
                    texttemplate="%{text}",
                    colorbar=dict(title="출제수"),
                )
            )
            figH.update_layout(
                title=f"{subj} — 단원 × 연도",
                template=TPL, plot_bgcolor=BGTR, paper_bgcolor=BGTR,
                height=330, margin=dict(l=155, r=10, t=40, b=50),
            )
            st.plotly_chart(figH, use_container_width=True)

    if "화학 I"  in sel_subj: draw_heatmap(hm_c1, "화학 I",  "Blues")
    if "화학 II" in sel_subj: draw_heatmap(hm_c2, "화학 II", "Purples")

    # ── 썬버스트 ──
    st.markdown('<p class="sec-title">단원 출제 비중 — 썬버스트</p>', unsafe_allow_html=True)

    sun_df = ff.groupby(["과목", "단원"])["출제수"].sum().reset_index()
    sun_df["전체"] = "전체 과목"
    fig8 = px.sunburst(
        sun_df, path=["전체", "과목", "단원"], values="출제수",
        color="과목", color_discrete_map=SUBJ_COLORS,
        template=TPL,
    )
    fig8.update_layout(
        plot_bgcolor=BGTR, paper_bgcolor=BGTR, height=440,
    )
    st.plotly_chart(fig8, use_container_width=True)

    # ── 시험 유형별 단원 비교 ──
    st.markdown('<p class="sec-title">시험 유형별 단원 출제 비교</p>', unsafe_allow_html=True)

    bar_exam = ff.groupby(["시험", "단원", "과목"])["출제수"].sum().reset_index()
    fig9 = px.bar(
        bar_exam, x="단원", y="출제수", color="시험",
        facet_row="과목",
        color_discrete_map=EXAM_COLORS,
        barmode="group",
        template=TPL,
        labels={"출제수": "출제 수", "단원": ""},
    )
    fig9.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig9.update_xaxes(tickangle=-30)
    fig9.update_layout(
        plot_bgcolor=BGTR, paper_bgcolor=BGTR,
        height=540, legend=dict(orientation="h", y=-0.12),
    )
    st.plotly_chart(fig9, use_container_width=True)


# ────────────────────────────────────────────────────────────
# TAB 3 ── 킬러문항 분석
# ────────────────────────────────────────────────────────────
with tab3:

    # ── 정답률 추이 ──
    st.markdown('<p class="sec-title">연도별 킬러·준킬러 정답률 추이</p>', unsafe_allow_html=True)

    k_c1, k_c2 = st.columns(2)

    with k_c1:
        avg_k = (
            fk.groupby(["연도", "시험", "과목", "난이도구분"])["정답률(%)"]
            .mean()
            .reset_index()
        )
        fig_k1 = px.line(
            avg_k[avg_k["난이도구분"] == "킬러"],
            x="연도", y="정답률(%)",
            color="시험", line_dash="과목",
            markers=True, color_discrete_map=EXAM_COLORS,
            template=TPL,
            title="킬러문항 평균 정답률",
            labels={"정답률(%)": "정답률 (%)", "연도": ""},
        )
        fig_k1.add_hline(y=10, line_dash="dot", line_color="#ff5252",
                         annotation_text="10% 기준선",
                         annotation_position="top right")
        fig_k1.update_traces(line_width=2.5, marker_size=7)
        fig_k1.update_layout(
            plot_bgcolor=BGTR, paper_bgcolor=BGTR,
            legend=dict(orientation="h", y=-0.22, x=0),
            height=360,
        )
        st.plotly_chart(fig_k1, use_container_width=True)

    with k_c2:
        fig_k2 = px.box(
            fk, x="시험", y="정답률(%)",
            color="난이도구분",
            facet_col="과목",
            color_discrete_sequence=["#ff5252", "#ffa726"],
            template=TPL,
            title="정답률 분포 (킬러 vs 준킬러)",
        )
        fig_k2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig_k2.update_layout(
            plot_bgcolor=BGTR, paper_bgcolor=BGTR,
            legend=dict(orientation="h", y=-0.22, x=0),
            height=360,
        )
        st.plotly_chart(fig_k2, use_container_width=True)

    # ── 유형별 / 단원별 분석 ──
    st.markdown('<p class="sec-title">킬러문항 출제 유형 & 단원 분포</p>', unsafe_allow_html=True)

    k_c3, k_c4 = st.columns(2)

    with k_c3:
        type_cnt = (
            fk.groupby(["유형", "난이도구분"])
            .size()
            .reset_index(name="건수")
        )
        fig_k3 = px.bar(
            type_cnt, x="유형", y="건수", color="난이도구분",
            color_discrete_sequence=["#ff5252", "#ffa726"],
            barmode="group", template=TPL,
            title="유형별 출제 건수",
        )
        fig_k3.update_layout(
            plot_bgcolor=BGTR, paper_bgcolor=BGTR, height=320,
            legend=dict(orientation="h", y=-0.22),
        )
        st.plotly_chart(fig_k3, use_container_width=True)

    with k_c4:
        unit_k = (
            fk[fk["난이도구분"] == "킬러"]
            .groupby(["단원", "과목"])
            .size()
            .reset_index(name="건수")
            .sort_values("건수")
        )
        fig_k4 = px.bar(
            unit_k, x="건수", y="단원", color="과목",
            color_discrete_map=SUBJ_COLORS,
            orientation="h", template=TPL,
            title="킬러문항 출제 단원",
        )
        fig_k4.update_layout(
            plot_bgcolor=BGTR, paper_bgcolor=BGTR,
            height=320, margin=dict(l=140),
            legend=dict(orientation="h", y=-0.22),
        )
        st.plotly_chart(fig_k4, use_container_width=True)

    # ── 버블 차트 ──
    st.markdown('<p class="sec-title">연도별 킬러문항 정답률 분포 (버블 크기 = 배점)</p>', unsafe_allow_html=True)

    killer_only = fk[fk["난이도구분"] == "킬러"].copy()
    fig_bub = px.scatter(
        killer_only,
        x="연도", y="정답률(%)",
        size="배점", color="과목",
        symbol="시험",
        color_discrete_map=SUBJ_COLORS,
        template=TPL,
        hover_data=["단원", "유형", "문항번호"],
        labels={"정답률(%)": "정답률 (%)"},
        size_max=18,
    )
    fig_bub.update_layout(
        plot_bgcolor=BGTR, paper_bgcolor=BGTR, height=380,
        legend=dict(orientation="h", y=-0.18),
    )
    st.plotly_chart(fig_bub, use_container_width=True)

    # ── 배점별 정답률 바이올린 ──
    st.markdown('<p class="sec-title">배점별 정답률 분포 (바이올린)</p>', unsafe_allow_html=True)

    fk["배점_str"] = fk["배점"].astype(str) + "점"
    fig_vio = px.violin(
        fk, x="배점_str", y="정답률(%)",
        color="과목", box=True, points="outliers",
        color_discrete_map=SUBJ_COLORS,
        template=TPL,
        labels={"배점_str": "배점", "정답률(%)": "정답률 (%)"},
    )
    fig_vio.update_layout(
        plot_bgcolor=BGTR, paper_bgcolor=BGTR,
        height=340, legend=dict(orientation="h", y=-0.18),
    )
    st.plotly_chart(fig_vio, use_container_width=True)


# ────────────────────────────────────────────────────────────
# TAB 4 ── 종합 비교
# ────────────────────────────────────────────────────────────
with tab4:

    # ── 레이더 차트 ──
    st.markdown('<p class="sec-title">시험 유형별 단원 출제 균형 — 레이더 차트</p>', unsafe_allow_html=True)

    r_c1, r_c2 = st.columns(2)

    def draw_radar(col_obj, subj, units):
        with col_obj:
            sub_ff = ff[ff["과목"] == subj]
            if sub_ff.empty:
                st.info(f"{subj} 데이터 없음")
                return
            radar_df = (
                sub_ff.groupby(["시험", "단원"])["출제수"]
                .sum()
                .reset_index()
            )
            figR = go.Figure()
            for exam in sel_exam:
                d = radar_df[radar_df["시험"] == exam]
                d = d.set_index("단원").reindex(units, fill_value=0).reset_index()
                r  = d["출제수"].tolist() + [d["출제수"].iloc[0]]
                th = d["단원"].tolist()   + [d["단원"].iloc[0]]
                figR.add_trace(
                    go.Scatterpolar(
                        r=r, theta=th, name=exam,
                        line_color=EXAM_COLORS.get(exam, "#888"),
                        fill="toself",
                        fillcolor=EXAM_COLORS.get(exam, "#888"),
                        opacity=0.22,
                        line_width=2,
                    )
                )
            figR.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, showticklabels=False),
                    angularaxis=dict(tickfont=dict(size=10)),
                ),
                template=TPL, paper_bgcolor=BGTR,
                legend=dict(orientation="h", y=-0.12),
                title=f"{subj} — 단원 출제 균형",
                height=420,
            )
            col_obj.plotly_chart(figR, use_container_width=True)

    if "화학 I"  in sel_subj: draw_radar(r_c1, "화학 I",  UNITS1)
    if "화학 II" in sel_subj: draw_radar(r_c2, "화학 II", UNITS2)

    # ── 상관관계 산점도 ──
    st.markdown('<p class="sec-title">시험 평균점수 ↔ 킬러문항 정답률 상관관계</p>', unsafe_allow_html=True)

    merged = fs.merge(
        fk[fk["난이도구분"] == "킬러"]
        .groupby(["연도", "시험", "과목"])["정답률(%)"]
        .mean()
        .reset_index(),
        on=["연도", "시험", "과목"],
        how="inner",
    )
    fig_corr = px.scatter(
        merged,
        x="평균점수", y="정답률(%)",
        color="과목", symbol="시험",
        color_discrete_map=SUBJ_COLORS,
        trendline="ols",
        template=TPL,
        hover_data=["연도"],
        labels={
            "평균점수":  "시험 평균점수 (점)",
            "정답률(%)": "킬러문항 정답률 (%)",
        },
        title="추세선: 평균점수가 높을수록 킬러 정답률도 높아지는 경향",
    )
    fig_corr.update_layout(
        plot_bgcolor=BGTR, paper_bgcolor=BGTR,
        height=390, legend=dict(orientation="h", y=-0.18),
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    # ── 전년 대비 변화율 ──
    st.markdown('<p class="sec-title">전년 대비 평균점수 변화율</p>', unsafe_allow_html=True)

    yoy = (
        fs.groupby(["연도", "과목"])["평균점수"]
        .mean()
        .reset_index()
        .sort_values("연도")
    )
    yoy["변화율(%)"] = yoy.groupby("과목")["평균점수"].pct_change() * 100
    yoy = yoy.dropna()

    fig_yoy = px.bar(
        yoy, x="연도", y="변화율(%)", color="과목",
        color_discrete_map=SUBJ_COLORS,
        barmode="group", template=TPL,
        labels={"변화율(%)": "전년 대비 변화율 (%)"},
    )
    fig_yoy.add_hline(y=0, line_color="white", line_width=1, opacity=0.35)
    fig_yoy.update_layout(
        plot_bgcolor=BGTR, paper_bgcolor=BGTR,
        height=310, legend=dict(orientation="h", y=-0.2),
    )
    st.plotly_chart(fig_yoy, use_container_width=True)

    # ── 시험별 평균 비교 ──
    st.markdown('<p class="sec-title">시험 유형 × 과목별 평균 점수 비교</p>', unsafe_allow_html=True)

    avg_bar = (
        fs.groupby(["시험", "과목"])["평균점수"]
        .mean()
        .reset_index()
    )
    fig_avg = px.bar(
        avg_bar, x="시험", y="평균점수", color="과목",
        color_discrete_map=SUBJ_COLORS,
        barmode="group", template=TPL,
        text_auto=".1f",
        labels={"평균점수": "평균 점수 (점)"},
    )
    fig_avg.update_traces(textposition="outside")
    fig_avg.update_layout(
        plot_bgcolor=BGTR, paper_bgcolor=BGTR,
        height=340, legend=dict(orientation="h", y=-0.2),
        yaxis_range=[0, 80],
    )
    st.plotly_chart(fig_avg, use_container_width=True)

# ── Footer ──────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#445; font-size:.8rem;'>"
    "⚗️ 화학 수능·모의고사 분석 대시보드 &nbsp;|&nbsp; "
    "데이터 기준: 2015–2024 수능·3월·6월 모의 &nbsp;|&nbsp; "
    "Powered by Streamlit &amp; Plotly"
    "</p>",
    unsafe_allow_html=True,
)
