Manufacturing Advisor Agent
Overview

Manufacturing Advisor Agent is an AI-powered manufacturing operations assistant built using:

Pega A2A (planned integration)
Python
Flask
SQLite
Ollama
Llama 3.1

The solution analyzes manufacturing operational data and provides intelligent recommendations related to:

Production performance
Quality issues
Maintenance risks
Operational risk assessment

The objective is to demonstrate how enterprise AI agents can leverage structured operational data and local LLMs to assist supervisors in making informed decisions.

Business Scenario

Manufacturing organizations often struggle with siloed operational data.

Different teams monitor different aspects of the factory:

Production Team
Production targets
Actual output
Capacity utilization
Quality Team
Defect rates
Scrap rates
Rework
Maintenance Team
Machine condition
Temperature
Vibration
Runtime

This makes it difficult to identify root causes and proactively address operational risks.

The Manufacturing Advisor Agent consolidates these perspectives and provides AI-generated recommendations.

Solution Architecture
Factory Supervisor
        |
        v

Manufacturing Advisor API
        |
        v

Flask
        |
        v

Advisor Service
        |
   --------------------
   |        |         |
Production Quality Maintenance
   Tool      Tool       Tool
        |
        v

SQLite Database
        |
        v

Business Calculations
        |
        v

Ollama (Llama 3.1)
        |
        v

AI Recommendations

Key Design Principles
Python Calculates

Business calculations are performed in Python.

Examples:

Production rate
Projected output
Production gap
Days since maintenance
AI Explains

The LLM receives calculated facts and generates:

Root cause analysis
Recommendations
Risk assessments
Business summaries

This approach improves consistency and avoids arithmetic errors.

Technology Stack
Frontend
--------
Future Pega Integration

Backend
-------
Python
Flask

Database
--------
SQLite

AI
--
Ollama
Llama3.1:8b

Architecture
------------
Manufacturing Advisor Agent

Database Design
ProductionStatus
Field	DescriptionLineID	Production Line
TargetProduction	Daily Target
CurrentProduction	Current Output
HoursElapsed	Hours Completed
HoursRemaining	Hours Left
ShiftHours	Shift Duration
MachineUtilization	Utilization Percentage
QualityMetrics
Field	DescriptionLineID	Production Line
DefectRate	Defect Percentage
ScrapRate	Scrap Percentage
ReworkRate	Rework Percentage
MachineHealth
Field	DescriptionMachineID	Machine Identifier
Temperature	Current Temperature
Vibration	Vibration Level
RuntimeHours	Runtime Hours
LastMaintenanceDate	Last Maintenance Date
Current Demo Data
Production
Metric	ValueTarget Production	15,000
Current Production	8,500
Projected Production	12,750
Production Gap	2,250
Quality
Metric	ValueDefect Rate	4.2%
Scrap Rate	1.8%
Rework Rate	2.6%
Maintenance
Metric	ValueMachine	CNC101
Temperature	92°C
Vibration	HIGH
Runtime Hours	460
Days Since Maintenance	22
Root Cause Storyline

The demo data follows a connected business scenario.

CNC101
High Vibration
        |
        v

Quality Degradation
(Defects Increase)
        |
        v

Production Impact
(Target At Risk)
        |
        v

Business Risk


This allows cross-domain risk analysis instead of isolated insights.

Project Structure
ManufacturingAdvisorAgent
│
├── app.py
├── factory.db
├── database_setup.py
├── seed_data.py
├── llm_service.py
│
├── tools
│   ├── production_tool.py
│   ├── quality_tool.py
│   └── maintenance_tool.py
│
├── services
│   ├── advisor_service.py
│   └── factory_risk_analyzer.py
│
├── tests
│
├── prompts
│
├── docs
│
├── README.md
└── requirements.txt

Setup Instructions
1. Create Virtual Environment
python -m venv venv


Activate:

venv\Scripts\activate

2. Install Dependencies
pip install -r requirements.txt

3. Start Ollama
ollama serve

4. Verify Model Availability
ollama list


Expected model:

llama3.1:8b

5. Create Database
python database_setup.py

6. Load Sample Data
python seed_data.py

7. Start Application
python app.py

API Endpoints
Health Check
GET /health


Example:

curl http://localhost:5000/health


Response:

{
  "service": "Manufacturing Advisor",
  "status": "UP"
}

Analyze Manufacturing Question
POST /analyze


Request:

{
  "question": "biggest operational risk"
}


Response:

{
  "question": "biggest operational risk",
  "response": "Machine failure risk identified..."
}

Sample Questions
production status

quality analysis

maintenance health

biggest operational risk

Current Status
Completed
SQLite database
Production analysis
Quality analysis
Maintenance analysis
Factory risk analysis
Ollama integration
Flask API
Health endpoint
Future Roadmap
Phase 2
Pega A2A Integration
Agent Card
JSON-RPC message/send
ngrok exposure
Pega Agent registration
Phase 3
Multi-Agent Architecture
Production Agent
Quality Agent
Maintenance Agent
Phase 4
Pega Case Creation
Corrective Actions
Supervisor Approval Workflow
Author

Piyush Sinha
 Associate Director - Technology
 Pega Lead System Architect

Disclaimer

This project uses synthetic manufacturing data for demonstration and learning purposes only. No real manufacturing data is included.