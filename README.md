# Faculty AI Timetable Generator

Overview
The Faculty AI Timetable Generator is a Python-based web application designed to streamline the process of creating, managing, and distributing faculty schedules in educational institutions. It allows administrators to efficiently generate, customize, and manage weekly timetables for faculty members, ensuring optimal use of resources and reducing scheduling conflicts.

## Key Features
- **User Authentication**: Secure login and sign-up for administrators and faculty members with role-based access control.
- **Dynamic Timetable Generation**: Generate and manage timetables for a 5-day schedule (Monday to Friday) from 9 AM to 5 PM.
- **Customizable Inputs**: Add details such as teacher names, departments, subjects, class types (lecture, lab), and time slots, along with breaks.
- **Interactive Management**: Edit, delete, and regenerate timetables with an intuitive interface.
- **PDF Export**: Easily export timetables to PDF format for printing or sharing.
- **Lab Auto Placement**: Intelligent scheduling of laboratory sessions to optimize resource utilization.
- **Free Period Balancing**: Ensures fair distribution of free periods across faculty members.
- **Responsive Design**: A user-friendly and interactive UI that works seamlessly across devices.

## Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite3
- **PDF Generation**: ReportLab
- **Authentication**: Session-based authentication

## Installation and Setup

### Prerequisites
- Python 3.x
- pip (Python package manager)
- SQLite3

### Step-by-Step Guide

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Pxdarkshadow/faculty-timetable-generator.git
   cd faculty-timetable-generator
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Development Server**:
   ```bash
   cd backend
   python app.py
   ```

5. **Access the Application**:
   - Open your browser and navigate to `http://localhost:5000`
   - Or open `frontend/index.html` directly for the static interface

## Usage
- **Dashboard**: Access the main interface to generate and manage timetables.
- **Timetable Management**: Use the interface to create, edit, or delete faculty schedules.
- **Export to PDF**: Click the "Download PDF" button to download a printable version of the timetable.
- **Conflict Management**: The system automatically detects and prevents scheduling conflicts.

## Future Enhancements
- **Automated Conflict Detection**: Enhanced highlighting of scheduling conflicts with visual indicators.
- **Email Notifications**: Notify faculty members of their schedules via email.
- **ML Integration**: Integrating an ML model which will take student timetable as input. It will then segregate all the lectures and insert them in the faculty's timetable accordingly, enabling automated schedule synchronization between student and faculty timetables.
- **Advanced Analytics**: Dashboard with insights into resource utilization and scheduling efficiency.
- **Multi-Department Support**: Enhanced support for coordinating schedules across multiple departments.

## Project Structure
```
faculty-timetable-generator/
├── backend/
│   ├── app.py           # Main Flask application
│   ├── database.py      # Database management
│   ├── models.py        # Data models
│   ├── scheduler.py     # Timetable scheduling logic
│   ├── export.py        # PDF export functionality
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── index.html       # Main HTML interface
│   ├── app.js          # JavaScript logic
│   └── style.css       # Styling
└── README.md           # This file
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
