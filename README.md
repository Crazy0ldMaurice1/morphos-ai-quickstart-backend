# Morphos AI Quickstart - Backend

This repository contains the **Flask API and Database Integration** for Morphos AI Quickstart.

## Features
- User input capture
- PostgreSQL storage and retrieval
- CORS-enabled API endpoints

## API Endpoints
- `GET /api/messages` - Retrieve stored messages
- `POST /api/echo` - Submit a message for storage

## Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL
- Virtual Environment (venv)

### Setup

```bash
git clone https://github.com/Crazy0ldMaurice1/morphos-ai-quickstart-backend.git
cd morphos-ai-quickstart-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
