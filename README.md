# PakWallet

PakWallet is a Streamlit-based MVP digital wallet for Pakistan.

Tagline: **Your Smart Financial Companion**

## Features

- Wallet dashboard with balance, income, expenses, savings rate, health score, recent transactions, and upcoming bills
- Financial calculators for mutual funds, home loans, car financing, child education, Zakat, and freelancer tax
- Savings goals for emergency fund, Hajj, and education planning
- Mock bill payments for electricity, gas, internet, and school fees
- Rule-based AI Budget Assistant
- Analytics with monthly reports, expense breakdown, savings trend, and net worth tracker
- SQLite database with SQLAlchemy models
- Login, bcrypt password hashing, session management, OTP placeholder, and transaction PIN placeholder

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── .streamlit/
│   └── config.toml
└── pakwallet/
    ├── components/
    │   └── ui.py
    ├── pages/
    │   ├── analytics_page.py
    │   ├── assistant.py
    │   ├── bills.py
    │   ├── calculators.py
    │   ├── dashboard.py
    │   ├── savings.py
    │   └── security.py
    ├── services/
    │   ├── auth.py
    │   └── database.py
    └── utils/
        ├── analytics.py
        ├── calculators.py
        └── formatting.py
```

## Local Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create an environment file.

```bash
cp .env.example .env
```

4. Run the app.

```bash
streamlit run app.py
```

Demo login:

```text
Email: demo@pakwallet.pk
Password: PakWallet@123
```

## Streamlit Cloud Deployment

### 1. Create a GitHub repository

1. Go to GitHub and create a new repository named `pakwallet`.
2. Keep it public or private based on your preference.
3. Do not add a README from GitHub if you are uploading this folder as-is.

### 2. Upload code to GitHub

From the project folder:

```bash
git init
git add .
git commit -m "Initial PakWallet MVP"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/pakwallet.git
git push -u origin main
```

### 3. Connect GitHub to Streamlit Cloud

1. Open [Streamlit Cloud](https://streamlit.io/cloud).
2. Sign in with GitHub.
3. Select **New app**.
4. Choose the `pakwallet` repository.
5. Set branch to `main`.
6. Set main file path to `app.py`.

### 4. Configure deployment settings

PakWallet runs with SQLite by default. For an MVP deployment, no extra secrets are required.

Optional Streamlit secrets can be added if you want to override environment values:

```toml
APP_NAME = "PakWallet"
DATABASE_URL = "sqlite:///pakwallet.db"
DEMO_USER_EMAIL = "demo@pakwallet.pk"
DEMO_USER_PASSWORD = "PakWallet@123"
```

### 5. Deploy

Click **Deploy**. Streamlit Cloud will install `requirements.txt` and launch `app.py`.

### 6. Update after deployment

Make changes locally, then push them:

```bash
git add .
git commit -m "Update PakWallet"
git push
```

Streamlit Cloud redeploys automatically after the push.

## Production Notes

- Replace demo authentication with a full user registration and account recovery flow before launch.
- Connect OTP to an SMS or email provider.
- Use a managed database such as PostgreSQL for multi-user production workloads.
- Review tax and Zakat formulas with qualified Pakistani finance and tax professionals.
- Add audit logs and stronger transaction authorization for real payments.
