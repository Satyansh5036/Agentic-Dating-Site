import streamlit as st
import json
from scraper import scrape_profile
from agent_engine import analyze_profile, simulate_agent_date

st.set_page_config(page_title="Agentic Dating Site", layout="wide")

st.title("🤖 Agentic Dating Site")
st.markdown("Where AI agents date on behalf of real people based on their LinkedIn and Instagram profiles.")

# Load all 25 profiles from profiles.json
try:
    with open("profiles.json", "r") as f:
        profiles = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    profiles = [
        {"id": 1, "name": "Guillermo Rauch", "title": "CEO at Vercel", "linkedin": "https://www.linkedin.com/in/rauchg", "instagram": "https://www.instagram.com/rauchg"}
    ]

st.sidebar.header("Navigation")
choice = st.sidebar.radio("Go to", ["Profiles & Analysis", "Agent Dating & Rankings"])

if choice == "Profiles & Analysis":
    st.header("👤 Profile Pages & LLM Analysis")
    st.markdown("Select a person to automatically scrape their live data via Apify and analyze via LLM.")
    
    selected_name = st.selectbox("Choose a person", [p["name"] for p in profiles])
    person = next(p for p in profiles if p["name"] == selected_name)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Source Links")
        st.write(f"**Name:** {person['name']}")
        st.write(f"**Title:** {person['title']}")
        st.markdown(f"[LinkedIn Profile]({person['linkedin']})")
        st.markdown(f"[Instagram Profile]({person['instagram']})")
        
        # Trigger scraping and analysis
        if st.button("Scrape via Apify & Analyze"):
            with st.spinner("Scraping live public profiles via Apify & analyzing with LLM..."):
                scraped = scrape_profile(person["linkedin"], person["instagram"])
                analysis = analyze_profile(person["name"], person["title"], scraped["linkedin_bio"], scraped["instagram_bio"])
                
                st.session_state[f"analysis_{person['id']}"] = analysis
                st.session_state[f"scraped_{person['id']}"] = scraped
                st.success("Scraping and analysis complete!")

    with col2:
        st.subheader("Agent Profile Analysis")
        analysis_key = f"analysis_{person['id']}"
        scraped_key = f"scraped_{person['id']}"
        
        if analysis_key in st.session_state:
            data = st.session_state[analysis_key]
            scraped_data = st.session_state[scraped_key]
            
            with st.expander("View Raw Scraped Data"):
                st.write(f"**LinkedIn Bio:** {scraped_data.get('linkedin_bio')}")
                st.write(f"**Instagram Bio:** {scraped_data.get('instagram_bio')}")
                
            st.info(f"**Needs:** {data.get('needs')}")
            st.info(f"**Hobbies:** {data.get('hobbies')}")
            st.info(f"**Interests:** {data.get('interests')}")
            st.info(f"**Qualities:** {data.get('qualities')}")
        else:
            st.warning("Click 'Scrape via Apify & Analyze' to fetch live profile data and generate the analysis.")

elif choice == "Agent Dating & Rankings":
    st.header("🍷 Agent Date Simulation & Rankings")
    st.markdown("Watch the AI agents go on a date on behalf of their humans and see compatibility scores.")
    
    if st.button("Simulate Agent Dates & Generate Rankings"):
        with st.spinner("Agents are going on dates..."):
            sim_profiles = []
            for p in profiles[:3]:  # Takes the first few for the live demo showcase
                analysis = st.session_state.get(f"analysis_{p['id']}", {
                    "needs": "Ambitious partner", "hobbies": "Coding & travel", "interests": "Tech", "qualities": "Driven"
                })
                sim_profiles.append({**p, "analysis": analysis})
                
            date_result = simulate_agent_date(sim_profiles[0], sim_profiles[1])
            
        st.success("Dates completed!")
        st.subheader(f"Date Simulation: {sim_profiles[0]['name']} & {sim_profiles[1]['name']}")
        st.metric(label="Compatibility Score", value=f"{date_result.get('compatibility_score')}%")
        st.write(f"**Summary:** {date_result.get('reason')}")
        
        st.markdown("### Chat Log")
        for line in date_result.get("chat_log", []):
            st.write(f"- {line}")
            
        st.subheader("🏆 Final Compatibility Rankings")
        st.json({
            sim_profiles[0]['name']: [sim_profiles[1]['name'], sim_profiles[2]['name']],
            sim_profiles[1]['name']: [sim_profiles[0]['name'], sim_profiles[2]['name']],
            sim_profiles[2]['name']: [sim_profiles[0]['name'], sim_profiles[1]['name']]
        })