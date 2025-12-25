import streamlit as st
import math

st.set_page_config(page_title="LED 전광판 가변 부하 설계기", layout="wide")

st.title("🏗️ LED 전광판 통합 설계 시스템 (v4.1)")
st.write("현장 조건에 맞춰 전력 여유율을 자유롭게 설정할 수 있는 전문가용 버전입니다.")

# 1. 사이드바 입력
st.sidebar.header("📏 물리적 사양")
pitch = st.sidebar.number_input("픽셀 피치 (P)", value=2.5, step=0.1)
cab_w_mm = st.sidebar.number_input("캐비닛 가로(mm)", value=640)
cab_h_mm = st.sidebar.number_input("캐비닛 세로(mm)", value=480)
count_w = st.sidebar.number_input("가로 개수(pcs)", value=10)
count_h = st.sidebar.number_input("세로 개수(pcs)", value=10)

st.sidebar.header("⚡ 전기 및 여유율 설정")
power_per_cab = st.sidebar.number_input("캐비닛당 최대소비전력(W)", value=600)

# 전력 여유율 선택
margin_percent = st.sidebar.slider("전력 여유율 추가 (%)", min_value=0, max_value=100, value=70, step=5)
st.sidebar.info(f"💡 현재 실제 전력의 {100 + margin_percent}%로 설계 중")

breaker_branch = st.sidebar.selectbox("분기 차단기 용량 (단상 220V)", [20, 30])

# --- 2. 연산 로직 ---

# [추가] 캐비닛 1개당 해상도 계산
cab_res_w = int(cab_w_mm / pitch)
cab_res_h = int(cab_h_mm / pitch)

# 전체 규격 계산
total_res_w = cab_res_w * count_w
total_res_h = cab_res_h * count_h
total_width_m = (cab_w_mm * count_w) / 1000
total_height_m = (cab_h_mm * count_h) / 1000

# 전력 계산 (가변 여유율 반영)
raw_power_w = (count_w * count_h) * power_per_cab
margin_factor = 1 + (margin_percent / 100)
design_power_w = raw_power_w * margin_factor

total_power_kw = raw_power_w / 1000
design_power_kw = design_power_w / 1000

# [단상 분기 회로 계산]
branch_limit_w = breaker_branch * 220 
required_circuits = math.ceil(design_power_w / branch_limit_w)

# [3상 4선식 메인 전류 계산]
main_current_3phase = design_power_w / (math.sqrt(3) * 380)

# CV 전선 굵기 판정 함수
def get_cv_size(current):
    if current <= 19: return "1.5 SQ"
    elif current <= 27: return "2.5 SQ"
    elif current <= 36: return "4.0 SQ"
    elif current <= 46: return "6.0 SQ"
    elif current <= 63: return "10.0 SQ"
    elif current <= 85: return "16.0 SQ"
    elif current <= 112: return "25.0 SQ"
    else: return "35.0 SQ 이상"

# --- 3. 결과 UI ---

st.subheader(f"📊 설계 요약 (전력 할증 {margin_percent}% 적용)")
m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric("전체 해상도", f"{total_res_w} x {total_res_h}")
m_col2.metric("전체 규격", f"{total_width_m:.2f}m x {total_height_m:.2f}m")
m_col3.metric("설계 전력량", f"{design_power_kw:.2f} kW", delta=f"실제 대비 +{margin_percent}%")

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.success("### 🛠️ 하드웨어 구성")
    st.write(f"- **픽셀 피치:** P{pitch}")
    # 캐비닛 개당 해상도 표시 추가
    st.write(f"- **캐비닛 해상도:** {cab_res_w} x {cab_res_h} (px)") 
    st.write(f"- **총 캐비닛:** {count_w * count_h}개 ({count_w}x{count_h})")
    st.write(f"- **총 면적:** {total_width_m * total_height_m:.2f}㎡")
    st.write(f"- **권장 시청 거리:** {pitch * 1:.1f}m 이상")

with col_right:
    st.error("### ⚡ 전기 및 배선 설계 (가변 부하)")
    
    # 메인
    main_breaker_size = math.ceil(main_current_3phase/10)*10 if main_current_3phase > 20 else 20
    st.write("#### [메인 - 3$\phi$4W 380V]")
    st.write(f"• **메인 차단기:** **{main_breaker_size}A (4P)**")
    st.write(f"• **메인 CV 전선:** **{get_cv_size(main_breaker_size)} x 4C**")
    
    st.divider()
    
    # 분기
    st.write("#### [분기 - 1$\phi$2W 220V]")
    st.write(f"• **분기 차단기:** {breaker_branch}A x **{required_circuits}회로**")
    st.write(f"• **분기 CV 전선:** {get_cv_size(breaker_branch)} x 3C")
    st.write(f"• **상별 부하:** 약 {math.ceil(required_circuits/3)}회로씩 분배")

st.info(f"💡 **설계 가이드:** \n- **일반 현장:** 여유율 20~30% 추천 \n- **관공서/장시간 운영:** 여유율 50~70% 추천 \n- **초안전 설계:** 여유율 70% 이상 추천")
