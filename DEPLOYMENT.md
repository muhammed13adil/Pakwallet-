# Deploying PakWallet to Streamlit Cloud

This guide provides step-by-step instructions for creating a GitHub repository, uploading your local code, connecting it to Streamlit Community Cloud, deploying the application, and updating it in the future.

---

## 1. Creating a GitHub Repository

1. **Log in to GitHub**: Open your browser and navigate to [github.com](https://github.com).
2. **Create New Repository**:
   - Click the **`+`** icon in the upper-right corner and select **New repository** (or go to [github.com/new](https://github.com/new)).
   - **Repository owner**: Choose your personal account.
   - **Repository name**: Enter `pakwallet` (or any name you prefer).
   - **Description**: Add an optional description (e.g., `PakWallet - Your Smart Financial Companion`).
   - **Public/Private**: Select **Public** or **Private** (both work with Streamlit Community Cloud).
   - **Initialize this repository with**:
     - ⚠️ **IMPORTANT**: Do **NOT** check "Add a README file", "Add .gitignore", or "Choose a license". Your local project folder already contains these files, and adding them on GitHub will create immediate merge conflicts.
3. Click **Create repository**.

---

## 2. Uploading Code to GitHub

Your local workspace is already initialized as a Git repository. However, if you see a permission error (such as HTTP `403 Forbidden` because the current remote points to a repository you do not own), you should update the remote URL to point to your new GitHub repository.

### Step 2.1: Update Remote URL (If needed)
If you created a new repository under your own account (e.g., `YOUR_USERNAME`), update your Git remote origin with the following command:

```bash
# Replace 'YOUR_USERNAME' and 'pakwallet' with your GitHub username and repository name
git remote set-url origin https://github.com/YOUR_USERNAME/pakwallet.git
```

If you are setting up a remote for the first time or starting fresh:
```bash
git remote add origin https://github.com/YOUR_USERNAME/pakwallet.git
```

### Step 2.2: Verify and Push Local Commits
Check your repository status to make sure all local changes are committed and the working tree is clean:

```bash
git status
```

Push your local `main` branch to your GitHub repository:
```bash
# Push the commits and set upstream
git push -u origin main
```
*Note: If prompted, authenticate using your GitHub Credentials or a Personal Access Token (PAT).*

---

## 3. Connecting GitHub to Streamlit Cloud

1. **Visit Streamlit Community Cloud**: Go to [share.streamlit.io](https://share.streamlit.io/).
2. **Sign In**: Click **Continue with GitHub** to log in.
3. **Authorize**: If prompted, authorize Streamlit to access your GitHub repositories.

---

## 4. Deploying the App

1. **Initiate Deploy**: Once logged into the Streamlit dashboard, click the **New app** (or **Create app**) button in the upper-right corner.
2. **Configure App Settings**:
   - **Repository**: Select your repository (e.g., `YOUR_USERNAME/pakwallet`).
   - **Branch**: Set to `main`.
   - **Main file path**: Set to `app.py` (the entry point of your application).
   - **App URL**: You can optionally customize the subdomain for your app URL (e.g., `pakwallet.streamlit.app`).

3. **Configure Environment Secrets and Python Version** (Critical for PakWallet configuration):
   Streamlit Cloud utilizes advanced settings for python environments and secrets. To configure these:
   - Click **Advanced settings** at the bottom of the deployment form.
   - **Python Version**: Select **3.11** or **3.12** from the Python version dropdown.
     - ⚠️ **IMPORTANT**: Streamlit Cloud ignores `runtime.txt` and defaults to the newest Python version (e.g., Python 3.14). Since older package versions pinned in `requirements.txt` (like `pillow==10.4.0` or `pandas==2.2.2`) do not have precompiled wheels for new Python versions, they will fail to compile. Selecting **3.11** or **3.12** ensures prebuilt wheels are used.
   - **Secrets**: In the **Secrets** text area, paste the keys and values exactly as they appear in your `.env.example` file, using TOML formatting:

     ```toml
     # PakWallet Environment Secrets
     APP_NAME = "PakWallet"
     TAGLINE = "Your Smart Financial Companion"
     DATABASE_URL = "sqlite:///pakwallet.db"
     DEMO_USER_EMAIL = "demo@pakwallet.pk"
     DEMO_USER_PASSWORD = "PakWallet@123"
     ```
   - Click **Save**.

4. **Deploy**: Click the **Deploy!** button.
   - Streamlit Cloud will spin up a container using the selected Python version, install the packages specified in `requirements.txt`, configure your secrets, and launch the application.
   - The deployment process takes 1–3 minutes. Once complete, you will see your live application.

---

## 5. Updating the App After Deployment

Streamlit Community Cloud has built-in Continuous Deployment (CD). Whenever you push new commits to your connected GitHub repository, Streamlit Cloud detects the changes and automatically redeploys your app in real-time.

To update your application:

1. **Stage Changes**:
   ```bash
   git add .
   ```

2. **Commit Changes**:
   ```bash
   git commit -m "feat: description of changes made"
   ```

3. **Push to GitHub**:
   ```bash
   git push origin main
   ```
   Streamlit Cloud will show a spinner in the bottom-right corner of your live app indicating that the update is being built and deployed.

---

## Production Security and Recommendations

- **Database Persistence**: SQLite database files (`pakwallet.db`) are stored locally inside the Streamlit Cloud container. Because these containers are ephemeral, any new data added (like transactions or new savings goals) will be lost when the app restarts or rebuilds. For a persistent multi-user experience, connect your app to a hosted database (such as PostgreSQL or Supabase) and update the `DATABASE_URL` secret.
- **Secrets Management**: Keep your credentials and production API keys secure. Never commit your `.env` or production secrets directly to your Git repository. Always use Streamlit Cloud's secrets manager.
