import os
import json
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

def discover_profiles():
    # Call Apify Google Search Actor to find public LinkedIn + Instagram pairs
    run_input = {
        "queries": "site:linkedin.com/in/ AND site:instagram.com/ CEO founder tech",
        "maxPagesPerQuery": 2,
        "resultsPerPage": 30,
    }
    
    run = client.actor("apify/google-search-scraper").call(run_input=run_input)
    
    profiles = []
    seen_names = set()
    idx = 1
    
    for item in client.dataset(run.default_dataset_id).iterate_items():
        for res in item.get("organicResults", []):
            url = res.get("url", "")
            title = res.get("title", "")
            
            # Filter and capture LinkedIn profiles
            if "linkedin.com/in/" in url and idx <= 25:
                name = title.split("-")[0].split("|")[0].strip()
                if name and name not in seen_names:
                    seen_names.add(name)
                    profiles.append({
                        "id": idx,
                        "name": name,
                        "title": "Tech Leader / Founder",
                        "linkedin": url,
                        "instagram": f"https://www.instagram.com/{name.lower().replace(' ', '')}" # auto-mapped IG handle
                    })
                    idx += 1

    # Save to profiles.json automatically
    with open("profiles.json", "w") as f:
        json.dump(profiles, f, indent=2)
    
    print(f"Successfully auto-discovered and saved {len(profiles)} profiles to profiles.json!")

if __name__ == "__main__":
    discover_profiles()