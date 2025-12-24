import streamlit as st
import math

# 페이지 설정
st.set_page_config(page_title="LED 전광판 통합 설계 앱", layout="wide")

st.title("🏗️ LED 전광판 통합 설계 시스템 (v3.5)")
st.write("픽셀 피치와 물리 규격을 포함한 정밀 설계 도구입니다.")

# 사이드바: 입력값 설정
st.sidebar.header("📏 물리적 사양 입력")
pitch = st.sidebar.number_input("픽셀 피치 (P) (mm)", value=2.5, step=0.1, format="%.1f")
cab_w_mm = st.sidebar.number_input("캐비닛 가로 길이 (mm)", value=640, step=1)
cab_h_mm = st.sidebar.number_input("캐비닛 세로 길이 (mm)", value=480, step=1)

st.sidebar.header("🧩 배열 설정")
count_w = st.sidebar.number_input("가로 캐비닛 개수 (pcs)", value=10, step=1)
count_h = st.sidebar.number_input("세로 캐비닛 개수 (pcs)", value=6, step=1)

st.sidebar.header("⚡ 전기 및 컨트롤러")
power_per_cab = st.sidebar.number_input("캐비닛당 최대 소비전력 (W)", value=600, step=10)
use_backup = st.sidebar.checkbox("노바스타 백업 라인 사용", value=False)
breaker_choice = st.sidebar.selectbox("분기 차단기 용량 선택 (A)", [20, 30])

# --- 연산 로직 ---
# 1. 해상도 계산 (가로길이 / 피치)
cab_w_px = int(cab_w_mm / pitch)
cab_h_px = int(cab_h_mm / pitch)
total_res_w = cab_w_px * count_w
total_res_h = cab_h_px * count_h
total_pixels = total_res_w * total_res_h

# 2. 물리적 전체 크기 계산
total_width_m = (cab_w_mm * count_w) / 1000
total_height_m = (cab_h_mm * count_h) / 1000
total_area = total_width_m * total_height_m

# 3. 포트 및 전력 계산
port_capacity = 655360
req_main_ports = math.ceil(total_pixels / port_capacity)
total_ports = req_main_ports * 2 if use_backup else req_main_ports

total_power_w = (count_w * count_h) * power_per_cab
design_current = (total_power_w / 220) * 1.25

# 4. 배전 설계
safe_limit = breaker_choice * 220 * 0.8
required_circuits = math.ceil(total_power_w / safe_limit)

# --- 결과 화면 UI ---
st.subheader("📊 설계 요약 리포트")
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

with m_col1:
    st.metric("전체 해상도", f"{total_res_w} x {total_res_h}")
    st.caption(f"캐비닛당 해상도: {cab_w_px}x{cab_h_px}")

with m_col2:
    st.metric("전체 크기 (W x H)", f"{total_width_m:.2f}m x {total_height_m:.2f}m")
    st.caption(f"총 면적: {total_area:.2f}㎡")

with m_col3:
    st.metric("필요 포트 (Nova)", f"{total_ports} Port")
    st.caption(f"Main: {req_main_ports} / Backup: {total_ports - req_main_ports}")

with m_col4:
    st.metric("최대 전력량", f"{total_power_w/1000:.2f} kW")
    st.caption(f"설계 전류: {design_current:.1f} A")

st.markdown("---")

# 상세 설계 섹션
col_left, col_right = st.columns(2)

with col_left:
    st.success("### 🛠️ 하드웨어 구성")
    st.write(f"- **픽셀 피치:** P{pitch}")
    st.write(f"- **캐비닛 수량:** {count_w * count_h}개 ({count_w}단 {count_h}열)")
    st.write(f"- **권장 시청 거리:** {pitch * 1:.1f}m 이상")
    
    

with col_right:
    st.error("### ⚡ 전기 및 배선")
    st.write(f"- **회로 분산:** {breaker_choice}A 차단기 x **{required_circuits}회로**")
    st.write(f"- **메인 전선:** {(1.5 if design_current<=16 else 2.5 if design_current<=24 else 4.0 if design_current<=32 else 6.0 if design_current<=42 else 10.0)} SQ 권장")
    st.write(f"- **데이터 경로:** NovaStar CAT.6 SFTP 권장")

st.info(f"💡 **전문가 팁:** 현재 설정된 P{pitch} 전광판의 가로 길이는 {total_width_m}m입니다. 구조물(프레임) 제작 시 열팽창 고려하여 좌우 5mm 정도 여유를 두세요.")
