// Use environment variable if available, otherwise use the deployed backend URL.
// If you deploy the frontend separately, replace the fallback with your Render backend URL.
const API_BASE =
  (typeof process !== "undefined" && process.env && process.env.NEXT_PUBLIC_API_URL)
    ? process.env.NEXT_PUBLIC_API_URL + "/api"
    : "https://faculty-timetable-web-1.onrender.com/api"; // <-- replace with your real render backend URL

// Period timings (50 mins each)
const PERIOD_TIMINGS = {
    0: "8:30 - 9:20",
    1: "9:20 - 10:10",
    2: "10:10 - 11:00",
    "break1": "11:00 - 11:10",
    3: "11:10 - 12:00",
    4: "12:00 - 12:50",
    "lunch": "12:50 - 1:25",
    5: "1:25 - 2:15",
    6: "2:15 - 3:05",
    "break3": "3:05 - 3:15",
    7: "3:15 - 4:05"
};

const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"];
const PERIOD_HEADERS = [
    { label: "P1", time: "8:30 - 9:20" },
    { label: "P2", time: "9:20 - 10:10" },
    { label: "P3", time: "10:10 - 11:00" },
    { label: "B1", time: "11:00 - 11:10" },
    { label: "P4", time: "11:10 - 12:00" },
    { label: "P5", time: "12:00 - 12:50" },
    { label: "Lunch", time: "12:50 - 1:25" },
    { label: "P6", time: "1:25 - 2:15" },
    { label: "P7", time: "2:15 - 3:05" },
    { label: "B3", time: "3:05 - 3:15" },
    { label: "P8", time: "3:15 - 4:05" }
];

// ======================
// ADD TEACHER FUNCTIONS
// ======================
async function addTeacher() {
    const teacherId = document.getElementById("teacherId").value.trim();
    const teacherName = document.getElementById("teacherName").value.trim();
    const messageDiv = document.getElementById("teacherMessage");

    if (!teacherId || !teacherName) {
        showMessage(messageDiv, "Please fill all fields", "error");
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/teachers`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ teacher_id: teacherId, name: teacherName })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(messageDiv, "Teacher added successfully!", "success");
            document.getElementById("teacherId").value = "";
            document.getElementById("teacherName").value = "";
            loadTeachers();
        } else {
            showMessage(messageDiv, data.error || "Error adding teacher", "error");
        }
    } catch (error) {
        showMessage(messageDiv, "Error: " + error.message, "error");
    }
}

// ======================
// ADD SUBJECT FUNCTIONS
// ======================
async function addSubject() {
    const teacherSelect = document.getElementById("teacherSelect");
    const subjectName = document.getElementById("subjectName").value.trim();
    const yearLevel = document.getElementById("yearLevel").value;
    const section = document.getElementById("section").value.trim();
    const hoursPerWeek = document.getElementById("hoursPerWeek").value;
    const isLab = document.getElementById("isLab").checked ? 1 : 0;
    const messageDiv = document.getElementById("subjectMessage");

    if (!teacherSelect.value || !subjectName || !yearLevel || !section || !hoursPerWeek) {
        showMessage(messageDiv, "Please fill all fields", "error");
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/subjects`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                subject_name: subjectName,
                year: parseInt(yearLevel),
                section: section,
                hours_per_week: parseInt(hoursPerWeek),
                teacher_id: teacherSelect.value,
                is_lab: isLab,
                lab_days: isLab ? "0" : ""  // Default: Monday only for labs
            })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(messageDiv, "Subject added successfully!", "success");
            document.getElementById("subjectName").value = "";
            document.getElementById("yearLevel").value = "";
            document.getElementById("section").value = "";
            document.getElementById("hoursPerWeek").value = "";
            document.getElementById("isLab").checked = false;
            loadTeachers();
        } else {
            showMessage(messageDiv, data.error || "Error adding subject", "error");
        }
    } catch (error) {
        showMessage(messageDiv, "Error: " + error.message, "error");
    }
}

// ======================
// DELETE SUBJECT
// ======================
async function deleteSubject(subjectId) {
    if (confirm("Are you sure you want to delete this subject?")) {
        try {
            const response = await fetch(`${API_BASE}/subjects/${subjectId}`, {
                method: "DELETE",
                headers: { "Content-Type": "application/json" }
            });

            if (response.ok) {
                loadTeachers();
            } else {
                const data = await response.json();
                alert(data.error || "Error deleting subject");
            }
        } catch (error) {
            alert("Error: " + error.message);
        }
    }
}

// ======================
// EDIT SUBJECT
// ======================
function showEditModal(subjectId, name, year, section, hours, isLab) {
    const modal = document.getElementById("editModal");
    document.getElementById("editSubjectId").value = subjectId;
    document.getElementById("editSubjectName").value = name;
    document.getElementById("editYearLevel").value = year;
    document.getElementById("editSection").value = section;
    document.getElementById("editHoursPerWeek").value = hours;
    document.getElementById("editIsLab").checked = isLab;
    modal.style.display = "block";
}

function closeEditModal() {
    const modal = document.getElementById("editModal");
    modal.style.display = "none";
}

async function updateSubject() {
    const subjectId = document.getElementById("editSubjectId").value;
    const subjectName = document.getElementById("editSubjectName").value.trim();
    const yearLevel = document.getElementById("editYearLevel").value;
    const section = document.getElementById("editSection").value.trim();
    const hoursPerWeek = document.getElementById("editHoursPerWeek").value;
    const isLab = document.getElementById("editIsLab").checked ? 1 : 0;

    if (!subjectName || !yearLevel || !section || !hoursPerWeek) {
        alert("Please fill all fields");
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/subjects/${subjectId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                subject_name: subjectName,
                year: parseInt(yearLevel),
                section: section,
                hours_per_week: parseInt(hoursPerWeek),
                is_lab: isLab
            })
        });

        const data = await response.json();

        if (response.ok) {
            closeEditModal();
            loadTeachers();
        } else {
            alert(data.error || "Error updating subject");
        }
    } catch (error) {
        alert("Error: " + error.message);
    }
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById("editModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// ======================
// LOAD TEACHERS
// ======================
async function loadTeachers() {
    try {
        const response = await fetch(`${API_BASE}/teachers`);
        const teachers = await response.json();

        // Update teacher dropdown
        const teacherSelect = document.getElementById("teacherSelect");
        const currentValue = teacherSelect.value;
        teacherSelect.innerHTML = '<option value="">Select Teacher</option>';

        teachers.forEach(teacher => {
            const option = document.createElement("option");
            option.value = teacher.teacher_id;
            option.textContent = teacher.name;
            teacherSelect.appendChild(option);
        });

        teacherSelect.value = currentValue;

        // Display teachers and subjects
        displayTeachers(teachers);
    } catch (error) {
        console.error("Error loading teachers:", error);
    }
}

function displayTeachers(teachers) {
    const container = document.getElementById("teachersList");
    
    if (teachers.length === 0) {
        container.innerHTML = "<p style='color: #888; text-align: center;'>No teachers added yet. Add a teacher to get started.</p>";
        return;
    }

    container.innerHTML = teachers.map(teacher => `
        <div class="teacher-card">
            <h3>${teacher.name} (ID: ${teacher.teacher_id})</h3>
            <p><strong>Total Hours per Week:</strong> ${teacher.total_hours_per_week}</p>
            <div style="margin-top: 10px;">
                <strong>Subjects:</strong>
                ${teacher.subjects.length === 0 ? 
                    "<p style='color: #999;'>No subjects added</p>" : 
                    teacher.subjects.map(subject => `
                        <div class="subject-item ${subject.is_lab ? 'lab' : ''}">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span><strong>${subject.name}</strong> - Year ${subject.year}${subject.section} | 
                                ${subject.hours_per_week} hrs/week
                                ${subject.is_lab ? ' [LAB]' : ''}</span>
                                <div style="display: flex; gap: 8px;">
                                    <button class="edit-btn" onclick="showEditModal(${subject.subject_id}, '${subject.name}', ${subject.year}, '${subject.section}', ${subject.hours_per_week}, ${subject.is_lab})">Edit</button>
                                    <button class="delete-btn" onclick="deleteSubject(${subject.subject_id})">Delete</button>
                                </div>
                            </div>
                        </div>
                    `).join('')
                }
            </div>
        </div>
    `).join('');
}

// ======================
// GENERATE TIMETABLE
// ======================
async function generateTimetable() {
    const messageDiv = document.getElementById("generateMessage");
    
    try {
        const response = await fetch(`${API_BASE}/generate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(messageDiv, data.message, "success");
            displayTimetable(data.timetable);
            document.getElementById("timetableSection").style.display = "block";
        } else {
            showMessage(messageDiv, data.error || "Error generating timetable", "error");
        }
    } catch (error) {
        showMessage(messageDiv, "Error: " + error.message, "error");
    }
}

// ======================
// DISPLAY TIMETABLE
// ======================
async function displayTimetable(timetable) {
    const container = document.getElementById("timetableContainer");
    
    try {
        const response = await fetch(`${API_BASE}/teachers`);
        const teachers = await response.json();

        let html = "";

        teachers.forEach(teacher => {
            const teacherId = teacher.teacher_id;
            const schedule = timetable[teacherId];

            if (!schedule) return;

            html += `
                <div class="teacher-timetable">
                    <div class="timetable-title">
                        📅 ${teacher.name} - ${teacher.subjects.map(s => s.name).join(", ")}
                    </div>
                    <table class="timetable">
                        <thead>
                            <tr>
                                <th>Day</th>
                                ${PERIOD_HEADERS.map(p => `<th><div class="period-header"><div>${p.label}</div><div class="time-small">${p.time}</div></div></th>`).join('')}
                            </tr>
                        </thead>
                        <tbody>
                            ${DAYS.map((day, dayIdx) => `
                                <tr>
                                    <td class="day-cell"><strong>${day}</strong></td>
                                    ${generatePeriodCells(schedule, day)}
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        });

        container.innerHTML = html;
    } catch (error) {
        console.error("Error displaying timetable:", error);
    }
}

function generatePeriodCells(schedule, day) {
    let html = "";
    const daySchedule = schedule[day];
    
    if (!daySchedule) return html;
    
    // Generate cells with breaks inserted at correct positions
    for (let i = 0; i < 8; i++) {
        const slot = daySchedule[i];
        const cellClass = getCellClass(slot);
        const content = getSlotContent(slot);
        html += `<td class="${cellClass}">${content}</td>`;
        
        // Insert breaks after periods 2, 4, 6 (indices)
        if (i === 2) {  // After P3
            html += `<td class="break">Break</td>`;
        } else if (i === 4) {  // After P5
            html += `<td class="break">Break</td>`;
        } else if (i === 6) {  // After P7
            html += `<td class="break">Break</td>`;
        }
    }
    
    return html;
}

function getCellClass(slot) {
    if (slot.type === "Free") return "free";
    if (slot.type === "Break") return "break";
    if (slot.type === "Lab") return "lab";
    if (slot.type === "Class") return "class";
    return "";
}

function getSlotContent(slot) {
    if (slot.type === "Free") return "";  // Blank for free periods
    if (slot.type === "Break") return "Break";
    if (slot.type === "Lab") {
        return `<strong>${slot.subject}</strong><br><small>(${slot.class || 'N/A'})</small><br><span style="color: #e65100; font-weight: bold;">LAB</span>`;
    }
    if (slot.subject) {
        return `<strong>${slot.subject}</strong><br><small>(${slot.class || 'N/A'})</small>`;
    }
    return "";
}

// ======================
// DOWNLOAD FUNCTIONS
// ======================
async function downloadExcel() {
    const messageDiv = document.getElementById("downloadMessage");
    
    try {
        const response = await fetch(`${API_BASE}/download/excel`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "timetable.xlsx";
            a.click();
            window.URL.revokeObjectURL(url);
            showMessage(messageDiv, "Excel file downloaded successfully!", "success");
        } else {
            const error = await response.json();
            showMessage(messageDiv, error.error || "Error downloading file", "error");
        }
    } catch (error) {
        showMessage(messageDiv, "Error: " + error.message, "error");
    }
}

async function downloadPDF() {
    const messageDiv = document.getElementById("downloadMessage");
    
    try {
        const response = await fetch(`${API_BASE}/download/pdf`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "timetable.pdf";
            a.click();
            window.URL.revokeObjectURL(url);
            showMessage(messageDiv, "PDF file downloaded successfully!", "success");
        } else {
            const error = await response.json();
            showMessage(messageDiv, error.error || "Error downloading file", "error");
        }
    } catch (error) {
        showMessage(messageDiv, "Error: " + error.message, "error");
    }
}

// ======================
// CLEAR DATA
// ======================
async function clearAllData() {
    if (!confirm("Are you sure you want to clear all data? This cannot be undone.")) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/clear`, {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById("teacherMessage").textContent = "";
            document.getElementById("subjectMessage").textContent = "";
            document.getElementById("generateMessage").textContent = "";
            document.getElementById("downloadMessage").textContent = "";
            document.getElementById("timetableSection").style.display = "none";
            loadTeachers();
            alert("All data has been cleared successfully!");
        } else {
            alert(data.error || "Error clearing data");
        }
    } catch (error) {
        alert("Error: " + error.message);
    }
}

// ======================
// UTILITY FUNCTIONS
// ======================
function showMessage(element, message, type) {
    element.textContent = message;
    element.className = "message " + type;
    
    // Auto-hide success messages after 5 seconds
    if (type === "success") {
        setTimeout(() => {
            element.textContent = "";
            element.className = "message";
        }, 5000);
    }
}

// ======================
// INITIALIZATION
// ======================
document.addEventListener("DOMContentLoaded", function() {
    loadTeachers();
});
