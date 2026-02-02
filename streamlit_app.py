import streamlit as st
from supabase import client
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url,key)


import streamlit as st
import pandas as pd
from datetime import date
import os

# --- 設定 ---
LOG_FILE = "study_history.csv"

# 1. ページ設定
st.set_page_config(page_title="学習ログ Pro", page_icon="📝", layout="wide")
st.title("📝 学習ToDo & 振り返りログ")

# --- データの読み込み・保存関数 ---
def load_data():
    if os.path.exists(LOG_FILE):
        return pd.read_csv(LOG_FILE)
    else:
        return pd.DataFrame(columns=["date", "task", "done", "reflection"])

def save_data(df):
    df.to_csv(LOG_FILE, index=False, encoding='utf-8-sig')

# データの初期化
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []

# --- メイン画面のレイアウト（タブ分け） ---
tab1, tab2 = st.tabs(["今日の学習", "過去の振り返り"])

with tab1:
    # 3. 計画フェーズ
    st.subheader("🚀 今日の学習計画")
    col1, col2 = st.columns([4, 1])
    with col1:
        new_task = st.text_input("何に挑戦しますか？", placeholder="例：統計学の分散を理解する", key="input_task")
    with col2:
        if st.button("追加") and new_task:
            st.session_state.todo_list.append({"task": new_task, "done": False})
            st.rerun()

    # 4. 遂行フェーズ
    st.subheader("✅ 学習の進捗")
    for i, item in enumerate(st.session_state.todo_list):
        st.session_state.todo_list[i]["done"] = st.checkbox(item["task"], value=item["done"], key=f"check_{i}")

    # 5. 自己省察フェーズ
    st.divider()
    st.subheader("🧐 今日の振り返り")
    reflection = st.text_area("学習して気づいたこと、次に活かしたいことは？", placeholder="例：概念マップを書いたら整理できた！")

    if st.button("💾 今日の内容を履歴に保存する"):
        if st.session_state.todo_list:
            # 新しいデータの作成
            new_data = pd.DataFrame(st.session_state.todo_list)
            new_data["date"] = str(date.today())
            new_data["reflection"] = reflection
            
            # 既存の履歴に結合して保存
            history_df = load_data()
            updated_df = pd.concat([history_df, new_data], ignore_index=True)
            save_data(updated_df)
            
            st.success("履歴に保存しました！「過去の振り返り」タブから確認できます。")
            # 保存後にリストをクリア（任意）
            st.session_state.todo_list = []
        else:
            st.warning("タスクがありません。")

with tab2:
    st.subheader("📊 過去の学習ログ")
    history_df = load_data()

    if not history_df.empty:
        # 日付でフィルタリングできるようにする
        dates = history_df["date"].unique()
        selected_date = st.selectbox("日付を選択して振り返る", reversed(dates))
        
        filtered_df = history_df[history_df["date"] == selected_date]
        
        # 表示の整理
        st.write(f"### {selected_date} の記録")
        
        col_ref, col_tasks = st.columns([1, 1])
        with col_ref:
            st.info(f"**振り返り:**\n\n {filtered_df.iloc[0]['reflection']}")
        with col_tasks:
            st.write("**実施したタスク:**")
            for _, row in filtered_df.iterrows():
                status = "✅" if row["done"] else "⬜"
                st.write(f"{status} {row['task']}")
        
        st.divider()
        st.write("#### 全履歴データ")
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("まだ履歴はありません。")

