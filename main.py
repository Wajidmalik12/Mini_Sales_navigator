from research.research_web import (
    find_relevant_pages,
    scrape_discovered_pages
)
from research.digital_system import analyze_digital_systems
from research.prospect_qualification import analyze_prospect
from research.industry_research import research_industry
from research.opportunity_identification import identify_opportunities
from research.primary_opportunity import select_primary_opportunity
from research.case_study_matching import match_case_study

from sales.lead_storage import (
    create_lead_record,
    assign_lead_lists
)
from sales.outreach_tracker import create_outreach_record
from sales.connection_request import generate_connection_request
from company_search_by_country import find_by_country



INDUSTRY = "AI"



def main():
    country = input("Enter the country : ")
    companies = find_by_country(country,limit=1)
    for doc in companies:
        print("="*50)
        print(doc)
        url = doc.get("Website")
        company = doc.get("Company_Name")


    pages = find_relevant_pages(url)

    documents = scrape_discovered_pages(pages)

    print("\nWebsite Research:")
    print("Pages found:", len(pages))
    print("Documents scraped:", len(documents))



    digital_systems = analyze_digital_systems(documents)

    print("\nDigital Systems Analysis:")
    print(digital_systems)



    qualification = analyze_prospect(digital_systems)

    print("\nProspect Qualification:")
    print(qualification)



    industry_research = research_industry(
        company=company,
        industry=INDUSTRY,
        digital_systems=digital_systems
    )

    print("\nIndustry Research:")
    print(industry_research)



    opportunities = identify_opportunities(
        company=company,
        industry=INDUSTRY,
        digital_systems=digital_systems,
        industry_research=industry_research
    )

    print("\nPotential Opportunities:")
    print(opportunities)


    

    primary_opportunity = select_primary_opportunity(
        opportunities
    )

    print("\nPrimary Opportunity:")
    print(primary_opportunity)



    case_study = match_case_study(
        primary_opportunity
    )

    print("\nCase Study Match:")
    print(case_study)



    lead = create_lead_record(
        company=company,
        website=url,
        contact="Test Contact",
        title="CEO",
        linkedin_url="https://linkedin.com/in/test",
        industry=INDUSTRY,
        opportunity=primary_opportunity,
        case_study=None,
        priority="REVIEW"
    )

    lead_lists = assign_lead_lists(
        industry=lead["industry"],
        opportunity=lead["opportunity"],
        case_study=lead["case_study"]
    )

    print("\nLead Record:")
    print(lead)

    print("\nLead Lists:")
    print(lead_lists)


    outreach_record = create_outreach_record(
        company=lead["company"],
        website=lead["website"],
        contact=lead["contact"],
        title=lead["title"],
        linkedin_url=lead["linkedin_url"],
        industry=lead["industry"],
        company_size="Unknown",
        opportunity=lead["opportunity"],
        existing_systems=digital_systems,
        case_study=lead["case_study"],
        rating=lead["priority"]
    )

    print("\nOutreach Record:")
    print(outreach_record)


    connection_message = generate_connection_request(
        prospect=lead,
        opportunity=primary_opportunity
    )

    print("\nConnection Request:")
    print(connection_message)


if __name__ == "__main__":
    main()