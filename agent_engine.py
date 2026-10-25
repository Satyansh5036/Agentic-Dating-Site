import os
import json
# pyrefly: ignore[missing-import]
from openai import OpenAI
client = OpenAI(api_key="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")
# pyrefly: ignore[missing-import]

def analyze_profile(name, title, linkedin_bio, instagram_bio):
    """
    Analyzes the scraped profile data to generate needs, hobbies, interests, and qualities.
    """
    prompt = f"""
    You are an expert psychological profiler for an agentic dating platform.
    Analyze this person based on their LinkedIn and Instagram data:
    Name: {name}
    Title: {title}
    LinkedIn Bio: {linkedin_bio}
    Instagram Bio: {instagram_bio}

    Return a valid JSON object with these exact keys:
    "needs": "...",
    "hobbies": "...",
    "interests": "...",
    "qualities": "..."
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def simulate_agent_date(agent_a, agent_b):
    """
    Simulates a multi-turn conversation between two agents representing their humans,
    then outputs a compatibility score and summary log.
    """
    prompt = f"""
    Simulate a 3-turn first date conversation between two AI dating agents:
    Agent A represents {agent_a['name']} ({agent_a['title']}). Profile analysis: {json.dumps(agent_a['analysis'])}
    Agent B represents {agent_b['name']} ({agent_b['title']}). Profile analysis: {json.dumps(agent_b['analysis'])}

    Have them chat based on their actual traits, hobbies, and mutual interests.
    At the end, output a valid JSON object with:
    "chat_log": ["A: ...", "B: ...", "A: ...", "B: ..."],
    "compatibility_score": 85 (an integer out of 100),
    "reason": "Short summary of why they match or don't."
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
