# Company Analysis Telegram Bot

A system for analyzing companies using Gemini AI and providing results through a Telegram bot interface. You can find the bot at [@Company_Analyzer_Bot](https://t.me/Company_Analyzer_Bot).

## Overview

This project combines the power of Google's Gemini AI model with a Telegram bot interface to provide detailed analysis of companies. Users can send company names or descriptions to the Telegram bot, which will return structured information including:

- Company details (name, website, industry, location)
- Company description
- Key people
- Competitors analysis with strengths and comparisons

## Architecture

The project consists of two main components:

1. **Analyzer API** - FastAPI service using Google's Gemini model for company analysis
2. **Telegram Bot** - User interface for interacting with the analyzer

## Installation1

### Prerequisites

- Python 3.10+
- Docker and docker-compose (optional)

### Setup

1. Clone the repository:
```bash 
cd
```
2. Navigate to the project directory:
```bash
cd textanalyzer
```
3. Install dependencies:
```bash
pip install -e .
```
3. Configure environment variables by creating a `.env` file with your API keys:
```
GOOGLE_API_KEY=your_gemini_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```
### Running with Docker

```bash
docker-compose up --build -d
```

## Usage

### Running Locally
1. Change Network in `analyzer/constants.py` to `local`:
```python
NETWORK = "local"
```

2. Start the analyzer API:
```bash
fastapi_app
```

3. In a separate terminal, start the Telegram bot:
```bash
tg_bot
```

3. Send messages to your Telegram bot to analyze companies



## API Reference

### Analyzer API

- **Endpoint**: `/api/v1/analyse-company`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "query": "Tell me about Google"
  }
  ```
- **Response**:
  ```json
  {
    "text": [
        {
            "company_name": "Google",
            "website": "www.google.com",
            "industry": "Technology, Online Advertising, Search Engine Technology, Cloud Computing, Artificial Intelligence, Consumer Electronics",
            "location": "Mountain View, California, USA",
            "description": "Google LLC is an American multinational technology company and a subsidiary of Alphabet Inc. [1]. Founded on September 4, 1998, by Larry Page and Sergey Brin, it began as a research project at Stanford University to organize the world's information [1, 2, 13, 19]. Google is best known for its dominant search engine, handling over 70% of worldwide online search requests [2]. Beyond search, Google offers a vast array of internet services and products, including online advertising (Google Ads), cloud computing (Google Cloud Platform), mobile operating systems (Android), web browsers (Chrome), email (Gmail), online video platforms (YouTube), mapping and navigation (Google Maps), and consumer electronics (Pixel) [1, 2, 15, 16]. It is considered one of the five 'Big Tech' companies alongside Amazon, Apple, Meta, and Microsoft, and is one of the world's most valuable brands [1].",
            "key_people": [
                "Sundar Pichai (CEO)",
                "Ruth Porat (President and CIO, Alphabet and Google)",
                "Prabhakar Raghavan (Chief Technology Officer)",
                "Larry Page (Co-founder)",
                "Sergey Brin (Co-founder)"
            ],
            "competitors_analysis": {
                "competitors": [
                    {
                        "name": "Microsoft",
                        "website": "www.microsoft.com",
                        "strength": "Strong presence in cloud computing (Azure), enterprise software (Office 365), and a persistent contender in the search market (Bing), often integrating AI and machine learning into its products. [10, 17]"
                    },
                    {
                        "name": "Apple",
                        "website": "www.apple.com",
                        "strength": "Dominant in the mobile operating system market (iOS) and consumer electronics, offering a unified user experience across its hardware and software, including search capabilities via Spotlight. [10, 17]"
                    },
                    {
                        "name": "Amazon",
                        "website": "www.amazon.com",
                        "strength": "A major competitor in e-commerce, cloud computing (Amazon Web Services), and online advertising, leveraging its vast e-commerce platform and cloud infrastructure. [17]"
                    }
                ],
                "comparison": "Google maintains a near-monopoly in the online search market, with over 91% of global online search volume, significantly outpacing competitors like Microsoft's Bing. [19] Its strength lies in its advanced search algorithms and extensive ecosystem of services (Android, Chrome, YouTube, Gmail) that integrate seamlessly, driving substantial advertising revenue [2, 16, 17]. Microsoft competes directly in cloud computing and productivity software, while Apple challenges in the mobile OS and consumer hardware space through tight hardware-software integration [17]. Amazon is a key rival in cloud services and increasingly in online advertising and product search. Google's broad product portfolio and strong brand presence give it a significant competitive advantage, though it faces ongoing scrutiny regarding market dominance and data privacy. [1, 17]"
            }
        }
    ]
    }
