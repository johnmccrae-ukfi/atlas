# Atlas Enterprise AI Intelligence Platform

## Installation Guide

This document explains how to install, configure and run the Atlas Enterprise AI Intelligence Platform development environment.

The project has been developed primarily on **Windows 11**, **Microsoft Fabric**, **Visual Studio Code** and **Python 3.12**.

Linux and macOS equivalents are included where appropriate.

---

# 1. Prerequisites

Before cloning the repository, ensure the following software is installed.

| Component | Recommended Version |
|-----------|--------------------|
| Windows 11 / macOS / Linux | Current |
| Python | 3.12 or later |
| Git | Latest |
| Visual Studio Code | Latest |
| Microsoft Fabric Workspace | Required |
| GitHub Account | Required |

---

# 2. Clone the Repository

Clone the repository from GitHub.

```bash
git clone https://github.com/<your-account>/atlas-trading-intelligence.git
```

Change into the project directory.

```bash
cd atlas-trading-intelligence
```

---

# 3. Create a Python Virtual Environment

## Windows

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

## Linux / macOS

```bash
python3 -m venv .venv
```

Activate

```bash
source .venv/bin/activate
```

---

# 4. Install Python Dependencies

Install the local development packages.

```bash
pip install -r requirements.txt
```

Verify installation.

```bash
pip list
```

---

# 5. Open the Project in Visual Studio Code

Open the repository.

```bash
code .
```

Select the newly created virtual environment as the Python interpreter.

Typical interpreter:

```
.venv
```

---

# 6. Recommended VS Code Extensions

The following extensions are recommended.

- Python
- Pylance
- Jupyter
- GitHub Pull Requests
- GitLens
- Rainbow CSV
- Markdown All in One
- Mermaid Markdown Syntax Highlighting
- SQLTools (optional)

---

# 7. Microsoft Fabric Setup

The repository uses Microsoft Fabric Git integration.

Create or connect to a Fabric workspace.

Connect Source Control to the **dev** branch.

Synchronise the workspace.

The Fabric artefacts are stored in the `/fabric` directory.

These include:

- Lakehouse
- Notebooks
- Semantic Model
- Power BI Report

---

# 8. GitHub Development Workflow

Development follows a Git Flow style workflow.

```
Feature Development

        │

        ▼

    dev branch

        │

        ▼

 Pull Request

        │

        ▼

   main branch

        │

        ▼

 Release Tag

        │

        ▼

 Sync dev
```

All development should occur in the **dev** branch.

The **main** branch contains stable releases only.

---

# 9. Environment Variables

Copy the example environment file.

```
.env.example
```

Create

```
.env
```

Populate any required configuration values before running local scripts.

Sensitive credentials should never be committed to source control.

---

# 10. Repository Structure

```
fabric/
    Microsoft Fabric artefacts

src/
    Application source code

scripts/
    Local development utilities

docs/
    Project documentation

images/
    Screenshots and diagrams

tests/
    Unit tests

README.md
    Project overview

INSTALLATION.md
    Installation guide
```

---

# 11. Verifying the Installation

The following checks confirm a successful setup.

✔ Python virtual environment activates successfully

✔ Dependencies install without errors

✔ Repository opens correctly in VS Code

✔ Microsoft Fabric workspace synchronises successfully

✔ Local scripts execute without import errors

---

# 12. Known Limitations

The AI inference notebooks currently target Microsoft Fabric AI Functions.

Fabric Trial capacities (for example **FTL64**) do not currently support AI Functions and return:

```
403 Forbidden

PERMISSION_DENIED

SKU Not Supported
```

This is a Microsoft Fabric capacity limitation rather than a software defect.

The project captures these failures gracefully within the AI metadata tables.

---

# 13. Notes for Fabric Trial Users

The remainder of the platform can be executed successfully using a Fabric Trial workspace.

Only the AI inference stage is affected by current Trial capacity limitations.

All deterministic processing remains fully functional, including:

- Bronze ingestion
- Silver transformation
- Gold analytics
- Direct Lake Semantic Model
- Power BI reporting

---

# 14. Troubleshooting

## Virtual environment cannot be activated

Ensure Python is installed and available on the system PATH.

---

## Fabric artefacts do not appear

Verify that Source Control is connected to the **dev** branch and perform a synchronisation.

---

## Missing Python modules

Re-run:

```bash
pip install -r requirements.txt
```

---

## AI commentary returns permission errors

This is expected when using unsupported Fabric Trial capacities.

Refer to the Known Limitations section above.

---

# 15. Next Steps

Once installation has been completed, refer to the project README for:

- Platform architecture
- Data flow
- AI architecture
- Documentation
- Release history
- Future roadmap

Happy building!