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
        return None

    try:
        df1 = pd.read_excel(file_path)
        
        # Check if the DataFrame is empty
        if df1.empty:
            print("The selected Excel file is empty.")
            return None

        # Check for required columns
        required_columns = ['CLASS', 'SUBJECT NAME', 'Course Code', 'Theory (hrs)', 'Lab (Hrs)', 'Hours per week', 'PROPOSED\nUNIVERSITY\nTIMING']
        if not all(col in df1.columns for col in required_columns):
            print("The Excel file is missing required columns.")
            return None

        generate_class_names(df1)
        courses = generate_courses_dict2(df1, class_names)
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
            class_names.add(i)  # Only one section, so just add the class without "A" or "B"

# Function to generate courses dictionary
def generate_courses_dict2(df1, class_names):
    courses = {}
    time_def = {}

    for class_name in class_names:
        # Initialize an empty dictionary for the class
        courses[class_name] = {}
        time_def[class_name] = False

        # Adjust the logic to account for classes without section B
        base_class_name = class_name.split()[0]
        # print(class_name)
        for index, row in df1[df1['CLASS'].str.startswith(base_class_name)].iterrows():
            
            subject = row['SUBJECT NAME']
            subject_code = row['Course Code']
            normal_hrs = row['Theory (hrs)']
            lab_hrs = row['Lab (Hrs)']
            total_hrs = row['Hours per week']
            purposed_timing = row['PROPOSED\nUNIVERSITY\nTIMING']
            
            # print(class_name,subject,subject_code,normal_hrs,lab_hrs,total_hrs)

            # Get teacher incharge for Section A and Section B
            teacher_a = row['SECTION - A\n (incharge)'] if 'SECTION - A\n (incharge)' in row else None
            teacher_b = row['SECTION -B\n (Incharge)'] if 'SECTION -B\n (Incharge)' in row else None

            # Skip the subject if both Section A and Section B have no teacher
            if pd.isna(teacher_a) and pd.isna(teacher_b):
                continue  # Skip this subject as there is no teacher for either section

            # Handle cases where only one section has a teacher
            if pd.isna(teacher_a):
                teacher_incharge_a = []  # No teacher for Section A
            else:
                # Ensure teacher is a string before splitting and iterating
                teacher_incharge_a = [t.strip() for t in str(teacher_a).replace('and', ',').split(',')]
                # print(teacher_incharge_a)

            if pd.isna(teacher_b):
                teacher_incharge_b = []  # No teacher for Section B
            else:
                # Ensure teacher is a string before splitting and iterating
                teacher_incharge_b = [t.strip() for t in str(teacher_b).replace('and', ',').split(',')]
                # print(teacher_incharge_b)

            subject_type = row['COURSE TYPE 2'].strip() if not pd.isnull(row['COURSE TYPE 2']) else "NORMAL"
            short_name = row["SHORT NAMES"]

            # Assign teachers based on the section (A or B)
            if class_name.endswith("A"):
                teacher_incharge = teacher_incharge_a
            elif class_name.endswith("B"):
                teacher_incharge = teacher_incharge_b
            else:
                # Handle classes with no sections, assign the available teacher
                teacher_incharge = teacher_incharge_a or teacher_incharge_b

            # Skip this subject if no teacher is assigned for the current section
            if not teacher_incharge:
                continue  # Skip the subject if there is no teacher assigned for the current section

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

            if not time_def[class_name]:
                time_def[class_name] = True    
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
    # pprint.pprint(process_excel_file(file_path))  # Process the selected file
    return process_excel_file(file_path)

# main()
