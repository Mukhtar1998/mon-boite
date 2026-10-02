import json
import os
from pathlib import Path
from email.message import EmailMessage
import smtplib

from flask import Flask, jsonify, request, send_from_directory
from flask import make_response
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")

# Configure structured logging for API requests and server errors
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger("maison_impeccable")


# Add CORS headers to all responses so frontend (even on another port) can call the API
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


# Return JSON for common HTTP errors on API paths to avoid HTML error pages (which caused
# the frontend to receive non-JSON responses and fail parsing).
@app.errorhandler(404)
def not_found(err):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Not found"}), 404
    return send_from_directory(str(BASE_DIR), "index.html")


@app.errorhandler(405)
def method_not_allowed(err):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Method not allowed"}), 405
    return jsonify({"error": "Method not allowed"}), 405


@app.before_request
def log_api_requests():
    # Only log API requests to avoid noisy static-file logs
    if request.path.startswith('/api/'):
        try:
            payload = request.get_data(as_text=True)
        except Exception:
            payload = '<unreadable>'
        logger.info('%s %s %s payload=%s', request.remote_addr, request.method, request.path, payload)


@app.errorhandler(Exception)
def handle_unexpected_error(e):
    # Log full exception with stacktrace and return a JSON 500
    logger.exception('Unhandled exception: %s', e)
    return jsonify({"error": "Internal server error"}), 500

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_TO = os.getenv("SMTP_TO", "mahsumim588@gmail.com")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER or "no-reply@maison-impeccable.fr")


def send_quote_email(data):
    if not SMTP_USER or not SMTP_PASSWORD:
        raise RuntimeError(
            "SMTP_USER and SMTP_PASSWORD are missing. Add them to the .env file."
        )

    nom = (data.get("nom") or "").strip()
    telephone = (data.get("telephone") or "").strip()
    email = (data.get("email") or "").strip()
    service = (data.get("service") or "").strip()
    message = (data.get("message") or "").strip()

    logger.info(f"Processing quote request from: nom={nom}, email={email}, telephone={telephone}")

    # Email to business
    business_email_msg = EmailMessage()
    business_email_msg["Subject"] = "Nouvelle demande de devis - Maison Impeccable"
    business_email_msg["From"] = EMAIL_FROM
    business_email_msg["To"] = SMTP_TO

    business_body = (
        "Nouvelle demande de devis\n\n"
        "========================================\n"
        f"Nom: {nom or 'Non renseigné'}\n"
        f"Téléphone: {telephone or 'Non renseigné'}\n"
        f"Email: {email or 'Non renseigné'}\n"
        f"Service: {service or 'Non renseigné'}\n"
        "========================================\n\n"
        f"Message:\n{message or 'Aucun message fourni'}\n"
    )
    business_email_msg.set_content(business_body)

    # Confirmation email to client
    client_email_msg = EmailMessage()
    client_email_msg["Subject"] = "Confirmation de votre demande de devis - Maison Impeccable"
    client_email_msg["From"] = SMTP_TO  # Send from business email for better deliverability
    client_email_msg["To"] = email

    client_body = (
        f"Bonjour {nom},\n\n"
        "Merci de votre demande de devis pour Maison Impeccable.\n\n"
        "Nous avons bien reçu votre message et nous vous recontacterons dans les 24 heures "
        "pour discuter de votre projet et vous proposer un devis personnalisé.\n\n"
        f"Service demandé: {service or 'Non renseigné'}\n"
        f"Numéro de téléphone: {telephone or 'Non fourni'}\n\n"
        "Si vous avez des questions en attendant, n'hésitez pas à nous contacter:\n"
        "☎ 07 80 54 86 63\n"
        "✉ mahsumim588@gmail.com\n\n"
        "Cordialement,\n"
        "L'équipe Maison Impeccable\n"
    )
    client_email_msg.set_content(client_body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        # Send email to business
        try:
            smtp.send_message(business_email_msg)
            logger.info(f"Business email sent to {SMTP_TO}")
        except Exception as e:
            logger.error(f"Failed to send business email: {e}")
            raise
        # Send confirmation to client
        if email:
            try:
                smtp.send_message(client_email_msg)
                logger.info(f"Confirmation email sent to {email}")
            except Exception as e:
                logger.error(f"Failed to send confirmation email to {email}: {e}")
                raise
        else:
            logger.warning("Client email is empty, skipping confirmation email")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/devis", methods=["POST", "OPTIONS"])
def devis():
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response

    data = request.get_json(silent=True) or {}
    nom = (data.get("nom") or "").strip()
    email = (data.get("email") or "").strip()

    if not nom or not email:
        return jsonify({"error": "Nom and email are required."}), 400

    try:
        send_quote_email(data)
    except Exception as exc:
        return jsonify({"error": f"Email could not be sent: {exc}"}), 500

    return jsonify({"success": True, "message": "Demande de devis envoyée avec succès."}), 200


def load_reviews_data():
    reviews_file = BASE_DIR / "reviews.json"
    if not reviews_file.exists():
        return {"reviews": []}

    try:
        with open(reviews_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and isinstance(data.get("reviews"), list):
            return data
    except Exception as exc:
        logger.error(f"Error reading reviews: {exc}")

    return {"reviews": []}


def save_reviews_data(data):
    reviews_file = BASE_DIR / "reviews.json"
    with open(reviews_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route("/api/reviews", methods=["GET", "POST", "OPTIONS"])
@app.route("/api/review", methods=["GET", "POST", "OPTIONS"])
def reviews_collection():
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return response

    if request.method == "GET":
        return jsonify(load_reviews_data()), 200

    data = request.get_json(silent=True) or {}
    nom = (data.get("nom") or "").strip()
    email = (data.get("email") or "").strip()
    rating = data.get("rating", "")
    location = (data.get("location") or "").strip()
    review_text = (data.get("review") or "").strip()

    if not nom or not email or not rating or not review_text:
        return jsonify({"error": "Nom, email, rating, and review are required."}), 400

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return jsonify({"error": "Rating must be between 1 and 5."}), 400
    except ValueError:
        return jsonify({"error": "Rating must be a number."}), 400

    reviews_data = load_reviews_data()
    reviews = reviews_data.setdefault("reviews", [])
    review_id = max((int(item.get("id", 0)) for item in reviews if str(item.get("id", "")).isdigit()), default=0) + 1

    new_review = {
        "id": review_id,
        "nom": nom,
        "email": email,
        "location": location,
        "rating": rating,
        "review": review_text,
    }
    reviews.append(new_review)
    save_reviews_data(reviews_data)

    logger.info(f"Review submitted by {nom} ({email}): {rating}/5")
    return jsonify({"success": True, "message": "Votre avis a été publié avec succès. Merci !", "review": new_review}), 201


@app.route("/api/reviews/<int:review_id>", methods=["DELETE", "OPTIONS"])
@app.route("/api/review/<int:review_id>", methods=["DELETE", "OPTIONS"])
def review_detail(review_id):
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "DELETE, OPTIONS"
        return response

    reviews_data = load_reviews_data()
    reviews = reviews_data.get("reviews", [])
    original_count = len(reviews)
    filtered_reviews = [r for r in reviews if int(r.get("id", -1)) != review_id]

    if len(filtered_reviews) == original_count:
        return jsonify({"error": "Review not found."}), 404

    reviews_data["reviews"] = filtered_reviews
    save_reviews_data(reviews_data)
    logger.info(f"Review #{review_id} deleted")
    return jsonify({"success": True, "message": "Avis supprimé avec succès."}), 200


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_site(path):
    file_path = BASE_DIR / path
    if path and file_path.exists() and file_path.is_file():
        return send_from_directory(str(BASE_DIR), path)
    return send_from_directory(str(BASE_DIR), "index.html")


# Bind to localhost rather than 0.0.0.0 to avoid Windows socket access restrictions.
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
