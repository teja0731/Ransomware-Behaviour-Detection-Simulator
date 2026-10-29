# Ransomware Behavior Detection Simulator

A safe, educational Streamlit app that generates synthetic file activity and displays a transparent risk score. It does not inspect, encrypt, rename, or modify files on your computer.

## Run on Windows

Install 64-bit Python 3.13 from https://www.python.org/downloads/ and enable **Add python.exe to PATH** during setup. Open this project folder in VS Code, select **Terminal → New Terminal**, then run:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The last command prints a local address, usually `http://localhost:8501`. Open it in your browser. These commands do not require activating the environment, so PowerShell's script policy does not interfere.

If `py -3.13` is not recognized after installing Python, close and reopen VS Code, then check installed versions with `py -0p`.

## Publish to GitHub

1. Create a new, empty repository on GitHub. Do not add a README or license there; this folder already contains a README.
2. In the VS Code terminal, run the commands below, replacing the URL with your repository's HTTPS URL:

```powershell
git init
git add app.py requirements.txt README.md .gitignore
git commit -m "Add ransomware behavior simulator"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

## Deploy on Streamlit Community Cloud

1. Sign in at https://share.streamlit.io/ with GitHub.
2. Choose **Create app** and select your repository and the `main` branch.
3. Set the app file to `app.py`, then deploy.

Community Cloud installs the packages in `requirements.txt`. New commits pushed to the selected branch update the app.

This simulator is for learning and demonstration. It is not endpoint protection or a real malware detector.
