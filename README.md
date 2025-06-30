# JobReady: Bridging the Skill Gap for Aspiring Developers

> 🚀 *A Python-based application that helps aspiring tech professionals identify skill gaps and provides personalized learning roadmaps.*

---

### 📌 Overview

**JobReady** is an innovative capstone project built as part of the **IDC 30 Days of Python Challenge (Day 30)**.  
Our goal was to create a tool that empowers junior developers, final-year students, fresh graduates, bootcampers, and career switchers by:

✅ Helping them **identify the exact skills required** for their chosen tech role  
✅ Enabling **self-assessment of current skill levels**  
✅ Providing **visual insight into skill gaps**  
✅ Generating **personalized learning roadmaps** to bridge those gaps  

---

### 💡 Problem Statement

Aspiring tech professionals often face:

- ❌ Unclear understanding of essential skills  
- ❌ Frustration from mismatched job applications  
- ❌ Lack of a focused, personalized learning plan  

**JobReady** simplifies the journey from learning to employment by offering clarity and guidance.

---

### 🛠️ Features

- **Role & Skill Selection** – Choose a tech role and rate your proficiency for required skills  
- **Skill Gap Visualization** – Instantly see where you need to improve using bar charts  
- **Personalized Roadmap** – Get concrete learning suggestions to upskill  
- **PDF Export** – Download your custom roadmap for future tracking  

---

### 🧑‍💻 Project Structure

| Part | Description | Owner |
|-------|-------------|--------|
| Part 1 | Role & skill management, self-assessment input, dynamic data handling (JSON/CSV) | Team Member 1 |
| Part 2 | Skill gap analysis logic, visualization using Matplotlib | **Suchitha Kamarapu** |
| Part 3 | Personalized roadmap generation, PDF export (FPDF/ReportLab) | Team Member 3 |

---

### ⚙️ Tech Stack

- **Python**
- **Kivy** – Cross-platform GUI
- **Matplotlib / Plotly** – Data visualization
- **FPDF / ReportLab** – PDF generation
- **JSON / CSV** – Data storage

---

### 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/YourGitHubUsername/JobReady-Skill-Gap-Analyzer.git
cd JobReady-Skill-Gap-Analyzer

# (Optional) Set up virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install required packages
pip install -r requirements.txt

# Run the app
python main.py
