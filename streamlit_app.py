import streamlit as st
from supabase import create_client
import pandas as pd
from datetime import date

# 1. ページ設定
st.set_page_config(page_title="学習ログ Supabase版", page_icon="📝", layout="wide")
st.title("📝 学習ToDo & 振り返りログ")

# 2. Supabase接続設定 (Secretsの名前を [supabase] url/key に合わせる)
try:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase = create_client(url, key)
except Exception as e:
    st.error("Secretsの設定を確認してください。名前が [supabase] url, key になっていますか？")
    st.stop()

# --- データベース操作関数 ---
def load_data_from_supabase():
    # todosテーブルから全データを取得
    response = supabase.table("todos").select("*").order("created_at").execute()
    return pd.DataFrame(response.data)

# 3. メイン画面のレイアウト
tab1, tab2 = st.tabs(["今日の学習", "過去の振り返り"])

with tab1:
    st.subheader("🚀 今日の学習計画")
    
    # セッション状態での一時的なToDo管理
    if "todo_list" not in st.session_state:
        st.session_state.todo_list = []

    col1, col2 = st.columns([4, 1])
    with col1:
        new_task = st.text_input("何に挑戦しますか？", placeholder="例：統計学の分散を理解する", key="input_task")
    with col2:
        if st.button("追加") and new_task:
            st.session_state.todo_list.append({"task": new_task, "done": False})
            st.rerun()

    st.subheader("✅ 学習の進捗")
    for i, item in enumerate(st.session_state.todo_list):
        st.session_state.todo_list[i]["done"] = st.checkbox(item["task"], value=item["done"], key=f"check_{i}")

    st.divider()
    st.subheader("🧐 今日の振り返り")
    reflection = st.text_area("学習して気づいたこと、次に活かしたいことは？")

    if st.button("💾 Supabaseに保存する"):
        if st.session_state.todo_list:
            for item in st.session_state.todo_list:
                # Supabaseに1件ずつ挿入
                data = {
                    "task": item["task"],
                    "is_done": item["done"],
                    "reflection": reflection
                }
                supabase.table("todos").insert(data).execute()
            
            st.success("クラウド上のデータベースに保存しました！")
            st.session_state.todo_list = [] # クリア
        else:
            st.warning("タスクを入力してください。")

with tab2:
    st.subheader("📊 過去の学習ログ (Cloud)")
    history_df = load_data_from_supabase()

    if not history_df.empty:
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("データベースにまだ履歴はありません。")
