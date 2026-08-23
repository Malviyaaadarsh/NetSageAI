# NetSage AI

NetSage AI is an AI-assisted troubleshooting helper for Cisco Packet Tracer and lab network problems. It combines deterministic rule checks with Google Gemini diagnosis and requires human review before a diagnosis or fix is accepted.

## Features

- Troubleshooting cases covering VLANs, routing, DHCP, DNS, ACLs, NAT, OSPF, and wireless networks
- Deterministic checks for common configuration issues
- Google Gemini-powered diagnostic suggestions
- Structured diagnosis output:
	- Root cause
	- OSI layer
	- Confidence
	- Evidence
	- Next diagnostic command
	- Suggested fix steps
- Mandatory human review workflow with Accepted, Edited, and Rejected decisions
- CSV and Markdown audit logging
- Dashboard showing issue types, severity, and AI-human agreement

## Prerequisites

- Python 3.9 or later
- Git
- pip
- A Google Gemini API key

## Installation

Clone the repository:

```bash
git clone <https://github.com/Malviyaaadarsh/NetSageAI.git>
cd NetSageAI
```

Create a Python virtual environment:

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
python -m venv venv
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configure Gemini

Create the Streamlit secrets directory:

```text
.streamlit/
```

Create a file named `.streamlit/secrets.toml` with the following contents:

```toml
GEMINI_API_KEY = "your-gemini-api-key"
GEMINI_MODEL = "gemini-3.5-flash-lite"
```

Replace `your-gemini-api-key` with your actual Google Gemini API key.

> The application currently reads `GEMINI_MODEL` in `src/engine.py`. Use the singular variable name `GEMINI_MODEL`, not `GEMINI_MODELS`.

The `.streamlit/secrets.toml` file is excluded from Git to prevent accidentally committing credentials.

## Run the Application

From the repository root, start the Streamlit dashboard:

```bash
streamlit run src/app.py
```

Streamlit will display a local URL:

```text
http://localhost:8501
```

Open the URL in a browser.

## How It Works

1. Select a troubleshooting case from the Case Explorer.
2. Review the symptom, topology note, and captured show-command output.
3. Select **Run Hybrid Diagnosis**.
4. NetSage AI runs deterministic checks using `src/checker.py`.
5. The application sends the case evidence to Gemini using the structured prompt in `prompts/diagnose_prompt.md`.
6. The deterministic result and Gemini response are merged into a final diagnosis.
7. Review the diagnosis and proposed CLI steps.
8. Select one of the required human review decisions:
	 - **Accepted**
	 - **Edited**
	 - **Rejected**
9. Save the review decision to record the result in the audit files.

The application does not automatically deploy configuration changes to a network device.

## Gemini Fallback Behavior

If `GEMINI_API_KEY` is not configured or the Gemini request fails, the application falls back to the deterministic rule checker.
The dashboard displays a warning when this fallback is used. Gemini is recommended for cases that do not match a deterministic rule.

## Project Structure

```text
NetSage_AI/
├── data/
│   ├── cases.csv              # Troubleshooting case dataset
│   └── review_log.csv         # Structured human review records
├── docs/
│   └── audit_logs.md          # Human review audit log
├── prompts/
│   └── diagnose_prompt.md     # Gemini diagnosis prompt and output schema
├── src/
│   ├── app.py                 # Streamlit dashboard
│   ├── checker.py             # Deterministic troubleshooting rules
│   └── engine.py              # Gemini integration and diagnosis orchestration
├── requirements.txt           # Python dependencies
└── README.md
└── main.pkt                   # Packet Tracer lab file with few troubleshooting cases
```

## Deterministic Rule Checks

The rule checker identifies common issues such as:

- Administratively down interfaces
- DHCP pool exhaustion
- DNS misconfiguration
- ACL blocking required traffic
- NAT or PAT configuration errors
- Trunk and VLAN mismatches
- Default gateway and subnet mismatches
- OSPF and routing configuration problems
- Duplicate IP addresses
- Missing DHCP relay configuration

## Review and Audit Data

Review decisions are stored in:

```text
data/review_log.csv
docs/audit_logs.md
```

The dashboard calculates:

- Total reviews
- Accepted diagnoses
- Edited diagnoses
- Rejected diagnoses
- AI-human agreement rate
- Severity distribution
- Issue type distribution
- Recent human overrides

To add five demonstration correction records for the Responsible AI workflow, click **Seed 5 demo correction logs** in the dashboard sidebar.

