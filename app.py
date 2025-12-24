import streamlit as st
import math

st.set_page_config(page_title="LED 전광판 3상 배전 설계기", layout="wide")

st.title("🏗️ LED 전광판 통합 설계 시스템 (v3.8)")
st.write("메인 3상 4선식 배전 및 단상 분기 회로 최적화 도구입니다.")

# 1. 사이드바 입력
st.sidebar.header("📏 물리적 사양")
pitch = st.sidebar.number_input("픽셀 피치 (P)", value=2.5, step=0.1)
cab_w_mm = st.sidebar.number_input("캐비닛 가로(mm)", value=640)
cab_h_mm = st.sidebar.number_input("캐비닛 세로(mm)", value=480)
count_w = st.sidebar.number_input("가로 개수(pcs)", value=10)
count_h = st.sidebar.number_input("세로 개수(pcs)", value=9)

st.sidebar.header("⚡ 전기 설계 옵션")
power_per_cab = st.sidebar.number_input("캐비닛당 최대소비전력(W)", value=600)
breaker_branch = st.sidebar.selectbox("분기 차단기 용량 (단상 220V)", [20, 30])

# --- 2. 연산 로직 ---

# 해상도 및 규격
total_res_w = int(cab_w_mm / pitch) * count_w
total_res_h = int(cab_h_mm / pitch) * count_h
total_width_m = (cab_w_mm * count_w) / 1000
total_height_m = (cab_h_mm * count_h) / 1000

# 전력 계산
total_power_w = (count_w * count_h) * power_per_cab
total_power_kw = total_power_w / 1000

# [단상 분기 회로 계산]
branch_limit_w = breaker_branch * 220 * 0.8  # 안전율 80% 적용
required_circuits = math.ceil(total_power_w / branch_limit_w)

# [3상 4선식 메인 전류 계산]
# I = P / (3 * 220) 또는 P / (1.732 * 380)
main_current_3phase = total_power_w / (math.sqrt(3) * 380)
design_main_current = main_current_3phase * 1.25 # 차단기 여유율 25%

# CV 전선 굵기 판정 (KS 규격 기준 근사치)
def get_cv_size(current):
    if current <= 19: return "1.5 SQ"
    elif current <= 27: return "2.5 SQ"
    elif current <= 36: return "4.0 SQ"
    elif current <= 46: return "6.0 SQ"
    elif current <= 63: return "10.0 SQ"
    elif current <= 85: return "16.0 SQ"
    else: return "25.0 SQ 이상"

# --- 3. 결과 UI ---

st.subheader("📊 설계 요약 리포트")
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
    st.write(f"- **권장 시청 거리:** {pitch * 1:.1f}m 이상")
    st.write(f"- **데이터 포트:** {math.ceil((total_res_w*total_res_h)/655360)} Port (NovaStar 기준)")

with col_right:
    st.error("### ⚡ 전기 및 배선 설계")
    
    # 1. 메인 (3상 4선식)
    st.write("#### [메인 전원 - 3$\phi$4W 380V]")
    st.write(f"• **메인 차단기:** **{math.ceil(design_main_current/10)*10 if design_main_current > 20 else 20}A (4P)**")
    st.write(f"• **메인 CV 전선:** **{get_cv_size(design_main_current)} x 4C**")
    st.write(f"• **설계 전류:** {main_current_3phase:.1f} A (Per Phase)")
    
    st.divider()
    
    # 2. 분기 (단상 220V)
    st.write(f"#### [분기 전원 - 1$\phi$2W 220V]")
    st.write(f"• **분기 차단기:** {breaker_branch}A (2P ELB) x **{required_circuits}회로**")
    st.write(f"• **분기 CV 전선:** {get_cv_size(breaker_branch)} x 3C (접지포함)")
    
    # 상별 배분 안내
    circuits_per_phase = math.ceil(required_circuits / 3)
    st.warning(f"💡 **부하 평형:** 각 상(R, S, T)에 **약 {circuits_per_phase}회로씩** 균등 배분하십시오.")



st.info(f"💡 **전문가 시공 팁:** \n1. **분기 전선(CV 2.5SQ/4.0SQ)**은 단상 220V 전원(L-N)을 사용합니다. \n2. 메인 차단기에서 각 상(R-N, S-N, T-N)으로 분기 회로를 나눌 때 부하가 치우치지 않게 연결해야 중성선(N) 과열을 방지할 수 있습니다.")
