# Publish Weather RAG LLM on Render.com

Follow these steps to deploy your app so anyone can use it at a public URL.

---

## 1. Push your code to GitHub

From your project folder (with the latest changes committed):

```powershell
cd C:\Users\Dumin\weather-rag-llm
git add .
git status
git commit -m "Add website and Render deploy config"
git push origin main
```

Your repo should be at: **https://github.com/dljayasekera-pixel/weather-rag-llm** (or your fork).

---

## 2. Sign in to Render

1. Go to **https://render.com**
2. Click **Get Started for Free**
3. Sign in with **GitHub** and authorize Render to access your repositories

---

## 3. Create a Web Service from your repo

**Option A – Using the Blueprint (easiest)**

1. In the Render dashboard, click **New +** → **Blueprint**
2. Connect your GitHub account if asked
3. Select the **weather-rag-llm** repository
4. Render will read `render.yaml` and prefill the service. Click **Apply**
5. Wait for the first deploy to finish. Your site will be at:  
   **https://weather-rag-llm.onrender.com** (or the name shown in the dashboard)

**Option B – Manual Web Service**

1. Click **New +** → **Web Service**
2. Connect the **weather-rag-llm** repository (or select it if already connected)
3. Use these settings:
   - **Name:** `weather-rag-llm` (or any name you like)
   - **Region:** Choose the closest to you
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Plan:** Free
5. Click **Create Web Service**

---

## 4. (Optional) Add OpenAI for LLM responses

If you want the app to use GPT for natural-language interpretations:

1. In your service on Render, go to **Environment**
2. Add variable: **Key** `OPENAI_API_KEY`, **Value** your OpenAI API key
3. Save. Render will redeploy automatically.

---

## 5. Use your live site

- **Website:** open your Render URL (e.g. **https://weather-rag-llm.onrender.com**)
- Enter a zipcode and click **Get prediction**

**Note:** On the free plan, the first request after the service has been idle can take 30–60 seconds (cold start + RAG model load). Later requests are faster.

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| Build fails | Check the **Logs** tab. Often a missing dependency or wrong Python version. Ensure `requirements.txt` is committed. |
| "Application failed to respond" | Start command must use `$PORT`. Confirm: `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| First prediction very slow | Normal on free tier. The RAG pipeline loads on first use; subsequent requests are quicker. |
| 502 / timeout | Free instances spin down after ~15 min idle. First request after that wakes the service and can take up to ~1 min. |

Your app is published when the deploy shows **Live** and the URL opens the zipcode form.
