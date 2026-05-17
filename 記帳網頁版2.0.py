import streamlit as st
from streamlit_local_storage import LocalStorage
import time

# --- 🚀 初始化網頁設定 ---
st.set_page_config(page_title="記帳程式 3.0", layout="centered")

# 初始化 LocalStorage 組件（用來和瀏覽器溝通）
local_storage = LocalStorage()

st.title("記帳管家 ")
st.divider()

# --- ⚙️ 核心：從各自的瀏覽器讀取資料 ---
# 由於瀏覽器載入需要時間，我們用 st.spinner 確保資料安全讀取
with st.spinner("正在讀取您的專屬帳本..."):
    # 從各自的手機瀏覽器撈出資料（如果撈不到，預設值給 0）
    saved_target = local_storage.getItem("target_amount")
    saved_current = local_storage.getItem("current_amount")
    
    # 處理初次讀取時的空值(None)狀況，將其轉為整數
    target_amount = int(saved_target) if saved_target is not None else 0
    current_amount = int(saved_current) if saved_current is not None else 0

# --- 💻 網頁介面設計 ---

# 第一區：設定目標
st.subheader("設定存款目標")
new_target = st.number_input("請輸入你的存款目標 (元):", min_value=0, step=100, value=target_amount)

if st.button("確認更新目標", type="primary"):
    # 關鍵：將新目標寫入該使用者的瀏覽器，並給伺服器一點時間寫入
    local_storage.setItem("target_amount", new_target)
    st.success(f"目標已設定為：{new_target} 元")
    time.sleep(0.5) # 暫停半秒確保瀏覽器寫入成功
    st.rerun()

st.divider()

# 第二區：顯示目前狀態
if target_amount == 0:
    st.info("請先輸入存款目標以開始記帳。")
else:
    remaining = target_amount - current_amount
    
    # 乾淨的數據看板
    st.text(f"存款目標： {target_amount} 元")
    st.text(f"目前累計： {current_amount} 元")
    
    if current_amount >= target_amount:
        st.write("狀態： 恭喜你達成目標了！")
    else:
        st.write(f"狀態： 加油！你還差 {remaining} 元就達成目標了！")

    st.divider()

    # 第三區：每日收支輸入
    st.subheader("每日收支輸入")
    income = st.number_input("今日收入 (元):", min_value=0, step=10, key="inc")
    expense = st.number_input("今日支出 (元):", min_value=0, step=10, key="exp")
        
    if st.button("寫入帳目並計算", use_container_width=True):
        new_current = current_amount + (income - expense)
        # 關鍵：將計算後的累計金額寫入該使用者的瀏覽器
        local_storage.setItem("current_amount", new_current)
        st.success("帳目已成功紀錄")
        time.sleep(0.5) # 暫停半秒確保瀏覽器寫入成功
        st.rerun()