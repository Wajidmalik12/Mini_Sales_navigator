# Mini Sales Navigator & Outreach Automation

A lightweight **Sales Navigator-style prospecting and outreach automation system** built as an alternative when direct LinkedIn Sales Navigator/API access was not available.

Instead of relying on LinkedIn's paid Sales Navigator search, this project uses a **MongoDB database containing company data** and provides a keyword/country-based company retrieval system that feeds the selected company into the existing scraping, research, and outreach pipeline.

## 🚀 Overview

The system follows a simplified prospecting workflow:

```text
User Search
    ↓
Mini Sales Navigator
    ↓
MongoDB Company Database
    ↓
Company Selection
    ↓
Website / URL Retrieval
    ↓
Web Scraping & Research
    ↓
Lead/Company Information
    ↓
Outreach Message Generation
```

The goal was to reproduce the **functional workflow** of a Sales Navigator-style system rather than recreate LinkedIn's UI.

## ✨ Features

* 🔎 Search companies using keywords
* 🌍 Filter/search companies by country
* 🗄️ Store and retrieve company data from MongoDB
* 🔗 Retrieve company names and website/LinkedIn-related URLs from stored records
* 📄 Use the selected company as input for the existing scraping pipeline
* 🌐 Scrape and research company websites
* 🤖 Generate outreach/connection messages
* 🔄 Connect the company-search stage with the rest of the outreach automation pipeline
* 🧩 Modular structure allowing the mini navigator to be modified independently

## 🛠️ Tech Stack

* **Python**
* **MongoDB**
* **FastAPI**
* **Web scraping**
* **LLM integration**
* **Pandas**
* **CSV / dataset processing**
* **Git & GitHub**
* 
## 🔎 How the Mini Navigator Works

The original plan was to use LinkedIn Sales Navigator to identify target companies and pass their information into the automation pipeline.

Because direct Sales Navigator access/API availability was not practical, the project uses a local MongoDB dataset instead.

For example:

```text
Country: United States
Keyword: AI
```

The system searches the MongoDB collection and retrieves matching company records.

A simplified result can look like:

```text
Company: Example AI
Industry: Artificial Intelligence
Country: United States
URL: https://example.com
```

The selected company can then be passed to the next stages of the system.

## 🗄️ MongoDB

Company information is stored in MongoDB so that the application can perform searches without repeatedly processing the original dataset.

Example conceptual document:

```json
{
    "company_name": "Example AI",
    "industry": "Artificial Intelligence",
    "country": "United States",
    "url": "https://example.com"
}
```

The database can be queried using different search parameters such as:

* Country
* Company keywords
* Industry
* Other available company fields

## 🔄 Outreach Pipeline

The mini navigator is only one part of the complete system.

After retrieving a company, the pipeline can continue with:

1. Company identification
2. URL extraction
3. Website scraping
4. Company research
5. Information extraction
6. Lead/prospect research
7. Outreach message generation
8. Outreach processing

This allows the project to function as a **complete prospecting workflow**, rather than just a database search tool.

## ⚠️ LinkedIn Sales Navigator Limitation

This project **does not directly access or automate LinkedIn Sales Navigator**.

The mini navigator was created because the required LinkedIn Sales Navigator/API functionality was not available.

Therefore, the MongoDB dataset acts as the **company discovery layer** while the rest of the automation pipeline remains usable.

This approach also makes the project easier to test and develop without depending entirely on a third-party paid API.

## 🎯 Purpose

The main purpose of this project is to demonstrate how a Sales Navigator-style workflow can be implemented using:

* Database-driven search
* Python automation
* Web scraping
* LLM-based research
* Automated outreach generation
* Modular backend architecture

It is intended as a **functional prototype**, not a replacement for LinkedIn's actual Sales Navigator product.

## 📌 Project Status

**Status: Functional Prototype**

The core company retrieval and outreach pipeline has been implemented and tested using a MongoDB-based company dataset.

---

### Author

**Abdul Wajid Malik**

AI/ML Engineer | Python | FastAPI | MongoDB | LLMs
