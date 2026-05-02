# Civic Nexus: Election Intelligence

An interactive, accessible, and robust enterprise-grade AI agent designed to educate users about the election process. Built with Streamlit and Google Gemini, optimized for maximum code quality, accessibility, testing, and Google Services integration.

## Features
- **Multimodal AI:** Upload sample ballots or documents for the AI to analyze.
- **Function Calling:** AI automatically looks up state-specific deadlines using real-time mock tools.
- **Persistent Memory:** Conversations retain context throughout the session.
- **Accessible UI:** High-contrast Streamlit theme and semantic markdown structure.
- **Enterprise Code Quality:** Strict type hinting, robust logging, and comprehensive unit testing.

## Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up environment variables by copying `.env.template` to `.env` and adding your Google Gemini API key.
   ```bash
   cp .env.template .env
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Testing
Run the test suite via pytest:
```bash
python -m pytest tests/
```
