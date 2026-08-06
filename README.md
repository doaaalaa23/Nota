<div align="center">

# 💳 Nota — Installment Management System

**Manage clients, products, and installment contracts — all in one place.**

Track balances automatically, gate contract creation on available capital, and watch your business health on a live dashboard.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

[![Status](https://img.shields.io/badge/status-active-success?style=flat-square)](.)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](.)

</div>

---

## 📖 About

**Nota** replaces messy manual spreadsheets with a single, consistent system for businesses that sell on installment plans. Add clients and products, create contracts, record payments, and let Nota automatically track your balance — increasing it as clients pay, and decreasing it whenever a new contract is funded. A built-in balance check stops you from over-committing capital you don't have.

> 📌 **Note:** Filtration is out of scope for this version. Search is available for clients and products only.

---

## ✨ Features

- 🔐 **Secure Authentication** — sign up and log in with validated, hashed credentials
- 👥 **Client Management** — add, edit, delete, and view client records
- 📦 **Product Management** — add, edit, delete, and view product records
- 🔍 **Search** — quickly find clients and products
- 💰 **Smart Balance Tracking** — set your balance at sign-up, top it up anytime
- 📄 **Contract Management** — link clients and products into installment contracts
- 🚦 **Balance Gate** — contracts are only created if your balance can cover them
- 💵 **Payments** — record client payments against contracts, balance updates instantly
- 📊 **Live Dashboard** — sales, collections, remaining amounts, due/overdue installments, monthly profit, and expected income at a glance

---

## 🖼️ Screenshots

<div align="center">

### 🏠 Home Page
<img src="screenshots/home_page.PNG" alt="Home Page" width="800"/>

### 📊 Dashboard
<img src="screenshots/dashboard.PNG" alt="Dashboard" width="800"/>

### ➕ Create Client
<img src="screenshots/create_client.PNG" alt="Create Client" width="800"/>

### 💰 Balance
<img src="screenshots/balance.PNG" alt="Balance" width="800"/>

</div>

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, FastAPI |
| **Database** | Supabase (PostgreSQL) |
| **Frontend** | HTML, CSS, JavaScript |
| **Deployment** | Cloud-hosted |

---

## 📂 Project Documentation

Full project documentation lives in the [`docs/`](docs) folder:

| Document | Description |
|---|---|
| 📃 [`Nota_Brief.pdf`](docs/Nota_Brief.pdf) | Project brief — purpose, problem statement, and proposed solution |
| 📋 [`Nota_BRD.pdf`](docs/Nota_BRD.pdf) | Business Requirements Document — objectives, scope, KPIs, and timeline |
| 🧩 [`Nota_PRD.pdf`](docs/Nota_PRD.pdf) | Product Requirements Document — user stories, functional & non-functional requirements |
| 🗂️ [`Nota_action_plan.pdf`](docs/Nota_action_plan.pdf) | Hierarchical action plan — epics, stories, and tasks |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- A [Supabase](https://supabase.com/) project (URL + API key)
- pip / virtualenv

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/nota.git
cd nota

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_api_key
SECRET_KEY=your_secret_key
```

### Run Locally

```bash
uvicorn main:app --reload
```

The app will be available at `http://127.0.0.1:8000` 🎉

---

## ☁️ Deployment

Nota is deployed and ready for production use. Update the badge/link below with your live URL:

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen?style=for-the-badge&logo=vercel&logoColor=white)](https://your-deployment-url.com)

---

## 🗺️ Roadmap

- [ ] Filtration mechanism
- [ ] Due-date notifications
- [ ] Client-facing external access
- [ ] Online/external payment processing

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](../../issues) or open a pull request.

---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

Made with ❤️ for business owners who deserve better than spreadsheets.

</div>
