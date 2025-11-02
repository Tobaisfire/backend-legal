# AI Legal Backend API

FastAPI backend for Legal Document Summarizer.

## Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   Create a `.env` file:
   ```
   GOOGLE_API_KEY=your-api-key-here
   ```

3. **Run the Server**
   ```bash
   uvicorn app:app --reload --port 8000
   ```

4. **Test the API**
   - Health check: http://localhost:8000/
   - API Docs: http://localhost:8000/docs

## API Endpoints

- `GET /` - Health check
- `POST /api/summarize` - Summarize legal documents
  - Accepts: `file` (optional) and `text` (optional)
  - Returns: Summary content and statistics

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

## Environment Variables

- `GOOGLE_API_KEY` (required) - Google Gemini API key
- `ALLOWED_ORIGINS` (optional) - Comma-separated list of allowed CORS origins

