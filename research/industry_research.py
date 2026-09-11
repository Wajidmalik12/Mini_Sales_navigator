import os
import serpapi

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv("D:/sales_navigator/.env")



def create_industry_research_target(company, industry):

    return {
        "company": company,
        "industry": industry,
        "research_areas": [
            "industry standards",
            "common digital workflows",
            "competitors",
            "relevant SaaS platforms",
            "technology trends"
        ]
    }



def search_web(query):

    client = serpapi.Client(
        api_key=os.getenv("Key")
    )

    results = client.search({
        "engine": "google",
        "q": query
    })

    return results.get("organic_results", [])


def extract_search_results(results):

    extracted = []

    for result in results:

        extracted.append({
            "title": result.get("title", ""),
            "url": result.get("link", ""),
            "description": result.get("snippet", "")
        })

    return extracted



def research_industry_topics(company, industry):

    queries = [

        f"{industry} industry standards",

        f"{industry} common digital workflows",

        f"{industry} competitors",

        f"{industry} SaaS platforms",

        f"{industry} technology trends 2026"

    ]

    all_results = {}

    for query in queries:

        results = search_web(query)

        results = extract_search_results(results)

        all_results[query] = results

    return all_results


def prepare_research_content(research_results):

    content = []

    for query, results in research_results.items():

        content.append(f"Research Query: {query}")

        for result in results:

            content.append(
                f"""
Title: {result["title"]}
URL: {result["url"]}
Description: {result["description"]}
"""
            )

    return "\n".join(content)



INDUSTRY_RESEARCH_PROMPT = """
You are researching an industry to validate a potential business opportunity.

Analyze the provided company, industry, and web research.

Research these areas:

1. Industry standards
2. Common digital workflows
3. Competitors
4. Relevant SaaS platforms
5. Current technology trends

Your goal is NOT to recommend a solution immediately.

Instead:

- Identify what successful companies in this industry commonly use.
- Identify common customer and operational workflows.
- Identify technologies or platforms commonly used.
- Identify important trends.
- Compare these findings with the company's existing digital systems.
- Look for gaps or opportunities supported by evidence.
- Do not invent facts about the company.

Important rules:

- Separate industry-level information from company-specific information.
- Do not assume that an industry standard is used by this company.
- Do not invent information.
- Use the provided research as evidence.
- If the evidence is weak or conflicting, say so.

Company:
{company}

Industry:
{industry}

Existing digital systems:
{digital_systems}

Web research:
{research_content}
"""



llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)




def research_industry(
    company,
    industry,
    digital_systems
):

    research_results = research_industry_topics(
        company,
        industry
    )

    research_content = prepare_research_content(
        research_results
    )

    prompt = INDUSTRY_RESEARCH_PROMPT.format(
        company=company,
        industry=industry,
        digital_systems=digital_systems,
        research_content=research_content
    )

    response = llm.invoke(prompt)

    return response.content



# if __name__ == "__main__":

#     company = "AssortTech"

#     industry = "Software Development"

#     digital_systems = """
#     The company website shows software development,
#     web development, mobile development, and AI services.
#     No clear evidence of an online customer portal,
#     RFQ system, or AI chatbot was found.
#     """

#     results = research_industry_topics(
#         company,
#         industry
    

    # for query, search_results in results.items():

    #     print("\n" + "=" * 60)
    #     print("QUERY:", query)
    #     print("=" * 60)

    #     for result in search_results[:5]:

    #         print("\nTitle:", result["title"])
    #         print("URL:", result["url"])
    #         print("Description:", result["description"])