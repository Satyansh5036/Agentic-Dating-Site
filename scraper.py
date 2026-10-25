import os
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")
client = ApifyClient(APIFY_TOKEN) if APIFY_TOKEN else None

def scrape_profile(linkedin_url: str, instagram_url: str):
    """
    Triggers Apify actors with robust error handling and fallback text.
    """
    scraped_data = {
        "linkedin_bio": "Experienced technology leader and builder focused on scaling high-performance platforms.",
        "instagram_bio": "Sharing moments, travel, and building cool tech products."
    }
    
    if not client:
        return scraped_data

    try:
        # Fetch Instagram profile details
        if instagram_url:
            try:
                insta_run = client.actor("apify/instagram-profile-scraper").call(
                    run_input={"directUrls": [instagram_url]}, timeout=15
                )
                for item in client.dataset(insta_run.default_dataset_id).iterate_items():
                    bio = item.get("biography", "") or item.get("caption", "")
                    if bio:
                        scraped_data["instagram_bio"] = bio
            except Exception:
                pass  # Fallback gracefully if Instagram URL is restricted or invalid
                
        # Fetch LinkedIn profile details
        if linkedin_url:
            try:
                linkedin_run = client.actor("curious_coder/linkedin-profile-scraper").call(
                    run_input={"url": linkedin_url}, timeout=15
                )
                for item in client.dataset(linkedin_run.default_dataset_id).iterate_items():
                    about = item.get("about", "") or item.get("headline", "")
                    if about:
                        scraped_data["linkedin_bio"] = about
            except Exception:
                pass  # Fallback gracefully if LinkedIn URL blocks scraping
                
    except Exception as e:
        print(f"Apify connection note: {e}")
        
    return scraped_data