import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

PRIMARY_OPPORTUNITY_PROMPT = """
You are selecting the single best opportunity for outreach.

Review the identified opportunities and select exactly ONE primary
opportunity.

Selection criteria:

- Strongest evidence
- Clear business relevance
- Realistic opportunity
- Good fit for outreach
- Potential to provide meaningful business value

Important rules:

- Select only ONE opportunity.
- Do not invent facts.
- Do not add new opportunities.
- Do not use unsupported percentages or ROI claims.
- Prefer an opportunity supported by both company evidence and
  industry research.

Return:

Primary opportunity:
<name>

Why this opportunity:
<short explanation>

Evidence:
<supporting evidence>

Potential outcome:
<realistic business outcome>

Opportunities:

{opportunities}
"""



load_dotenv("D:/sales_navigator/.env")


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


def select_primary_opportunity(opportunities):

    prompt = PRIMARY_OPPORTUNITY_PROMPT.format(
        opportunities=opportunities
    )

    response = llm.invoke(prompt)

    return response.content

# if __name__ == "__main__":

#     opportunities = """
#     1. Customer self-service portal
#        Evidence: No clear customer portal was found.
#        Business problem: Clients may rely on manual communication
#        for updates and requests.

#     2. AI chatbot
#        Evidence: No clear AI chatbot was found.
#        Business problem: Routine questions may require staff attention.

#     3. AI workflow automation
#        Evidence: The company provides AI services.
#        Business problem: Some internal development workflows may
#        potentially be automated.
#     """

#     result = select_primary_opportunity(opportunities)

#     print(result)