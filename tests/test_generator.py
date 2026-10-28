import asyncio
import json

import pytest

from analyzer.core.generator import GeminiAnalyser


@pytest.fixture
def analyser():
    return GeminiAnalyser(api_key="test-key")


def fenced(data) -> str:
    return f"Here is the result:\n```json\n{json.dumps(data)}\n```"


def company(name, website="www.example.com", competitors=None):
    return {
        "company_name": name,
        "website": website,
        "competitors_analysis": {"competitors": competitors or []},
    }


class FakeModel:
    """Replaces GeminiAnalyser.generate_response and remembers every prompt."""

    def __init__(self, first_answer: str, follow_ups: dict[str, str] | None = None):
        self.first_answer = first_answer
        self.follow_ups = follow_ups or {}
        self.prompts = []

    async def __call__(self, input_text: str, find_competitors: bool = True) -> str:
        self.prompts.append(input_text)
        return self.first_answer if find_competitors else self.follow_ups.get(input_text, "")


def test_remove_square_bracket_references():
    text = "Google is a search engine [1, 2]. Founded in 1998 [3]."
    assert GeminiAnalyser.remove_square_bracket_references(text) == "Google is a search engine . Founded in 1998 ."


def test_extract_json_from_fenced_block():
    assert GeminiAnalyser.extract_all_json_objects(fenced({"a": 1})) == [{"a": 1}]


def test_extract_json_ignores_invalid_blocks():
    assert GeminiAnalyser.extract_all_json_objects("no json here {broken") == []


def test_find_companies_without_website_checks_main_companies_and_competitors():
    data = [
        company("Kaspi", website="N/A", competitors=[
            {"name": "Halyk", "website": None},
            {"name": "Freedom", "website": "freedom.kz"},
        ]),
        company("Google"),
    ]

    assert GeminiAnalyser.find_companies_without_website(data) == ["Kaspi", "Halyk"]
    assert GeminiAnalyser.find_companies_without_website(data, extract_competitors=False) == ["Kaspi"]


def test_flatten_companies_accepts_objects_and_arrays():
    blobs = [{"company_name": "A"}, [{"company_name": "B"}, "noise"], "noise"]
    assert GeminiAnalyser.flatten_companies(blobs) == [{"company_name": "A"}, {"company_name": "B"}]


def test_analysis_with_all_websites_makes_one_request(analyser, monkeypatch):
    model = FakeModel(fenced(company("Google")))
    monkeypatch.setattr(analyser, "generate_response", model)

    result = asyncio.run(analyser.get_company_analysis("Tell me about Google"))

    assert result == [company("Google")]
    assert len(model.prompts) == 1


def test_missing_websites_are_requested_once_per_company(analyser, monkeypatch):
    first = fenced(company("Kaspi", website="Unknown", competitors=[{"name": "Halyk", "website": "N/A"}]))
    model = FakeModel(first, {
        # Follow-up answers have no competitors_analysis (see COMPETITORS_SYSTEM_PROMPT)
        "Kaspi": fenced({"company_name": "Kaspi", "website": "kaspi.kz"}),
        "Halyk": fenced([{"company_name": "Halyk", "website": "halykbank.kz"}]),
    })
    monkeypatch.setattr(analyser, "generate_response", model)

    result = asyncio.run(analyser.get_company_analysis("Kaspi"))

    # One request for the analysis and one per company without a website, not one per character
    assert model.prompts == ["Kaspi", "Kaspi", "Halyk"]
    assert result[0]["website"] == "kaspi.kz"
    assert result[0]["competitors_analysis"]["competitors"][0]["website"] == "halykbank.kz"


def test_answer_as_json_array_is_not_nested(analyser, monkeypatch):
    model = FakeModel(fenced([company("Google"), company("Apple")]))
    monkeypatch.setattr(analyser, "generate_response", model)

    result = asyncio.run(analyser.get_company_analysis("Google and Apple"))

    assert [c["company_name"] for c in result] == ["Google", "Apple"]


def test_answer_without_json_returns_empty_list(analyser, monkeypatch):
    monkeypatch.setattr(analyser, "generate_response", FakeModel("Sorry, I could not find it."))

    assert asyncio.run(analyser.get_company_analysis("???")) == []
