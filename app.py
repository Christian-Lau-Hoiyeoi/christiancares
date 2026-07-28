import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ----------------------------- 页面设置 -----------------------------
st.set_page_config(
    page_title="心靈守護者 - 早期心理健康支持平台",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------- 自定义CSS -----------------------------
st.markdown("""
<style>
    .disclaimer-box {
        background-color: #fff3cd;
        border-left: 6px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .ai-box {
        background-color: #e8f4f8;
        border-left: 6px solid #2196F3;
        padding: 1.5rem;
        border-radius: 5px;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
    .score-box {
        background-color: #f0f0f0;
        padding: 0.8rem;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------- 数据文件路径 -----------------------------
DATA_FILE = "user_assessments.csv"

# ----------------------------- 初始化会话状态 -----------------------------
if 'phq9_score' not in st.session_state:
    st.session_state.phq9_score = None
if 'gad7_score' not in st.session_state:
    st.session_state.gad7_score = None
if 'assessment_done' not in st.session_state:
    st.session_state.assessment_done = False
if 'show_institution' not in st.session_state:
    st.session_state.show_institution = False

# ----------------------------- 辅助函数 -----------------------------
def save_assessment(phq9, gad7):
    """将评估结果保存到CSV文件"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        '时间戳': [now],
        'PHQ-9分数': [phq9],
        'GAD-7分数': [gad7],
        '抑郁等级': [get_depression_level(phq9)],
        '焦虑等级': [get_anxiety_level(gad7)]
    })
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
    df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

def get_depression_level(score):
    if score <= 4: return "無明顯憂鬱"
    elif score <= 9: return "輕度憂鬱"
    elif score <= 14: return "中度憂鬱"
    elif score <= 19: return "中重度憂鬱"
    else: return "重度憂鬱"

def get_anxiety_level(score):
    if score <= 4: return "無明顯焦慮"
    elif score <= 9: return "輕度焦慮"
    elif score <= 14: return "中度焦慮"
    else: return "重度焦慮"

# ----------------------------- 页面导航 -----------------------------
st.sidebar.title("🧭 導航")
page = st.sidebar.radio(
    "請選擇頁面：",
    ["🏠 首頁", "📋 自我檢測", "🤖 AI 智慧建議", "🏥 機構專區"],
    index=0
)

# ----------------------------- 首页 -----------------------------
if page == "🏠 首頁":
    st.title("🧠 心靈守護者")
    st.subheader("為懷疑自身精神健康出現變化的您，提供科學化的早期支援")
    
    st.markdown("""
    ### 我們的核心使命
    本平台專為 **尚未確定自己是否患有精神類疾病** 的人士而設。  
    我們透過：
    - 🔬 **臨床心理學家訓練的AI模型**，提供具專業權威性的初步建議  
    - 📊 **結構化自我檢測工具**，幫助您客觀審視自身狀態  
    - 🛡️ **早期干預策略**，在情況惡化前協助您採取行動  
    
    始終以 **您的意願為第一準則**，在未獲得您同意前，絕不會強制干預。
    """)

    st.markdown("---")
    st.markdown("### ⚠️ 重要免責聲明")
    st.markdown("""
    <div class="disclaimer-box">
    <strong>本網站提供的所有內容（包括AI建議）僅供參考及教育用途，不能取代正式的臨床診斷與治療。</strong><br><br>
    • 若您正經歷嚴重情緒困擾、有自殺或傷害他人的念頭，請立即尋求專業醫療協助。<br>
    • 本平台的分析結果並非醫學診斷，請勿據此自行決定治療方針。<br>
    • 我們鼓勵您在有需要時，主動聯絡精神科醫師、臨床心理師或撥打心理輔導熱線。
    </div>
    """, unsafe_allow_html=True)

    st.info("💡 您可以先從左側選單進入「自我檢測」開始，或了解我們的「AI智慧建議」如何運作。")

# ----------------------------- 自我检测页 -----------------------------
elif page == "📋 自我檢測":
    st.title("📋 精神健康自我檢測")
    st.markdown("以下問卷結合了 **PHQ-9 (憂鬱)** 與 **GAD-7 (焦慮)** 兩個國際通用量表。請根據 **過去兩週** 的實際情況誠實作答。")
    
    st.markdown("---")
    st.subheader("第一部分：憂鬱情緒評估 (PHQ-9)")
    
    phq9_questions = [
        "1. 做事時提不起勁或沒有樂趣",
        "2. 感到心情低落、沮喪或絕望",
        "3. 入睡困難、睡不安穩或睡眠過多",
        "4. 感覺疲倦或沒有活力",
        "5. 食慾不振或吃太多",
        "6. 覺得自己很糟、失敗，或讓自己或家人失望",
        "7. 做事時無法集中精神，如看報紙或看電視",
        "8. 動作或說話速度緩慢到別人能察覺，或相反，比平常更煩躁不安、坐立不安",
        "9. 有不如死掉或用某種方式傷害自己的念頭"
    ]
    options = ["完全沒有 (0)", "幾天 (1)", "超過一半的日子 (2)", "幾乎每天 (3)"]
    score_map = {opt: i for i, opt in enumerate(options)}
    
    phq9_responses = []
    for q in phq9_questions:
        ans = st.radio(q, options, key=f"phq9_{q}", horizontal=True)
        phq9_responses.append(score_map[ans])
    
    phq9_total = sum(phq9_responses)
    
    st.markdown("---")
    st.subheader("第二部分：焦慮情緒評估 (GAD-7)")
    
    gad7_questions = [
        "1. 感覺緊張、焦慮或不安",
        "2. 無法停止或控制擔憂",
        "3. 對各種事情過度擔憂",
        "4. 難以放鬆",
        "5. 坐立不安，以至於很難安靜坐著",
        "6. 變得容易煩躁或急躁",
        "7. 感覺害怕，好像有什麼可怕的事情會發生"
    ]
    
    gad7_responses = []
    for q in gad7_questions:
        ans = st.radio(q, options, key=f"gad7_{q}", horizontal=True)
        gad7_responses.append(score_map[ans])
    
    gad7_total = sum(gad7_responses)
    
    st.markdown("---")
    if st.button("✅ 提交檢測結果並獲得AI建議", type="primary"):
        st.session_state.phq9_score = phq9_total
        st.session_state.gad7_score = gad7_total
        st.session_state.assessment_done = True
        save_assessment(phq9_total, gad7_total)
        st.success("檢測完成！請前往「AI 智慧建議」頁面查看您的個人化分析。")
        st.balloons()
    
    st.markdown("""
    <div class="disclaimer-box">
    <strong>⚠️ 隱私與免責提醒：</strong>您的回答僅用於提供即時建議，系統不會要求任何可識別個人身份的資料。
    此檢測結果不能作為診斷依據。
    </div>
    """, unsafe_allow_html=True)

# ----------------------------- AI建议页 -----------------------------
elif page == "🤖 AI 智慧建議":
    st.title("🤖 AI 臨床心理分析與建議")
    
    if not st.session_state.assessment_done:
        st.warning("您尚未完成自我檢測，請先前往「自我檢測」頁面填寫問卷。")
    else:
        phq9 = st.session_state.phq9_score
        gad7 = st.session_state.gad7_score
        dep_level = get_depression_level(phq9)
        anx_level = get_anxiety_level(gad7)
        
        st.markdown("### 📊 您的檢測分數")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='score-box'>憂鬱指數 (PHQ-9)：{phq9} 分<br>({dep_level})</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='score-box'>焦慮指數 (GAD-7)：{gad7} 分<br>({anx_level})</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🧠 AI 模型綜合建議")
        
        # 基于规则的AI建议生成
        advice = ""
        if phq9 >= 20 or gad7 >= 15:
            advice = """
            <div class="ai-box">
            <strong>🔴 高風險注意</strong><br><br>
            您的檢測分數顯示目前可能存在<strong>較嚴重</strong>的憂鬱或焦慮症狀。AI模型根據臨床心理學家訓練的知識庫，強烈建議您：<br>
            1. 在<strong>一週內</strong>尋求精神科醫師或臨床心理師的專業評估。<br>
            2. 若出現自殺念頭或無法控制的行為，請立即撥打緊急求助熱線。<br>
            3. 暫時避免獨自承受壓力，告訴您信任的家人或朋友您的狀況。<br><br>
            <em>（本建議遵循您的意願，系統不會主動通報任何機構。）</em>
            </div>
            """
        elif phq9 >= 15 or gad7 >= 10:
            advice = """
            <div class="ai-box">
            <strong>🟡 中度風險提示</strong><br><br>
            您的分數落在<strong>中度範圍</strong>，AI模型偵測到明顯的情緒困擾。建議您：<br>
            1. 安排時間與家庭醫師或心理健康專業人員討論您的狀況。<br>
            2. 嘗試結構化的自助策略，如規律運動、正念練習、保持社交連結。<br>
            3. 持續使用本平台的檢測功能追蹤變化。<br><br>
            <em>早期干預能顯著降低惡化風險，請重視這些信號。</em>
            </div>
            """
        elif phq9 >= 10 or gad7 >= 5:
            advice = """
            <div class="ai-box">
            <strong>🟢 輕度至中度風險</strong><br><br>
            檢測顯示有<strong>輕度</strong>情緒影響。AI模型建議：<br>
            1. 注意自我照顧，維持規律作息與均衡飲食。<br>
            2. 可考慮諮詢心理諮商師，學習壓力調適技巧。<br>
            3. 若症狀持續超過兩週或加重，請進一步尋求醫療協助。
            </div>
            """
        else:
            advice = """
            <div class="ai-box">
            <strong>✅ 目前無明顯症狀</strong><br><br>
            您的分數在正常範圍內。AI模型未偵測到顯著憂鬱或焦慮特徵。請繼續保持健康的生活型態，並定期關心自己的心理狀態。
            </div>
            """
        
        st.markdown(advice, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div class="disclaimer-box">
        <strong>⚠️ 再次提醒：</strong>此AI建議乃根據您的自填問卷分數產生，並非正式診斷。
        若您對結果感到擔憂，請務必諮詢合格的心理健康專業人員。
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 重新進行檢測"):
            st.session_state.assessment_done = False
            st.session_state.phq9_score = None
            st.session_state.gad7_score = None
            st.rerun()

# ----------------------------- 机构专区 -----------------------------
elif page == "🏥 機構專區":
    st.title("🏥 機構監控與個案管理")
    
    st.markdown("""
    此專區為 **學校、公共醫療單位、私立診所** 等機構提供服務。
    系統可定期收集服務對象的自我檢測數據，並整理成專業報表，協助專業人士追蹤個案心理健康變化。
    """)
    
    # 简单密码保护
    if not st.session_state.show_institution:
        with st.form("login_form"):
            st.subheader("🔐 機構人員登入")
            pwd = st.text_input("請輸入機構密碼", type="password")
            submitted = st.form_submit_button("登入")
            if submitted:
                if pwd == "psy2024":  # 演示密码
                    st.session_state.show_institution = True
                    st.success("登入成功")
                    st.rerun()
                else:
                    st.error("密碼錯誤，請重試")
    else:
        st.success("已登入機構管理模式")
        if st.button("登出"):
            st.session_state.show_institution = False
            st.rerun()
        
        st.markdown("---")
        st.subheader("📈 使用者檢測數據總覽")
        
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 下載完整數據 (CSV)",
                data=csv,
                file_name='mental_health_data.csv',
                mime='text/csv',
            )
            
            # 简易统计图
            st.subheader("📊 分數分佈")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**PHQ-9 憂鬱分數分佈**")
                st.bar_chart(df['PHQ-9分数'].value_counts().sort_index())
            with col2:
                st.markdown("**GAD-7 焦慮分數分佈**")
                st.bar_chart(df['GAD-7分数'].value_counts().sort_index())
        else:
            st.info("尚無使用者數據。當有使用者完成自我檢測後，數據將自動匯集於此。")
        
        st.markdown("---")
        st.subheader("⏰ 定期收集設定 (模擬功能)")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.selectbox("收集頻率", ["每週", "每兩週", "每月"])
        with col2:
            st.selectbox("通知方式", ["系統內提醒", "電子郵件"])
        with col3:
            st.button("💾 儲存設定", disabled=True)  # 仅演示
        st.caption("此為模擬介面，完整版可自動寄送問卷提醒並收集回覆。")
        
        st.markdown("---")
        st.markdown("""
        <div class="disclaimer-box">
        <strong>機構使用規範：</strong>所有數據均需符合資料保護法規。使用者於填寫檢測前已被告知數據可能用於專業監控，
        且機構人員有責任確保數據安全。
        </div>
        """, unsafe_allow_html=True)

# ----------------------------- 页脚 -----------------------------
st.sidebar.markdown("---")
st.sidebar.caption("© 2026心靈守護者 | 僅供參考，非醫療用途")
