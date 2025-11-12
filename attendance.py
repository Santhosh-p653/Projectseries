from fpdf import FPDF
import re
from google.colab import files

# === User Inputs ===
class_name = input("Enter class (e.g., XII-A): ")
tutor = input("Enter faculty in charge/tutor name: ")
total_students = int(input("Enter total number of students in class: "))
start_reg = input("Enter starting registration number (e.g., CS2301A001): ")

print("\nEnter registration numbers of absentees (comma-separated):")
absent_reg_nos = [reg.strip() for reg in input().split(',') if reg.strip()]
absent_set = set(absent_reg_nos)

# === Parse Registration Format ===
match = re.match(r"(.*?)(\d+)$", start_reg)
if not match:
    print("❌ Invalid registration number format. It should end with a number (e.g., CS2301A001)")
    exit()

prefix, start_number = match.groups()
start_number = int(start_number)
number_width = len(match.group(2))  # To keep leading zeros

# === Generate All Registration Numbers ===
all_reg_nos = [f"{prefix}{str(start_number + i).zfill(number_width)}" for i in range(total_students)]

# === Create Attendance Table ===
attendance_data = []
for reg in all_reg_nos:
    status = "Absent" if reg in absent_set else "Present"
    attendance_data.append([reg, status])

# === Generate PDF ===
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, f"Attendance Report - Class {class_name}", ln=1, align="C")

pdf.set_font("Arial", "", 12)
pdf.cell(0, 10, f"Tutor: {tutor}", ln=1)
pdf.cell(0, 10, f"Total Students: {total_students}", ln=1)
pdf.cell(0, 10, f"Present: {total_students - len(absent_set)} | Absent: {len(absent_set)}", ln=1)
pdf.ln(5)

# Table Headers
pdf.set_font("Arial", "B", 12)
pdf.cell(70, 10, "Registration Number", 1)
pdf.cell(40, 10, "Status", 1)
pdf.ln()

# Table Data
pdf.set_font("Arial", "", 12)
for reg, status in attendance_data:
    pdf.cell(70, 10, reg, 1)
    pdf.cell(40, 10, status, 1)
    pdf.ln()

# === Save PDF ===
filename = f"Attendance_{class_name.replace(' ', '_')}.pdf"
pdf.output(filename)

# === Download PDF (Google Colab specific) ===
files.download(filename)
