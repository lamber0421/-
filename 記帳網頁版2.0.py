import streamlit as st
from streamlit_local_storage import LocalStorage
import time

# 初始化網頁設定
st.set_page_config(page_title="記帳程式 3.0", layout="centered")

# 初始化瀏覽器記憶體組件
local_storage = LocalStorage()

st.title("記帳管家")
st.divider()

# 核心安全讀取區：不用 ready()，改用更穩定的 None 檢查機制
with st.spinner("正在讀取您的專屬帳本..."):
    saved_target = local_storage.getItem("target_amount")
    saved_current = local_storage.getItem("current_amount")
    
    # 如果瀏覽器還在載入中（兩者都是 None），我們就稍微等一下並重試
    # 為了防止第一次開啟網頁的人卡死，我們給他一個安全的預設通行證
    if saved_target is None and saved_current is None:
        # 讓網頁稍微緩衝 0.3 秒，給瀏覽器時間把資料拿出來
        time.sleep(0.3)
        
        # 再次嘗試讀取
        saved_target = local_storage.getItem("target_amount")
        saved_current = local_storage.getItem("current_amount")

    # 安全地轉換成數字，如果真的完全沒資料（新用戶），就當作 0
    target_amount = int(saved_target) if saved_target is not None else 0
    current_amount = int(saved_current) if saved_current is not None else 0

# 第一區：設定目標
st.subheader("設定存款目標")
new_target = st.number_input("請輸入你的存款目標", min_value=0, step=100, value=target_amount)

if st.button("確認更新目標", type="primary"):
    local_storage.setItem("target_amount", new_target)
    st.success(f"目標已設定為：{new_target} 元")
    time.sleep(0.5)  # 給瀏覽器時間寫入晶片
    st.rerun()

st.divider()

# 第二區：顯示目前狀態
if target_amount == 0:
    st.info("請先輸入存款目標以開始記帳")
else:
    remaining = target_amount - current_amount
    
    st.text(f"存款目標： {target_amount} 元")
    st.text(f"目前累計： {current_amount} 元")
    
    if current_amount >= target_amount:
        st.write("狀態： 恭喜你達成目標了")
    else:
        st.write(f"狀態： 加油！你還差 {remaining} 元就達成目標了")

    st.divider()

    # 第三區：每日收支輸入
    st.subheader("每日收支輸入")
    income = st.number_input("今日收入", min_value=0, step=10, key="inc")
    expense = st.number_input("今日支出", min_value=0, step=10, key="exp")
        
    if st.button("寫入帳目並計算", use_container_width=True):
        new_current = current_amount + (income - expense)
        local_storage.setItem("current_amount", new_current)
        st.success("帳目已成功寫入您的手機")
        time.sleep(0.5)  # 給瀏覽器時間寫入晶片
        st.rerun()