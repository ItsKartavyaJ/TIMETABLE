import ui
import tkinter as tk
def print_courses_table(courses, shortsub):
    # Print overall headers
    print(f"{'Subject Name':<40} {'Theory Hours':<15} {'Lab Hours':<10} {'Total Hours':<10}")
    print("=" * 85)

    # Filter classes or subjects if needed
    class_ignore = ["6BCA A", "4BCA A", "2BCA B", "BCOM-II", "BCOM-I", "BCOM-III"]
    subject_ignore = [ "LIBRARY", "MATHS"]

    grand_total_hours = 0  # Overall total hours

    for class_name, categories in courses.items():
        total_hours_for_class = 0

        if class_name in class_ignore:
            continue

        print(f"\nClass name: {class_name}")
        print("-" * 85)

        for category, subjects in categories.items():
            for subject_name, details in subjects.items():
                if subject_name in subject_ignore:
                    continue

                lab_hours = details.get('lab_hours', 0)
                theory_hours = details.get('normal_hours', 0)
                total_hours = lab_hours + theory_hours
                total_hours_for_class += total_hours

                print(f"{shortsub.get(subject_name, subject_name):<40} {theory_hours:<15} {lab_hours:<10} {total_hours:<10}")

        print(f"{'Total for ' + class_name:<40} {'':<15} {'':<10} {total_hours_for_class:<10}")
        grand_total_hours += total_hours_for_class

    print("=" * 85)
    print(f"{'Grand Total':<40} {'':<15} {'':<10} {grand_total_hours:<10}")



# Create a hidden Tkinter root window for UI interactions
root = tk.Tk()
root.withdraw()  



courses = ui.main()
import pprint


# pprint.pprint(courses.keys())
CLASSES_t={x:None for x in courses.keys() if x not in ["BCOM-I","BCOM-II","BCOM-III"]}


# Check if courses were returned and print the output
if courses is not None:
    # print("Courses loaded successfully.")
   
    shortsub = {}
    for classz, classinfo in courses.items():
        for category, subject_info in classinfo.items():
            for sub_name, sub_details in subject_info.items():
                if 'short_name' in sub_details:
                    if sub_name not in shortsub:
                        shortsub[sub_name] = sub_details['short_name']

    # Process course and teacher information (replace with your actual logic)
    
    short_teachers = {
    "Dr ANITA H B":"AN",
    "DR AROKIA PAUL RAJAN":"APR",
    "Dr ASHOK IMMANUEL V":"AI",
    "Dr BEAULAH SOUNDARABAI P":"BE",
    "Dr CECIL DONALD A":"CD",
    "Dr CHANDRA J":"JC",
    "Dr CYNTHIA T":"CY",
    "Dr DEEPA V JOSE":"DVJ",
    "Dr FABIOLA HAZEL POHRMEN":"FHP",
    "Dr GOBI R":"GR",
    "Dr HELEN K JOY":"HKJ",
    "Dr HUBERT SHANTHAN":"HU",
    "Dr KAVITHA R":"RK",
    "Dr KIRUBANAND V B":"KR",
    "Dr MANJUNATHA HIREMATH":"MN",
    "Dr MOHANA PRIYA T":"TM",
    "Dr NISMON RIO R":"NR",
    "Dr NISHA VARGHEESE":"NIS",
    "Dr NIZAR BANU P K":"NB",
    "Dr PETER AUGUSTIN D":"PA",
    "Dr PRABU P":"PR",
    "Dr RAJESH KANNA R":"RKR",
    "Dr RAMAMURTHY B":"RM",
    "Dr RAMESH CHANDRA POONIA":"RCP",
    "Dr RESMI K R":"RES",#
    "Dr ROHINI V":"RV",#
    "Dr SAGAYA AURELIA P":"SA",#
    "Dr SANDEEP J":"SD",
    "Dr SANGEETHA GOVINDA":"SG",#
    "Dr SARAVANAKUMAR K":"SK",
    "Dr SARAVANAN K N":"KNS",
    "Dr SHONY SEBASTIAN":"SS",
    "Dr SMITHA VINOD":"SV",
    "Dr SOMNATH SINHA":"SOM",
    "DR SREEJA c s":"SR",#
    "Dr SRIDEVI R":"SRI",
    "Dr SUDHAKAR":"SU",
    "Dr SURESH K":"KS",
    "Dr THIRUNAVUKKARASU V":"VT",
    "Dr VAIDHEHI V":"VV",
    "Dr VIJAY ARPUTHARAJ":"VA",
    "Dr VINEETHA KR":"VKR",#
    "Dr Amrutha ":"AMR",
    "Dr Smera":"SME",
    "Dr Chanti s":"CHA",
    "Dr New begin":"NEB",
    "Dr MANASA":"MAN",
    "Dr SHAMINE":"SH",
    "Dr LOKESHWARAN":"LJ",
    "Dr CYNTHIA":"CYN",
    "Dr RAINA":"RA",
    "DR ASHOK IMMANUEL":"AI"
    
    }

    short_teachers = {key.upper().strip(): value for key, value in short_teachers.items()}
       
    # Calculate total hours for each course
    TOTALHR = {}
    for course, details in courses.items():
        total_hours = 0
        subjects_hours = []  # List to keep track of hours for subjects
        for section, subjects in details.items():
            elective_counted = False
            for subject, info in subjects.items():
                if "ELECTIVE" in section.upper():
                    if not elective_counted:
                        total_hours += info.get("total_hours_per_week", 0)
                        subjects_hours.append((subject, info.get("total_hours_per_week", 0)))  # Store subject hours
                        elective_counted = True
                else:
                    total_hours += info.get("total_hours_per_week", 0)
                    subjects_hours.append((subject, info.get("total_hours_per_week", 0)))  # Store subject hours

        TOTALHR[course] = (total_hours, subjects_hours)  # Store total hours and subject hours

    # Sort the TOTALHR dictionary by total hours in descending order
    sorted_courses = dict(sorted(TOTALHR.items(), key=lambda item: item[1][0], reverse=True))
    

    # Now sort subjects within each course by their hours in descending order
    for course, (total_hours, subjects_hours) in sorted_courses.items():
        # Sort subjects by their hours
        sorted_subjects = sorted(subjects_hours, key=lambda x: x[1], reverse=True)
        sorted_courses[course] = (total_hours, sorted_subjects)  # Update with sorted subjects

    # sorted_courses now contains total hours and sorted subject hours
    # pprint.pprint(sorted_courses)


    # If you want to keep the original courses in sorted order, you can update or create a new dictionary
    courses = {course: courses[course] for course in sorted_courses.keys()}
 # pprint.pprint(courses)
    CLASSES={x:None for x in courses.keys()}

    for course, details in courses.items():
        for section, subjects in details.items():
            for subject, info in subjects.items():
                # Ensure the key exists before processing
                if"teacher_incharge" in info:
                    # Strip spaces from each teacher's name and capitalize them
                    info["teacher_incharge"] = [
                        teacher.strip().upper() if teacher !="--" else teacher
                        for teacher in info["teacher_incharge"]
                    ]

                    

    n_m=[x for x,j in courses.items() if"NOT MORNING" in j ]

    m=list(set(courses.keys())-set(n_m))

    ele = [key for key in courses if "ELECTIVE-I" in courses[key] or "ELECTIVE-II" in courses[key] 
        and courses[key]["ELECTIVE-I"]  # Check if "ELECTIVE-I" is not empty
        and courses[key]["ELECTIVE-II"]]  # Check if "ELECTIVE-II" is not empty


   
    ele_sub = set()

    for key in ele:  # Iterate over identified classes
        if "ELECTIVE-I" in courses[key]:  # Ensure "ELECTIVE-I" exists
            ele_sub.update(courses[key]["ELECTIVE-I"].keys())  # Add subjects for "ELECTIVE-I"
        if "ELECTIVE-II" in courses[key]:  # Ensure "ELECTIVE-II" exists
            ele_sub.update(courses[key]["ELECTIVE-II"].keys())  # Add subjects for "ELECTIVE-II"

    ele_sub = list(ele_sub)  # Convert the set back to a list

    # print(ele_sub)
  
    
    cc = dict()
    for class_name, info in courses.items():
        cc[class_name] = dict()  # Initialize a dictionary for each class name
        for category, subjects in info.items():
            for subject_name, details in subjects.items():
                if "subject_code" in details:
                    cc[class_name][subject_name] = details["subject_code"]



else:
    print("No courses found or file upload failed.")


list1 = ["Dr KIRUBANAND V B","Dr VIJAY ARPUTHARAJ J"]
list2 = ["Dr BEAULAH SOUNDARABAI P" , "Dr NISMON RIO R"]
list3 = ["Dr MOHANA PRIYA T","Dr AMURTHA K"]

# Converting all elements to upper case
# print(list1)
list1 = [name.upper() for name in list1]
list2 = [name.upper() for name in list2]
list3 = [name.upper() for name in list3]
import pprint

mdc_teacher=["Dr SANGEETHA GOVINDA","Dr SARAVANAN K N","Dr SMERA","Dr HUBERT SHANTHAN","Dr VINEETHA KR"]
mdc_teacher = [name.upper() for name in mdc_teacher]
# print(ele)
# print(ele_sub)
# pprint.pprint(courses)



print_courses_table(courses, shortsub)