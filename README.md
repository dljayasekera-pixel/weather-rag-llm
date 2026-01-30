# Weather RAG LLM

An **LLM-based application using RAG (Retrieval-Augmented Generation)** that predicts **maximum and minimum temperature** and **relative humidity** when a user enters a **zipcode**.

## Architecture

- **Retrieval**: Knowledge base (weather glossary, comfort tips) is embedded and stored in ChromaDB. For each query, relevant chunks are retrieved.
- **Weather data**: [Open-Meteo](https://open-meteo.com/) (free, no API key) is used to geocode the zipcode and fetch daily forecast (min/max temp, mean relative humidity).
- **Generation**: An LLM (OpenAI GPT-4o-mini when `OPENAI_API_KEY` is set) produces a natural-language summary and interpretation; otherwise a structured template response is returned.

## Requirements

- Python 3.10+
- See `requirements.txt` for dependencies.

## Setup

1. **Clone the repository** (or navigate to the project folder).

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # Linux/macOS
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Optional – LLM interpretations**: Copy `.env.example` to `.env` and set your OpenAI API key:
   ```bash
   copy .env.example .env
   # Edit .env and add: OPENAI_API_KEY=sk-...
   ```
   Without this, the app still returns forecast numbers in a clear template format.

## Usage

### CLI

```bash
python main.py <zipcode> [country]
```

Example:

```bash
python main.py 90210
python main.py 10001 US
```

### Website (recommended)

Start the server and open the site in your browser:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- **Website**: http://localhost:8000 — enter a zipcode and get max/min temperature and relative humidity.
- **API docs**: http://localhost:8000/docs  
- **Predict API**: `POST /predict` with JSON body:
  ```json
  { "zipcode": "90210", "country": "US" }
  ```

## Deploy the website

The app serves the website and API from the same process. Deploy to a host that runs Python (e.g. **Render**, **Railway**, **Fly.io**).

### Render (free tier)

1. Push the repo to GitHub.
2. Go to [render.com](https://render.com) → **New** → **Web Service**.
3. Connect your GitHub repo `weather-rag-llm`.
4. **Build command**: `pip install -r requirements.txt`  
   **Start command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. (Optional) Add **Environment** → `OPENAI_API_KEY` for LLM interpretations.
6. Deploy. Render will give you a URL like `https://weather-rag-llm.onrender.com`.

You can also use the included **Blueprint**: **New** → **Blueprint** and point it at this repo; `render.yaml` will configure the service.

### Railway / Fly.io

- **Railway**: New project → Deploy from GitHub → same build/start commands as above; set `PORT` from Railway’s env.
- **Fly.io**: Use `fly launch` and set the start command to `uvicorn main:app --host 0.0.0.0 --port 8080` (or the port Fly provides).

## Project structure

```
weather-rag-llm/
├── app/
│   ├── __init__.py
│   ├── weather_service.py   # Geocoding + Open-Meteo forecast
│   ├── rag_service.py       # Knowledge base + ChromaDB + retrieval
│   ├── llm_service.py       # LLM response generation (OpenAI or template)
│   └── predict.py           # RAG pipeline orchestration
├── static/                   # Website frontend
│   ├── index.html
│   ├── style.css
│   └── app.js
├── knowledge_base/         # Markdown docs for RAG
│   ├── weather_glossary.md
│   └── comfort_tips.md
├── main.py                  # FastAPI app + static site + CLI
├── render.yaml              # Optional: Render blueprint
├── requirements.txt
├── .env.example
└── README.md
```

## Publishing to GitHub

1. **Create a new repository** on GitHub (e.g. `weather-rag-llm`). Do not initialize with a README if this repo already has one.

2. **Initialize Git and push** (from the project folder):
   ```bash
   cd weather-rag-llm
   git init
   git add .
   git commit -m "Initial commit: Weather RAG LLM - zipcode to temp/humidity prediction"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/weather-rag-llm.git
   git push -u origin main
   ```
   Replace `YOUR_USERNAME` with your GitHub username.

3. If you use SSH:
   ```bash
   git remote add origin git@github.com:YOUR_USERNAME/weather-rag-llm.git
   git push -u origin main
   ```

## License

MIT.
