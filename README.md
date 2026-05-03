# Civic Nexus: Election Intelligence

An interactive, accessible, and robust enterprise-grade AI agent designed to educate users about the election process. Built with Streamlit and Google Gemini, optimized for maximum code quality, accessibility, testing, and Google Services integration.

## 1. Chosen Vertical
**Community Needs and Educational Outreach**
Civic Nexus operates within the community outreach vertical. Its persona is an impartial, expert Election Intelligence Agent whose sole purpose is to increase voter turnout and reduce friction by demystifying the election process for the general public.

## 2. Approach and Logic
The solution is built using a strict modular architecture (separating UI, AI logic, and external services). To ensure accuracy and reduce hallucinations, the system relies heavily on **Function Calling (Tools)** rather than internal model knowledge alone. When asked about deadlines or polling locations, the AI automatically delegates the task to the Google Workspace integration layer to fetch structured data, which it then translates into highly accessible, 8th-grade reading level markdown.

## 3. How the Solution Works
- **Multimodal AI:** Users can upload sample ballots or voter ID documents directly into the UI. The Gemini Vision model analyzes the image alongside user prompts to provide contextual, step-by-step guidance.
- **Google Workspace Integrations:** The application integrates with the `google-api-python-client` to simulate adding election reminders directly to Google Calendar and looking up polling locations via Google Maps.
- **Persistent Memory:** Conversations retain context throughout the session using Gemini's `ChatSession`.
- **Accessible UI:** A custom, high-contrast Streamlit theme and semantic markdown structure ensure the application is readable for visually impaired users.
- **Enterprise Code Quality:** The application utilizes strict type hinting, robust python `logging`, and is built for maximum efficiency using Streamlit's `@st.cache_resource` decorators.

## 4. Any Assumptions Made
- It is assumed that the user has a valid Google Gemini API key with access to `gemini-2.5-flash`.
- It is assumed that the provided `google_workspace.py` mock methods represent the final business logic for Calendar/Maps integrations, which would be authenticated via OAuth in a full production rollout.
- The default target reading level for maximum accessibility is 8th grade.

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
Run the comprehensive test suite via pytest:
```bash
python -m pytest tests/
```
