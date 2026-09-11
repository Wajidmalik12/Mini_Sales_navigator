def create_outreach_record(
    company,
    website,
    contact,
    title,
    linkedin_url,
    industry,
    company_size,
    opportunity,
    existing_systems,
    case_study=None,
    rating=None
):

    return {
        "company": company,
        "website": website,
        "contact": contact,
        "title": title,
        "linkedin_url": linkedin_url,
        "industry": industry,
        "company_size": company_size,
        "opportunity": opportunity,
        "existing_systems": existing_systems,
        "case_study": case_study,
        "rating": rating,
        "connection_status": "NOT_SENT",
        "message_date": None,
        "follow_up_date": None,
        "response": None,
        "notes": None,
        "next_action": "SEND_CONNECTION_REQUEST"
    }
def update_outreach_record(record, **updates):

    for key, value in updates.items():

        if key in record:
            record[key] = value

    return record


if __name__ == "__main__":

    record = create_outreach_record(
        company="AssortTech",
        website="https://assorttech.com",
        contact="Test Contact",
        title="CEO",
        linkedin_url="https://linkedin.com/in/test",
        industry="Software Development",
        company_size="10-50",
        opportunity="AI Automation",
        existing_systems="Web development, mobile development, AI services",
        case_study=None,
        rating="HIGH"
    )
    updated_record = update_outreach_record(
    record,
    connection_status="SENT",
    message_date="2026-09-09",
    next_action="WAIT_FOR_RESPONSE"
                              )

    print("\nUpdated Record:")
    print(updated_record)

    print(record)