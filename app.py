import streamlit as st
import math

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="LED 전광판 전문가 설계 시스템", layout="wide")

st.title("🏗️ LED 전광판 통합 설계 시스템 (v3.6)")
st.write("픽셀 피치, 물리 규격, 포트 대역폭 및 배전 설계를 통합한 전문가용 도구입니다.")

# 2. 사이드바: 모든 입력 변수 정의
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

# --- 3. 실시간 연산 로직 (입력 변수 바로 아래에 위치해야 함) ---

# 해상도 계산
cab_w_px = int(cab_w_mm / pitch)
cab_h_px = int(cab_h_mm / pitch)
total_res_w = cab_w_px * count_w
total_res_h = cab_h_px * count_h
total_pixels = total_res_w * total_res_h

# 물리적 전체 크기 및 면적 계산
total_width_m = (cab_w_mm * count_w) / 1000
total_height_m = (cab_h_mm * count_h) / 1000
total_area = total_width_m * total_height_m

# 포트 계산 (NovaStar 60Hz: 655,360px 기준)
port_capacity = 655360
req_main_ports = math.ceil(total_pixels / port_capacity)
total_ports = req_main_ports * 2 if use_backup else req_main_ports

# 전력 및 전류 계산
total_power_w = (count_w * count_h) * power_per_cab
operating_current = total_power_w / 220
design_current = operating_current * 1.25 # 안전율 25%

# 라인 분산 설계 (차단기 용량의 80% 안전 가동 기준)
safe_limit_w = breaker_choice * 220 * 0.8
required_circuits = math.ceil(total_power_w / safe_limit_w)

# 메인 전선 굵기 판정
if design_current <= 16: wire_size = "1.5 SQ"
elif design_current <= 24: wire_size = "2.5 SQ"
elif design_current <= 32: wire_size = "4.0 SQ"
elif design_current <= 42: wire_size = "6.0 SQ"
elif design_current <= 54: wire_size = "10.0 SQ"
else: wire_size = "16.0 SQ 이상 권장"

# --- 4. 결과 화면 UI 출력 ---

st.subheader("📊 설계 요약 리포트")
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

with m_col1:
    st.metric("전체 해상도", f"{total_res_w} x {total_res_h}")
    st.caption(f"캐비닛당: {cab_w_px}x{cab_h_px} px")

with m_col2:
    st.metric("전체 크기 (W x H)", f"{total_width_m:.2f}m x {total_height_m:.2f}m")
    st.caption(f"총 면적: {total_area:.2f}㎡")

with m_col3:
    st.metric("필요 포트 (Nova)", f"{total_ports} Port")
    st.caption(f"Main: {req_main_ports} / Backup: {total_ports - req_main_ports if use_backup else 0}")

with m_col4:
    st.metric("최대 전력량", f"{total_power_w/1000:.2f} kW")
    st.caption(f"설계 전류: {design_current:.1f} A")

st.markdown("---")

# 상세 설계 섹션 (2칼럼 배치)
col_left, col_right = st.columns(2)

with col_left:
    st.success("### 🛠️ 하드웨어 구성")
    st.write(f"**• 픽셀 피치:** P{pitch}")
    st.write(f"**• 캐비닛 수량:** 총 {count_w * count_h}개 ({count_w}단 {count_h}열)")
    st.write(f"**• 권장 시청 거리:** {pitch * 1:.1f}m 이상")
    st.write(f"**• 화면 비율:** {total_res_w / math.gcd(total_res_w, total_res_h):.0f}:{total_res_h / math.gcd(total_res_w, total_res_h):.0f}")
    

with col_right:
    st.error("### ⚡ 전기 및 배선 설계")
    st.write(f"**• 분기 회로:** {breaker_choice}A 차단기 x **{required_circuits}회로**")
    st.write(f"**• 메인 전선 굵기:** {wire_size} (CV/VCTF)")
    st.write(f"**• 추천 차단기:** {math.ceil(design_current/10)*10}A")
    st.write(f"**• 데이터 케이블:** CAT.6 SFTP (이중차폐)")
    

st.info(f"💡 **전문가 시공 팁:** 가로 {total_width_m}m 규격 시공 시, 함체 간 유격을 방지하기 위해 정밀 수평계(Laser Level) 사용이 필수입니다. 전원 투입 시 회로별로 2~3초 간격을 두고 순차 투입하세요.")
