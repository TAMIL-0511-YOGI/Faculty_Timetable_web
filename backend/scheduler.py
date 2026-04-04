import random
from itertools import combinations

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
PERIODS = 8  # 8 periods per day

# Consecutive 3-period lab slots
LAB_SLOTS = [
    (0, 1, 2),      # Periods 1-3
    (1, 2, 3),      # Periods 2-4
    (2, 3, 4),      # Periods 3-5
    (3, 4, 5),      # Periods 4-6
    (4, 5, 6),      # Periods 5-7
    (5, 6, 7)       # Periods 6-8
]

def create_empty_schedule():
    """Create empty schedule for all days and periods"""
    return {day: [{"type": "Free", "subject": None, "class": None} for _ in range(PERIODS)] for day in DAYS}

def is_slot_free(schedule, day, period):
    """Check if a specific slot is free"""
    slot = schedule[day][period]
    return slot["type"] == "Free"

def is_consecutive_free(schedule, day, periods_list):
    """Check if consecutive periods are all free"""
    return all(is_slot_free(schedule, day, p) for p in periods_list)

def allocate_class_period(schedule, day, period, subject_name, class_name):
    """Allocate a single class period"""
    if is_slot_free(schedule, day, period):
        schedule[day][period] = {"type": "Class", "subject": subject_name, "class": class_name}
        return True
    return False

def allocate_lab_block(schedule, day, periods_tuple, subject_name, class_name):
    """Allocate a 3-period lab block"""
    if is_consecutive_free(schedule, day, periods_tuple):
        for period in periods_tuple:
            schedule[day][period] = {"type": "Lab", "subject": subject_name, "class": class_name}
        return True
    return False

def schedule_labs_for_teacher(schedule, teacher):
    """Schedule lab periods for a teacher based on actual hours_per_week"""
    for subject in teacher.subjects:
        if subject.is_lab and subject.hours_per_week > 0:
            # Each 3-period block = 3 hours, so allocate blocks accordingly
            # hours_per_week / 3 = number of blocks needed
            blocks_needed = subject.hours_per_week // 3
            
            lab_day = subject.lab_days[0] if subject.lab_days else 0  # Use preferred day
            day = DAYS[lab_day]
            
            allocated_blocks = 0
            attempts = 0
            
            # Allocate consecutive 3-period blocks for the lab
            while allocated_blocks < blocks_needed and attempts < 50:
                slot = random.choice(LAB_SLOTS)
                
                if allocate_lab_block(schedule, day, slot, subject.name, subject.class_name):
                    allocated_blocks += 1
                
                attempts += 1

def schedule_classes_for_teacher(schedule, teacher):
    """Schedule class periods for a teacher"""
    for subject in teacher.subjects:
        if not subject.is_lab and subject.hours_per_week > 0:
            hours_needed = subject.hours_per_week
            allocated = 0
            attempts = 0
            
            # Allocate individual periods for the class
            while allocated < hours_needed and attempts < 100:
                day = random.choice(DAYS)
                period = random.randint(0, PERIODS - 1)
                
                if allocate_class_period(schedule, day, period, subject.name, subject.class_name):
                    allocated += 1
                
                attempts += 1

def generate(teachers):
    """Main function to generate independent timetables for each teacher"""
    if not teachers or len(teachers) == 0:
        return {}
    
    teacher_schedules = {}
    global_lab_slots = {}  # Track which (day, slot) combinations are used for labs
    
    # Generate independent schedule for each teacher
    for teacher in teachers:
        schedule = create_empty_schedule()
        
        # Schedule labs first for this teacher, avoiding conflicts with other teachers
        schedule_labs_for_teacher_no_conflict(schedule, teacher, global_lab_slots)
        
        # Then schedule classes for this teacher
        schedule_classes_for_teacher(schedule, teacher)
        
        teacher_schedules[teacher.teacher_id] = schedule
    
    return teacher_schedules

def schedule_labs_for_teacher_no_conflict(schedule, teacher, global_lab_slots):
    """Schedule lab periods for a teacher, avoiding time conflicts with other teachers"""
    for subject in teacher.subjects:
        if subject.is_lab and subject.hours_per_week > 0:
            # Each 3-period block = 3 hours
            blocks_needed = subject.hours_per_week // 3
            
            allocated_blocks = 0
            attempts = 0
            
            # Try different days in the week, not just Monday
            available_days = list(range(len(DAYS)))  # [0, 1, 2, 3, 4] for Mon-Fri
            random.shuffle(available_days)
            
            # Allocate consecutive 3-period blocks for the lab across different days
            while allocated_blocks < blocks_needed and attempts < 100:
                day_idx = available_days[attempts % len(available_days)]
                day = DAYS[day_idx]
                slot = random.choice(LAB_SLOTS)
                slot_key = (day, slot)
                
                # Check if this slot is already used by another teacher for lab
                if slot_key not in global_lab_slots:
                    if allocate_lab_block(schedule, day, slot, subject.name, subject.class_name):
                        allocated_blocks += 1
                        global_lab_slots[slot_key] = True  # Mark as used
                
                attempts += 1
