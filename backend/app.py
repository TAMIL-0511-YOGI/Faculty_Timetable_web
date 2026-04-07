import os
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from database import add_teacher, add_subject, get_all_teachers, clear_all, delete_subject, update_subject, save_timetable
from scheduler import generate
from export import export_excel, export_pdf

# ✅ Resolve absolute path to repo root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'frontend'), static_url_path='')

# Allow frontend requests from the deployed Vercel app plus local dev origins.
# Replace or extend this list if your frontend uses another production domain.
allowed_origins = [
    "https://faculty-timetable-web-udml.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]
CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

latest_timetable = None

# ✅ Serve index.html
@app.route("/")
def index():
    return send_from_directory(os.path.join(BASE_DIR, 'frontend'), 'index.html')

# ✅ Serve static files (CSS, JS)
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'frontend'), filename)

@app.route("/api/teachers", methods=["GET"])
def get_teachers():
    try:
        teachers = get_all_teachers()
        return jsonify([t.to_dict() for t in teachers])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/teachers", methods=["POST"])
def create_teacher():
    try:
        data = request.json
        teacher_id = data.get("teacher_id")
        name = data.get("name")
        
        if not teacher_id or not name:
            return jsonify({"error": "teacher_id and name are required"}), 400
        
        add_teacher(teacher_id, name)
        return jsonify({"message": "Teacher added successfully", "teacher_id": teacher_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/subjects", methods=["POST"])
def create_subject():
    try:
        data = request.json
        required_fields = ["subject_name", "year", "section", "hours_per_week", "teacher_id"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": f"Missing required fields: {required_fields}"}), 400
        
        add_subject(
            subject_name=data.get("subject_name"),
            year=data.get("year"),
            section=data.get("section"),
            hours_per_week=int(data.get("hours_per_week")),
            teacher_id=data.get("teacher_id"),
            is_lab=int(data.get("is_lab", 0)),
            lab_days=data.get("lab_days", "0")
        )
        return jsonify({"message": "Subject added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/generate", methods=["POST"])
def gen_timetable():
    global latest_timetable
    try:
        teachers = get_all_teachers()
        if not teachers:
            return jsonify({"error": "No teachers found. Please add teachers and subjects first."}), 400
        
        latest_timetable = generate(teachers)
        save_timetable(latest_timetable)
        
        formatted_timetable = {teacher_id: schedule for teacher_id, schedule in latest_timetable.items()}
        
        return jsonify({
            "success": True,
            "timetable": formatted_timetable,
            "message": "Timetable generated successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/download/excel", methods=["GET"])
def download_excel():
    try:
        if latest_timetable is None:
            return jsonify({"error": "No timetable generated yet"}), 400
        export_excel(latest_timetable)
        return send_file("timetable.xlsx", as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/download/pdf", methods=["GET"])
def download_pdf():
    try:
        if latest_timetable is None:
            return jsonify({"error": "No timetable generated yet"}), 400
        export_pdf(latest_timetable)
        return send_file("timetable.pdf", as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/subjects/<int:subject_id>", methods=["DELETE"])
def remove_subject(subject_id):
    try:
        delete_subject(subject_id)
        return jsonify({"message": "Subject deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/subjects/<int:subject_id>", methods=["PUT"])
def edit_subject(subject_id):
    try:
        data = request.json
        update_subject(
            subject_id=subject_id,
            subject_name=data.get("subject_name"),
            year=int(data.get("year")),
            section=data.get("section"),
            hours_per_week=int(data.get("hours_per_week")),
            is_lab=int(data.get("is_lab", 0))
        )
        return jsonify({"message": "Subject updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/clear", methods=["POST"])
def clear_data():
    try:
        clear_all()
        global latest_timetable
        latest_timetable = None
        return jsonify({"message": "All data cleared successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Correct Railway port binding
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
