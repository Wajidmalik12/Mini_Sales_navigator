def create_lead_record(
    company,
    website,
    contact,
    title,
    linkedin_url,
    industry,
    opportunity,
    case_study=None,
    priority=None
):

    return {
        "company": company,
        "website": website,
        "contact": contact,
        "title": title,
        "linkedin_url": linkedin_url,
        "industry": industry,
        "opportunity": opportunity,
        "case_study": case_study,
        "priority": priority,
        "saved": False
    }

def assign_lead_lists(industry, opportunity, case_study=None):

    lists = []

    if industry:
        lists.append(industry)

    if opportunity:
        lists.append(opportunity)

    if case_study:
        lists.append(case_study)

    return lists

if __name__ == "__main__":

    lead = create_lead_record(
        company="AssortTech",
        website="https://assorttech.com",
        contact="Test Contact",
        title="CEO",
        linkedin_url="https://linkedin.com/in/test",
        industry="Software Development",
        opportunity="AI Automation",
        case_study=None,
        priority="HIGH"
    )

    lists = assign_lead_lists(
        industry=lead["industry"],
        opportunity=lead["opportunity"],
        case_study=lead["case_study"]
    )

    print("Lead:")
    print(lead)

    print("\nLists:")
    print(lists)