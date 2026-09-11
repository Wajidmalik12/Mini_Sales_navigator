from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


def prepare_website_content(documents):

    content = []

    for document in documents:

        page_content = document.page_content[:3000]

        content.append(
            f"""
Page: {document.metadata.get("page_name", "Unknown")}
URL: {document.metadata.get("source", "Unknown")}

Content:
{page_content}
"""
        )

    return "\n\n".join(content)

def identify_digital_systems(documents):
    systems = {
        "portal": False,
        "mobile_app": False,
        "crm": False,
        "erp": False,
        "online_ordering": False,
        "rfq_system": False,
        "scheduling": False,
        "ai_chatbot": False,
        "product_configurator": False,
        "iot": False,
        "case_management": False,
        "field_service": False,
        "integrations": False,
    }

    return systems

DIGITAL_SYSTEMS_PROMPT = """
You are analyzing a company's website to identify digital systems
that the company already uses.

Your job is to identify only systems that are supported by evidence
in the provided website content.

Check for:

- Customer portal
- Mobile app
- CRM
- ERP
- Online ordering
- RFQ / quote system
- Scheduling / appointment system
- AI chatbot
- Product configurator
- IoT
- Case management
- Field service management
- Integrations

For every system, return:

1. exists: true or false
2. evidence: the relevant information found on the website
3. source: the page or URL where it was found
4. confidence: high, medium, or low

Important rules:

- Do not assume a system exists just because the company mentions it.
- Do not invent information.
- If there is not enough evidence, mark exists as false.
- Preserve systems that already work.
- The goal is to understand the company's existing digital environment,
  not to recommend a replacement.

Website research:

{website_content}
"""
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b",temperature=0)
def analyze_digital_systems(documents):
    website_content = prepare_website_content(documents)

    prompt = DIGITAL_SYSTEMS_PROMPT.format(
        website_content=website_content
    )

    response = llm.invoke(prompt)

    return response.content