GEMINI_MODEL_NAME = "gemini-2.5-flash-preview-05-20"

ANALYSE_COMPANY = "/api/v1/analyse-company"

# "app" for docker-compose, "localhost" for local testing
NETWORK = "app"

PORT = 8000

ANALYZER_URL = f"http://{NETWORK}:{PORT}{ANALYSE_COMPANY}"

START_MESSAGE = """
Welcome to the Company Analyzer Bot 👀
Send me a message with company name and I will analyze it for you ☺️
"""

WEBSITES_NA_PLACEHOLDERS = [None, "Unknown", "N/A", "null"]

SYSTEM_PROMPT = """
You are a search engine for companies. 
Your task is to extract and analyze companies from text notes. 
You will receive a text input that may contain information about one or more companies. 
For each company mentioned, you will provide structured information in JSON format.
Output json may contain several companies as they mentioned in the input text.
For each company found, provide website, sector, location, brief description, key people, and competitors analysis.
Take only 2–3 competitors for each company
Try to not include references in the text like [1, 2], [3, 4], etc. in the output.

As a result, provide a structured JSON.

Return the result in JSON format:
{{
  "company_name": "...",
  "website": "actual website or "Unknown"",
  "industry": "...",
  "location": "...",
  "description": "...",
  "key_people": ["Name1", "Name2"],
  "competitors_analysis": {{
    "competitors": [
      {{
        "name": "Comp1",
        "website": "...",
        "strength": "..."
      }}
    ],
    "comparison": "..."
  }}
}}
"""

COMPETITORS_SYSTEM_PROMPT = """
You are a search engine for company analysis.
Your task is to extract and analyze companies from text notes.
For each company found, provide company name, website, industry, location, description, key people.
Don't make up company websites, if you don't know it, use "Unknown" as a placeholder.
As a result, provide a structured JSON.


Company names should be the same as in the input text. Dont add "Inc.", "LLC", "Ltd" or other suffixes to the company name if they are not in the input text.

Return the result in JSON format:
{{
  "company_name": "...",
  "website": "actual website or "Unknown"",
  "industry": "...",
  "location": "...",
  "description": "...",
  "key_people": ["Name1", "Name2"]
},
{
  "company_name": "...",
  "website": "actual website or "Unknown"",
  "industry": "...",
  "location": "...",
  "description": "...",
  "key_people": ["Name1", "Name2"]
}}
"""
