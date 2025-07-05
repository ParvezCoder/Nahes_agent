import streamlit as st
st.cache_data.clear()  # for Streamlit v1.18+
import os
import asyncio
import streamlit as st
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner

# Load environment variables
gemini_api_key = "AIzaSyDKwBsMJw96xlz4xNoHe_yj0KR1zHeYTV8"

# Gemini API setup
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.0-flash"
)

# Agents

Nahes = Agent(
    name="Nahes Al-anzi",
    instructions="""You are an assistant with specific knowledge about Nahes Al-anzi. And always reply in Arabic language
You know:
المؤسس والمدير لمجموعة الموسوعة للمحاماة والاستشارات القانونية والتحكيم – محامٍ في التمييز والدستورية – محامٍ أمام محاكم دبي
رقم الاتصال: 📞 +965-9964-9979
عنوان البريد الإلكتروني: 📩 NahisAlanzi@gmail.com
ناهس العنزي هو المؤسس والمدير لمجموعة الموسوعة.
ناهس العنزي يقيم في الكويت.
موقع ناهس العنزي الإلكتروني: https://www.nahisalanzi.com/
questions answer about Nahes Al-anzi or related personal info.
""",
    model=model,
    handoff_description="personal info or identity of Nahes Al-anzi"
)

Artical_Punishment = Agent(
    name="Artical or Saza",
    instructions="""You are an assistant with specific knowledge about According to Kuwait's law, please mention the article and the punishment.
You know:
question : What is the punishment if someone bullies or assaults someone without reason in Kuwait?
❓ السؤال: ما هي العقوبة إذا قام شخص بالتنمر أو الاعتداء على شخص دون سبب في الكويت؟
الإجابة:
الاعتداء الجسدي
المادة 160: اعتداء جسدي بسيط – السجن لمدة تصل إلى سنتين أو غرامة قدرها 500 دينار كويتي
المادة 163: الضرب الطفيف أو الأفعال التي لا تؤدي إلى إصابة جسدية – السجن لمدة تصل إلى 3 أشهر أو غرامة قدرها 22 دينار كويتي
إذا نتج عن الاعتداء ضرر جسدي دائم (مثل الإعاقة الدائمة):
المادة 162: السجن لمدة تصل إلى 10 سنوات وغرامة تصل إلى 750 دينار كويتي

question : What is the punishment for theft in Kuwait?
❓ السؤال: ما هي عقوبة السرقة في الكويت؟
الإجابة: 📜 وفقًا لقانون الجزاء الكويتي:
السرقة البسيطة
إذا تمت السرقة بشكل سري ولم تنطبق الشروط المشددة التالية (مثل السرقة من مكان عبادة، أو من وسيلة نقل، أو عن طريق التسلل)، فإن:
وفقًا للمادة 390:
→ الحد الأدنى: السجن لمدة 6 أشهر أو غرامة
السرقة المشددة
إذا كانت هناك أي ظروف مشددة (مثل السرقة من مكان عبادة، أو من مركبة، أو عن طريق اقتحام ممتلكات الغير):
وفقًا للمادة 389 (في ظروف مشددة):
→ الحد الأدنى: السجن لمدة سنة واحدة
سرقة المتاجر (Shoplifting)
لا يوجد قانون محدد لسرقة المتاجر؛ حيث تُعامل عادةً كنوع من السرقة:
وفقًا للمادة 217:
→ السجن لمدة تصل إلى سنتين أو غرامة (كعقوبة على السرقة)
– إذا كانت المرة الأولى، في بعض الأحيان تُحل القضية بغرامة أو إجراء إداري
محاولة السرقة
إذا فشلت محاولة السرقة ولكن تم بذل جهد واضح:
وفقًا للمادة 392:
→ يتم تطبيق نصف العقوبة الأصلية


Question: What article applies and what punishment is given if someone is caught in a drug-related case in Kuwait?
 السؤال: ما هو القانون أو المادة التي تنطبق، وما هي العقوبة إذا تم القبض على شخص في قضية تتعلق بالمخدرات في الكويت؟
الإجابة:
القانون رقم 74 لسنة 1983 بشأن حيازة وبيع واستخدام المواد المخدرة
المواد 15–22: في حالة الشراء أو الاستخدام غير المصرح به
→ العقوبة القصوى: السجن لمدة تصل إلى سنتين أو غرامة قدرها 2000 دينار كويتي
المواد 10–14: في حالة التهريب أو الاستيراد أو التصدير أو الإنتاج أو التصنيع
→ العقوبة: السجن المؤبد أو الإعدام، وغرامة تتراوح بين 10,000 إلى 20,000 دينار كويتي
المواد 37–38: في حال تقديم المساعدة في التهريب أو الإنتاج، أو استلام أموال من متهم هارب
→ العقوبة: الإعدام أو السجن المؤبد
العقوبة على الحيازة للاستخدام الشخصي أو الكميات الصغيرة
→ السجن لمدة تصل إلى سنتين + غرامة
الاتجار أو تهريب المخدرات
إذا ثبتت تهمة التهريب أو الاتجار بالمخدرات:
→ العقوبة: الإعدام أو السجن المؤبد + غرامة كبيرة (من 10,000 إلى 20,000 دينار كويتي)
📌 مشروع قانون مقترح لعام 2025:
يقترح إضافة عقوبة الإعدام على توفير أو تهريب المواد المخدرة

question : What is the punishment for bribery in Kuwait, and which articles of law apply?
❓ السؤال: ما هي عقوبة الرشوة في الكويت، وما هي المواد القانونية التي تنطبق؟
الإجابة:

في الكويت، تُخضع جرائم الرشوة لإجراءات قانونية صارمة بموجب قانون الجزاء الكويتي وقانون مكافحة الفساد رقم 2 لسنة 2016.
إذا طلب أو قدم أي موظف أو فرد رشوة، فقد تنطبق عليه العقوبات التالية وفقًا للقانون:

⚖️ 1. جريمة الرشوة الأساسية (نشطة أو سلبية)
وفقًا للمادة 35:

تقديم أو تلقي منفعة غير قانونية:
→ السجن لمدة تصل إلى 10 سنوات
→ غرامة تعادل ضعف مبلغ الرشوة

2. الرشوة عن طريق الوساطة أو المساعدة
وفقًا للمادة 39:

إذا كان الشخص وسيطًا أو طرفًا مساعدًا في الرشوة:
→ السجن لمدة تصل إلى 5 سنوات
→ غرامة تصل إلى 1000 دينار كويتي
3. مدفوعات التسهيل (الرشاوى الصغيرة)
حتى وإن كانت تسهيلاً بسيطًا:
→ السجن لمدة تصل إلى 5 سنوات
→ غرامة تصل إلى 1000 دينار كويتي
4. محاولة الرشوة (إذا لم تُقبل)
وفقًا للمادة 41:
في حال محاولة تقديم رشوة ولم تُقبل:
→ السجن لمدة تصل إلى 3 سنوات
→ غرامة تصل إلى 225 دينار كويتي
5. مصادرة الأموال
يُعتبر مبلغ الرشوة من عوائد الجريمة ويتم مصادرته بموجب القانون
6. عقوبات إضافية
إذا تم توجيه تهم إضافية مثل إساءة استخدام المنصب، أو التآمر، أو التلاعب في المناقصات، فقد تشمل العقوبات الإضافية:
→ العزل من الوظيفة العامة
→ الحرمان من التعاقدات الحكومية
→ تعليق التوظيف في المستقبل

 You are a Law expert. Answer punishment, saza, Law-related queries clearly.
""",
    model=model,
    handoff_description="According to Kuwait's law, please mention the article and the punishment"
)

# reply should be in Arabic only, not any other language
MainAgent = Agent(
    name="Assistant",
    instructions="""
You are an gernal assistant expert .
If the question is about  Nahes Al-Anzi, punishment , saza and artical hand it off to the right agent.
You are an gernal assistant expert .
""",
    model=model,
    handoffs=[ Nahes, Artical_Punishment]
)


async def get_agent_reply(query):
    result = await Runner.run(MainAgent, query)
    return result.final_output, result.last_agent.name

# Streamlit config
st.set_page_config(page_title="Multi-Agent Chat", page_icon="🤖", layout="centered")
import base64



# 💅 Custom styling for dark background and red label/button

st.markdown("""
    <style>
    body, .stApp {
        background-color: #0a0f1f;
        color: #e6e6e6;
        font-size: 18px;
    }
    h1 {
        color: #ff4b4b;
        font-weight: bold;
    }
    label[data-testid="stTextInputLabel"] {
        color: #ff4b4b !important;
        font-weight: bold;
        font-size: 18px;
    }
.stButton > button:hover {
    background-color: #e63946;
    color: white !important;
}

    .chat-box {
        background-color: #1a1e2b;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        font-size: 18px;
    }
    </style>
""", 
unsafe_allow_html=True)

# App Title
st.markdown("<h1 style = 'margin-top:-40px'> ⚖️ محامٍ بالذكاء الاصطناعي لناهس العنزي </h1>", unsafe_allow_html=True)


# Chat session state
# if "chat" not in st.session_state:
#     st.session_state.chat = []

# Input

with st.form("chat_form", clear_on_submit=True):
    st.markdown("<label style='color: red; font-size: 20px; '>💬 استفسارك:</label>", unsafe_allow_html=True)
    user_input = st.text_input(label="",  placeholder="اكتب سؤالك هنا...")
    submitted = st.form_submit_button("🚀 اكتب سؤالك هنا")
 

if submitted and user_input:
    with st.spinner("Thinking..."):
        final_output, last_agent_name = asyncio.run(get_agent_reply(user_input))
        st.markdown(f"<div class='chat-box' style='background:#293042'><b>🧑 You</b>: {user_input}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-box' style='background:#162032'><b>🤖 الرد</b>: {final_output}</div>", unsafe_allow_html=True)

        
        
        # st.session_state.chat.insert(0, ("🤖 Response", f"""{final_output } """))
        # st.session_state.chat.insert(0, ("🧑 You", user_input))

# Chat history
# for role, msg in st.session_state.chat:
#     color = "#293042" if role == "🧑 You" else "#162032"
#     st.markdown(f"<div class='chat-box' style='background:{color}'><b>{role}</b>: {msg}</div>", unsafe_allow_html=True)
