from src.ScriptIngest import run_full_analysis
import os
import sys
import time
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash

# Ensure src/ is on the Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = "enhanced-budget-pro-secret"  # replace later if needed

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_ROOT = os.path.join(BASE_DIR, "web_output")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_ROOT, exist_ok=True)


def safe_slug(name: str) -> str:
    base = os.path.splitext(os.path.basename(name))[0]
    base = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in base)
    return base or "script"


@app.route("/", methods=["GET"])
def index():
    # Simple upload page; results show after POST to /analyze
    return render_template("dashboard.html", mode="upload")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "script_file" not in request.files:
        flash("No file part in request.")
        return redirect(url_for("index"))

    file = request.files["script_file"]
    if file.filename == "":
        flash("No file selected.")
        return redirect(url_for("index"))

    filename = file.filename
    slug = safe_slug(filename)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    job_id = f"{slug}_{timestamp}"

    # Save uploaded script
    upload_path = os.path.join(
        UPLOAD_FOLDER, job_id + os.path.splitext(filename)[1])
    file.save(upload_path)

    # Create output folder for this job
    output_dir = os.path.join(OUTPUT_ROOT, job_id)
    os.makedirs(output_dir, exist_ok=True)

    try:
        result = run_full_analysis(upload_path, output_dir)
    except Exception as exc:
        flash(f"Error analyzing script: {exc}")
        return redirect(url_for("index"))

    scenes = result["scenes"]
    characters = result["characters"]
    budget_summary = result["budget_summary"]
    budget_rows = result["budget_rows"]
    risk_rows = result["risk_rows"]
    export_summary = result["export_summary"]

    return render_template(
        "dashboard.html",
        mode="results",
        job_id=job_id,
        script_name=filename,
        scenes=scenes,
        characters=sorted(set(characters)),
        budget_summary=budget_summary,
        budget_rows=budget_rows,
        risk_rows=risk_rows,
        export_summary=export_summary,
    )


@app.route("/download/<job_id>/<path:filename>")
def download_file(job_id, filename):
    # Only allow files from that job's output folder
    output_dir = os.path.join(OUTPUT_ROOT, job_id)
    return send_from_directory(output_dir, filename, as_attachment=True)


if __name__ == "__main__":
    # Flask dev server
    app.run(host="0.0.0.0", port=8000, debug=True)
