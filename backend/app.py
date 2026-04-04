from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from database import add_teacher, add_subject, get_all_teachers, clear_all, delete_subject, update_subject, save_timetable
from scheduler import generate
from export import export_excel, export_pdf
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

latest_timetable = None

@app.route("/")
def index():
    """Serve the main index.html"""
    return send_from_directory('../frontend', 'index.html')

@app.route("/<path:filename>")
def static_files(filename):
    """Serve static files (CSS, JS)"""
    return send_from_directory('../frontend', filename)

@app.route("/api/teachers", methods=["GET"])
def get_teachers():
    """Get all teachers with their subjects"""
    try:
        teachers = get_all_teachers()
        return jsonify([t.to_dict() for t in teachers])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/teachers", methods=["POST"])
def create_teacher():
    """Add a new teacher"""
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
    """Add a subject to a teacher"""
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
            lab_days=data.get("lab_days", "0")  # Default: Monday only
        )
        
        return jsonify({"message": "Subject added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/generate", methods=["POST"])
def gen_timetable():
    """Generate timetable for all teachers"""
    global latest_timetable
    
    try:
        teachers = get_all_teachers()
        
        if not teachers:
            return jsonify({"error": "No teachers found. Please add teachers and subjects first."}), 400
        
        latest_timetable = generate(teachers)
        save_timetable(latest_timetable)
        
        # Format for frontend
        formatted_timetable = {}
        for teacher_id, schedule in latest_timetable.items():
            formatted_timetable[teacher_id] = schedule
        
        return jsonify({
            "success": True,
            "timetable": formatted_timetable,
            "message": "Timetable generated successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/download/excel", methods=["GET"])
def download_excel():
    """Download timetable as Excel"""
    try:
        if latest_timetable is None:
            return jsonify({"error": "No timetable generated yet"}), 400
        
        export_excel(latest_timetable)
        return send_file("timetable.xlsx", as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/download/pdf", methods=["GET"])
def download_pdf():
    """Download timetable as PDF"""
    try:
        if latest_timetable is None:
            return jsonify({"error": "No timetable generated yet"}), 400
        
        export_pdf(latest_timetable)
        return send_file("timetable.pdf", as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/subjects/<int:subject_id>", methods=["DELETE"])
def remove_subject(subject_id):
    """Delete a specific subject"""
    try:
        delete_subject(subject_id)
        return jsonify({"message": "Subject deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/subjects/<int:subject_id>", methods=["PUT"])
def edit_subject(subject_id):
    """Update a specific subject"""
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
    """Clear all teachers and subjects"""
    try:
        clear_all()
        global latest_timetable
        latest_timetable = None
        return jsonify({"message": "All data cleared successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
