# Publish this project to your GitHub account

Run these commands from the **weather-rag-llm** folder in a terminal.

## 1. Create the repo on GitHub

- Go to https://github.com/new
- Repository name: `weather-rag-llm` (or any name you prefer)
- Leave "Initialize with README" **unchecked**
- Create repository

## 2. Initialize and push from your machine

```powershell
cd C:\Users\Dumin\weather-rag-llm

git init
git add .
git commit -m "Initial commit: Weather RAG LLM - zipcode to temp/humidity prediction"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/weather-rag-llm.git
git push -u origin main
```

Replace **YOUR_GITHUB_USERNAME** with your actual GitHub username.

If you use **SSH** instead of HTTPS:

```powershell
git remote add origin git@github.com:YOUR_GITHUB_USERNAME/weather-rag-llm.git
git push -u origin main
```

## 3. If Git asks for credentials

- **HTTPS**: Use a [Personal Access Token](https://github.com/settings/tokens) as the password when prompted.
- **SSH**: Ensure your SSH key is added to GitHub (Settings → SSH and GPG keys).

After this, your Weather RAG LLM project will be on your GitHub account.
