import json
import re
from typing import List, Union

from google import genai
from google.genai.types import GenerateContentConfig, GoogleSearch, Tool

from analyzer.constants import (
    COMPETITORS_SYSTEM_PROMPT,
    GEMINI_MODEL_NAME,
    SYSTEM_PROMPT,
    WEBSITES_NA_PLACEHOLDERS,
)


class GeminiAnalyser:
    def __init__(self, api_key: str, model_name: str = GEMINI_MODEL_NAME):
        """
        model_name: str - The model we use for generating the answer
        api_key: str - The Google`s api key
        """
        self.model_name = model_name
        self.client = genai.Client(api_key=api_key)
        self.google_search_tool = Tool(google_search=GoogleSearch())

    @staticmethod
    def remove_square_bracket_references(text: str) -> str:
        # Remove references in square brackets like [1, 2], [3, 4], etc.
        return re.sub(r"\[\s*\d+(?:\s*,\s*\d+)*\s*\]", "", text)

    @staticmethod
    def find_companies_without_website(
        json_data: list, extract_competitors: bool = True
    ) -> List[str]:
        """
        Find companies without a website in the provided JSON data.
        Args:
            json_data: list - The JSON data containing company information.
            extract_competitors: bool - Whether to extract competitors' companies as well.

        Returns:
            List[str]: A list of company names that do not have a website.
        """
        companies_without_website = []
        for item in json_data:
            # Loop for the main companies
            if item.get("website") in WEBSITES_NA_PLACEHOLDERS and item.get("company"):
                companies_without_website.append(item.get("company"))

            if extract_competitors:
                # Now we check competitors companies
                competitors = item.get("competitors_analysis", {}).get(
                    "competitors", []
                )
                if isinstance(competitors, list):
                    for company in competitors:
                        if isinstance(company, dict):
                            if company.get("website") in WEBSITES_NA_PLACEHOLDERS:
                                companies_without_website.append(company.get("name"))
                        else:
                            print(
                                f"Unexpected type for 'company' in competitors list: {type(company)}"
                            )
                else:
                    print(f"Unexpected type for 'competitors': {type(competitors)}")

        return companies_without_website

    @staticmethod
    def extract_all_json_objects(text: str) -> List[Union[dict, list]]:
        """
        Extract all JSON objects or arrays from the text and return them as a list.
        Args:
            text (str): The input text containing JSON objects or arrays.
        Returns:
            List[Union[dict, list]]: A list of JSON objects or arrays extracted from the text.
        """
        try:
            json_blobs = []
            # Match multiple JSON blocks inside ```json ... ``` or just {...} or [...]
            matches = re.findall(r"```json\s*(\{.*?\}|\[.*?\])\s*```", text, re.DOTALL)

            # Fallback: also catch raw {...} or [...] blocks not wrapped in ```json ... ```
            if not matches:
                matches = re.findall(r"(\{.*?\}|\[.*?\])", text, re.DOTALL)

            for json_str in matches:
                try:
                    json_blobs.append(json.loads(json_str))
                except json.JSONDecodeError:
                    continue

            return json_blobs
        except Exception as e:
            raise ValueError(f"Unexpected error during JSON extraction: {e}")

    async def generate_response(
        self, input_text: str, find_competitors: bool = True
    ) -> str:
        """
        Generate a response based on the input text using the Gemini model.
        Args:
            input_text: str - The input text to analyze.
            find_competitors: bool - Whether to find competitors in the analysis.

        Returns:
            str: The generated response containing company analysis.
        """
        if find_competitors:
            prompt = SYSTEM_PROMPT
        else:
            prompt = COMPETITORS_SYSTEM_PROMPT

        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=input_text,
            config=GenerateContentConfig(
                tools=[self.google_search_tool],
                response_modalities=["TEXT"],
                system_instruction=prompt,
            ),
        )
        extended_answer = ""

        for each in response.candidates[0].content.parts:
            extended_answer += each.text

        return extended_answer

    async def get_company_analysis(self, text: str) -> Union[List[dict], List[list]]:
        """Analyze the provided text to extract company information.
        Args:
            text (str): The text to analyze for company information.
        Returns:
            Union[List[dict], List[list]]: A list of dictionaries containing company information.
        """
        text = self.remove_square_bracket_references(text)
        analysis = await self.generate_response(text)

        extracted_json = self.extract_all_json_objects(analysis)

        json_data = extracted_json[0] if extracted_json else []

        # If json_data is a dictionary (single company), wrap it in a list
        if isinstance(json_data, dict):
            json_data = [json_data]

        companies_wo_website = str(self.find_companies_without_website(json_data))

        if len(companies_wo_website) > 2:
            new_companies_wo_website = ""
            for company in companies_wo_website:
                filled_company = await self.generate_response(
                    company, find_competitors=False
                )
                new_companies_wo_website += filled_company

            final_json = self.extract_all_json_objects(new_companies_wo_website)
            new_companies_wo_web = self.find_companies_without_website(
                final_json, extract_competitors=False
            )

            # Update the main data with the new company information
            for updated_company_data in final_json:
                company_name = updated_company_data.get("company_name")
                if not company_name:
                    continue

                for item in json_data:
                    if (
                        item.get("company_name") == company_name
                        and item.get("website") in WEBSITES_NA_PLACEHOLDERS
                    ):
                        item.update(updated_company_data)

                    competitors = item.get("competitors_analysis", {}).get(
                        "competitors", []
                    )
                    for competitor in competitors:
                        if (
                            competitor.get("name") == company_name
                            and competitor.get("website") in WEBSITES_NA_PLACEHOLDERS
                        ):
                            competitor.update(updated_company_data)

            return json_data if isinstance(extracted_json[0], list) else [json_data]

        return extracted_json
