# Employee Benefits Portal

A web application providing employees with information about company benefits.

## Quick Start

```bash
# Install dependencies
pip install fastapi uvicorn jinja2 sqlalchemy pydantic python-dotenv

# Run the application
python -m uvicorn generated_app.main:app --host 0.0.0.0 --port 8000
```

## Features

- **Benefits Overview**: Browse all available employee benefits
- **FAQ Section**: Find answers to common questions
- **Eligibility Checker**: Determine which benefits you qualify for
- **Contact Form**: Submit questions to HR support
- **Admin Dashboard**: View submitted messages

## Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Welcome page with quick links |
| Benefits | `/benefits` | List of all available benefits |
| FAQ | `/faq` | Frequently asked questions |
| Eligibility | `/eligibility` | Check your benefit eligibility |
| Contact | `/contact` | Submit a support request |
| Admin | `/admin` | View submitted messages |

## API Endpoints

- `GET /api/benefits` - Get all benefits
- `GET /api/faqs` - Get all FAQs
- `POST /api/eligibility` - Check eligibility
- `POST /api/contact` - Submit contact message
- `GET /api/admin/messages` - View messages (admin)

## Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Jinja2 templates + CSS
- **Database**: SQLite
- **ORM**: SQLAlchemy

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
DATABASE_URL=sqlite:///generated_app/database.db
SECRET_KEY=your-secret-key-here
DEBUG=false
```

## Development

```bash
# Run with auto-reload
python -m uvicorn generated_app.main:app --reload

# Run tests
pytest generated_app/integration_test.py -v
```

## Important Notes

- This is a **demo application** using **synthetic data only**
- No real personal or company information is included
- Admin endpoints have no authentication in this demo
- Not intended for production use without additional security measures

## License

MIT License
