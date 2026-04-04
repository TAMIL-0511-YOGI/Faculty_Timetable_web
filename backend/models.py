class Subject:
    def __init__(self, name, year, section, hours_per_week, is_lab=False, lab_days=None, subject_id=None):
        self.subject_id = subject_id  # Database ID
        self.name = name  # e.g., "AAI", "OOPS", "DS"
        self.year = year  # 1st, 2nd, 3rd, 4th
        self.section = section  # A, B, C
        self.hours_per_week = hours_per_week  # Total hours needed per week
        self.is_lab = is_lab  # True if lab period
        self.lab_days = lab_days or []  # [0, 2] for Mon, Wed if is_lab=True
        self.class_name = f"{year}{section}"  # e.g., "3A", "2B"
        self.assigned_periods = []  # List of (day, period) tuples

    def to_dict(self):
        return {
            'subject_id': self.subject_id,
            'name': self.name,
            'year': self.year,
            'section': self.section,
            'hours_per_week': self.hours_per_week,
            'is_lab': self.is_lab,
            'lab_days': self.lab_days,
            'class_name': self.class_name
        }


class Teacher:
    def __init__(self, teacher_id, name):
        self.teacher_id = teacher_id
        self.name = name
        self.subjects = []  # List of Subject objects
        self.total_hours_per_week = 0
        self.assigned_periods = []  # List of (day, period, subject_name, class_name)
        self.free_periods_count = 0

    def add_subject(self, subject):
        """Add a subject assignment to this teacher"""
        self.subjects.append(subject)
        self.total_hours_per_week += subject.hours_per_week

    def get_free_periods(self):
        """Calculate free periods (should be 3-4 per week)"""
        total_periods = 5 * 8  # 5 days, 8 periods/day
        # Subtract breaks (3 breaks per day * 5 days = counted in free)
        assigned = len([p for p in self.assigned_periods if p[2] != "Free"])
        self.free_periods_count = total_periods - assigned
        return self.free_periods_count

    def to_dict(self):
        return {
            'teacher_id': self.teacher_id,
            'name': self.name,
            'subjects': [s.to_dict() for s in self.subjects],
            'total_hours_per_week': self.total_hours_per_week,
            'free_periods_count': self.free_periods_count
        }
