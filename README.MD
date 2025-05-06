# Compliance Reasoning Agent

This repository provides a **Contract Compliance & Risk Evaluation** tool built with Streamlit and Azure OpenAI. The application allows users to upload vendor agreements and corporate compliance policies in PDF format, analyze them for compliance, and evaluate associated risks.

## Features

1. **Clause Extraction**: Extracts sections related to Data Protection, Audit Rights, Anti-Corruption, and ESG from vendor agreements.
2. **Compliance Mapping**: Maps extracted clauses to corporate compliance policies and identifies met/not-met areas.
3. **Risk Evaluation**: Assigns risk levels (Low, Medium, High) for each compliance area and highlights ambiguous clauses or missing details.

## Prerequisites

- Python 3.9 or higher
- Azure OpenAI resource with a deployed chat model
- Docker (optional, for containerized deployment)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/compliance-reasoning-agent.git
cd compliance-reasoning-agent
```

### 2. Create a Virtual Environment
Create and activate a virtual environment:

On Windows
```
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:
```
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
Install the required Python packages:
```
pip install --upgrade pip
pip install -r 
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory based on the provided `.env.sample` file:
```
AZURE_OPENAI_ENDPOINT=https://<OPEN-AI-RESOURCE>.openai.azure.com/
AZURE_OPENAI_API_KEY=<YOUR-API-KEY>
AZURE_OPENAI_CHAT_DEPLOYMENT=<MODEL-NAME>
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

### 5. Run the Application
Start the Streamlit application:
```
streamlit run src/complaince_analysis.py
```