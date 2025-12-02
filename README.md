# SustiAI – AI Partner for Carbon-Conscious Events

## Overview
SustiAI is a **multi-agent AI system** built using **Google AI Agent Development Kit (ADK)** and powered by **Gemini models**. It helps companies analyze, report, and reduce the carbon footprint of their **corporate events**. The system stores event-related data and carbon accounting per event, enabling **comparisons across events, benchmarking, and trend analysis over time**.

---

## Problem
Companies hosting events struggle to:
- Understand and manage **carbon emissions** across multiple events.
- Generate **customized compliance reports** for different stakeholders.
- Plan future events with **predictive sustainability insights**.
- Avoid high costs of hiring sustainability consultants.

---

## Solution
SustiAI solves these challenges by:
- **Automating carbon footprint analysis** for single or multiple events.
- **Generating branded, stakeholder-specific reports** aligned with GHG Protocol and ISO standards.
- **Providing predictive recommendations** for future events.
- **Enabling benchmarking and offset integration** for ESG compliance.

---

## Key Features
- **Multi-event analysis** and comparison across years.
- **Customizable HTML reports** for organizers, sponsors, vendors, and compliance teams.
- **Predictive modeling** for smarter event planning.
- **Offset calculation and integration** with verified providers.

---

## Architecture
SustiAI uses an **Agentic AI architecture** built on **Google ADK** and **Gemini**:

### Core Components
- **Multi-Agent System**:
  - **LLM-powered Agent** for report generation and insights.
  - **Sequential Agents** for data collection → analysis → reporting → storage.
- **Tools**:
  - **MCP (Model Context Protocol)** for multi-event analysis and customization.
  - **Custom tools** for emissions calculations and benchmarking.
  - **Built-in tools** like **Code Execution** for dynamic computations.
- **Sessions & Memory**:
  - **InMemorySessionService** for state management across agent interactions.
- **Observability**:
  - Logging, tracing, and metrics for monitoring agent performance.
- **Agent Evaluation**:
  - Continuous evaluation for accuracy and quality of generated reports.

---

## Tech Stack
- **Google ADK** for agent orchestration.
- **Gemini LLM** for natural language processing and report generation.
- **Python** for backend logic.
- **HTML/CSS** for interactive report outputs.

---

## Setup Instructions
### Prerequisites
- Python 3.9+
- Google ADK installed
- Git
- Virtual environment (recommended)

### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/dollyagarwal/sustiAI.git
   cd sustiAI
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Google ADK & Gemini**
   - Set up your API keys and environment variables in `.env` (GOOGLE_API_KEY)

5. **Run the application**
   ```bash
   python main.py
   ```

---

## Usage
1. **Create the database**:
   - Execute `ddl.sql` to create the schema.
   - Execute `mockdata.sql` to populate mock data.

2. **Run the main application**:
   ```bash
   python main.py
   ```

3. **Call the API to generate reports**:
   - Use the `run_agent_report` API endpoint with your query.
   - The API will return an **HTML response** containing the report.


## Future Enhancements
- Reflection loop for continuous improvement.
- Integration with carbon offset providers.
- Advanced predictive modeling for event planning.



## Sample Reports

### 1. EcoSphere Ltd (company_id = 3)
**Query:** Compare carbon emissions across multiple events of the same type for EcoSphere Ltd, broken down by GHG Scope and category.

**Generated Report:**
[View Full Report](assets/ecosphere-report.html)

**Why Insightful:**
- Shows trends across years for recurring events (e.g., Tech Expo 2024 vs 2025).
- Highlights scope-wise and category-wise contributions.
- Enables benchmarking and predictive insights.
---

### 2. BlueSky Corp (company_id = 1)
**Query:** Compare emissions per attendee across all events for BlueSky Corp, grouped by category and scope.

**Generated Report:**
[View Full Report](reports/bluesky-report.html)

**Why Insightful:**
- Shows carbon intensity per attendee, a key sustainability KPI.
- Enables benchmarking across event types (Product Launch vs Sustainability Summit).


**Disclaimer:** The data used in this codebase is mocked for demo purposes. The mock data was generated using LLM.
