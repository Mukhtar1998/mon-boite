# Maison Impeccable - Devis API

This project includes a simple Python backend that accepts quote requests from the website and sends them by email.

## Run locally

1. Create a `.env` file from `.env.example`.
2. Fill your SMTP credentials.
3. Start the server:

   python server.py

4. Open the site at:

   http://localhost:8000

## API endpoint

POST /api/devis

Body example:

{
"nom": "Jean Dupont",
"telephone": "06 12 34 56 78",
"email": "jean@example.com",
"service": "Particulier",
"message": "Bonjour, je souhaite un devis pour un appartement de 80m2."
}

## SMTP setup

For Gmail, use a Google App Password instead of your normal account password.

Required environment variables:

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `SMTP_TO`
- `EMAIL_FROM` (optional)

## Gmail setup

1. Open your Google Account.
2. Go to Security.
3. Enable 2-Step Verification.
4. Create an App Password.
5. Put the Gmail address in `SMTP_USER`.
6. Put the generated App Password in `SMTP_PASSWORD`.
7. Keep `SMTP_TO` as your business email: `mahsumim588@gmail.com`.

Example `.env`:

```env
HOST=0.0.0.0
PORT=8000
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_account@gmail.com
SMTP_PASSWORD=your_16_char_app_password
SMTP_TO=mahsumim588@gmail.com
EMAIL_FROM=your_account@gmail.com
```

## Test the Gmail connection

Run:

```bash
python smtp_test.py
```

This will test the SMTP connection and send a test email to `SMTP_TO`.

## Notes

- The frontend fetches `/api/devis` and displays success/error status.
- The API supports CORS for local frontend usage.
