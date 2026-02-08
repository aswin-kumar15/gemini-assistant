# Gemini Assistant (Flask)

Web-based chat assistant powered by Google Gemini with optional real-time web search via Google Custom Search. Includes conversation memory, a Bootstrap UI, and JSON APIs for chat, history, and health.

**Features**
- Gemini responses with conversation history
- Real-time search integration for time-sensitive queries
- Simple Flask JSON API
- Clean Bootstrap-based UI

**Tech Stack**
- Python, Flask
- `google-generativeai` (Gemini API)
- Google Custom Search API
- Bootstrap (UI)

**Project Structure**
- `app.py` Flask app and routes
- `config.py` configuration and env validation
- `services/gemini_service.py` Gemini client wrapper
- `services/search_service.py` Google Custom Search wrapper
- `templates/index.html` UI
- `static/` frontend assets

**Setup**
1. Create and activate a virtual environment.
2. Install dependencies.
3. Create a `.env` file with required keys.
4. Run the server.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

The server runs on `http://localhost:5002`.

**Environment Variables**
Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_SEARCH_API_KEY=your_google_search_api_key
GOOGLE_SEARCH_ENGINE_ID=your_custom_search_engine_id
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

Notes:
- `GEMINI_API_KEY`, `GOOGLE_SEARCH_API_KEY`, and `GOOGLE_SEARCH_ENGINE_ID` are required. The app will exit on startup if any are missing.
- Set `SECRET_KEY` to a strong value in production.

**API Endpoints**
- `GET /` UI
- `POST /chat` JSON body: `{ "message": "..." }`
- `GET /history` returns conversation history
- `POST /clear` clears conversation history
- `GET /health` returns health and configuration status

**Behavior**
- Conversation history is stored in memory and scoped to the session cookie.
- Search is triggered based on keyword heuristics (e.g., "today", "latest", "price").

**Troubleshooting**
- If startup fails, verify `.env` variables and API key validity.
- If search results are empty, confirm your Custom Search Engine is configured to search the web and that the API key has quota.
