# 📝 学習ToDo & 振り返りログ

StreamlitとSupabaseを利用した、自己調整学習（Self-Regulated Learning）を支援するためのWebアプリケーションです。学習計画の立案、進捗の可視化、そして一日の終わりの振り返りを一気通貫で行うことができます。

## URL

このURLで試すことができます：
[https://your-app-link.streamlit.app/](https://your-app-link.streamlit.app/)

## 🚀 主な機能

* **今日の学習計画**: その日に挑戦したい内容（例：「統計学の分散を理解する」など）を入力し、ToDoリストを即座に作成します。
* **学習の進捗管理**: チェックボックス形式で完了済みタスクを可視化し、遂行コントロールを助けます。
* **今日の振り返り**: 学習後の気づきや次に活かしたいことを記録し、メタ認知能力を向上させます。
* **Cloud DB連携**: 入力データはSupabaseへ保存されるため、デバイスを問わず過去のログを確認可能です。

## 🛠 セットアップ方法

### 1. 依存ライブラリのインストール
Python環境がインストールされていることを確認し、必要なライブラリをインストールしてください。

```bash
pip install streamlit supabase pandas
[supabase]
url = "https://yohahnnpczefohrdzxpt.supabase.co"
key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlvaGFobm5wY3plZm9ocmR6eHB0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk3MzEyNzcsImV4cCI6MjA4NTMwNzI3N30.YsyklfsvqB5jlci4vYLz46-yVZQVq9hZHMuUnCzvQbk"

streamlit run streamlit_app.py

データの仕組み
このアプリは Supabase (PostgreSQL) を使用して学習履歴を管理しています。

todosテーブル:

task: 学習タスクの内容（text）

is_done: 完了状態（bool）

reflection: 振り返りの内容（text）

created_at: 記録日時（timestamp）

💻 使用技術
Frontend/UI: Streamlit

Database: Supabase (PostgreSQL)

Data Handling: Pandas

💡 今後のロードマップ（カスタマイズ例）
学習カテゴリのタグ付け: 統計学、プログラミング、アグリビジネス等のカテゴリ別分類。

進捗グラフの表示: 過去のデータに基づいたタスク完了率の可視化。

リマインド機能: 未完了タスクがある場合の通知機能。
---
