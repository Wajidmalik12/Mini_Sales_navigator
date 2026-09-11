
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

def qualify_prospect(digital_systems):

    has_opportunity = False

    if digital_systems.get("portal") is False:
        has_opportunity = True

    if digital_systems.get("online_ordering") is False:
        has_opportunity = True

    if digital_systems.get("rfq_system") is False:
        has_opportunity = True

    if digital_systems.get("ai_chatbot") is False:
        has_opportunity = True

    if has_opportunity:
        return "QUALIFY"

    return "SKIP"

QUALIFICATION_PROMPT = """
You are qualifying a company as a potential business prospect.

Analyze the company's existing digital systems and determine whether
there is a credible business opportunity.

Possible decisions:

- QUALIFY: There is a credible opportunity worth researching further.
- SKIP: The company already has mature systems that cover the relevant
  opportunity, or there is no meaningful opportunity.
- REVIEW: There is not enough evidence to make a confident decision.

Consider:

- Existing digital systems
- Missing or weak digital capabilities
- Potential operational inefficiency
- Manual processes
- Customer experience gaps
- Opportunities for automation
- Opportunities for better data usage
- Whether an existing system should be improved or integrated rather
  than replaced

Important rules:

- Do not assume that a missing system automatically means there is an opportunity.
- Do not invent facts.
- Base the decision only on the provided evidence.
- Preserve systems that already work well.
- Explain the reasoning behind the decision.

Return:

Decision: QUALIFY, SKIP, or REVIEW

Reason:
A short explanation based on the evidence.

Potential opportunity:
If QUALIFY, briefly describe what could be investigated further.
If SKIP or REVIEW, say why.

Digital systems analysis:

{digital_systems}
"""

load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-120b",temperature=0)


def analyze_prospect(digital_systems):

    prompt = QUALIFICATION_PROMPT.format(digital_systems=digital_systems)
    response = llm.invoke(prompt)
    return response.content


# if __name__ == "__main__":

#     digital_systems = {
#         "portal": False,
#         "mobile_app": False,
#         "crm": False,
#         "erp": False,
#         "online_ordering": False,
#         "rfq_system": False,
#         "scheduling": False,
#         "ai_chatbot": False,
#         "product_configurator": False,
#         "iot": False,
#         "case_management": False,
#         "field_service": False,
#         "integrations": False
#     }

#     result = analyze_prospect(digital_systems)

#     print("\nProspect Qualification:\n")
#     print(result)