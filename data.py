import ui
import tkinter as tk




def print_courses_table(courses, shortsub):
    # Print overall headers
    print(f"{'Subject Name':<40} {'Theory Hours':<15} {'Lab Hours':<10} {'Total Hours':<10}")
    print("=" * 85)

    # Filter classes or subjects if needed
    class_ignore = ["5BCA B", "3BCA B", "1BCA B", "BCOM-II", "BCOM-I", "BCOM-III"]
    subject_ignore = ["MDC", "LIBRARY", "HED", "MATHEMATICS"]

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
root.withdraw()  # Hide the root window since we just need the file dialog

# Call the function that uploads and processes the file

courses = ui.main()
# pprint.pprint(courses.keys())
CLASSES_t={x:None for x in courses.keys() if x not in ["BCOM-I","BCOM-II","BCOM-III"]}

CLASSES={k:None for k in courses.keys()}

# Check if courses were returned and print the output
if courses is not None:
    print("Courses loaded successfully.")
    # pprint.pprint(courses)
    
    # ele = ["5BCA A","5BCA B"]
    # print(ele)

    # Build shortsub dictionary from courses
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
    "Dr AROKIA PAUL RAJAN R":"APR",
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
    "Dr RESMI KR":"RES",#
    "Dr ROHINI V":"RV",#
    "Dr SAGAYA AURELIA P":"SA",#
    "Dr SANDEEP J":"SD",
    "Dr SANGEETHA GOVINDA":"SG",#
    "Dr SARAVANAKUMAR K":"SK",
    "Dr SARAVANAN KN":"KNS",
    "Dr SHONY SEBASTIAN":"SS",
    "Dr SMITHA VINOD":"SV",
    "Dr SOMNATH SINHA":"SOM",
    "Dr SREEJA":"SR",#
    "Dr SRIDEVI R":"SRI",
    "Dr SUDHAKAR":"SU",
    "Dr SURESH K":"KS",
    "Dr THIRUNAVUKKARASU V":"VT",
    "Dr VAIDHEHI V":"VV",
    "Dr VIJAY ARPUTHARAJ":"VA",
    "Dr VINEETHA KR":"VKR",#
    "Dr Amrutha ":"AMR",
    "Dr Smera":"SME",
    "Dr Chanti":"CHA",
    "Dr Newbegin":"NEB",
    "Dr Manasa":"MAN",
    "Dr SHAMINE":"SH",
    "Dr LOKESHWARAN":"LJ",
    "Dr CYNTHIA":"CYN",
    "Dr RAINA":"RA",
    
    }

    short_teachers = {key.upper().strip(): value for key, value in short_teachers.items()}
       # print(CLASSES_t)

    # Calculate total hours for each course
    TOTALHR = {}
    for course, details in courses.items():
        total_hours = 0
        for section, subjects in details.items():
            elective_counted = False
            for subject, info in subjects.items():
                if "ELECTIVE" in section.upper():
                    if not elective_counted:
                        total_hours += info.get("total_hours_per_week", 0)
                        elective_counted = True
                else:
                    total_hours += info.get("total_hours_per_week", 0)
        TOTALHR[course] = total_hours

    # Sort the TOTALHR dictionary by total hours in descending order
    sorted_courses = dict(sorted(TOTALHR.items(), key=lambda item: item[1], reverse=True))

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
   # Step 2: Retrieve subjects from both categories for those classes
    # List comprehension to check if both "ELECTIVE-I" and "ELECTIVE-II" exist and are not empty
    ele = [key for key in courses if "ELECTIVE-I" in courses[key] or "ELECTIVE-II" in courses[key] 
        and courses[key]["ELECTIVE-I"]  # Check if "ELECTIVE-I" is not empty
        and courses[key]["ELECTIVE-II"]]  # Check if "ELECTIVE-II" is not empty


    # Step 3: Extract elective subjects if the key exists
    # Create a set of unique elective subjects from both "ELECTIVE-I" and "ELECTIVE-II"
    # Create a set of unique elective subjects from both "ELECTIVE-I" and "ELECTIVE-II"
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


# print(ele_sub)



    # Print sorted results in table format
    # print_courses_table(courses, shortsub)

else:
    print("No courses found or file upload failed.")


list1 = ["Dr KIRUBANAND V B", "Dr FABIOLA HAZEL POHRMEN", "Dr CYNTHIA"]
list2 = ["Dr SARAVANAKUMAR K", "Dr SANGEETHA GOVINDA", "Dr SMERA"]
list3 = ["Dr RAMAMURTHY B", "Dr AMRUTHA"]

# Converting all elements to upper case
# print(list1)
list1 = [name.upper() for name in list1]
list2 = [name.upper() for name in list2]
list3 = [name.upper() for name in list3]
import pprint
# print(ele)
# print(ele_sub)
# pprint.pprint(courses)



