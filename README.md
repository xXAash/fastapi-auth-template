# Money App – Personal Financial Tracker

## Overview

Money App is a modular, microservice-based application designed to help users gain control over their finances by tracking:

- Spending and income
- Savings goals and automatic transfers
- Investment accounts (e.g., Roth IRA, 401k)
- Debts and loan payments
- Credit card usage, rewards, and due dates

The app prioritizes simplicity, clarity, and security, and is built with scalability in mind.

---

## Architecture

- **Frontend:** React
- **Backend:** Python (FastAPI)
- **Structure:**
```
/frontend         - React client  
/microservices    - Auth, savings, debt, investments, creditcards  
/shared           - Shared schemas and configuration  
/docs             - Wireframes and planning notes
```
  
---

## Current Status

- Project structure initialized
- README drafted
- Auth and frontend scaffolding in progress
- Sprint 2 will focus on implementing the Cash Accounts section

Project progress is tracked using a GitHub Project Board.

---

## Sprint 1 Goals

- Set up project folders and shared files
- Scaffold the FastAPI authentication microservice
- Initialize the React frontend
- Define transaction schema and bank link mappings
- Organize planning documentation

---

## Developer Setup

### Requirements

- Python 3.10+
- Node.js + npm
- (Optional) Virtualenv or Pipenv for backend setup

### Running the Project

**Frontend:**
```bash
cd frontend
npm install
npm start
```

**Backend:**
```bash
cd microservices/auth


pip install -r requirements.txt
uvicorn main:app --reload
```
