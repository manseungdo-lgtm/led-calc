import streamlit as st
import math

st.set_page_config(page_title="LED 설계기", layout="wide")
st.title("🏗️ LED 전광판 통합 설계기")

# 1. 사이드바에서 입력을 먼저 받습니다.
st.sidebar.header("📋 사양 입력")
pitch = st.sidebar.number_input("픽셀 피치(mm)", value=2.5, step=0.1)
cab_w_mm = st.sidebar.number_input("캐비닛 가로(mm)", value=640)
cab_h_mm = st.sidebar.number_input("캐비닛 세로(mm)", value=480)
count_w = st.sidebar.number_input("가로 캐비닛 개수(pcs)", value=10)
count_h = st.sidebar.number_input("세로 캐비닛 개수(pcs)", value=6)
power_per_cab = st.sidebar.number_input("캐비닛당 소비전력(W)", value=600)

# 2. 입력을 받은 직후에 모든 계산을 수행합니다. (중요!)
cab_w_px = int(cab_w_mm / pitch)
cab_h_px = int(cab_h_mm / pitch)
total_res_w = cab_w_px * count_w
total_res_h = cab_h_px * count_h
total_power_w = (count_w * count_h) * power_per_cab

# 3. 계산된 결과를 화면에 뿌려줍니다.
col1, col2 = st.columns(2)
with col1:
    st.metric("전체 해상도", f"{total_res_w} x {total_res_h}")
with col2:
    st.metric("총 소비전력", f"{total_power_w/1000:.2f} kW")

st.write(f"현재 설정: P{pitch} / {count_w}x{count_h} 배열")
