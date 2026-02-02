import streamlit as st
from st_supabase_connection import SupabaseConnection

st.title("🔗 Supabase 接続テスト")

try:
    # 1. Secretsから情報を読み込んで接続
    conn = st.connection("supabase", type=SupabaseConnection)
    
    # 2. 実際にデータを1件だけ取ってみるテスト
    response = conn.table("todos").select("*").limit(1).execute()
    
    # 3. 結果表示
    st.success("✅ Supabaseとの接続に成功しました！")
    st.write("現在テーブルにあるデータ:", response.data)
    st.info("データが空（[]）でも、エラーが出なければ接続設定は完璧です。")

except Exception as e:
    st.error("❌ 接続に失敗しました。")
    st.write("エラー内容:", e)
    st.warning("StreamlitのSecrets設定（urlとkey）をもう一度確認してください。")
        st.write("#### 全履歴データ")
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("まだ履歴はありません。")

