import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Set default USER_AGENT to prevent langchain_community delay/warning
os.environ.setdefault("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MiniSalesNavigator/1.0")

# Ensure local directory is in Python path and load local .env
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=str(env_path), override=False)

# Ensure GROQ_API_KEY is mapped from Groq_Api_Key if needed
if not os.getenv("GROQ_API_KEY") and os.getenv("Groq_Api_Key"):
    os.environ["GROQ_API_KEY"] = os.getenv("Groq_Api_Key")

app = FastAPI(title="Mini Sales Navigator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = BASE_DIR / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class PipelineRequest(BaseModel):
    company: str
    website: str
    industry: str = "AI"
    max_pages: int = 6


def get_mongo_collection():
    from company_search_by_country import collection
    return collection


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = static_dir / "index.html"
    if not index_file.exists():
        return HTMLResponse("<h1>Loading UI...</h1>", status_code=200)
    return HTMLResponse(index_file.read_text(encoding="utf-8"))


@app.get("/api/health")
async def health_check():
    mongo_status = False
    company_count = 0
    try:
        col = get_mongo_collection()
        company_count = col.estimated_document_count()
        mongo_status = True
    except Exception as e:
        mongo_status = False

    has_groq = bool(os.getenv("GROQ_API_KEY") or os.getenv("Groq_Api_Key"))
    has_serp = bool(os.getenv("Key"))

    return {
        "status": "healthy",
        "mongodb": {
            "connected": mongo_status,
            "total_records": company_count
        },
        "api_keys": {
            "groq_configured": has_groq,
            "serpapi_configured": has_serp
        }
    }


@app.get("/api/companies")
async def search_companies(
    country: Optional[str] = Query(None, description="Country filter"),
    query: Optional[str] = Query(None, description="Name or keyword search"),
    limit: int = Query(10, ge=1, le=50)
):
    try:
        col = get_mongo_collection()
        filter_dict: Dict[str, Any] = {}
        if country and country.strip():
            filter_dict["Location"] = {"$regex": country.strip(), "$options": "i"}
        if query and query.strip():
            filter_dict["Company_Name"] = {"$regex": query.strip(), "$options": "i"}

        cursor = col.find(filter_dict, {"_id": 0}).limit(limit)
        companies = list(cursor)
        return {"count": len(companies), "companies": companies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/pipeline/stream")
async def stream_pipeline(req: PipelineRequest):
    """
    Server-Sent Events (SSE) endpoint streaming execution updates step-by-step.
    """
    async def event_generator():
        def sse_message(step: str, status: str, detail: str, data: Any = None):
            payload = {
                "step": step,
                "status": status,
                "detail": detail,
                "data": data
            }
            return f"data: {json.dumps(payload)}\n\n"

        company = req.company.strip()
        url = req.website.strip()
        industry = req.industry.strip() or "AI"

        try:
            yield sse_message("init", "running", f"Starting research for {company} ({url})...")
            await asyncio.sleep(0.05)

            # Lazy import existing modules
            yield sse_message("init", "running", "Loading research modules...")
            loop = asyncio.get_running_loop()

            def load_modules():
                from research.research_web import find_relevant_pages, scrape_discovered_pages
                from research.digital_system import analyze_digital_systems
                from research.prospect_qualification import analyze_prospect
                from research.industry_research import research_industry
                from research.opportunity_identification import identify_opportunities
                from research.primary_opportunity import select_primary_opportunity
                from research.case_study_matching import match_case_study
                from sales.lead_storage import create_lead_record, assign_lead_lists
                from sales.outreach_tracker import create_outreach_record
                from sales.connection_request import generate_connection_request
                return {
                    "find_relevant_pages": find_relevant_pages,
                    "scrape_discovered_pages": scrape_discovered_pages,
                    "analyze_digital_systems": analyze_digital_systems,
                    "analyze_prospect": analyze_prospect,
                    "research_industry": research_industry,
                    "identify_opportunities": identify_opportunities,
                    "select_primary_opportunity": select_primary_opportunity,
                    "match_case_study": match_case_study,
                    "create_lead_record": create_lead_record,
                    "assign_lead_lists": assign_lead_lists,
                    "create_outreach_record": create_outreach_record,
                    "generate_connection_request": generate_connection_request,
                }

            mods = await loop.run_in_executor(None, load_modules)

            # Step 1: Discover and scrape pages
            yield sse_message("scrape", "running", "Discovering and scraping relevant website pages...")
            pages = await loop.run_in_executor(None, mods["find_relevant_pages"], url)
            limited_pages = pages[:req.max_pages] if pages else []
            documents = await loop.run_in_executor(None, mods["scrape_discovered_pages"], limited_pages)
            
            scraped_summary = {
                "pages_found": len(pages) if pages else 0,
                "pages_scraped": len(documents) if documents else 0,
                "pages_list": [{"title": p.get("text"), "url": p.get("url")} for p in limited_pages]
            }
            yield sse_message("scrape", "completed", f"Scraped {len(documents)} pages successfully.", scraped_summary)

            # Step 2: Digital Systems Analysis
            yield sse_message("digital_systems", "running", "Analyzing digital systems from web evidence...")
            digital_systems = await loop.run_in_executor(None, mods["analyze_digital_systems"], documents)
            yield sse_message("digital_systems", "completed", "Digital systems identified.", {"analysis": digital_systems})

            # Step 3: Prospect Qualification
            yield sse_message("qualification", "running", "Qualifying prospect readiness & fit...")
            qualification = await loop.run_in_executor(None, mods["analyze_prospect"], digital_systems)
            yield sse_message("qualification", "completed", "Prospect qualification completed.", {"qualification": qualification})

            # Step 4: Industry & Competitor Research
            yield sse_message("industry_research", "running", f"Conducting live industry research for {industry}...")
            industry_research = await loop.run_in_executor(
                None,
                mods["research_industry"],
                company,
                industry,
                digital_systems
            )
            yield sse_message("industry_research", "completed", "Industry research gathered.", {"industry_research": industry_research})

            # Step 5: Potential Opportunities Identification
            yield sse_message("opportunities", "running", "Identifying high-impact business opportunities...")
            opportunities = await loop.run_in_executor(
                None,
                mods["identify_opportunities"],
                company,
                industry,
                digital_systems,
                industry_research
            )
            yield sse_message("opportunities", "completed", "Opportunities identified.", {"opportunities": opportunities})

            # Step 6: Primary Opportunity Selection
            yield sse_message("primary_opportunity", "running", "Selecting single highest-conviction opportunity...")
            primary_opportunity = await loop.run_in_executor(
                None,
                mods["select_primary_opportunity"],
                opportunities
            )
            yield sse_message("primary_opportunity", "completed", "Primary opportunity selected.", {"primary_opportunity": primary_opportunity})

            # Step 7: Case Study Matching
            yield sse_message("case_study", "running", "Matching with proven relevant case studies...")
            case_study_raw = await loop.run_in_executor(
                None,
                mods["match_case_study"],
                primary_opportunity
            )
            case_study_text = case_study_raw.content if hasattr(case_study_raw, "content") else str(case_study_raw or "No match found")
            yield sse_message("case_study", "completed", "Case study matching complete.", {"case_study": case_study_text})

            # Step 8: Lead Record & Outreach Tracking
            yield sse_message("lead_record", "running", "Synthesizing lead record and list assignments...")
            lead = mods["create_lead_record"](
                company=company,
                website=url,
                industry=industry,
                opportunity=primary_opportunity,
                case_study=case_study_text,
                priority="REVIEW"
            )
            lead_lists = mods["assign_lead_lists"](
                industry=lead["industry"],
                opportunity=lead["opportunity"],
                case_study=lead["case_study"]
            )
            outreach_record = mods["create_outreach_record"](
                company=lead["company"],
                website=lead["website"],
                industry=lead["industry"],
                opportunity=lead["opportunity"],
                existing_systems=digital_systems,
                case_study=lead["case_study"],
                rating=lead["priority"]
            )
            yield sse_message("lead_record", "completed", "Lead & outreach records structured.", {
                "lead": lead,
                "lead_lists": lead_lists,
                "outreach_record": outreach_record
            })

            # Step 9: LinkedIn Connection Request
            yield sse_message("connection_request", "running", "Crafting personalized LinkedIn connection message...")
            connection_message = await loop.run_in_executor(
                None,
                mods["generate_connection_request"],
                lead,
                primary_opportunity
            )
            yield sse_message("connection_request", "completed", "Connection message crafted.", {
                "connection_message": connection_message
            })

            # Final Complete Summary Event
            yield sse_message("done", "finished", "Navigator analysis completed successfully!", {
                "company": company,
                "website": url,
                "industry": industry,
                "scraped_summary": scraped_summary,
                "digital_systems": digital_systems,
                "qualification": qualification,
                "industry_research": industry_research,
                "opportunities": opportunities,
                "primary_opportunity": primary_opportunity,
                "case_study": case_study_text,
                "lead": lead,
                "lead_lists": lead_lists,
                "outreach_record": outreach_record,
                "connection_message": connection_message
            })

        except Exception as err:
            yield sse_message("error", "failed", f"Pipeline error: {str(err)}", {"error": str(err)})

    return StreamingResponse(event_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
