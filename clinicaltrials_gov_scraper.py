#!/usr/bin/env python3
"""Clinical studies, sponsors, and sites from ClinicalTrials.gov. Python, Node.js and cURL clients for the ClinicalTrials.gov Scraper on Apify, pay per result.

Command-line client for the themineworks/clinicaltrials-scraper actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/clinicaltrials-scraper/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/clinicaltrials-scraper"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--condition", help="Medical condition or disease to search for (for example diabetes, breast cancer…")
    ap.add_argument("--search-term", help="Free-text terms matched across the whole record (for example a keyword, NCT number, or…")
    ap.add_argument("--intervention", help="Drug, device or intervention name (for example semaglutide, pembrolizumab)")
    ap.add_argument("--sponsor", help="Lead sponsor or collaborator name (for example Pfizer, National Cancer Institute)")
    ap.add_argument("--location", help="Location term, country, state or city (for example United States, California, Boston)")
    ap.add_argument("--status", help="Comma-separated. Filter by recruitment status, for example 'RECRUITING' or 'COMPLETED'")
    ap.add_argument("--max-results", type=int, help="Maximum number of studies to return")
    ap.add_argument("--include-locations", action=argparse.BooleanOptionalAction, help="Attach the full list of study sites (facility, city, country) for each study")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.condition is not None: run_input["condition"] = a.condition
    if a.search_term is not None: run_input["searchTerm"] = a.search_term
    if a.intervention is not None: run_input["intervention"] = a.intervention
    if a.sponsor is not None: run_input["sponsor"] = a.sponsor
    if a.location is not None: run_input["location"] = a.location
    if a.status: run_input["status"] = [s.strip() for s in a.status.split(",") if s.strip()]
    if a.max_results is not None: run_input["maxResults"] = a.max_results
    if a.include_locations is not None: run_input["includeLocations"] = a.include_locations

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
