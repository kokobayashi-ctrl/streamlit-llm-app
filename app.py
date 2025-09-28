import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 環境変数の読み込み
load_dotenv()

def get_llm_response(user_input: str, expert_type: str) -> str:
    """
    入力テキストと専門家の種類を受け取り、LLMからの回答を返す関数
    
    Args:
        user_input (str): ユーザーからの入力テキスト
        expert_type (str): 選択された専門家の種類
    
    Returns:
        str: LLMからの回答
    """
    # 専門家の種類に応じたシステムメッセージを設定
    system_messages = {
        "医師": "あなたは経験豊富な医師です。医学的知識に基づいて、患者の健康に関する質問に親切で専門的な回答を提供してください。ただし、診断や治療の最終判断は実際の医師に相談するよう促してください。",
        "弁護士": "あなたは経験豊富な弁護士です。法律に関する質問に対して、正確で分かりやすい法的アドバイスを提供してください。ただし、具体的な法的問題については専門の弁護士に相談するよう促してください。",
        "ソフトウェアエンジニア": "あなたは経験豊富なソフトウェアエンジニアです。プログラミング、システム設計、技術的な問題に関して、実践的で詳細な技術的アドバイスを提供してください。コード例も含めて説明してください。",
        "料理専門家": "あなたは経験豊富な料理専門家・栄養士です。料理のレシピ、調理方法、栄養に関する質問に対して、実践的で美味しい料理を作るためのアドバイスを提供してください。"
    }
    
    try:
        # LLMの初期化
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
        
        # メッセージの作成
        messages = [
            SystemMessage(content=system_messages[expert_type]),
            HumanMessage(content=user_input)
        ]
        
        # LLMから回答を取得
        result = llm.invoke(messages)
        return result.content
        
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

def main():
    """
    Streamlitアプリのメイン関数
    """
    # アプリのタイトル
    st.title("🤖 AI専門家相談アプリ")
    
    # アプリの説明
    st.markdown("""
    ### 📋 アプリの概要
    このアプリは、様々な分野の専門家としてAIが回答するチャットボットです。
    質問したい分野の専門家を選択し、質問を入力してください。
    
    ### 🔧 使い方
    1. **専門家を選択**: ラジオボタンから相談したい専門家を選んでください
    2. **質問を入力**: テキストエリアに質問や相談内容を入力してください  
    3. **回答を取得**: 「回答を取得」ボタンをクリックして、AI専門家からの回答を受け取ってください
    
    ### ⚠️ 注意事項
    - このアプリの回答は参考情報として利用し、重要な判断については実際の専門家にご相談ください
    - OpenAI APIキーが必要です（.envファイルに設定済み）
    """)
    
    st.divider()
    
    # 専門家の選択（ラジオボタン）
    expert_type = st.radio(
        "相談したい専門家を選択してください:",
        ["医師", "弁護士", "ソフトウェアエンジニア", "料理専門家"],
        index=0,
        help="選択した専門家の知識に基づいて回答します"
    )
    
    # 専門家の説明を表示
    expert_descriptions = {
        "医師": "🩺 健康、病気、症状、治療法に関する医学的なアドバイスを提供します",
        "弁護士": "⚖️ 法律問題、契約、権利関係に関する法的なアドバイスを提供します",
        "ソフトウェアエンジニア": "💻 プログラミング、システム開発、技術的な問題の解決策を提供します",
        "料理専門家": "👨‍🍳 料理のレシピ、調理方法、栄養に関するアドバイスを提供します"
    }
    
    st.info(f"**選択中の専門家**: {expert_type}\n\n{expert_descriptions[expert_type]}")
    
    # 質問入力フォーム
    user_input = st.text_area(
        "質問を入力してください:",
        height=150,
        placeholder=f"{expert_type}に相談したい内容を詳しく入力してください...",
        help="具体的で詳細な質問ほど、より良い回答が得られます"
    )
    
    # 回答取得ボタン
    if st.button("🎯 回答を取得", type="primary", use_container_width=True):
        if user_input.strip():
            # ローディング表示
            with st.spinner(f"{expert_type}が回答を準備中..."):
                # LLMから回答を取得
                response = get_llm_response(user_input, expert_type)
            
            # 回答を表示
            st.divider()
            st.subheader(f"💬 {expert_type}からの回答")
            st.write(response)
            
            # 追加情報
            st.info("💡 この回答が参考になったら、さらに詳しい質問もお気軽にどうぞ！")
            
        else:
            st.warning("⚠️ 質問を入力してから「回答を取得」ボタンをクリックしてください。")
    
    # フッター情報
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
    🤖 AI専門家相談アプリ | Powered by OpenAI GPT-4o-mini & LangChain & Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # OpenAI APIキーの確認
    if not os.getenv("OPENAI_API_KEY"):
        st.error("❌ OpenAI APIキーが設定されていません。.envファイルを確認してください。")
        st.stop()
    
    main()