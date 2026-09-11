import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv("D:/sales_navigator/.env")




CASE_STUDIES = [
    {
        "name": "Legl+",
        "workflows": [
            "contract generation",
            "AI review",
            "risk detection",
            "e-signature",
            "milestones",
            "reminders"
        ]
    },
    {
        "name": "WrightDraft",
        "workflows": [
            "firm-specific legal drafting",
            "approved precedents",
            "controlled revisions",
            "lawyer review"
        ]
    },
    {
        "name": "Jagnify.AI",
        "workflows": [
            "property-specific self-service",
            "guest support",
            "resident support",
            "tenant support",
            "visitor support"
        ]
    },
    {
        "name": "ParentingFlow AI",
        "workflows": [
            "structured coaching",
            "tasks",
            "summaries",
            "progress workflows"
        ]
    }
]


CASE_STUDY_MATCH_PROMPT = """
You are matching a qualified business opportunity to an existing case study.

Review the primary opportunity and compare it with the available case studies.

Rules:

- Select ONE case study only if the underlying workflow genuinely matches.
- Do not match based only on the industry.
- The business problem and workflow should be meaningfully similar.
- Do not force a match.
- If none genuinely matches, return "NO MATCH".
- Do not invent case-study capabilities.

Return:

Case study:
<case study name or NO MATCH>

Match:
<short explanation of why the workflow matches>

Evidence:
<evidence from the opportunity that supports the match>

Confidence:
HIGH, MEDIUM, or LOW

Primary opportunity:
{primary_opportunity}

Available case studies:
{case_studies}
"""

load_dotenv("D:/sales_navigator/.env")


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


def match_case_study(primary_opportunity):

    prompt = CASE_STUDY_MATCH_PROMPT.format(
        primary_opportunity=primary_opportunity,
        case_studies=CASE_STUDIES
    )

    response = llm.invoke(prompt)

# if __name__ == "__main__":

#     primary_opportunity = """
#     Primary opportunity:
#     Customer self-service portal

#     Evidence:
#     No clear customer portal was found on the company website.

#     Business problem:
#     Clients may rely on manual communication for updates and requests.

#     Potential outcome:
#     Better customer self-service and reduced manual communication.
#     """

#     result = match_case_study(primary_opportunity)

#     print(result)