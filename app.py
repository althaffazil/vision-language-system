import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

from services.inference import VQAService
from utils.question_utils import normalize_question, is_valid_question
from utils.image_utils import load_image

UPLOAD_FOLDER = "static/uploads"

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

vqa_service = VQAService()


# ===============================
# Web UI Route
# ===============================
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_path = session.get("image_path")

    if request.method == "POST":

        # Handle new image upload
        file = request.files.get("image")
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(image_path)
            session["image_path"] = image_path

        question = request.form.get("question")

        if question and image_path and is_valid_question(question):
            image = load_image(image_path)
            normalized_question = normalize_question(question)
            result = vqa_service.answer(image, normalized_question)

    return render_template("index.html", result=result, image_path=image_path)


@app.route("/reset")
def reset():
    session.pop("image_path", None)
    return redirect(url_for("index"))


# ===============================
# REST API Route
# ===============================
@app.route("/api/vqa", methods=["POST"])
def api_vqa():
    file = request.files.get("image")
    question = request.form.get("question")

    if not file or not question:
        return jsonify({"error": "Image and question are required"}), 400

    if not is_valid_question(question):
        return jsonify({"error": "Invalid question format"}), 400

    # Save image temporarily
    filename = secure_filename(file.filename)
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(image_path)

    image = load_image(image_path)
    normalized_question = normalize_question(question)

    result = vqa_service.answer(image, normalized_question)

    return jsonify({
        "answer": result["answer"],
        "confidence": result["confidence"],
        "question_type": result["question_type"],
        "is_valid": result["is_valid"],
        "warning": result["warning"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)