## What this project does

This is a small automation bot for **Welcome to the Jungle** (WTTJ): it uses **Selenium** to:

- Log in to your WTTJ account
- Open a job search URL (your saved filters)
- Iterate through job pages
- Apply to jobs you haven’t applied to yet
- Keep track of already-applied jobs in `wttj/applied_jobs_list.json`

The browser itself runs in Docker (`selenium/standalone-chrome`) and the Python bot connects to it via Selenium Remote WebDriver.

Project entrypoint: [wttj/main.py](wttj/main.py)

## Run (recommended: Docker Compose)

### Prerequisites

- Docker + Docker Compose

### 1) Create your local env file

Create a `.env` file at the repo root (this file must stay local):

```bash
echo "NO_VNC_PORT=7900" > .env
```

Then you can open the browser UI at `http://localhost:7900`.

### 2) Create your credentials file

Create `wttj/cred.json` (local only) with:

```json
{
	"email": "YOUR_EMAIL",
	"password": "YOUR_PASSWORD",
	"job_list_url": "YOUR_WTTJ_JOB_LIST_URL"
}
```

### 3) (Optional) Enable AI-generated cover letters

If you want cover letters / answers to be generated, set:

```bash
export OPENAI_API_KEY="..."
```

If not set, the bot uses simple fallback text.

### 4) Start

```bash
docker compose up --build
```

Stop with `Ctrl+C`, and clean up with:

```bash
docker compose down
```

## Notes

- Do not commit `.env` or `wttj/cred.json` (they should be ignored by git).

Reference: [Demo of Selenium tests in Docker container (Chrome runs in Docker too)](https://www.rokpoto.com/selenium-tests-in-docker/)
