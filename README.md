# 🗓️ Timetable Generator

## Overview
This project is a backend-only **Timetable Generator** built in Python. It takes an Excel sheet with class and teacher details as input and generates optimized timetables based on a set of hard and soft constraints. The system is designed to eliminate scheduling conflicts, enforce institutional rules, and ensure a fair workload distribution among teachers.

## Features
- Accepts Excel input of class-teacher-subject assignments
- Generates valid timetables considering:
  - Teacher availability
  - Lab usage
  - Subject placement preferences
  - Elective synchronization
  - Hour limits and session continuity
- Outputs structured timetable data

## Constraints

### ✅ Hard Constraints
1. No teacher should be assigned to multiple classes at the same time.
2. No class should have overlapping subjects in the same period.
3. Only one lab session (2 continuous hours) allowed per day per class.
4. LCA subjects must be scheduled in the first two continuous hours.
5. Teachers teaching first two periods (7:30 or 8:15 AM) must not teach after 1:45 PM.
6. Labs must be used by one class at a time and span exactly 2 hours.
7. Certain subjects (e.g., HED, MDC, lunch) must occupy fixed time slots.
8. Lab hours must match exact required hours in 2-hour blocks.
9. Elective subjects for paired sections must occur simultaneously.
10. Teachers must not exceed 18 teaching hours per week.
11. A subject cannot exceed 2 hours per day.

### ⚙️ Soft Constraints
- Ideally, labs should have 5 teachers per session (2-hour block only).
- Distribute theory hours evenly across the week.
- Respect teacher preferences (e.g., avoid early or late hours).
- Avoid back-to-back lab sessions.
- Limit continuous teaching to 3 hours per day per teacher.
- Minimize gaps in teacher and student schedules.

## Input Format
- Excel sheet with columns: `Class`, `Subject`, `Teacher`, `Type (Lab/Theory)`, `Hours per Week`, `Category (e.g., LCA)`
- Template available in `/input/template.xlsx`

## Output
- Timetable stored in a structured format (e.g., Excel, CSV, or printed to console)
- Format: Weekly timetable per class and per teacher

## Tools Used
- Python  
- Pandas  
- openpyxl


   python main.py
