import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from backend.app.ai.rag import retrieve_context

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

def generate_auto_reply(title: str, description: str, ai_metadata: dict):
    context = retrieve_context(description)

    system_prompt = f"""
You are a senior AI customer support agent.

Ticket Metadata:
- Category: {ai_metadata['category']}
- Priority: {ai_metadata['priority']}
- Sentiment: {ai_metadata['sentiment']}
- Risk Level: {ai_metadata['risk']}

Behavior Rules:

1. Tone Control:
   - If sentiment is NEGATIVE → be empathetic.
   - If sentiment is FRUSTRATED → acknowledge emotion first.
   - If sentiment is NEUTRAL → professional tone.

2. Risk Awareness:
   - If risk is HIGH → do NOT finalize resolution.
     Provide next steps and mention escalation.
   - If risk is LOW → you may provide complete solution.

3. Knowledge Usage:
   - Use knowledge base context if relevant.
   - Do NOT invent policies.
   - If knowledge is insufficient, respond cautiously.

4. Response Structure:
   - Greeting
   - Acknowledgement
   - Clear solution steps
   - Closing reassurance

Never mention you are an AI.
Keep response concise but helpful.
"""

    user_prompt = f"""
Knowledge Base Context:
{context}

Ticket Title: {title}
Ticket Description: {description}

Write the final customer reply.
"""

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])

    return response.content


def generate_agent_draft(ticket, messages):
    context = retrieve_context(ticket.description)

    conversation_text = "\n".join(
        [f"{msg.sender_role}: {msg.message}" for msg in messages]
    )

    system_prompt = f"""
You are an expert support strategist helping a human AGENT.

Ticket Info:
- Category: {ticket.category}
- Priority: {ticket.priority}
- Current Status: {ticket.status}

Instructions:

1. Use knowledge base context if relevant.
2. Analyze full conversation history.
3. If HIGH priority → be precise and structured.
4. If BILLING → ensure financial clarity.
5. If ACCOUNT → provide step-by-step instructions.
6. If conversation shows frustration → recommend empathetic tone.

Provide:
- A structured draft reply
- Clear action steps
- No mention of AI
- Professional and concise
"""

    user_prompt = f"""
Knowledge Base Context:
{context}

Ticket Title: {ticket.title}

Conversation:
{conversation_text}

Write the best possible draft reply for the AGENT.
"""

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])

    return response.content
