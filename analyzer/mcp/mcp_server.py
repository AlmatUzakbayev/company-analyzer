# mcp.py
import sys
import traceback
from typing import Dict, Any
from mcp.server import FastMCP

from analyzer.config import GOOGLE_API_KEY
from analyzer.constants import GEMINI_MODEL_NAME
from analyzer.core.generator import GeminiAnalyser

mcp = FastMCP("company-extractor")

generator = GeminiAnalyser(api_key=GOOGLE_API_KEY, model_name=GEMINI_MODEL_NAME)

@mcp.tool()
async def extract_companies(text: str) -> Dict[str, Any]:
    try:
        companies = await generator.get_company_analysis(text)
        return {
            "status": "success",
            "result": companies,
            "message": f"Extracted and enriched {len(companies)} companies"
        }
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return {
            "status": "error",
            "message": f"Error while extracting companies: {str(e)}"
        }

if __name__ == "__main__":
    mcp.run(transport="stdio")
