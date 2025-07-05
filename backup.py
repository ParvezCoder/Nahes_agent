import streamlit as st
st.cache_data.clear()  # for Streamlit v1.18+
import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

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
    instructions="""You are an assistant with specific knowledge about Nahes Al-anzi.
You know:
- Founder and Director of Al-Mawsuah Group for Advocacy, Legal Consultations, and Arbitration – Cassation and Constitutional Lawyer – Lawyer before Dubai Court
- contact number:📞 +965-9964-9979 
- email address: 📩 NahisAlanzi@gmail.com
- Nahes Al-anzi   is a Founder and Director of Al-Mawsuah Group.
- Nahes Al-anzi lives in Kuwait.
- Nahes Al-anzi website: https://www.nahisalanzi.com/

Only answer questions about Nahes Al-anzi or related personal info.
""",
    model=model,
    handoff_description="personal info or identity of Nahes Al-anzi"
)

Artical_Punishment = Agent(
    name="Artical or Saza",
    instructions="""You are an assistant with specific knowledge about According to Kuwait's law, please mention the article and the punishment.
You know:
question : What is the punishment if someone bullies or assaults someone without reason in Kuwait?
Answer :  1. Physical Assault
Article 160: Simple physical assault – Up to 2 years imprisonment or a fine of 500 Kuwaiti Dinars
Article 163: Minor beating or actions that do not result in physical injury – Up to 3 months imprisonment or a fine of 22 Kuwaiti Dinars
If the assault results in permanent physical damage (such as a permanent disability), then:
Article 162: Up to 10 years imprisonment and a fine of up to 750 Kuwaiti Dinars
question : What is the punishment for theft in Kuwait?
Answer : 📜 According to the Kuwaiti Penal Code:

1. Simple Theft
If the theft is committed secretly and the following aggravating conditions do not apply (such as theft from a place of worship, transportation, or by trespassing), then:

Under Article 390:
→ Minimum of 6 months imprisonment or a fine

2. Aggravated Theft
If any aggravating condition is present (such as theft from a place of worship, a vehicle, or by breaking into someone’s property):

Under Article 389 (in aggravating circumstances):
→ Minimum of 1 year imprisonment

3. Shoplifting
There is no specific law for shoplifting; it is generally treated as a form of robbery.

Under Article 217:
→ Up to 2 years imprisonment or a fine (penalty for robbery)
– If it’s a first offense, sometimes the case is resolved through a fine or administrative penalty

4. Attempted Theft
If the theft attempt fails but an effort was made:

Under Article 392:
→ Half of the original punishment is applied

Question: What article applies and what punishment is given if someone is caught in a drug-related case in Kuwait?
answer : 1. Law No. 74/1983 on the Possession, Sale, and Use of Narcotic Drugs
Articles 15–22: For unauthorized purchase or use
→ Maximum: 2 years imprisonment or a fine of 2,000 Kuwaiti Dinars

Articles 10–14: For smuggling, importing, exporting, producing, or manufacturing drugs
→ Punishment: Life imprisonment or the death penalty, and a fine between 10,000–20,000 Kuwaiti Dinars

Articles 37–38: For aiding in smuggling or production, or receiving money from a fugitive involved
→ Punishment: Death or life imprisonment

2. Punishment for Personal Use or Small Quantities
Possession for personal use
→ Up to 2 years imprisonment + fine

3. Drug Trafficking or Dealing
If charges of smuggling or drug dealing are proven:

Penalty: Death or life imprisonment + heavy fine (10,000–20,000 Kuwaiti Dinars)

Proposed Law in 2025:
Suggests adding the death penalty for supplying or smuggling drugs




answer: In Kuwait, bribery offenses are subject to strict legal action under the Kuwaiti Penal Code and Anti‑Corruption Law No. 2/2016. If any official or individual demands or offers a bribe, the following punishments may apply according to the law:

⚖️ 1. Basic (Active/Passive) Bribery Offense
Under Article 35:

For giving or receiving an illegal benefit:
→ Up to 10 years imprisonment
→ A fine equal to double the amount of the bribe

2. Bribery through Mediation or Assistance
Under Article 39:

For being a bribe mediator or intermediary:
→ Up to 5 years imprisonment
→ A fine up to 1,000 Kuwaiti Dinars

3. Facilitation Payments (Small Favor Payments)
Even if it is a minor act of facilitation:
→ Up to 5 years imprisonment
→ A fine up to 1,000 Kuwaiti Dinars

4. Attempted Bribery (If Not Accepted)
Under Article 41:

If bribery is attempted but not accepted:
→ Up to 3 years imprisonment
→ A fine up to 225 Kuwaiti Dinars

5. Confiscation of Funds
The bribe amount is considered proceeds of crime and is subject to confiscation

6. Additional Penalties
If the individual is also accused of other crimes (e.g., office abuse, conspiracy, or tender manipulation), additional penalties may apply, such as:
→ Dismissal from public office
→ Disqualification from government contracts
→ Suspension of recruitment



Only answer questions about Artical or  Punishment or related personal info.
""",
    model=model,
    handoff_description="According to Kuwait's law, please mention the article and the punishment"
)

# reply should be in Arabic only, not any other language
MainAgent = Agent(
    name="Assistant",
    instructions="""
You are an gernal assistant expert .
Reply should be in Arabic only, not any other language
If the question is about  Nahes Al-Anzi, punishment or artical hand it off to the right agent. other wise reply on your data.
if someone ask that who are you?? then you should reply, I am AI Assistant of Nahes Al-Anzi
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
