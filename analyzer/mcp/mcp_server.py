# mcp.py
import sys
import traceback
from typing import Dict, Any
from dotenv import load_dotenv
from mcp.server import FastMCP

from analyzer.constants import MODEL_VERSION_GEMINI
from analyzer.core.gemini_generator import GeminiGenerator

load_dotenv()

mcp = FastMCP("company-extractor")

generator = GeminiGenerator(model_name=MODEL_VERSION_GEMINI)

@mcp.tool()
async def extract_companies(text: str) -> Dict[str, Any]:
    try:
        result = generator.generate_answer(text)
        companies = result.get("companies", [])
        return {
            "status": "success",
            "result": result,
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