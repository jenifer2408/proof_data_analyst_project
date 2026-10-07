# VERITAS — Proof-Carrying AI Data Analyst

> **Don't just trust the answer. Verify it.**

VERITAS is an AI-powered data analyst designed to answer questions over messy, multi-table datasets while providing executable proof for numerical answers.

Instead of directly trusting an LLM-generated answer, VERITAS follows:

**Question → AI-generated analysis → Python execution → Independent verification → Verified Answer / Refusal**

## Problem

Traditional AI data analysts can generate convincing answers even when:

- Data contains missing values
- Duplicate records exist
- Multiple tables need to be joined
- Units or currencies differ
- Data contains invalid values
- Questions are ambiguous
- Required information is unavailable

A plausible answer is not necessarily a trustworthy answer.

## Solution

VERITAS introduces **Proof-Carrying Data Analysis**.

For supported questions, the system:

1. Understands the user's question
2. Inspects the available dataset schema
3. Generates executable Python/Pandas analysis code
4. Executes the generated code against the actual data
5. Independently recalculates the result
6. Compares both results
7. Reports the appropriate status:
   - VERIFIED
   - VERIFICATION FAILED
   - NOT VERIFIED
   - CLARIFICATION REQUIRED

> **The LLM proposes the analysis, Python executes it, and an independent verifier decides whether the result deserves to be trusted.**

## Architecture

```text
                 ┌─────────────────┐
                 │      User       │
                 │   Data Query    │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   Streamlit UI  │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   LLM Planner   │
                 │  Query → Code   │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Code Validation │
                 │ & Safe Execution│
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Python/Pandas   │
                 │   Execution     │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   Independent   │
                 │    Verifier     │
                 └────────┬────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
       ┌─────────────┐        ┌─────────────┐
       │   VERIFIED  │        │ NOT VERIFIED│
       │    Answer   │        │ / REFUSAL   │
       └─────────────┘        └─────────────┘
```

## Technology Stack

- Python
- Pandas
- NumPy
- Streamlit
- OpenAI API
- Plotly
- CSV / tabular datasets
- GitHub

## Project Structure

```text
data_analyst/
│
├── data/
│   ├── superstore.csv
│   ├── customer_ids.csv
│   └── customer_registry.csv
│
├── app.py
├── analyzer.py
├── agent.py
├── executor.py
├── verifier.py
├── profiler.py
├── extract_ids.py
├── create_registry.py
├── ai_test.py
├── audit_rules.txt
├── requirements.txt
├── .gitignore
└── README.md
```

## Demo Dataset

VERITAS includes a built-in demonstration dataset consisting of:

### 1. Superstore Transaction Data

Contains fields such as:

- Customer ID
- Sales
- Quantity
- Discount
- Profit
- Region
- Order Date
- Ship Date
- Category

### 2. Customer Registry

Contains:

- Customer ID
- Risk Level
- Verification Date
- Currency Unit
- Audit Status

The customer registry is **synthetic hackathon enrichment data** created to demonstrate multi-table reasoning, risk filtering, and currency normalization.

## Data Quality Handling

The demo dataset intentionally contains data-quality issues.

VERITAS detects and handles:

- Missing Customer IDs
- Missing Sales values
- Duplicate records
- Negative quantities
- Missing registry information
- Unsupported currencies
- Ambiguous questions
- Insufficient information

Example demo observations:

```text
Missing Customer IDs : 6
Missing Sales        : 4
Duplicate rows       : 8
Negative Quantity    : 5
```

## Currency Normalization

The demo uses the operational audit rule:

```text
1 EUR = 1.12 USD
```

USD transactions remain unchanged.

```text
USD → × 1.00
EUR → × 1.12
```

The conversion is represented in the executable proof and independent verification.

This is a **fixed operational rate for the hackathon demo**, not a live exchange-rate feed.

## Audit Rules

VERITAS follows the rules defined in `audit_rules.txt`.

### Currency Conversion

EUR transactions are converted to USD using:

```text
1 EUR = 1.12 USD
```

### High-Risk Customers

High-risk customers are excluded from corporate financial liability summaries.

### Missing Customer ID

Transactions without a Customer ID are excluded from customer-level financial aggregation.

### Missing Sales

Transactions with missing Sales values are excluded from revenue calculations.

### Duplicate Records

Duplicate transaction records are identified before aggregation.

### Negative Quantity

Negative quantities are treated as data-quality issues and are not automatically considered valid sales.

### Ambiguous Questions

If the question does not clearly specify the required interpretation, VERITAS asks for clarification.

### Insufficient Information

If the required information is not available, VERITAS refuses to provide an unsupported numerical answer.

## Example Queries

### Basic Analysis

```text
What is the total sales?
```

### Maximum / Minimum

```text
What is the maximum sales?
```

```text
What is the minimum sales?
```

### Group Analysis

```text
Which region has the highest total sales?
```

### Multi-Table Analysis

```text
How much total Sales would be excluded from corporate financial liability summaries because the customers are classified as High risk?
```

For this query, VERITAS:

1. Loads transaction data
2. Loads the customer registry
3. Joins both datasets using Customer ID
4. Identifies high-risk customers
5. Removes invalid records
6. Applies currency normalization
7. Calculates the amount
8. Independently verifies the result

## Ambiguity Handling

VERITAS does not automatically guess when a question is ambiguous.

For example:

```text
What was the highest sales?
```

This could mean:

- Highest individual transaction
- Highest regional sales
- Highest product sales
- Highest customer sales

Instead of choosing an arbitrary interpretation, VERITAS can ask the user to clarify.

## Refusal Capability

VERITAS can refuse to provide an unsupported numerical answer.

For example:

```text
What is the profit margin?
```

If the required information is not reliably available, the system should not invent a value.

The appropriate result is:

```text
NOT VERIFIED / INSUFFICIENT INFORMATION
```

## Code Safety

Generated code is checked before execution.

The prototype blocks potentially dangerous operations such as:

```text
import
from
os.
sys.
subprocess
eval()
exec()
open()
```

The execution environment also exposes a restricted set of built-in functions.

> Note: This is a hackathon prototype safety layer and is not intended to be a production-grade sandbox.

## Verification Pipeline

A key distinction is:

```text
Code executed successfully
        ≠
Answer is logically verified
```

VERITAS performs an independent calculation whenever a deterministic verifier is available.

Example:

```text
AI Generated Result:
9447.6932

Independent Result:
9447.6932

Difference:
0.0

Status:
VERIFIED
```

If the values differ:

```text
AI Result:
9447.6932

Independent Result:
269250.47

Status:
VERIFICATION FAILED
```

The system does not silently accept the AI result.

## Custom Dataset Support

Users can upload CSV files through the Streamlit interface.

VERITAS can inspect the uploaded schema and generate analysis code based on the available columns.

Supported deterministic operations include common tasks such as:

- SUM
- MEAN / AVERAGE
- MIN
- MAX
- COUNT
- UNIQUE COUNT
- ROW COUNT

For unsupported complex analyses, the system can display:

```text
NOT VERIFIED
```

instead of pretending that the result has been independently validated.

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd data_analyst
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

On Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## API Key Setup

Set your OpenAI API key as an environment variable.

Windows CMD:

```cmd
set "OPENAI_API_KEY=YOUR_API_KEY"
```

Do **not** commit the API key to GitHub.

## Run the Application

```bash
streamlit run app.py
```

Then open the Streamlit URL shown in the terminal.

## Running Individual Components

Dataset profiler:

```bash
python profiler.py
```

Extract customer IDs:

```bash
python extract_ids.py
```

Create customer registry:

```bash
python create_registry.py
```

Run the AI agent:

```bash
python agent.py
```

Run analyzer:

```bash
python analyzer.py
```

Run executor:

```bash
python executor.py
```

Run verifier:

```bash
python verifier.py
```

## Sample Workflow

```text
User:
"What is the total sales?"

        ↓

LLM generates Pandas proof

        ↓

Proof executes on actual dataset

        ↓

Independent verifier recalculates

        ↓

AI Result = calculated value
Verifier Result = independently calculated value

        ↓

VERIFIED / FAILED / NOT VERIFIED
```

## Key Innovation

### Proof-Carrying Answers

Instead of returning only:

```text
Total Sales = <value>
```

VERITAS provides:

```text
Answer
   +
Executable Proof
   +
Data Evidence
   +
Verification Status
```

This allows the user or judge to inspect how the answer was produced and whether it was independently verified.

## Why VERITAS?

Traditional AI systems often optimize for:

> "Give me an answer."

VERITAS focuses on:

> **"Give me an answer that I can reproduce and verify."**

## Limitations

Current prototype limitations include:

- Primarily designed for CSV/tabular data
- Independent verification currently supports selected deterministic operations
- Complex analyses may return `NOT VERIFIED`
- The code execution safety mechanism is prototype-level
- The demo customer registry is synthetic
- Currency conversion uses a fixed operational rate rather than live market data

## Future Enhancements

Possible future improvements:

- Stronger sandboxed code execution
- Support for Excel, PDF and document data
- More advanced multi-table reasoning
- Automatic verifier generation
- Query planning using an agent graph
- Rich visualizations
- Provenance graphs
- More comprehensive contradiction detection
- Human approval workflows
- Production-grade security isolation

## Team

**Project:** VERITAS — Proof-Carrying AI Data Analyst

**Hackathon:** Karunya Institute of Technology and Sciences

**Problem Statement:** PSI08 — Proof-Carrying Data Analyst (Agentic GenAI)

## Disclaimer

This project is a hackathon prototype created for demonstration and evaluation purposes.

The synthetic customer registry and operational audit rules are designed specifically to demonstrate multi-table reasoning, data-quality handling, currency normalization, and verification.

## Core Principle

> **Don't just trust the answer. Verify it.**
