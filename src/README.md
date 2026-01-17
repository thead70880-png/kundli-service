# Kundli Service

This is a standalone microservice for generating Kundli (astrological charts). It is built with FastAPI and follows production-grade microservice principles.

## Features

-   **Standalone:** Independent of the main consultancy system.
-   **Clean HTTP APIs:** Exposes a clear and documented API for generating Kundli and searching for locations.
-   **Isolated Engine:** The Kundli computation engine is fully isolated from the API layer, allowing for independent development and testing.
-   **Production-Ready Structure:** The service is organized in a way that is easy to maintain, test, and deploy.

## Getting Started

### Prerequisites

-   Python 3.9+
-   pip
-   Docker (optional)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd kundli-service
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create a `.env` file:**
    ```bash
    cp .env.example .env
    ```
    You will need to add an API key for the location service to the `.env` file.

### Running the Service

You can run the service directly with `uvicorn`:

```bash
uvicorn app.main:app --reload
```

The service will be available at `http://localhost:8000`.

### Running with Docker

You can also run the service with Docker:

```bash
docker build -t kundli-service .
docker run -p 8000:8000 kundli-service
```

## API Endpoints

The following API endpoints are available:

-   `GET /health`: Checks the health of the service.
-   `POST /kundli/generate`: Generates a Kundli based on birth details.
-   `GET /location/search`: Searches for a location.

You can find the full API documentation at `http://localhost:8000/docs`.
