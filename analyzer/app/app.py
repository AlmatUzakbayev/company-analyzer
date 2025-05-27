import uvicorn
from fastapi import FastAPI

from analyzer.app.data import TextInput
from analyzer.config import GOOGLE_API_KEY
from analyzer.constants import ANALYSE_COMPANY, GEMINI_MODEL_NAME, NETWORK, PORT
from analyzer.core.generator import GeminiAnalyser

app = FastAPI()

generator = GeminiAnalyser(api_key=GOOGLE_API_KEY, model_name=GEMINI_MODEL_NAME)


@app.post(ANALYSE_COMPANY)
async def company_analyser(request: TextInput):
    try:
        response = await generator.get_company_analysis(request.query)
        return {"text": response}
    except Exception as e:
        raise e


def main():
    uvicorn.run(app, host=NETWORK, port=PORT)


if __name__ == "__main__":
    main()
