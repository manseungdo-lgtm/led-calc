import streamlit as st
import math

st.set_page_config(page_title="LED 전광판 초안전 설계기 (170%)", layout="wide")

st.title("🏗️ LED 전광판 통합 설계 시스템 (v4.0)")
st.write("총 전력량에 70% 여유를 더한(1.7배) 초안전 설계 모드입니다. (메인 3상 4선식 / 분기 단상)")

# 1. 사이드바 입력
st.sidebar.header("📏 물리적 사양")
pitch = st.sidebar.number_input("픽셀 피치 (P)", value=2.5, step=0.1)
cab_w_mm = st.sidebar.number_input("캐비닛 가로(mm)", value=640)
cab_h_mm = st.sidebar.number_input("캐비닛 세로(mm)", value=480)
count_w = st.sidebar.number_input("가로 개수(pcs)", value=10)
count_h = st.sidebar.number_input("세로 개수(pcs)", value=10)

st.sidebar.header("⚡ 전기 설계 (전력량 170% 적용)")
power_per_cab = st.sidebar.number_input("캐비닛당 최대소비전력(W)", value=600)
breaker_branch = st.sidebar.selectbox("분기 차단기 용량 (단상 220V)", [20, 30])

# --- 2. 연산 로직 (전력량 + 70% 적용) ---

# 해상도 및 규격
cab_w_px = int(cab_w_mm / pitch)
cab_h_px = int(cab_h_mm / pitch)
total_res_w = cab_w_px * count_w
total_res_h = cab_h_px * count_h
total_width_m = (cab_w_mm * count_w) / 1000
total_height_m = (cab_h_mm * count_h) / 1000

# [중요] 전력 계산 (70% 할증 반영)
raw_power_w = (count_w * count_h) * power_per_cab
design_power_w = raw_power_w * 1.7  # 전력량에 70%를 더함
total_power_kw = raw_power_w / 1000
design_power_kw = design_power_w / 1000

# [단상 분기 회로 계산]
# 할증된 전력을 기준으로 회로 수 산출
branch_limit_w = breaker_branch * 220 
required_circuits = math.ceil(design_power_w / branch_limit_w)

# [3상 4선식 메인 전류 계산]
# 할증된 전력을 3상으로 나누어 전류 산출
main_current_3phase = design_power_w / (math.sqrt(3) * 380)

# CV 전선 굵기 판정 함수 (KS 기준)
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

st.subheader("📊 안전 설계 요약 (전력 할증 170% 반영)")
m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric("전체 해상도", f"{total_res_w} x {total_res_h}")
m_col2.metric("전체 규격", f"{total_width_m:.2f}m x {total_height_m:.2f}m")
m_col3.metric("설계 전력 (1.7배)", f"{design_power_kw:.2f} kW", delta=f"실제: {total_power_kw:.2f}kW")

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.success("### 🛠️ 하드웨어 구성")
    st.write(f"**• 픽셀 피치:** P{pitch}")
    st.write(f"**• 총 캐비닛:** {count_w * count_h}개")
    st.write(f"**• 캐비닛당 해상도:** {cab_w_px} x {cab_h_px}")
    st.write(f"**• 권장 시청 거리:** {pitch * 1:.1f}m 이상")
    

with col_right:
    st.error("### ⚡ 전기 및 배선 설계 (할증 적용)")
    
    # 1. 메인 (3상 4선식)
    main_breaker_size = math.ceil(main_current_3phase/10)*10 if main_current_3phase > 20 else 20
    st.write("#### [메인 전원 - 3$\phi$4W 380V]")
    st.write(f"• **권장 메인 차단기:** **{main_breaker_size}A (4P)**")
    st.write(f"• **메인 CV 전선:** **{get_cv_size(main_breaker_size)} x 4C**") 
    st.write(f"• **설계 전류(상당):** {main_current_3phase:.1f} A")
    
    st.divider()
    
    # 2. 분기 (단상 220V)
    st.write(f"#### [분기 전원 - 1$\phi$2W 220V]")
    st.write(f"• **분기 차단기:** {breaker_branch}A (2P ELB) x **{required_circuits}회로**")
    st.write(f"• **분기 CV 전선:** {get_cv_size(breaker_branch)} x 3C")
    st.write(f"• **회로당 캐비닛:** 약 {math.floor((count_w*count_h)/required_circuits)}개 권장")



st.info(f"💡 **전문가 시뮬레이션:** 현재 설계는 실제 전력량({total_power_kw:.2f}kW)보다 70% 많은 {design_power_kw:.2f}kW를 견딜 수 있도록 전선과 차단기를 배치했습니다. 대형 관공서나 장시간 운영 현장에 적합한 최고 수준의 안전 규격입니다.")
