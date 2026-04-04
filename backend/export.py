import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from database import get_all_teachers

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
PERIODS = 8

def export_excel(timetable):
    """Export timetable to Excel format with separate sheets for each teacher"""
    try:
        teachers = get_all_teachers()
        
        with pd.ExcelWriter("timetable.xlsx", engine="openpyxl") as writer:
            for teacher in teachers:
                teacher_id = teacher.teacher_id
                
                if teacher_id not in timetable:
                    continue
                
                schedule = timetable[teacher_id]
                
                # Build data structure: rows = days, columns = periods
                data = []
                header = ["Day"] + [f"Period {i+1}" for i in range(PERIODS)]
                data.append(header)
                
                for day in DAYS:
                    row = [day]
                    for period in range(PERIODS):
                        slot = schedule[day][period]
                        
                        if slot["type"] == "Break":
                            row.append("Break")
                        elif slot["type"] == "Free":
                            row.append("")  # Blank instead of "Free"
                        else:
                            # Class or Lab
                            subject = slot.get("subject", "")
                            class_name = slot.get("class", "")
                            entry_type = slot.get("type", "Class")
                            if entry_type == "Lab":
                                row.append(f"{subject}\n({class_name})\n[LAB]")
                            else:
                                row.append(f"{subject}\n({class_name})")
                    
                    data.append(row)
                
                # Create DataFrame and write to Excel
                df = pd.DataFrame(data[1:], columns=data[0])
                df.to_excel(writer, sheet_name=f"{teacher.name[:20]}", index=False)
        
        print("Excel file exported successfully as timetable.xlsx")
    except Exception as e:
        print(f"Error exporting Excel: {str(e)}")
        raise

def export_pdf(timetable):
    """Export timetable to PDF format with table per teacher"""
    try:
        teachers = get_all_teachers()
        
        doc = SimpleDocTemplate("timetable.pdf")
        story = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        teacher_style = ParagraphStyle(
            'TeacherName',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#003366'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph("Faculty AI Timetable Management System", title_style))
        story.append(Spacer(1, 0.3 * inch))
        
        for teacher in teachers:
            teacher_id = teacher.teacher_id
            
            if teacher_id not in timetable:
                continue
            
            # Teacher info
            teacher_info = f"<b>Teacher:</b> {teacher.name} | <b>Subjects:</b> {', '.join(s.name for s in teacher.subjects)}"
            story.append(Paragraph(teacher_info, teacher_style))
            
            schedule = timetable[teacher_id]
            
            # Build table data: rows = days, columns = periods
            table_data = []
            header = ["Day"] + [f"P{i+1}" for i in range(PERIODS)]
            table_data.append(header)
            
            for day in DAYS:
                row = [day]
                for period in range(PERIODS):
                    slot = schedule[day][period]
                    
                    if slot["type"] == "Break":
                        row.append("Break")
                    elif slot["type"] == "Free":
                        row.append("")  # Blank instead of "Free"
                    else:
                        subject = slot.get("subject", "")
                        class_name = slot.get("class", "")
                        entry_type = slot.get("type", "Class")
                        if entry_type == "Lab":
                            row.append(f"{subject}\n({class_name})\n[LAB]")
                        else:
                            row.append(f"{subject}\n({class_name})")
                
                table_data.append(row)
            
            # Create and style table
            table = Table(table_data, colWidths=[0.8*inch] + [0.7*inch]*PERIODS)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#e6f0ff')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f5ff')]),
            ]))
            
            story.append(table)
            story.append(Spacer(1, 0.5 * inch))
            story.append(PageBreak())
        
        doc.build(story)
        print("PDF file exported successfully as timetable.pdf")
    except Exception as e:
        print(f"Error exporting PDF: {str(e)}")
        raise
