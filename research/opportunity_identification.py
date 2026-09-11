from langchain_groq import ChatGroq
from dotenv import load_dotenv

def create_opportunity_target(company, industry):

    return {
        "company": company,
        "industry": industry,
        "max_opportunities": 3,
        "focus": [
            "customer experience",
            "operational efficiency",
            "automation",
            "data usage",
            "digital systems"
        ]
    }

OPPORTUNITY_PROMPT = """
You are identifying potential business opportunities for a company.

Analyze the company's existing digital systems and the provided
industry research.

Identify up to 3 realistic opportunities.

Focus on:

- Customer experience
- Operational efficiency
- Automation
- Data usage
- Digital systems

For each opportunity, provide:

1. Opportunity
2. Evidence
3. Business problem
4. Potential outcome

CRITICAL EVIDENCE RULES:

- Separate FACTS from HYPOTHESES.
- A system being absent from the public website does NOT prove that
  the company does not use that system internally.
- Never state or imply that a process is manual unless the provided
  evidence explicitly says so.
- Never assume that clients use email, phone calls, spreadsheets,
  manual processes, or other workflows unless the evidence supports it.
- Industry best practices can suggest an area worth investigating,
  but they cannot be presented as evidence that this company has a
  problem.
- Do not treat a service the company sells or builds for clients as
  proof that the company uses that system internally.
- Do not invent company-specific problems.

For every opportunity, clearly distinguish:

Company evidence:
What is actually known about the company.

Industry signal:
What the industry research suggests is commonly used or valuable.

Hypothesis to investigate:
What MIGHT be a business problem, but has not yet been confirmed.

Important rules:

- Only identify opportunities worth investigating.
- Do not claim an unverified problem as a fact.
- Do not recommend replacing systems that already work well.
- Prefer improving, integrating, or automating existing processes.
- If evidence is weak, say that discovery is required.
- Do not force 3 opportunities if fewer are justified.
- Do not provide numerical ROI, percentages, savings, timelines,
  conversion increases, or performance improvements unless they are
  explicitly supported by the provided evidence.
- Do not recommend specific vendors unless the provided evidence
  specifically supports them.
- If there is no opportunity then say no opportunity if there 1 then give 1 if there are 2 then give 2 if there are then 3, and 3 is max limit

Company:
{company}

Industry:
{industry}

Existing digital systems:
{digital_systems}

Industry research:
{industry_research}
"""

load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-120b",temperature=0)


def identify_opportunities(
    company,
    industry,
    digital_systems,
    industry_research
):

    prompt = OPPORTUNITY_PROMPT.format(
        company=company,
        industry=industry,
        digital_systems=digital_systems,
        industry_research=industry_research
    )

    response = llm.invoke(prompt)

    return response.content

if __name__ == "__main__":

    result = identify_opportunities(
        company="AssortTech",
        industry="Software Development",
        digital_systems="""
        The company provides web development, mobile development,
        AI services, and software development.
        No clear customer portal or AI chatbot was found.
        """,
        industry_research="""
        Software companies are increasingly using AI automation,
        customer self-service portals, and integrated workflows.
        """
    )

    print(result)
