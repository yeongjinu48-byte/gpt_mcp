# Copilot Instructions for AI Agents

## Project Overview
This project automates multi-step workflows for aggregating, processing, and publishing market and productivity data using the Rube API and various external integrations (Google, Slack, Discord, GitHub, Notion, YouTube, NewsAPI, AlphaVantage, Finage, Coinranking, Twitter).

## Architecture & Data Flow
- **Macro-driven orchestration**: The main workflow is defined in `macro.json` as a sequence of steps, each specifying an API endpoint, arguments, and session management.
- **Session management**: The first step (`NEW_SESSION`) initializes a session and propagates its ID (`$SID`) through subsequent steps for stateful API calls.
- **External API calls**: All requests are routed via the Rube API, with authentication managed by environment variables (`RUBE_BASE`, `RUBE_AUTH`).
- **Dynamic argument substitution**: Steps use placeholders (e.g., `$SID`, `<PUT_CHANNEL_ID_FROM_PREV_STEP>`) that are replaced at runtime based on previous responses.
- **Data publishing**: Final steps create documents/spreadsheets and send notifications via Google Docs/Sheets, Slack, and Discord.

## Key Files
- `run_macro.py`: Main Python script for executing macros. Reads `macro.json`, manages session, and prints step status.
- `macro.json`: Defines the workflow steps, API endpoints, and argument templates.

## Developer Workflows
- **Run workflow**: Execute `run_macro.py` to process the macro steps. Ensure `RUBE_BASE` and `RUBE_AUTH` are set in your environment.
- **Debugging**: Print statements in `run_macro.py` show step progress. Errors in session ID extraction or API responses will raise exceptions.
- **Customizing macros**: Edit `macro.json` to add, remove, or modify steps. Use argument placeholders for dynamic data flow.

## Conventions & Patterns
- **Step names**: Each macro step has a unique `name` for tracking and debugging.
- **Session propagation**: Always use `$SID` in steps requiring session context.
- **API endpoints**: All paths are relative to `RUBE_BASE` and require `RUBE_AUTH` for authorization.
- **Output handling**: Data and status are printed to stdout; markdown and sheet rows are written to files and uploaded as part of the workflow.

## Integration Points
- **Google Workspace**: Read/write emails, files, calendars, docs, and sheets.
- **Slack/Discord**: List channels, post messages, send webhook notifications.
- **Finance/Crypto APIs**: Fetch FX rates, coin stats, and news headlines.
- **Twitter/X**: Search and aggregate recent tweets.

## Example Patterns
- Macro step with session propagation:
  ```json
  {
    "name": "CONNECTIONS_CHECK",
    "path": "/Rube.app/.../RUBE_MANAGE_CONNECTIONS",
    "args": "{... 'session_id': '$SID' ...}"
  }
  ```
- Dynamic argument substitution:
  ```json
  "args": "{... 'channel_id': '<PUT_CHANNEL_ID_FROM_PREV_STEP>' ...}"
  ```

## Tips for AI Agents
- Always initialize a session before running other steps.
- Propagate session ID and other dynamic values as required by macro step templates.
- Review `macro.json` for workflow logic and integration details before making changes.
- Use print outputs and file artifacts for debugging and validation.

---
*Update this file as workflows or integration patterns evolve. Ask for feedback if any section is unclear or incomplete.*

## OpenAI Codex Integration
- If OpenAI Codex is enabled, you can use it for code generation, refactoring, and automation tasks in this project.
- Store your OpenAI API key securely (e.g., in environment variables or a secrets manager). Do not hardcode keys in source files.
- For Codex-powered agents, reference this `copilot-instructions.md` for project context and conventions.
- To extend Codex usage, add Codex-specific patterns, prompt examples, or API usage notes to this file.
- Example: To generate macro steps or API call code, prompt Codex with the macro.json structure and required placeholders.

---
*If you add new Codex workflows or patterns, document them here for future agents and contributors.*
