import streamlit as st
import math

st.set_page_config(page_title="LED 전광판 70% 안전 설계기", layout="wide")

st.title("🏗️ LED 전광판 통합 설계 시스템 (v3.9)")
st.write("부하율 70%를 적용한 초안전 설계 모드입니다. (메인 3상 4선식 / 분기 단상)")

# 1. 사이드바 입력
st.sidebar.header("📏 물리적 사양")
pitch = st.sidebar.number_input("픽셀 피치 (P)", value=2.5, step=0.1)
cab_w_mm = st.sidebar.number_input("캐비닛 가로(mm)", value=640)
cab_h_mm = st.sidebar.number_input("캐비닛 세로(mm)", value=480)
count_w = st.sidebar.number_input("가로 개수(pcs)", value=10)
count_h = st.sidebar.number_input("세로 개수(pcs)", value=10)

st.sidebar.header("⚡ 전기 설계 (부하율 70% 적용)")
power_per_cab = st.sidebar.number_input("캐비닛당 최대소비전력(W)", value=600)
breaker_branch = st.sidebar.selectbox("분기 차단기 용량 (단상 220V)", [20, 30])

# --- 2. 연산 로직 (70% 요율 적용) ---

# 해상도 및 규격
total_res_w = int(cab_w_mm / pitch) * count_w
total_res_h = int(cab_h_mm / pitch) * count_h
total_width_m = (cab_w_mm * count_w) / 1000
total_height_m = (cab_h_mm * count_h) / 1000

# 전력 계산
total_power_w = (count_w * count_h) * power_per_cab
total_power_kw = total_power_w / 1000

# [단상 분기 회로 계산 - 70% 적용]
# 220V * 차단기A * 0.7
branch_safe_limit_w = breaker_branch * 220 * 0.7 
required_circuits = math.ceil(total_power_w / branch_safe_limit_w)

# [3상 4선식 메인 전류 계산 - 70% 적용]
main_current_3phase = total_power_w / (math.sqrt(3) * 380)
# 설계 전류는 실제 전류를 0.7로 나누어 차단기 정격 결정 (I / 0.7)
design_main_current = main_current_3phase / 0.7 

# CV 전선 굵기 판정 함수 (KS C IEC 60364 기준 공사방법에 따른 허용전류 근사치)
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

st.subheader("📊 안전 설계 요약 (부하 요율 70%)")
m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric("전체 해상도", f"{total_res_w} x {total_res_h}")
m_col2.metric("전체 규격", f"{total_width_m:.2f}m x {total_height_m:.2f}m")
m_col3.metric("총 소비전력", f"{total_power_kw:.2f} kW")

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.success("### 🛠️ 하드웨어 구성")
    st.write(f"- **픽셀 피치:** P{pitch}")
    st.write(f"- **총 캐비닛:** {count_w * count_h}개")
    st.write(f"- **총 픽셀 수:** {total_res_w * total_res_h:,} px")
    st.write(f"- **권장 시청 거리:** {pitch * 1:.1f}m 이상")

with col_right:
    st.error("### ⚡ 전기 및 배선 설계 (70% Load)")
    
    # 1. 메인 (3상 4선식)
    main_breaker_size = math.ceil(design_main_current/10)*10 if design_main_current > 20 else 20
    st.write("#### [메인 전원 - 3$\phi$4W 380V]")
    st.write(f"• **권장 메인 차단기:** **{main_breaker_size}A (4P)**")
    st.write(f"• **메인 CV 전선:** **{get_cv_size(main_breaker_size * 0.75)} x 4C**") 
    st.write(f"• **상당 부하 전류:** {main_current_3phase:.1f} A")
    
    st.divider()
    
    # 2. 분기 (단상 220V)
    st.write(f"#### [분기 전원 - 1$\phi$2W 220V]")
    st.write(f"• **분기 차단기:** {breaker_branch}A (2P ELB) x **{required_circuits}회로**")
    st.write(f"• **분기 CV 전선:** {get_cv_size(breaker_branch)} x 3C")
    st.write(f"• **회로당 부하:** 약 {total_power_w / required_circuits / 220:.1f} A (최대 {breaker_branch * 0.7:.1f}A 제한)")



st.info(f"⚠️ **안전 설계 안내:** 본 설계는 전력 요율의 70%만 사용하는 보수적 설계입니다. 전력 소모가 많은 White 화면 장시간 재생 시에도 전선 가열이나 차단기 내려감 현상을 방지할 수 있습니다.")
