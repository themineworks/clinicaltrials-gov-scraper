# ClinicalTrials.gov Scraper: Trial & Pipeline Data

Search ClinicalTrials.gov for studies by condition, drug, sponsor, status, phase, and location. Clean structured JSON with sponsors, enrollment, phases, and sites. Empty results are never charged.

**Run it on Apify:** [apify.com/themineworks/clinicaltrials-scraper](https://apify.com/themineworks/clinicaltrials-scraper)
**Docs, FAQ and pricing:** [themineworks.com/actors/clinicaltrials-scraper](https://themineworks.com/actors/clinicaltrials-scraper/)

**Price:** From $2.50 per 1,000 studies on Apify's higher plans ($3.50 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* Filter by condition, drug, sponsor, and phase
* Enrollment numbers and study status
* Sponsor and investigator details
* Site locations and contact information
* Empty results are never charged

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/clinicaltrials-scraper").call(run_input={
    "condition": "diabetes",
    "searchTerm": "NCT04280705",
    "intervention": "semaglutide",
    "sponsor": "Pfizer"
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/clinicaltrials-scraper').call({
    "condition": "diabetes",
    "searchTerm": "NCT04280705",
    "intervention": "semaglutide",
    "sponsor": "Pfizer"
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~clinicaltrials-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"condition": "diabetes", "searchTerm": "NCT04280705", "intervention": "semaglutide", "sponsor": "Pfizer"}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 clinicaltrials_gov_scraper.py --token YOUR_APIFY_TOKEN --condition "diabetes" --search-term "NCT04280705" --intervention "semaglutide" --sponsor "Pfizer"
node clinicaltrials_gov_scraper.mjs --token YOUR_APIFY_TOKEN --condition "diabetes" --search-term "NCT04280705" --intervention "semaglutide" --sponsor "Pfizer"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `condition` | string |  | Medical condition or disease to search for (for example diabetes, breast cancer, alzheimer) |
| `searchTerm` | string |  | Free-text terms matched across the whole record (for example a keyword, NCT number, or phrase) |
| `intervention` | string |  | Drug, device or intervention name (for example semaglutide, pembrolizumab) |
| `sponsor` | string |  | Lead sponsor or collaborator name (for example Pfizer, National Cancer Institute) |
| `location` | string |  | Location term, country, state or city (for example United States, California, Boston) |
| `status` | array |  | Filter by recruitment status, for example "RECRUITING" or "COMPLETED" |
| `maxResults` | integer | `100` | Maximum number of studies to return |
| `includeLocations` | boolean | `false` | Attach the full list of study sites (facility, city, country) for each study |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `nct_id` | string | ClinicalTrials.gov NCT identifier |
| `title` | string | Brief study title |
| `official_title` | string | Official full study title |
| `overall_status` | string | Overall recruitment status |
| `study_type` | string | Study type (Interventional, Observational, etc.) |
| `phases` | array | Study phases |
| `conditions` | array | Medical conditions being studied |
| `interventions` | array | Interventions being evaluated |
| `lead_sponsor` | string | Lead sponsor name |
| `sponsor_class` | string | Sponsor class (NIH, Industry, etc.) |
| `collaborators` | array | Collaborating organizations |
| `enrollment` | number | Enrollment count |
| `enrollment_type` | string | Enrollment type (Actual or Anticipated) |
| `start_date` | string | Study start date |
| `primary_completion_date` | string | Primary completion date |
| `completion_date` | string | Study completion date |
| `last_update_date` | string | Date of last update |
| `sex` | string | Eligible sex |
| `minimum_age` | string | Minimum eligible age |
| `maximum_age` | string | Maximum eligible age |
| `healthy_volunteers` | string | Whether healthy volunteers are accepted |
| `brief_summary` | string | Brief study description |
| `location_count` | number | Number of study locations |
| `location_countries` | array | Countries where study is conducted |
| `study_url` | string | URL to study on ClinicalTrials.gov |
| `scraped_at` | string | Timestamp when the record was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/clinicaltrials-scraper
```

## FAQ

### What data can I pull from ClinicalTrials.gov?

Study title, NCT ID, sponsor, phase, status, enrollment, conditions, interventions, site locations, and contact information. All from the official ClinicalTrials.gov v2 API.

### Can I track all trials for a specific drug or compound?

Yes. Search by drug name, intervention type, sponsor name, condition, or any combination. The scraper returns all matching studies with full structured data.

### Is there an official ClinicalTrials.gov API?

Yes. ClinicalTrials.gov has a public v2 REST API with no authentication required. This scraper handles pagination and rate limiting, returning clean normalized JSON.

### What use cases is this built for?

Pharma competitive intelligence, patient recruitment research, clinical trial landscape analysis, and building RAG pipelines over clinical study data for biotech research tools.

### How current is the data?

ClinicalTrials.gov is updated daily. Each scraper run pulls live data from the official registry.

### Can I filter by trial phase and status at once?

Yes. Condition, drug, sponsor, status, phase and location combine in a single query rather than needing separate runs.

### How much does the ClinicalTrials.gov Scraper cost?

From $2.50 per 1,000 studies on Apify's higher plans ($3.50 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged. You can cap what a single run may spend with the maximum cost setting on Apify.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [Google Trends Scraper](https://themineworks.com/actors/google-trends-pro/): Interest over time, regional breakdown, and related queries
* [OpenAlex Scholarly Works](https://themineworks.com/actors/openalex-scholarly-works/): 250M+ research papers, authors, and citations as structured JSON
* [Tennis Match & Player Data Scraper](https://themineworks.com/actors/tennis-match-data/): ATP and WTA match results with serve and return stats

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
