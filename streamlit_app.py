import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
from st_supabase_connection import SupabaseConnection

st.set_page_config(page_title="Supabase学習ログ", page_icon="🗄️")

# 1. Supabase への接続（Secretsから自動読み込み）
conn = st.connection("supabase", type=SupabaseConnection)

st.title("🗄️ 永続化ToDoリスト (Supabase版)")
st.caption("データはクラウド上のPostgreSQLに保存されるため、消えません。")

# 2. データの取得 (READ)
# queryの結果をst.cache_resource等でキャッシュせず、常に最新を取得
def get_todos():
    return conn.table("todos").select("*").order("created_at").execute()

# 3. 新規タスクの追加 (CREATE)
with st.form("add_task_form", clear_on_submit=True):
    new_task = st.text_input("新しい学習タスクを入力")
    submitted = st.form_submit_button("データベースに保存")
    
    if submitted and new_task:
        conn.table("todos").insert({"task": new_task, "is_done": False}).execute()
        st.success("保存しました！")
        st.rerun()

# 4. タスク一覧の表示と更新 (UPDATE / DELETE)
st.subheader("現在のタスク")
response = get_todos()

for row in response.data:
    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
    
    # 完了チェックボックス
    is_done = col1.checkbox("", value=row["is_done"], key=f"check_{row['id']}")
    if is_done != row["is_done"]:
        conn.table("todos").update({"is_done": is_done}).eq("id", row["id"]).execute()
        st.rerun()
        
    col2.write(row["task"])
    
    # 削除ボタン
    if col3.button("削除", key=f"del_{row['id']}"):
        conn.table("todos").delete().eq("id", row["id"]).execute()
        st.rerun()

# 5. 学習データの可視化（簡易）
if response.data:
    st.divider()
    done_count = sum(1 for item in response.data if item["is_done"])
    total_count = len(response.data)
    st.progress(done_count / total_count if total_count > 0 else 0)
    st.write(f"進捗率: {done_count} / {total_count} 完了")
