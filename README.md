# GitHub Analytics Beacon

A lightweight, asynchronous FastAPI application designed to capture and visualize request data. This project acts as a web beacon that can be embedded in Markdown files (like GitHub READMEs) to monitor traffic and identify request sources.

<img src="http://44.213.120.40?page=github-analytics-beacon&v=1768614082" alt="Github View Analytics">

## Features

- **Request Analysis**: Automatically captures request headers. **Note:** No additional processing is done as part of this project.
- **Dynamic Visualization**: Serves a PNG image generated from HTML templates using `TemplateManager`.
- **Modify Visibility**: Includes a `/hidden` endpoint that serves a 1x1 transparent pixel.
- **Async Database Support**: Uses `SQLModel` and `AsyncSession` for high-performance data persistence.

## Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database ORM**: [SQLModel](https://sqlmodel.tiangolo.com/)
- **Image Processing**: [Pillow (PIL)](https://python-pillow.org/), [Playwright](https://playwright.dev/)
- **Data Visualization**: [D3.js](https://d3js.org/)
- **Static Files**: Starlette StaticFiles for template assets.

## Endpoints

### 1. Visual Beacon
`GET /`
- Saves request metadata to the database.
- Returns a rendered PNG image (927.5x194) based on `graph_template.html`.
- **Usage**: `<img src="https://your-app-url.com/">`

### 2. Hidden Beacon
`GET /hidden`
- Saves request metadata to the database.
- Returns a transparent 1x1 PNG.
- **Usage**: Used for analytics without visual impact on the page.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/github-analytics.git
   cd github-analytics
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   uvicorn endpoints:app --reload
   ```

## Project Structure

- `endpoints.py`: Main FastAPI application and routing logic.
- `models.py`: Database schemas for `CapturedRequest` and `IdentifiedRequestSource`.
- `database.py`: Session management and engine configuration.
- `visualization/`: Contains a `TemplateManager` class and HTML templates for image generation.