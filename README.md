# YORU Terminal

**A Shinobi-Inspired Cybersecurity Training Simulator**

YORU Terminal is a local, menu-driven cybersecurity training game built with Python. Inspired by the stealth and discipline of a hidden shinobi clan, it lets players practice cybersecurity concepts through interactive missions, investigate simulated threats, and develop their security decision-making skills.

> **Infiltrate. Analyze. Adapt.**

## Features

- **User Authentication** — Account registration and login with Argon2 password hashing.
- **Phishing Detective** — Examine suspicious messages and identify phishing indicators.
- **Log Investigator** — Analyze simulated system logs and investigate unusual activity.
- **Security Puzzle Room** — Practice encoding concepts, password security, and exposed-secret response.
- **Incident Response Simulator** — Make decisions during simulated security incidents.
- **XP and Ranking System** — Earn experience and progress through operator ranks.
- **Mission History** — Review previous attempts, scores, completion status, and XP earned.
- **Tactical Terminal Interface** — Rich-powered terminal styling with a Hidden Clan identity.
- **Windows Launcher** — Start the application using `YORU.bat`.
- **Automated Tests** — A pytest suite covering core functionality and mission behavior.

## Technology Stack

- **Language:** Python
- **Terminal Interface:** Rich
- **Database:** SQLite
- **Password Hashing:** Argon2
- **Testing:** pytest
- **Platform:** Windows (with a Python environment)

## Requirements

- Python 3.11 or newer recommended
- Git (optional, for cloning the repository)
- Windows Command Prompt or PowerShell

## Getting Started

### 1. Clone the repository

After this project is published on GitHub, replace the placeholder below with the repository URL:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd YoruTerminal
```

Alternatively, download the repository as a ZIP and extract it.

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the virtual environment's Python directly:

```powershell
.\.venv\Scripts\python.exe --version
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Launch YORU Terminal

**Option A — Tactical Launcher**

Double-click `YORU.bat` and select **1** to initialize a training session.

**Option B — PowerShell**

```powershell
python main.py
```

Follow the on-screen prompts to register or log in and access the training missions.

## Mission Overview

| Mission | Focus |
|---|---|
| Phishing Detective | Identify suspicious messages and phishing indicators |
| Log Investigator | Interpret logs and recognize unusual access |
| Security Puzzle Room | Explore encoding, password safety, and exposed secrets |
| Incident Response Simulator | Practice containment, investigation, and recovery decisions |

## Progression System

Players receive scores based on their answers and can use hints at a scoring cost. XP is awarded for a mission's first completion, and accumulated XP determines the player's rank.

Mission attempts and progression are stored in a local SQLite database.

## Running Tests

Run the test suite from the project root:

```powershell
python -m pytest -q
```

The project currently has **101 passing tests** in the development environment. Results may vary if the code or environment changes.

## Project Structure

```text
YoruTerminal/
├── auth/          # Authentication logic
├── core/          # Game engine, sessions, and progression
├── database/      # SQLite connection and schema
├── missions/      # Mission content and registry
├── tests/         # Automated tests
├── ui/            # Terminal interface and menus
├── main.py        # Application entry point
├── YORU.bat       # Windows tactical launcher
├── requirements.txt
├── .gitignore
└── README.md
```

The application creates its local database under `data/` when initialized. The database contains local application data and should not be committed to the public repository.

## Learning and Safety

YORU Terminal is an educational simulator. Its missions use simulated scenarios to teach cybersecurity concepts and defensive decision-making.

It is not a replacement for professional security training, and it does not authorize testing systems you do not own or have permission to assess.

## Current Release

**Target release:** v1.0.0

This release focuses on the core terminal experience, four interactive missions, account authentication, player progression, mission history, and automated testing.

## Author

YoruTerminal is a personal project that I genuinely enjoy working on as a cybersecurity student. I wanted to build something that combines my interest in cybersecurity, programming, and terminal-based applications into an interactive learning experience.

This project is also a way for me to challenge myself, strengthen my Python development skills, and explore how cybersecurity concepts can be turned into engaging missions. I'm building YoruTerminal step by step, learning along the way, and improving it as I gain more experience.

For me, YoruTerminal is more than just a portfolio project. It's a passion project that reflects my curiosity, creativity, and commitment to growing in cybersecurity.

---

*YORU Terminal — Enter the night. Sharpen your instincts.*