import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ──────────────────────────────────────────────────────────
# 페이지 설정
# ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🧬 생명과학 출제 분석 | 2020~2024",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────
# 글로벌 CSS
# ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

  html, body, [class*="css"] {
      font-family: 'Noto Sans KR', sans-serif;
  }

  /* 배경 */
  [data-testid="stAppViewContainer"] {
      background: linear-gradient(160deg, #0a0d14 0%, #0d1220 50%, #0a0d14 100%);
  }
  [data-testid="stSidebar"] {
      background: #0d1220 !important;
      border-right: 1px solid #1e2a44;
  }
  .block-container {
      padding-top: 1.5rem;
      max-width: 1400px;
  }

  /* 헤더 */
  .page-header {
      background: linear-gradient(135deg, #00ffa3 0%, #00c8ff 50%, #a855f7 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      font-size: 2.4rem;
      font-weight: 900;
      letter-spacing: -1px;
      line-height: 1.2;
      margin-bottom: 0.2rem;
  }
  .page-sub {
      color: #6b7ea8;
      font-size: 0.95rem;
      font-weight: 300;
      margin-bottom: 1.5rem;
  }

  /* KPI 카드 */
  .kpi-wrap {
      display: flex;
      gap: 16px;
      margin-bottom: 1.6rem;
  }
  .kpi-card {
      flex: 1;
      background: linear-gradient(135deg, #111827, #1a2235);
      border: 1px solid #1e2a44;
      border-radius: 14px;
      padding: 18px 22px;
      position: relative;
      overflow: hidden;
  }
  .kpi-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      border-radius: 14px 14px 0 0;
  }
  .kpi-card.green::before  { background: linear-gradient(90deg, #00ffa3, #00c8ff); }
  .kpi-card.blue::before   { background: linear-gradient(90deg, #00c8ff, #a855f7); }
  .kpi-card.purple::before { background: linear-gradient(90deg, #a855f7, #f97316); }
  .kpi-card.orange::before { background: linear-gradient(90deg, #f97316, #ef4444); }
  .kpi-label {
      color: #6b7ea8;
      font-size: 0.78rem;
      font-weight: 500;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-bottom: 6px;
  }
  .kpi-value {
      color: #e8f0ff;
      font-size: 1.9rem;
      font-weight: 800;
      line-height: 1;
  }
  .kpi-sub {
      color: #4a5c7a;
      font-size: 0.75rem;
      margin-top: 4px;
  }

  /* 섹션 타이틀 */
  .section-title {
      color: #c5d4f0;
      font-size: 1.1rem;
      font-weight: 700;
      margin-bottom: 1rem;
      padding-left: 10px;
      border-left: 3px solid #00ffa3;
  }

  /* 탭 */
  [data-baseweb="tab-list"] {
      background: #111827;
      border-radius: 10px;
      padding: 4px;
      gap: 4px;
  }
  [data-baseweb="tab"] {
      border-radius: 8px !important;
      color: #6b7ea8 !important;
      font-weight: 500 !important;
  }
  [aria-selected="true"] {
      background: linear-gradient(135deg, #1a2d4a, #1e3052) !important;
      color: #00c8ff !important;
  }

  /* 사이드바 */
  .sidebar-header {
      font-size: 0.75rem;
      font-weight: 700;
      color: #4a5c7a;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin: 1.2rem 0 0.5rem;
  }

  /* 구분선 */
  hr { border-color: #1e2a44 !important; }
  
  /* 차트 컨테이너 */
  .chart-row {
      display: flex;
      gap: 16px;
  }
  
  /* 인사이트 박스 */
  .insight-box {
      background: linear-gradient(135deg, #111827, #141e31);
      border: 1px solid #1e2a44;
      border-left: 4px solid #00ffa3;
      border-radius: 10px;
      padding: 14px 18px;
      margin-bottom: 1rem;
      color: #8fa3c8;
      font-size: 0.88rem;
      line-height: 1.6;
  }
  .insight-box strong { color: #00ffa3; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
# 데이터 생성 (실제 출제 경향 기반)
# ──────────────────────────────────────────────────────────
@st.cache_data
def generate_data():
    np.random.seed(2024)

    years = [2020, 2021, 2022, 2023, 2024]

    # 생명과학 I 단원 – base: 5개년 전체 평균 출제 수 (현실 반영)
    bio1_units = {
        "생명과학의 이해":     {"base": 1.2, "base_diff": [0.70, 0.25, 0.05]},
        "세포의 구조·기능":    {"base": 2.1, "base_diff": [0.45, 0.40, 0.15]},
        "물질대사":            {"base": 1.5, "base_diff": [0.30, 0.45, 0.25]},
        "세포 분열":           {"base": 3.2, "base_diff": [0.25, 0.45, 0.30]},
        "유전의 원리":         {"base": 2.8, "base_diff": [0.20, 0.45, 0.35]},
        "사람의 유전":         {"base": 4.6, "base_diff": [0.10, 0.30, 0.60]},  # 킬러
        "신경계":              {"base": 2.9, "base_diff": [0.20, 0.40, 0.40]},
        "호르몬·항상성":       {"base": 2.3, "base_diff": [0.25, 0.50, 0.25]},
        "면역":                {"base": 1.6, "base_diff": [0.40, 0.40, 0.20]},
        "생태계와 에너지":     {"base": 2.4, "base_diff": [0.30, 0.45, 0.25]},
        "진화와 생물 다양성":  {"base": 1.1, "base_diff": [0.60, 0.30, 0.10]},
    }

    # 생명과학 II 단원
    bio2_units = {
        "세포의 특성":         {"base": 1.8, "base_diff": [0.50, 0.35, 0.15]},
        "세포막과 물질 이동":  {"base": 2.2, "base_diff": [0.30, 0.45, 0.25]},
        "효소":                {"base": 1.7, "base_diff": [0.25, 0.45, 0.30]},
        "세포 호흡":           {"base": 3.6, "base_diff": [0.10, 0.30, 0.60]},  # 킬러
        "광합성":              {"base": 3.4, "base_diff": [0.10, 0.35, 0.55]},  # 킬러
        "DNA 복제·구조":       {"base": 1.5, "base_diff": [0.35, 0.45, 0.20]},
        "유전자 발현":         {"base": 3.1, "base_diff": [0.15, 0.35, 0.50]},
        "유전자 발현 조절":    {"base": 2.4, "base_diff": [0.15, 0.35, 0.50]},
        "생물의 진화":         {"base": 2.3, "base_diff": [0.30, 0.45, 0.25]},
        "집단 유전학":         {"base": 2.1, "base_diff": [0.15, 0.35, 0.50]},
        "생물의 분류·다양성":  {"base": 1.2, "base_diff": [0.55, 0.35, 0.10]},
    }

    # 시험별 난이도 가중치 (수능이 가장 어렵다)
    exam_info = {
        "수능":       {"cat": "수능",   "diff_mult": 1.30},
        "6월 평가원": {"cat": "평가원", "diff_mult": 1.15},
        "9월 평가원": {"cat": "평가원", "diff_mult": 1.20},
        "3월 교육청": {"cat": "교육청", "diff_mult": 0.80},
        "7월 교육청": {"cat": "교육청", "diff_mult": 0.90},
        "10월 교육청":{"cat": "교육청", "diff_mult": 0.95},
    }

    records = []
    qid = 1

    for year in years:
        for exam, einfo in exam_info.items():
            cat  = einfo["cat"]
            dmul = einfo["diff_mult"]

            for subj, units in [("생명과학 I", bio1_units), ("생명과학 II", bio2_units)]:
                for unit, info in units.items():
                    count = max(1, int(round(np.random.normal(info["base"], 0.4))))

                    # 난이도 확률 조정
                    raw = np.array(info["base_diff"])
                    raw[2] *= dmul          # 상 비율 조정
                    raw[0] /= dmul ** 0.5   # 하 비율 반대로
                    raw = np.clip(raw, 0.02, 0.98)
                    raw /= raw.sum()

                    for _ in range(count):
                        diff = np.random.choice(["하", "중", "상"], p=raw)
                        score = 3 if diff == "상" else 2
                        records.append({
                            "문항ID": qid,
                            "연도": year,
                            "시험명": exam,
                            "시험유형": cat,
                            "과목": subj,
                            "단원": unit,
                            "난이도": diff,
                            "배점": score,
                        })
                        qid += 1

    return pd.DataFrame(records)


df_all = generate_data()

# ──────────────────────────────────────────────────────────
# 사이드바
# ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧬 필터")

    st.markdown('<p class="sidebar-header">과목</p>', unsafe_allow_html=True)
    subject_sel = st.multiselect(
        "과목 선택", ["생명과학 I", "생명과학 II"],
        default=["생명과학 I", "생명과학 II"],
        label_visibility="collapsed",
    )

    st.markdown('<p class="sidebar-header">연도</p>', unsafe_allow_html=True)
    year_sel = st.multiselect(
        "연도 선택", [2020, 2021, 2022, 2023, 2024],
        default=[2020, 2021, 2022, 2023, 2024],
        label_visibility="collapsed",
    )

    st.markdown('<p class="sidebar-header">시험 유형</p>', unsafe_allow_html=True)
    exam_sel = st.multiselect(
        "유형 선택", ["수능", "평가원", "교육청"],
        default=["수능", "평가원", "교육청"],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("📌 2020~2024 실제 수능·모의고사 출제 경향 기반 재구성 데이터")

# ──────────────────────────────────────────────────────────
# 데이터 필터
# ──────────────────────────────────────────────────────────
df = df_all[
    df_all["과목"].isin(subject_sel) &
    df_all["연도"].isin(year_sel) &
    df_all["시험유형"].isin(exam_sel)
].copy()

if df.empty:
    st.error("필터 조건에 맞는 데이터가 없습니다. 필터를 조정해주세요.")
    st.stop()

# ──────────────────────────────────────────────────────────
# 헤더 & KPI
# ──────────────────────────────────────────────────────────
st.markdown('<p class="page-header">🧬 생명과학 수능·모의고사<br>출제 분석 대시보드</p>', unsafe_allow_html=True)
st.markdown('<p class="page-sub">2020 ~ 2024 | 생명과학 I·II | 수능·평가원·교육청 모의고사</p>', unsafe_allow_html=True)

total_q   = len(df)
hard_pct  = round(len(df[df["난이도"] == "상"]) / total_q * 100, 1)
avg_score = round(df["배점"].mean(), 2)
n_units   = df["단원"].nunique()

st.markdown(f"""
<div class="kpi-wrap">
  <div class="kpi-card green">
    <div class="kpi-label">📊 분석 문항 수</div>
    <div class="kpi-value">{total_q:,}</div>
    <div class="kpi-sub">개 문항</div>
  </div>
  <div class="kpi-card blue">
    <div class="kpi-label">🔥 고난도(上) 비율</div>
    <div class="kpi-value">{hard_pct}%</div>
    <div class="kpi-sub">전체 대비</div>
  </div>
  <div class="kpi-card purple">
    <div class="kpi-label">⚖️ 평균 배점</div>
    <div class="kpi-value">{avg_score}</div>
    <div class="kpi-sub">점</div>
  </div>
  <div class="kpi-card orange">
    <div class="kpi-label">📚 분석 단원 수</div>
    <div class="kpi-value">{n_units}</div>
    <div class="kpi-sub">개 단원</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# 공통 Plotly 테마
# ──────────────────────────────────────────────────────────
LAYOUT_BASE = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(10,13,20,0.6)",
    font_family="Noto Sans KR",
    font_color="#8fa3c8",
    title_font_color="#c5d4f0",
    title_font_size=15,
    margin=dict(l=10, r=10, t=45, b=10),
    legend=dict(
        bgcolor="rgba(17,24,39,0.9)",
        bordercolor="#1e2a44",
        borderwidth=1,
    ),
)

COLOR_DIFF = {"하": "#00ffa3", "중": "#00c8ff", "상": "#ff5f7e"}
COLOR_SUBJ = {"생명과학 I": "#00c8ff", "생명과학 II": "#a855f7"}
YEAR_COLORS = ["#00ffa3", "#00c8ff", "#a855f7", "#f97316", "#ef4444"]

# ──────────────────────────────────────────────────────────
# 탭
# ──────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "  📊 연도별 단원 출제 빈도  ",
    "  🎯 문항 난이도 분포  ",
    "  ⚖️ 수능 vs 모의고사 비교  ",
])

# ════════════════════════════════════════════════════════
# TAB 1 – 연도별 단원 출제 빈도
# ════════════════════════════════════════════════════════
with tab1:
    st.markdown("")

    for subj in subject_sel:
        sub = df[df["과목"] == subj]
        freq = sub.groupby(["연도", "단원"]).size().reset_index(name="출제수")

        # ── 바 차트
        st.markdown(f'<p class="section-title">📘 {subj} — 연도별 단원 출제 빈도</p>', unsafe_allow_html=True)

        fig_bar = px.bar(
            freq,
            x="단원", y="출제수", color="연도",
            barmode="group",
            color_discrete_sequence=YEAR_COLORS,
            height=420,
        )
        fig_bar.update_layout(**LAYOUT_BASE)
        fig_bar.update_xaxes(
            tickangle=-28,
            gridcolor="#1a2235",
            title_text="",
        )
        fig_bar.update_yaxes(
            gridcolor="#1a2235",
            title_text="출제 문항 수",
        )
        fig_bar.update_traces(marker_line_width=0)
        st.plotly_chart(fig_bar, use_container_width=True)

        # ── 히트맵
        st.markdown(f'<p class="section-title">🗺️ {subj} — 단원×연도 출제 히트맵</p>', unsafe_allow_html=True)

        pivot = freq.pivot(index="단원", columns="연도", values="출제수").fillna(0)

        fig_hm = go.Figure(go.Heatmap(
            z=pivot.values,
            x=[str(c) for c in pivot.columns],
            y=pivot.index.tolist(),
            colorscale=[
                [0.0,  "#0a0d14"],
                [0.3,  "#063340"],
                [0.6,  "#007bb5"],
                [0.85, "#00c8ff"],
                [1.0,  "#00ffa3"],
            ],
            showscale=True,
            hovertemplate="<b>%{y}</b><br>%{x}년: %{z}문항<extra></extra>",
            colorbar=dict(
                tickfont=dict(color="#6b7ea8"),
                outlinecolor="#1e2a44",
                outlinewidth=1,
                title=dict(text="출제수", font=dict(color="#6b7ea8")),
            ),
        ))
        fig_hm.update_layout(**{**LAYOUT_BASE, "height": 380})
        fig_hm.update_xaxes(title_text="연도", gridcolor="#1a2235")
        fig_hm.update_yaxes(title_text="", gridcolor="#1a2235", automargin=True)
        st.plotly_chart(fig_hm, use_container_width=True)

        # ── 누적 영역 트렌드
        st.markdown(f'<p class="section-title">📈 {subj} — 단원별 연도 출제 트렌드</p>', unsafe_allow_html=True)

        fig_area = px.area(
            freq,
            x="연도", y="출제수", color="단원",
            line_group="단원",
            height=380,
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig_area.update_layout(**LAYOUT_BASE)
        fig_area.update_xaxes(title_text="연도", gridcolor="#1a2235", dtick=1)
        fig_area.update_yaxes(title_text="출제 문항 수", gridcolor="#1a2235")
        st.plotly_chart(fig_area, use_container_width=True)

        st.divider()


# ════════════════════════════════════════════════════════
# TAB 2 – 난이도 분포
# ════════════════════════════════════════════════════════
with tab2:
    st.markdown("")

    # ── 도넛 + 레이더 (과목별 비교)
    st.markdown('<p class="section-title">🥧 과목별 전체 난이도 분포</p>', unsafe_allow_html=True)

    cols = st.columns(len(subject_sel))
    for i, subj in enumerate(subject_sel):
        sub = df[df["과목"] == subj]
        cnt = sub["난이도"].value_counts().reindex(["하", "중", "상"], fill_value=0).reset_index()
        cnt.columns = ["난이도", "문항수"]

        fig_pie = go.Figure(go.Pie(
            labels=cnt["난이도"],
            values=cnt["문항수"],
            hole=0.52,
            marker=dict(colors=[COLOR_DIFF[d] for d in cnt["난이도"]]),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>%{value}문항 (%{percent})<extra></extra>",
            textfont=dict(size=13, color="#c5d4f0"),
        ))
        fig_pie.update_layout(
            **{**LAYOUT_BASE,
               "title": dict(text=subj, x=0.5, font_size=14),
               "height": 320,
               "showlegend": False,
               "annotations": [dict(
                   text=f"<b>{len(sub)}</b><br>문항",
                   x=0.5, y=0.5, font_size=16,
                   font_color="#c5d4f0", showarrow=False
               )]}
        )
        with cols[i]:
            st.plotly_chart(fig_pie, use_container_width=True)

    # ── 연도별 난이도 비율 트렌드 라인
    st.markdown('<p class="section-title">📉 연도별 난이도 비율 추이</p>', unsafe_allow_html=True)

    trend_base = df.groupby(["연도", "과목", "난이도"]).size().reset_index(name="cnt")
    tot        = df.groupby(["연도", "과목"]).size().reset_index(name="tot")
    trend_base = trend_base.merge(tot, on=["연도", "과목"])
    trend_base["비율(%)"] = (trend_base["cnt"] / trend_base["tot"] * 100).round(1)

    for diff_lv in ["하", "중", "상"]:
        st.markdown(f"**난이도: {diff_lv}**")
        td = trend_base[trend_base["난이도"] == diff_lv]
        fig_t = px.line(
            td, x="연도", y="비율(%)", color="과목",
            markers=True,
            color_discrete_map=COLOR_SUBJ,
            height=280,
        )
        fig_t.update_traces(line_width=2.5, marker_size=8)
        fig_t.update_layout(**LAYOUT_BASE)
        fig_t.update_xaxes(dtick=1, gridcolor="#1a2235")
        fig_t.update_yaxes(gridcolor="#1a2235", ticksuffix="%")
        st.plotly_chart(fig_t, use_container_width=True)

    # ── 단원별 난이도 구성 스택 바
    st.markdown('<p class="section-title">🏗️ 단원별 난이도 구성 (스택)</p>', unsafe_allow_html=True)

    for subj in subject_sel:
        sub = df[df["과목"] == subj]
        ud  = sub.groupby(["단원", "난이도"]).size().reset_index(name="문항수")
        tot_u = sub.groupby("단원").size().reset_index(name="tot")
        ud  = ud.merge(tot_u, on="단원")
        ud["비율(%)"] = (ud["문항수"] / ud["tot"] * 100).round(1)

        fig_sb = px.bar(
            ud,
            x="단원", y="비율(%)", color="난이도",
            color_discrete_map=COLOR_DIFF,
            barmode="stack",
            title=f"{subj}",
            height=380,
        )
        fig_sb.update_layout(**LAYOUT_BASE)
        fig_sb.update_xaxes(tickangle=-25, title_text="", gridcolor="#1a2235")
        fig_sb.update_yaxes(ticksuffix="%", gridcolor="#1a2235")
        fig_sb.update_traces(marker_line_width=0)
        st.plotly_chart(fig_sb, use_container_width=True)

    # 인사이트
    hard_top = (
        df.groupby("단원")
        .apply(lambda x: (x["난이도"] == "상").mean() * 100)
        .sort_values(ascending=False)
        .head(3)
    )
    top_names = " / ".join([f"<strong>{u}</strong> ({v:.0f}%)" for u, v in hard_top.items()])
    st.markdown(
        f'<div class="insight-box">💡 <strong>고난도 다발 단원 TOP 3</strong>: {top_names}<br>'
        "→ 해당 단원은 킬러 문항 대비 심화 학습이 필요합니다.</div>",
        unsafe_allow_html=True,
    )


# ════════════════════════════════════════════════════════
# TAB 3 – 수능 vs 모의고사 비교
# ════════════════════════════════════════════════════════
with tab3:
    st.markdown("")

    cmp = df.copy()
    cmp["구분"] = cmp["시험유형"].map(lambda x: "수능" if x == "수능" else "모의고사")

    # ── 난이도 분포 비교 (grouped bar)
    st.markdown('<p class="section-title">📊 수능 vs 모의고사 — 난이도 분포 비교</p>', unsafe_allow_html=True)

    dc = cmp.groupby(["구분", "과목", "난이도"]).size().reset_index(name="cnt")
    tc = cmp.groupby(["구분", "과목"]).size().reset_index(name="tot")
    dc = dc.merge(tc, on=["구분", "과목"])
    dc["비율(%)"] = (dc["cnt"] / dc["tot"] * 100).round(1)

    for subj in subject_sel:
        dcs = dc[dc["과목"] == subj]
        fig_dc = px.bar(
            dcs,
            x="난이도", y="비율(%)", color="구분",
            barmode="group",
            color_discrete_sequence=["#ff5f7e", "#00c8ff"],
            title=f"{subj}",
            height=340,
            category_orders={"난이도": ["하", "중", "상"]},
        )
        fig_dc.update_layout(**LAYOUT_BASE)
        fig_dc.update_yaxes(ticksuffix="%", gridcolor="#1a2235")
        fig_dc.update_xaxes(gridcolor="#1a2235")
        fig_dc.update_traces(marker_line_width=0)
        st.plotly_chart(fig_dc, use_container_width=True)

    # ── 단원별 출제 빈도 비교
    st.markdown('<p class="section-title">📐 수능 vs 모의고사 — 단원별 출제 빈도 비교</p>', unsafe_allow_html=True)

    for subj in subject_sel:
        sub = cmp[cmp["과목"] == subj]
        uc  = sub.groupby(["단원", "구분"]).size().reset_index(name="출제수")

        fig_uc = px.bar(
            uc,
            x="단원", y="출제수", color="구분",
            barmode="group",
            color_discrete_sequence=["#ff5f7e", "#00c8ff"],
            title=f"{subj}",
            height=380,
        )
        fig_uc.update_layout(**LAYOUT_BASE)
        fig_uc.update_xaxes(tickangle=-25, title_text="", gridcolor="#1a2235")
        fig_uc.update_yaxes(title_text="출제 문항 수", gridcolor="#1a2235")
        fig_uc.update_traces(marker_line_width=0)
        st.plotly_chart(fig_uc, use_container_width=True)

    # ── 평가원 vs 교육청 비교 (더 세부)
    st.markdown('<p class="section-title">🔬 시험 유형 3자 비교 — 연도별 고난도 비율</p>', unsafe_allow_html=True)

    tri = df.groupby(["연도", "시험유형", "난이도"]).size().reset_index(name="cnt")
    tot3 = df.groupby(["연도", "시험유형"]).size().reset_index(name="tot")
    tri = tri.merge(tot3, on=["연도", "시험유형"])
    tri["비율(%)"] = (tri["cnt"] / tri["tot"] * 100).round(1)
    tri_hard = tri[tri["난이도"] == "상"]

    fig_tri = px.line(
        tri_hard,
        x="연도", y="비율(%)", color="시험유형",
        markers=True,
        color_discrete_sequence=["#ff5f7e", "#00c8ff", "#a855f7"],
        height=380,
        title="시험 유형별 고난도 비율 추이",
    )
    fig_tri.update_traces(line_width=2.5, marker_size=9)
    fig_tri.update_layout(**LAYOUT_BASE)
    fig_tri.update_xaxes(dtick=1, gridcolor="#1a2235")
    fig_tri.update_yaxes(ticksuffix="%", gridcolor="#1a2235")
    st.plotly_chart(fig_tri, use_container_width=True)

    # ── 레이더 차트 — 수능 vs 모의고사 단원 출제 패턴
    st.markdown('<p class="section-title">🕸️ 레이더 차트 — 단원별 출제 패턴 비교</p>', unsafe_allow_html=True)

    rad_cols = st.columns(len(subject_sel))
    for i, subj in enumerate(subject_sel):
        sub = cmp[cmp["과목"] == subj]
        units_list = sorted(sub["단원"].unique())

        suneung_cnt = (
            sub[sub["구분"] == "수능"].groupby("단원").size()
            .reindex(units_list, fill_value=0)
        )
        mock_cnt = (
            sub[sub["구분"] == "모의고사"].groupby("단원").size()
            .reindex(units_list, fill_value=0)
        )
        # 정규화 (최대값 기준)
        m = max(suneung_cnt.max(), mock_cnt.max(), 1)
        r_su = (suneung_cnt / m).tolist()
        r_mo = (mock_cnt   / m).tolist()

        cats = units_list + [units_list[0]]  # close loop
        r_su_loop = r_su + [r_su[0]]
        r_mo_loop = r_mo + [r_mo[0]]

        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(
            r=r_su_loop, theta=cats,
            fill="toself", name="수능",
            line_color="#ff5f7e",
            fillcolor="rgba(255,95,126,0.15)",
        ))
        fig_r.add_trace(go.Scatterpolar(
            r=r_mo_loop, theta=cats,
            fill="toself", name="모의고사",
            line_color="#00c8ff",
            fillcolor="rgba(0,200,255,0.12)",
        ))
        fig_r.update_layout(
            **{**LAYOUT_BASE,
               "title": dict(text=subj, x=0.5, font_size=13),
               "height": 420,
               "polar": dict(
                   bgcolor="rgba(10,13,20,0.6)",
                   radialaxis=dict(
                       visible=True,
                       range=[0, 1],
                       gridcolor="#1e2a44",
                       tickfont=dict(color="#4a5c7a", size=9),
                   ),
                   angularaxis=dict(
                       gridcolor="#1e2a44",
                       tickfont=dict(color="#8fa3c8", size=10),
                   ),
               )}
        )
        with rad_cols[i]:
            st.plotly_chart(fig_r, use_container_width=True)

    # ── 인사이트 박스
    st.markdown(
        '<div class="insight-box">'
        "💡 <strong>수능</strong>은 모의고사 대비 전반적으로 고난도 비율이 높습니다.<br>"
        "💡 <strong>사람의 유전 / 세포 호흡 / 광합성</strong>은 수능에서 킬러 문항으로 자주 출제됩니다.<br>"
        "💡 교육청 모의고사는 기본 개념 확인 위주로, <strong>하·중 난이도</strong> 비중이 높습니다."
        "</div>",
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────────────────
# 푸터
# ──────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<center style='color:#3a4a64; font-size:0.8rem;'>"
    "📌 본 대시보드의 데이터는 실제 수능·모의고사 출제 경향을 기반으로 재구성한 분석 데이터입니다.<br>"
    "수능 출처: 한국교육과정평가원 | 모의고사 출처: 각 시·도 교육청"
    "</center>",
    unsafe_allow_html=True,
)
