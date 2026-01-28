import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
import pandas as pd
from datetime import date

# 1. ページ設定
st.set_page_config(page_title="学習ログ", page_icon="📝")
st.title("📝 学習ToDo & 振り返りログ")
st.caption("自己調整学習：計画(Forethought)と振り返り(Reflection)を習慣化しましょう")

# 2. セッション状態の初期化（ブラウザをリロードするまでデータを保持）
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []

# 3. 計画フェーズ：ToDoの追加
with st.container():
    st.subheader("🚀 今日の学習計画")
    col1, col2 = st.columns([4, 1])
    with col1:
        new_task = st.text_input("何に挑戦しますか？", placeholder="例：統計学の分散を理解する", key="input_task")
    with col2:
        if st.button("追加") and new_task:
            st.session_state.todo_list.append({"task": new_task, "done": False})
            st.rerun()

# 4. 遂行フェーズ：チェックリスト
st.subheader("✅ 学習の進捗")
for i, item in enumerate(st.session_state.todo_list):
    # チェックボックスの状態をセッションに反映
    st.session_state.todo_list[i]["done"] = st.checkbox(item["task"], value=item["done"], key=f"check_{i}")

# 5. 自己省察フェーズ：振り返り
st.divider()
st.subheader("🧐 今日の振り返り")
reflection = st.text_area("学習して気づいたこと、次に活かしたいことは？", placeholder="例：概念マップを書いたら整理できた！")

# 6. データ書き出し（CSV形式）
if st.session_state.todo_list:
    # データを整形
    df = pd.DataFrame(st.session_state.todo_list)
    df["reflection"] = reflection
    df["date"] = date.today()

    # CSVダウンロードボタン
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📊 今日のログを保存（CSV）",
        data=csv,
        file_name=f"study_log_{date.today()}.csv",
        mime="text/csv",
    )

# おまけ：リセットボタン
if st.button("リストをクリア"):
    st.session_state.todo_list = []
    st.rerun()
   
