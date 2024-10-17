import pandas as pd
import pprint
import tkinter as tk
from tkinter import filedialog

# Global variable for class names
class_names = set()

# Function to process the Excel file
def process_excel_file(file_path):
    if not file_path:
        print("No file selected. Please provide an Excel file path.")
        return None  # Return None if no file is selected

    try:
        # Read Excel file directly to DataFrame
        df1 = pd.read_excel(file_path)

        # Generate class names from the DataFrame
        generate_class_names(df1)

        # Generate course dictionary with class_names passed as argument
        courses = generate_courses_dict2(df1, class_names)
        
        # Display the course data using pprint for readability
        # pprint.pprint(courses)
        return courses
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Function to generate class names based on the Excel data
def generate_class_names(df1):
    temp = list(set(df1['CLASS'].str.strip()))  # Strip whitespace from class names
    for i in temp:
        if 'SECTION -B\n (Incharge)' in df1.columns and df1[df1['CLASS'] == i]['SECTION -B\n (Incharge)'].notna().any():
            class_names.add(i + " A")
            class_names.add(i + " B")
        else:
            class_names.add(i)

    # Debugging: Print the generated class names to check for duplicates
    print("Generated class names:", class_names)

# Function to generate courses dictionary
def generate_courses_dict2(df1, class_names):
    courses = {}
    
    for class_name in class_names:
        # Initialize an empty dictionary for the class
        courses[class_name] = {}

        for index, row in df1[df1['CLASS'].str.startswith(class_name.split()[0])].iterrows():
            subject = row['SUBJECT NAME']
            subject_code = row['Course Code']
            normal_hrs = row['Theory (hrs)']
            lab_hrs = row['Lab (Hrs)']
            total_hrs = row['Hours per week']
            purposed_timing = row['PROPOSED\nUNIVERSITY\nTIMING']

            # Get teacher incharge for Section A and Section B
            teacher_a = row['SECTION - A\n (incharge)']
            teacher_b = row['SECTION -B\n (Incharge)']

            # Split teacher names if separated by comma or 'and'
            teacher_incharge_a = [t.strip() for t in str(teacher_a).replace('and', ',').split(',')] if teacher_a else []
            teacher_incharge_b = [t.strip() for t in str(teacher_b).replace('and', ',').split(',')] if teacher_b else []

            subject_type = row['COURSE TYPE 2'].strip() if not pd.isnull(row['COURSE TYPE 2']) else "NORMAL"

            # Create a shorter subject name (short_name)
            short_name = row["SHORT NAMES"]

            # Assign teachers based on class section (A or B)
            teacher_incharge = teacher_incharge_a
            if class_name.endswith("B") and teacher_incharge_b:
                teacher_incharge = teacher_incharge_b  # Use Section B teacher if available

            # Handle elective courses for classes with two sections
            if subject_type.startswith("ELECTIVE") and class_name.endswith("A"):
                class_name_b = class_name.replace("A", "B")
                if class_name_b in courses:
                    if subject_type not in courses[class_name_b]:
                        courses[class_name_b][subject_type] = {}
                    courses[class_name_b][subject_type][subject] = {
                        "subject_code": subject_code,
                        "short_name": short_name,
                        "teacher_incharge": teacher_incharge_b,  # Use Section B teacher for elective
                        "normal_hours": normal_hrs,
                        "lab_hours": lab_hrs if subject_type == "ELECTIVE-I" else 0,
                        "total_hours_per_week": min(8 if subject_type == "ELECTIVE-I" else 4, total_hrs)  # Use min to ensure we don't exceed the elective hours
                    }

            # Add the subject type key only if it doesn't already exist
            if subject_type not in courses[class_name]:
                courses[class_name][subject_type] = {}

            # Assign the course details to the corresponding subject type
            courses[class_name][subject_type][subject] = {
                "subject_code": subject_code,
                "short_name": short_name,
                "teacher_incharge": teacher_incharge,
                "normal_hours": normal_hrs,
                "lab_hours": lab_hrs,
                "total_hours_per_week": total_hrs
            }
            
            # Add special condition for timing
            if "9.30am-3.30pm" in purposed_timing:
                if 'NOT MORNING' not in courses[class_name]:
                    courses[class_name]['NOT MORNING'] = {}

    return courses

# Function to select the file
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    return file_path

# Main execution
def main():
    file_path = select_file()  # Open file dialog to select the Excel file
    return process_excel_file(file_path)  # Process the selected file
