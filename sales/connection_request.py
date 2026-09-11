import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

CONNECTION_REQUEST_PROMPT = """
You are writing a LinkedIn connection request.

Create a short, natural, non-salesy message for the prospect.

Use the available prospect information to personalize the message lightly.

Rules:

- Keep it short.
- Sound like a real person, not a marketing campaign.
- Mention the company or industry naturally when useful.
- Do not pitch a service.
- Do not mention pricing.
- Do not include a feature list.
- Do not make claims about the company that are not supported by the provided information.
- The goal is simply to start a professional connection.

Prospect:
{prospect}

Primary opportunity:
{opportunity}

Return only the connection request message.
"""

import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv("D:/sales_navigator/.env")


llm = ChatGroq(model="openai/gpt-oss-120b",temperature=0.7)


def generate_connection_request(prospect, opportunity):
    prompt = CONNECTION_REQUEST_PROMPT.format(prospect=prospect,opportunity=opportunity)
    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":

    prospect = {
        "company": "AssortTech",
        "title": "CEO",
        "industry": "Software Development"
    }

    opportunity = "AI Automation"

    message = generate_connection_request(
        prospect,
        opportunity
    )

    print(message)