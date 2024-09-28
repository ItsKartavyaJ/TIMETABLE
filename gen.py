import random
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side
from data import courses, short_teachers, shortsub,CLASSES,n_m,m,ele,ele_sub,list1,list2,list3

class TimetableGenerator:
    def __init__(self, courses, num_days=6, num_hours=9):
        self.courses = courses
        self.classes = list(CLASSES.keys())
        self.num_days = num_days
        self.num_hours = num_hours
        self.lab_timetables = {
            "BCA Lab": {day: {hour: [] for hour in range(num_hours)} for day in range(num_days)},
            "MCA Lab": {day: {hour: [] for hour in range(num_hours)} for day in range(num_days)},
            "BSc Lab": {day: {hour: [] for hour in range(num_hours)} for day in range(num_days)}
        }
        self.teacher_schedule = {day: {hour: set() for hour in range(num_hours)} for day in range(num_days)}  # Initialize teacher_schedule
        self.lab_count = {
            c: {sub: 0 for category in self.courses[c] for sub in self.courses[c][category].keys()}
            for c in self.courses
        }
        self.timetable = None  # Initialize timetable as None
    def generate_timetable(self):
        # Initialize timetable structure
        timetable = self.initialize_timetable()
        allocated_subjects, theory_hours_assigned, lab_assigned_per_day, teacher_schedule = self.initialize_tracking_structures()

        # Pre-assign subjects
        self.pre_assign_subjects(timetable)
        
         # # Assign LCA subjects to the first two hours of the day
        self.assign_lca_and_lab_hours(timetable, allocated_subjects, lab_assigned_per_day)  
           #  # Assign all elective subjects at the same time for both sections A and B
               
        self.assign_elective_hours(timetable, allocated_subjects, teacher_schedule)
        self.assign_elective_lab(timetable, allocated_subjects, lab_assigned_per_day, teacher_schedule)
  
        self.assign_lab_hours_multiple_electives(timetable, allocated_subjects, lab_assigned_per_day, teacher_schedule, "5CME")
        self.assign_elective_hours_single_section(timetable, allocated_subjects, teacher_schedule, "5CME")
    
               
        # Assign lab hours and theory hours
        self.assign_lab_hours(timetable, allocated_subjects, lab_assigned_per_day, teacher_schedule)
        self.assign_theory_hours(timetable, allocated_subjects, theory_hours_assigned, teacher_schedule)
       
        # self.finalize_timetable(timetable, theory_hours_assigned, allocated_subjects, teacher_schedule)
        # self.print_teacher_hr(self.calculate_teacher_hours())
        # self.print_teacher_hr(self.get_lab_hours(timetable))
        
        
        
        
        self.assign_teachers_to_all_labs(timetable)
        
        self.print_teacher_hr(self.calculate_teacher_hours())
        
        self.cross_verify_timetable_with_courses(timetable)
        
        
        self.timetable = timetable

        return timetable
    
    
    def cross_verify_timetable_with_courses(self, timetable):
        """
        Traverses the timetable and creates a dictionary with (class, subject) as key
        and the number of hours taught as the value. Prints classes with irregularities 
        in assigned hours.

        Args:
        timetable (list): The timetable structure where timetable[day][class_name][hour] contains subjects.
        
        Returns:
        None: Prints classes and subjects with irregular assigned hours.
        """
        hours_taught = {}  # Dictionary to store hours taught for each (class, subject)
        
        # Traverse the timetable to count the hours each subject is taught
        for day in range(self.num_days):  # Assuming `self.num_days` is defined
            for class_name in timetable[day]:  # Traverse each class in the timetable for that day
                for hour in range(self.num_hours):  # Traverse each hour
                    for subject_info in timetable[day][class_name][hour]:
                        subject_name = subject_info[0]  # Assuming the subject name is the first element
                        
                        # Create key (class_name, subject_name)
                        key = (class_name, subject_name)
                        
                        # Count the number of hours taught for this subject
                        if key in hours_taught:
                            hours_taught[key] += 1
                        else:
                            hours_taught[key] = 1

        # Compare the hours taught with the courses dictionary and print irregularities
        for class_name, class_data in self.courses.items():
            for category, subjects in class_data.items():
                for subject_name, subject_info in subjects.items():
                    required_hours = subject_info["total_hours_per_week"]
                    
                    # Key to lookup in hours_taught
                    key = (class_name, subject_name)
                    
                    # Check if the subject is in hours_taught and compare with required hours
                    if key in hours_taught:
                        if hours_taught[key] != required_hours:
                            print(f"Class {class_name} - Subject '{subject_name}' has {hours_taught[key]} assigned hours, "
                                f"but requires {required_hours} hours.")
                    else:
                        print(f"Class {class_name} - Subject '{subject_name}' is not assigned in the timetable.")


    
    


    def assign_teachers_to_all_labs(self, timetable):
        """
        Assigns a total of 6 teachers to all lab sessions, updates the timetable,
        and blocks the teacher's schedule for all relevant days.

        Args:
        timetable (list): The timetable structure.
        """
        # Get all lab hours available in the timetable
        lab_hours = self.get_lab_hours(timetable)

        # Get all teacher free hours
        teacher_free_hours = self.get_teacher_free_hours(timetable, self.num_days, self.num_hours)

        # Calculate total hours for each teacher
        teacher_hours = self.calculate_teacher_hours()

        # Iterate over each lab session
        for (class_name, subject_name), lab_time_slots in lab_hours.items():
            teacher_free_hours = self.get_teacher_free_hours(timetable, self.num_days, self.num_hours)
            teacher_hours = self.calculate_teacher_hours()
            # Skip if the subject matches the elective condition
            if subject_name not in ele_sub:
                # Convert lab_time_slots to a set for easier subset checking
                lab_time_slots_set = set(lab_time_slots)

                # List to keep track of allocated teachers for this lab
                allocated_teachers = []

                # Check existing teachers assigned to the lab session
                for (day, hour) in lab_time_slots:
                    if len(timetable[day][class_name][hour]) > 0 and len(timetable[day][class_name][hour][0]) > 0:
                        # Get the number of pre-assigned teachers
                        allocated_teachers.extend(timetable[day][class_name][hour][0][1])  # Assuming teachers are in the second index

                        # If the total number of allocated teachers exceeds 6, stop
                        if len(allocated_teachers) >= 6:
                            break

                # Ensure unique teachers
                allocated_teachers = list(set(allocated_teachers))

                # Check each teacher's availability
                for teacher, free_slots in teacher_free_hours.items():
                    free_slots_set = set(free_slots)

                    # Check if "Dr SAGAYA AURELIA P" has exceeded their hours
                    if ((teacher.lower() == "dr sagaya aurelia p".lower() and teacher_hours.get(teacher, 0) >= 12)or 
                        teacher.lower() == "Dr MANJUNATHA HIREMATH".lower() and teacher_hours.get(teacher, 0) >= 12):
                        continue

                    # Check if the lab hours are a subset of the teacher's free hours
                    if lab_time_slots_set.issubset(free_slots_set):
                        current_hours = teacher_hours.get(teacher, 0)

                        # Check if adding the current lab session will exceed 18 hours
                        if current_hours < 18:
                            allocated_teachers.append(teacher)  # Allocate the teacher
                            teacher_hours[teacher] = current_hours + len(lab_time_slots[:2])  # Update the teacher's hours for 2 slots

                        # Stop allocating if we have reached the required number of teachers
                        if len(allocated_teachers) >= 6:
                            break

                # Ensure we only keep unique teachers again
                allocated_teachers = list(set(allocated_teachers))

                # Block the teacher's schedule for the first 2 lab time slots
                lab_time_slots = lab_time_slots[:2] if len(lab_time_slots) == 4 else lab_time_slots
                for (day, hour) in lab_time_slots:
                    if hour <= 8:  # Ensure we are within valid hours
                        if allocated_teachers:  # Only update if we have allocated teachers
                            # Update the timetable with the allocated teachers
                            timetable[day][class_name][hour].append(("", allocated_teachers))  # Add to the timetable

                            # Block the teacher's schedule for all relevant days and hours
                            for teacher in allocated_teachers:
                                self.teacher_schedule[day][hour].add(teacher)  # Ensure only teacher names (strings) are added

                # If less than 6 teachers are allocated, notify about unallocated teachers
                if len(allocated_teachers) < 6:
                    print(f"Only {len(allocated_teachers)} teachers allocated for {class_name} - {subject_name} lab. Need more teachers.")

    
    def get_teacher_free_hours(self,timetable, num_days=6, num_hours=8):
        """
        Retrieves all free hours for each teacher in the timetable.

        Args:
        timetable (list): A list of lists where timetable[day][class_name][hour] contains subjects for each hour in each class.
        num_days (int): The number of days in the timetable.
        num_hours (int): The number of hours in the timetable for each day.

        Returns:
        dict: A dictionary where the key is the teacher's name and the value is a list of tuples (day, hour) representing their free hours.
        """
        # Dictionary to track all busy hours for each teacher
        teacher_busy_hours = {}

        for day in range(num_days):  # Iterate over each day
            for class_name in timetable[day]:  # Iterate over each class
                for hour in range(num_hours):  # Iterate over each hour
                    subjects = timetable[day][class_name][hour]

                    for subject in subjects:
                        subject_name = subject[0]
                        teachers = subject[1]  # Teachers responsible for the subject
                        
                        for teacher in teachers:
                            if teacher.lower().startswith("dr"):    
                                if teacher not in teacher_busy_hours:
                                    teacher_busy_hours[teacher] = []

                                # Record the time when the teacher is busy
                                teacher_busy_hours[teacher].append((day, hour))

        # Now, we create a dictionary to store the free hours for each teacher
        teacher_free_hours = {}

        # Loop through all teachers and identify their free hours
        for teacher, busy_hours in teacher_busy_hours.items():
            all_hours = [(day, hour) for day in range(num_days) for hour in range(num_hours)]
            busy_hours_set = set(busy_hours)
            
            # Calculate free hours by subtracting busy hours from all possible hours
            free_hours = [time for time in all_hours if time not in busy_hours_set]

            teacher_free_hours[teacher] = free_hours

        return teacher_free_hours

    
    
    
    def get_lab_hours(self,timetable):
        """
        Retrieves all lab hours for each (class_name, subject_name) in the timetable.

        Args:
        timetable (list): A list of lists where timetable[day][class_name][hour] contains subjects for each hour in each class.

        Returns:
        dict: A dictionary where the key is a tuple (class_name, subject_name) and the value is a list of tuples (day, hour) representing the lab timings.
        """
        lab_hours = {}

        for day in range(len(timetable)):  # Iterate over each day
            for class_name in timetable[day]:  # Iterate over each class
                for hour in range(len(timetable[day][class_name])):  # Iterate over each hour
                    subjects = timetable[day][class_name][hour]

                    for subject in subjects:
                        # Check if it's a lab (lab subjects are usually indicated by having 3 elements in the tuple)
                        if len(subject) == 3:  # Subject tuple (subject_name, teachers, lab_venue)
                            subject_name = subject[0]  # First element is the subject name
                            lab_venue = subject[2]     # Third element is the lab venue

                            # Create the key (class_name, subject_name)
                            key = (class_name, subject_name)

                            # Store the day and hour as lab timing
                            if key in lab_hours:
                                lab_hours[key].append((day, hour))
                            else:
                                lab_hours[key] = [(day, hour)]

        return lab_hours

    
    def print_teacher_hr(self,teacherhr):
        i=1
        for x,y in teacherhr.items():
            print(f"{i} {x} :{y} ")
            i=i+1
           
            
        
    
    def calculate_teacher_hours(self):
        """
        Calculates the total number of teaching hours for each teacher based on their schedule.

        Returns:
        dict: A dictionary where the key is the teacher's name and the value is the number of hours they are teaching.
        """
        teacher_hours = {}

        # Traverse through each day and each hour in the teacher's schedule
        for day in range(self.num_days):  # Assuming num_days is defined
            for hour in range(self.num_hours):  # Assuming num_hours is defined
                # Check which teachers are scheduled for this hour
                for teacher in self.teacher_schedule[day][hour]:
                    teacher = teacher.strip()  # Clean any extra whitespace

                    # Increment the count of teaching hours for this teacher
                    if teacher.lower().startswith("dr"):  # Check for title if necessary
                        if teacher in teacher_hours:
                            teacher_hours[teacher] += 1
                        else:
                            teacher_hours[teacher] = 1

        return teacher_hours


        

    def initialize_timetable(self):
        return {
            day: {class_name: {hour: [] for hour in range(self.num_hours)} for class_name in self.classes}
            for day in range(self.num_days)
        }

    def initialize_tracking_structures(self):
        allocated_subjects = {day: {class_name: set() for class_name in self.classes} for day in range(self.num_days)}
        theory_hours_assigned = {day: {class_name: {} for class_name in self.classes} for day in range(self.num_days)}
        lab_assigned_per_day = {day: {class_name: False for class_name in self.classes} for day in range(self.num_days)}
        teacher_schedule = {day: {hour: set() for hour in range(self.num_hours)} for day in range(self.num_days)}
        return allocated_subjects, theory_hours_assigned, lab_assigned_per_day, teacher_schedule
    
    def pre_assign_subjects(self, timetable):
        """Pre-assign subjects to the timetable."""
        for class_name in self.classes:
            self.commerce()
            self.assign_hed(timetable, class_name)
            self.assign_mdc(timetable, class_name)
            self.assign_lunch(timetable, class_name)
            self.assign_language(timetable,class_name)
            self.assign_act(timetable,class_name)
            self.block_hours(timetable, class_name)
    def commerce(self):
       for d in range(self.num_days):
            if d==5:
               self.teacher_schedule[d][0].add(list1[0])
               self.teacher_schedule[d][1].add(list1[0])
               
               self.teacher_schedule[d][0].add(list2[0])
               self.teacher_schedule[d][1].add(list2[0])

               self.teacher_schedule[d][0].add(list3[0])
               self.teacher_schedule[d][1].add(list3[0])
            elif d==6:
                
               self.teacher_schedule[d][0].add(i for i in list1)
               self.teacher_schedule[d][1].add(i for i in list1)
               
               self.teacher_schedule[d][0].add(i for i in list2)
               self.teacher_schedule[d][1].add(i for i in list2)

               self.teacher_schedule[d][0].add(i for i in list3)
               self.teacher_schedule[d][1].add(i for i in list3)
                
       
       
        
           
    def assign_act(self, timetable, class_name):
        """Pre-assign 'activity' to the specific periods on Wednesday for different classes."""
        
        if 'act' in self.courses[class_name]:
                timetable[2][class_name][5].append(("activity", [""]))
           
                

                

            
    def assign_language(self, timetable, class_name):
        """Pre-assign 'language' to specific periods on Thursday and Friday for all classes."""
        
        if 'language' in self.courses[class_name]:
            if class_name in n_m:
                # Thursday (5th period)
                timetable[3][class_name][4].append(("English", []))
                # Friday (4th period)
                timetable[4][class_name][3].append(("English", [])) 
            elif class_name in m:
                # Tuesday (4th period)
                timetable[1][class_name][3].append(("language", []))
                # Thursday (4th period)
                timetable[3][class_name][3].append(("language", [])) 

    def assign_hed(self, timetable, class_name):
        """Pre-assign 'HED' to the 5th hour for all classes."""
        if 'HED' in self.courses[class_name]:
            timetable[0][class_name][4].append(("HED", []))  # 5th hour

    def assign_mdc(self, timetable, class_name):
        """Pre-assign 'MDC' to specific hours if the class has it."""
        if 'MDC' in self.courses[class_name]:  # Check if "MDC" exists for this class
            for hour in range(3, 5):  # 3rd and 4th hours on day 1
                timetable[1][class_name][hour].append(("MDC", []))
            # Pre-assign "MDC" to the 2nd hour on day 4
            timetable[3][class_name][4].append(("MDC", []))  # 2nd hour on day 4

    def assign_lunch(self, timetable, class_name):
        """Assign lunch based on the 'NOT MORNING' key."""
        for day in range(self.num_days):
            if day == 5:  # Skip Saturday
                continue
            if "NOT MORNING" in self.courses[class_name]:
                timetable[day][class_name][6].append(("LUNCH", []))  # 7th hour for lunch
            else:
                timetable[day][class_name][2].append(("LUNCH", []))  # 3rd hour for lunch

    def block_hours(self, timetable, class_name):
        """Block hours based on the 'NOT MORNING' key."""
        # Block the first two hours for classes with "NOT MORNING"
        if "NOT MORNING" in self.courses[class_name]:
            timetable[5][class_name][7].append(("BLOCKED", []))
            timetable[5][class_name][8].append(("BLOCKED", []))
            for hour in range(3):  # First two hours
                for day in range(self.num_days):
                    timetable[day][class_name][hour].append(("BLOCKED", []))  # Blocked hours

        # Block all hours after the 5th for classes without "NOT MORNING"
        if "NOT MORNING" not in self.courses[class_name]:
            timetable[5][class_name][5].append(("BLOCKED", []))
            timetable[5][class_name][6].append(("BLOCKED", []))
            for hour in range(6, len(timetable[0][class_name])):  # Start from the 6th hour
                for day in range(self.num_days):
                    timetable[day][class_name][hour].append(("BLOCKED", []))  # Blocked hours




    def assign_lca_and_lab_hours(self, timetable, allocated_subjects, lab_assigned_per_day):
        """
        Assigns lab and LCA hours to the timetable based on the number of hours mentioned for each subject.

        Args:
        timetable (list): The timetable structure.
        allocated_subjects (set): The set of subjects already allocated in the timetable.
        lab_assigned_per_day (list): A boolean list that tracks whether a lab has been assigned for each class per day.
        """
        for class_name in self.classes:
            # Check if LCA exists for this class
            if 'LCA' in self.courses[class_name]:  
                lca_subjects = self.courses[class_name]['LCA']

                # Iterate over each LCA subject for the class
                for subject_name, subject_info in lca_subjects.items():
                    # Handle lab hours first
                    lab_hours = subject_info["lab_hours"]  # Total required lab hours
                    teachers_for_subject = subject_info["teacher_incharge"]
                    assigned_lab_hours = 0

                    # Assign lab hours to the first available day and time
                    for day in range(self.num_days):
                        if assigned_lab_hours >= lab_hours:
                            break  # Stop if we've assigned all required lab hours

                        # Ensure that the lab hasn't been assigned already and the first two hours are free
                        if not lab_assigned_per_day[day][class_name]:
                            if (len(timetable[day][class_name][0]) == 0 and len(timetable[day][class_name][1]) == 0):
                                # Check if teachers are available
                                if all(teacher not in self.teacher_schedule[day][0] for teacher in teachers_for_subject):
                                    lab_venue = self.get_available_lab(day, 0)  # Get an available lab venue
                                    if lab_venue and self.is_lab_available(lab_venue, day, 0):  # Check if the lab is available
                                        # Assign the lab to the timetable and block the teacher's schedule
                                        self.assign_lab(timetable, day, class_name, 0, subject_name, teachers_for_subject, lab_venue, allocated_subjects, self.teacher_schedule)
                                        lab_assigned_per_day[day][class_name] = True
                                        assigned_lab_hours += 2  # Increment assigned lab hours by 2
                                        break  # Move to the next subject once lab hours are assigned

                    # Now, handle the normal LCA hours
                    required_hours = subject_info["normal_hours"]  # Required LCA hours
                    assigned_lca_hours = 0

                    # Assign LCA hours incrementally
                    for day in range(self.num_days):
                        if assigned_lca_hours >= required_hours:
                            break  # Stop if all required LCA hours have been assigned

                        # Check if we can assign two consecutive hours in the first two hours of the day
                        for hour in range(2):  # Only check hours 0 and 1
                            teachers_for_lca = subject_info["teacher_incharge"]
                            # Ensure both hours are free and teachers are available
                            can_assign = (len(timetable[day][class_name][hour]) == 0 and 
                                        len(timetable[day][class_name][hour + 1]) == 0 and
                                        all(teacher not in self.teacher_schedule[day][hour] and teacher not in self.teacher_schedule[day][hour + 1]
                                            for teacher in teachers_for_lca))

                            # Try to assign hours one by one to meet the required total
                            if can_assign:
                                if assigned_lca_hours + 1 <= required_hours:
                                    # Assign the first hour
                                    timetable[day][class_name][hour].append((subject_name, teachers_for_lca))
                                    for teacher in teachers_for_lca:
                                        self.teacher_schedule[day][hour].add(teacher)  # Block the teacher's schedule
                                    assigned_lca_hours += 1  # Increment the assigned LCA hours

                                if assigned_lca_hours < required_hours and assigned_lca_hours + 1 <= required_hours:
                                    # Assign the second hour
                                    timetable[day][class_name][hour + 1].append((subject_name, teachers_for_lca))
                                    for teacher in teachers_for_lca:
                                        self.teacher_schedule[day][hour + 1].add(teacher)  # Block the teacher's schedule
                                    assigned_lca_hours += 1  # Increment again

                                break  # Move to the next day after assigning hours

                        # If the LCA subject has been assigned for all required hours, stop assigning
                        if assigned_lca_hours >= required_hours:
                            break

    def assign_elective_subject(self, timetable, day, class_name, hour, subject_name, teachers_for_subject, teacher_schedule):
        # Check if the subject is already assigned for this hour
        if any(subject[0] == subject_name for subject in timetable[day][class_name][hour]):
            return False

        # Ensure teachers_for_subject is a list
        available_teachers = teachers_for_subject if isinstance(teachers_for_subject, list) else [teachers_for_subject]

        # Select a random teacher from available teachers
        if available_teachers:
            teacher = random.choice(available_teachers)
            timetable[day][class_name][hour].append((subject_name, [teacher]))
            self.teacher_schedule[day][hour].add(teacher)
            return True
        return False

    def assign_elective_hours(self, timetable, allocated_subjects, teacher_schedule):
        theory_hours_assigned = {day: {class_name: {} for class_name in self.courses.keys()} for day in range(self.num_days)}

        for class_name, class_data in self.courses.items():
            if class_name in [ele[0]]:
                for category, subjects in class_data.items():
                    if category in ["ELECTIVE-I", "Elective-II"]:
                        elective_subjects = list(subjects.keys())
                        if len(elective_subjects) < 2:
                            continue  # Skip if less than 2 subjects

                        subject1_name = elective_subjects[0]
                        subject1_info = subjects[subject1_name]
                        subject2_name = elective_subjects[1]
                        subject2_info = subjects[subject2_name]

                        normal_hours1 = subject1_info["normal_hours"]
                        normal_hours2 = subject2_info["normal_hours"]
                        teachers_for_subject1 = subject1_info["teacher_incharge"]
                        teachers_for_subject2 = subject2_info["teacher_incharge"]

                        assigned_theory_hours1 = 0
                        assigned_theory_hours2 = 0

                        while assigned_theory_hours1 < normal_hours1 or assigned_theory_hours2 < normal_hours2:
                            for day in range(self.num_days):
                                total_hours1_A = theory_hours_assigned[day][ele[0]].get(subject1_name, 0)
                                total_hours1_B = theory_hours_assigned[day][ele[1]].get(subject1_name, 0)
                                total_hours2_A = theory_hours_assigned[day][ele[0]].get(subject2_name, 0)
                                total_hours2_B = theory_hours_assigned[day][ele[1]].get(subject2_name, 0)

                                # Check availability for both subjects
                                if (total_hours1_A < 2 and total_hours1_B < 2 and 
                                    total_hours2_A < 2 and total_hours2_B < 2 and 
                                    subject1_name not in allocated_subjects[day][ele[0]] and 
                                    subject1_name not in allocated_subjects[day][ele[1]] and 
                                    subject2_name not in allocated_subjects[day][ele[0]] and 
                                    subject2_name not in allocated_subjects[day][ele[1]]):
                                    
                                    for hour in range(self.num_hours):
                                        if (len(timetable[day][ele[0]][hour]) == 0 and 
                                            len(timetable[day][ele[1]][hour]) == 0):
                                            
                                            # Check if teachers are free for both subjects
                                            teachers_available = (all(teacher not in self.teacher_schedule[day][hour] for teacher in teachers_for_subject1) and 
                                                                all(teacher not in self.teacher_schedule[day][hour] for teacher in teachers_for_subject2))

                                            if teachers_available:
                                                # Assign subject 1 if hours are available
                                                if assigned_theory_hours1 < normal_hours1:
                                                    if self.assign_elective_subject(timetable, day, ele[0], hour, subject1_name, teachers_for_subject1, teacher_schedule) and \
                                                    self.assign_elective_subject(timetable, day, ele[1], hour, subject1_name, teachers_for_subject1, teacher_schedule):
                                                        
                                                        for teacher in teachers_for_subject1:
                                                            self.teacher_schedule[day][hour].add(teacher)

                                                        theory_hours_assigned[day][ele[0]][subject1_name] = total_hours1_A + 1
                                                        allocated_subjects[day][ele[0]].add(subject1_name)
                                                        theory_hours_assigned[day][ele[1]][subject1_name] = total_hours1_B + 1
                                                        allocated_subjects[day][ele[1]].add(subject1_name)
                                                        assigned_theory_hours1 += 1

                                                # Assign subject 2 if hours are available
                                                if assigned_theory_hours2 < normal_hours2:
                                                    if self.assign_elective_subject(timetable, day, ele[0], hour, subject2_name, teachers_for_subject2, teacher_schedule) and \
                                                    self.assign_elective_subject(timetable, day, ele[1], hour, subject2_name, teachers_for_subject2, teacher_schedule):
                                                        
                                                        for teacher in teachers_for_subject2:
                                                            self.teacher_schedule[day][hour].add(teacher)

                                                        theory_hours_assigned[day][ele[0]][subject2_name] = total_hours2_A + 1
                                                        allocated_subjects[day][ele[0]].add(subject2_name)
                                                        theory_hours_assigned[day][ele[1]][subject2_name] = total_hours2_B + 1
                                                        allocated_subjects[day][ele[1]].add(subject2_name)
                                                        assigned_theory_hours2 += 1

                                                break  # Exit for loop if assignments are made

                                # Check if both subjects have been assigned the required hours
                                if assigned_theory_hours1 >= normal_hours1 and assigned_theory_hours2 >= normal_hours2:
                                    break

    
    def assign_elective_lab(self, timetable, allocated_subjects, lab_assigned_per_day, teacher_schedule):
        for class_name, class_data in self.courses.items():
            if class_name in ['5BCA A']:
                for category, subjects in class_data.items():
                    if category == "ELECTIVE-I":
                        assigned_lab_hours = 0
                        # Prepare subject names
                        subjects_to_assign = ["GRAPHICS AND ANIMATION", "BUSINESS INTELLIGENCE"]

                        for day in range(self.num_days):
                            if assigned_lab_hours >= sum(subjects[subject_name]["lab_hours"] for subject_name in subjects_to_assign):
                                break

                            # Check if both subjects can be assigned on the same day
                            if all(subject_name not in allocated_subjects[day][class_name] for subject_name in subjects_to_assign) and not lab_assigned_per_day[day][class_name]:
                                for hour in range(self.num_hours - 1):  # Ensure space for two hours
                                    # Check if both classes can be assigned in the same time slot
                                    if (len(timetable[day][ele[0]][hour]) == 0 and 
                                        len(timetable[day][ele[0]][hour + 1]) == 0 and 
                                        len(timetable[day][ele[1]][hour]) == 0 and 
                                        len(timetable[day][ele[1]][hour + 1]) == 0):

                                        # Collect teachers for both subjects
                                        teachers_for_ga = subjects["GRAPHICS AND ANIMATION"]["teacher_incharge"]
                                        teachers_for_bi = subjects["BUSINESS INTELLIGENCE"]["teacher_incharge"]
                                        
                                        teachers_available = (all(teacher not in self.teacher_schedule[day][hour] for teacher in teachers_for_ga) and 
                                                                all(teacher not in self.teacher_schedule[day][hour] for teacher in teachers_for_bi))

                                        # Check availability of teachers for both subjects
                                        if teachers_available : 
                                            lab_venue_ga = self.get_available_lab(day, hour)
                                            lab_venue_bi = self.get_available_lab(day, hour)  # Get a second lab for BI

                                            if lab_venue_ga and self.is_lab_available(lab_venue_ga, day, hour) and lab_venue_bi and self.is_lab_available(lab_venue_bi, day, hour):
                                                # Assign lab for 5BCA A - GA
                                                self.assign_lab(timetable, day, ele[0], hour, "GRAPHICS AND ANIMATION", teachers_for_ga, lab_venue_ga, allocated_subjects, teacher_schedule)
                                                lab_assigned_per_day[day][ele[0]] = True
                                                for teacher in teachers_for_ga:
                                                    self.teacher_schedule[day][hour].add(teacher)
                                                
                                                lab_venue_bi = self.get_available_lab(day, hour)  # Get a second lab for BI
                                                # Assign lab for 5BCA A - BI
                                                self.assign_lab(timetable, day, ele[0], hour, "BUSINESS INTELLIGENCE", teachers_for_bi, lab_venue_bi, allocated_subjects, teacher_schedule)
                                                lab_assigned_per_day[day][ele[0]] = True
                                                for teacher in teachers_for_bi:
                                                    self.teacher_schedule[day][hour].add(teacher)

                                                # Assign lab for 5BCA B - GA
                                                self.assign_lab(timetable, day, ele[1], hour, "GRAPHICS AND ANIMATION", teachers_for_ga, lab_venue_ga, allocated_subjects, teacher_schedule)
                                                lab_assigned_per_day[day][ele[1]] = True
                                                
                                                for teacher in teachers_for_ga:
                                                    self.teacher_schedule[day][hour].add(teacher)
                                                
                                                # Assign lab for 5BCA B - BI
                                                self.assign_lab(timetable, day, ele[1], hour, "BUSINESS INTELLIGENCE", teachers_for_bi, lab_venue_bi, allocated_subjects, teacher_schedule)
                                                lab_assigned_per_day[day][ele[1]] = True
                                                
                                                for teacher in teachers_for_bi:
                                                    self.teacher_schedule[day][hour].add(teacher)

                                                # Update assigned lab hours
                                                assigned_lab_hours += 4  # Two labs for each subject (4 in total)
                                                break  # Exit after assigning both subjects

    
    def assign_elective_hours_single_section(self, timetable, allocated_subjects, teacher_schedule, class_name):
        theory_hours_assigned = {day: {class_name: {} for day in range(self.num_days)} for day in range(self.num_days)}

        class_data = self.courses[class_name]
        for category, subjects in class_data.items():
            if category == "ELECTIVE-I":
                elective_subjects = list(subjects.keys())
                if len(elective_subjects) < 2:
                    continue  # Skip if less than 2 subjects

                subject1_name, subject2_name = elective_subjects[0], elective_subjects[1]
                subject1_info, subject2_info = subjects[subject1_name], subjects[subject2_name]

                normal_hours1, normal_hours2 = subject1_info["normal_hours"], subject2_info["normal_hours"]
                teachers_for_subject1, teachers_for_subject2 = subject1_info["teacher_incharge"], subject2_info["teacher_incharge"]

                assigned_theory_hours1, assigned_theory_hours2 = 0, 0

                while assigned_theory_hours1 < normal_hours1 or assigned_theory_hours2 < normal_hours2:
                    for day in range(self.num_days):
                        total_hours1 = theory_hours_assigned[day][class_name].get(subject1_name, 0)
                        total_hours2 = theory_hours_assigned[day][class_name].get(subject2_name, 0)

                        if (total_hours1 < 2 and total_hours2 < 2 and
                            subject1_name not in allocated_subjects[day][class_name] and
                            subject2_name not in allocated_subjects[day][class_name]):

                            for hour in range(self.num_hours):
                                if len(timetable[day][class_name][hour]) == 0:  # If the hour is free
                                    # Check if the teacher is free for both subjects
                                    if (all(teacher not in self.teacher_schedule[day][hour] for teacher in teachers_for_subject1) and
                                        all(teacher not in self.teacher_schedule[day][hour] for teacher in teachers_for_subject2)):
                                        
                                        # Assign subject 1
                                        if assigned_theory_hours1 < normal_hours1:
                                            self.assign_elective_subject(timetable, day, class_name, hour, subject1_name, teachers_for_subject1, teacher_schedule)
                                            for teacher in teachers_for_subject1:
                                                self.teacher_schedule[day][hour].add(teacher)
                                            
                                            theory_hours_assigned[day][class_name][subject1_name] = total_hours1 + 1
                                            allocated_subjects[day][class_name].add(subject1_name)
                                            assigned_theory_hours1 += 1

                                        # Assign subject 2
                                        if assigned_theory_hours2 < normal_hours2:
                                            self.assign_elective_subject(timetable, day, class_name, hour, subject2_name, teachers_for_subject2, teacher_schedule)
                                            for teacher in teachers_for_subject2:
                                                self.teacher_schedule[day][hour].add(teacher)
                                            theory_hours_assigned[day][class_name][subject2_name] = total_hours2 + 1
                                            allocated_subjects[day][class_name].add(subject2_name)
                                            assigned_theory_hours2 += 1

                                        break  # Exit loop to re-evaluate assigned hours

                        if assigned_theory_hours1 >= normal_hours1 and assigned_theory_hours2 >= normal_hours2:
                            break

    def assign_lab_hours_multiple_electives(self, timetable, allocated_subjects, lab_assigned_per_day, teacher_schedule, class_name):
        for category, subjects in self.courses[class_name].items():
            if category == "ELECTIVE-I":
                elective_subjects = list(subjects.keys())
                if len(elective_subjects) < 2:
                    continue  # Skip if less than 2 subjects

                # Get the first two elective subjects
                subject1_name = elective_subjects[0]
                subject2_name = elective_subjects[1]
                subject1_info = subjects[subject1_name]
                subject2_info = subjects[subject2_name]

                lab_hours1 = subject1_info["lab_hours"]
                lab_hours2 = subject2_info["lab_hours"]
                teachers_for_subject1 = subject1_info["teacher_incharge"]
                teachers_for_subject2 = subject2_info["teacher_incharge"]

                assigned_lab_hours1 = 0
                assigned_lab_hours2 = 0

                for day in range(self.num_days):
                    if assigned_lab_hours1 >= lab_hours1 and assigned_lab_hours2 >= lab_hours2:
                        break

                    # Check if lab hours can be assigned for both subjects
                    if (subject1_name not in allocated_subjects[day][class_name] and 
                        subject2_name not in allocated_subjects[day][class_name] and
                        not lab_assigned_per_day[day][class_name]):
                        
                        for hour in range(self.num_hours - 1):  # Ensure space for two hours
                            # Check if both hours are free
                            if (len(timetable[day][class_name][hour]) == 0 and 
                                len(timetable[day][class_name][hour + 1]) == 0):

                                # Check if the teachers are free for both subjects
                                if (all(teacher not in self.teacher_schedule[day][hour] for teacher in teachers_for_subject1) and
                                    all(teacher not in self.teacher_schedule[day][hour] for teacher in teachers_for_subject2)):
                                    
                                    lab_venue1 = self.get_available_lab(day, hour)
                                    lab_venue2 = self.get_available_lab(day, hour)  # Assuming same lab for both subjects
                                    
                                    if lab_venue1 and self.is_lab_available(lab_venue1, day, hour):
                                        # Assign lab for both subjects in the same hour
                                        self.assign_lab(timetable, day, class_name, hour, subject1_name, teachers_for_subject1, lab_venue1, allocated_subjects, teacher_schedule)
                                        for teacher in teachers_for_subject1:
                                            self.teacher_schedule[day][hour].add(teacher)
                                        self.assign_lab(timetable, day, class_name, hour, subject2_name, teachers_for_subject2, lab_venue2, allocated_subjects, teacher_schedule)
                                        for teacher in teachers_for_subject2:
                                            self.teacher_schedule[day][hour].add(teacher)
                                        
                                        lab_assigned_per_day[day][class_name] = True
                                        assigned_lab_hours1 += 2  # Increment for subject 1
                                        assigned_lab_hours2 += 2  # Increment for subject 2
                                        break  # Exit the loop to re-evaluate lab assignments

                    if assigned_lab_hours1 >= lab_hours1 and assigned_lab_hours2 >= lab_hours2:
                        break  # Exit if all lab hours have been assigned

    
                                                    
    def assign_lab_hours(self, timetable, allocated_subjects, lab_assigned_per_day, teacher_schedule):
            lab_venues = ["BCA Lab", "MCA Lab", "BSc Lab"]

            for class_name, class_data in self.courses.items():
                for category, subjects in class_data.items():
                    if category not in ["LCA", "ELECTIVE-I",  "HED", "MDC","Elective-II","act"]:
                        for subject_name, subject_info in subjects.items():
                                lab_hours = subject_info["lab_hours"]
                                teachers_for_subject = subject_info.get("teacher_incharge", [])
                                assigned_lab_hours = 0

                                for day in range(self.num_days):
                                    if assigned_lab_hours >= lab_hours:
                                        break
                                    if subject_name not in allocated_subjects[day][class_name] and not lab_assigned_per_day[day][class_name]:
                                        for hour in range(self.num_hours - 1):  # Ensure space for two hours
                                            if len(timetable[day][class_name][hour]) == 0 and len(timetable[day][class_name][hour + 1]) == 0:
                                                t=all(teacher not in self.teacher_schedule[day][hour] for teacher in teachers_for_subject)
                                                if t:
                                                    lab_venue = self.get_available_lab(day, hour)
                                                    if lab_venue and self.is_lab_available(lab_venue, day, hour):
                                                        self.assign_lab(timetable, day, class_name, hour, subject_name, teachers_for_subject, lab_venue, allocated_subjects, teacher_schedule)
                                                        lab_assigned_per_day[day][class_name] = True
                                                        assigned_lab_hours += 2
                                                        break
    
    def assign_theory_hours(self, timetable, allocated_subjects, theory_hours_assigned, teacher_schedule):
        for class_name, class_data in self.courses.items():
            for category, subjects in class_data.items():
                if category not in ["LCA", "ELECTIVE-I",  "HED", "MDC","Elective-II","act"]:
                    for subject_name, subject_info in subjects.items():
                        normal_hours = subject_info["normal_hours"]
                        teachers_for_subject = subject_info["teacher_incharge"]

                        # Proceed only if normal_hours is greater than 0
                        if normal_hours > 0:
                            assigned_theory_hours = 0

                            for day in range(self.num_days):
                                # Check if assigned theory hours have reached normal_hours limit
                                if assigned_theory_hours >= normal_hours:
                                    break

                                total_hours = theory_hours_assigned[day][class_name].get(subject_name, 0)

                                # Check if more hours can be assigned for this subject
                                if total_hours < 2 and subject_name not in allocated_subjects[day][class_name]:
                                    for hour in range(self.num_hours):
                                        if len(timetable[day][class_name][hour]) == 0:  # If the hour is free
                                            # Check if any teacher for the subject is available
                                            t=any(teacher not in self.teacher_schedule[day][hour] for teacher in teachers_for_subject)
                                            if t:
                                                self.assign_subject(timetable, day, class_name, hour, subject_name, teachers_for_subject, category, teacher_schedule)
                                                for teacher in teachers_for_subject:
                                                    self.teacher_schedule[day][hour].add(teacher)
                                                    
                                                theory_hours_assigned[day][class_name][subject_name] = total_hours + 1
                                                allocated_subjects[day][class_name].add(subject_name)
                                                assigned_theory_hours += 1  # Increment assigned hours
                                                break  # Move to the next subject

                                    if assigned_theory_hours >= normal_hours:
                                        break  # Exit the loop once normal hours are assigned

                            # Check if the exact number of required theory hours was assigned
                            if assigned_theory_hours < normal_hours:
                                self.allocate_missing_hours_for_subject( class_name, subject_name, timetable, theory_hours_assigned, allocated_subjects, teacher_schedule,category)
                                # print(f"Warning: Could not assign the exact number of theory hours for {subject_name} in {class_name}. Assigned: {assigned_theory_hours}, Required: {normal_hours}")
                                
    
    def allocate_missing_hours_for_subject(self, class_name, subject_name, timetable, theory_hours_assigned, allocated_subjects, teacher_schedule,c="NORMAL"):
        # Access the relevant data for the specific class and subject
        subject_info = self.courses[class_name][c].get(subject_name)
        
        if not subject_info:
            print(f"Subject {subject_name} not found in class {class_name}.")
            return
        
        normal_hours = subject_info["normal_hours"]
        assigned_hours = sum(
            theory_hours_assigned[day][class_name].get(subject_name, 0) for day in range(self.num_days)
        )
        
        # Check if assigned hours are less than normal hours
        if assigned_hours < normal_hours:
            hours_to_allocate = normal_hours - assigned_hours
            
            print(f"Allocating hours for {subject_name} in {class_name}")
            print(f"Normal hours: {normal_hours}, Assigned hours: {assigned_hours}, Hours to allocate: {hours_to_allocate}")
            
            # Get free hours for teachers and class
            teachers_for_subject = subject_info["teacher_incharge"]
            free_teacher_hours = self.get_free_teacher_hours(teacher_schedule, teachers_for_subject)
            free_class_hours = self.get_free_class_hours(timetable, class_name)

            # Attempt to allocate the missing hours
            for day in range(self.num_days):
                if hours_to_allocate <= 0:
                    print(f"All required hours for {subject_name} have been allocated.")
                    break  # Exit if all required hours have been allocated

                total_hours_day = theory_hours_assigned[day][class_name].get(subject_name, 0)

                # # Debugging check: Print if more than 2 hours are already assigned for the day
                if total_hours_day >= 2:
                    print(f"Skipping day {day} for {subject_name} as 2 hours already assigned.")
                    continue

                # Find the available slots for both teacher and class
                available_slots = free_teacher_hours[day].intersection(free_class_hours[day])

                # Allocate hours from available slots
                for hour in available_slots:
                    # Check if the subject has already been allocated at this time
                    # if subject_name in allocated_subjects[day][class_name]:
                    #     print(f"Skipping day {day}, hour {hour}: {subject_name} already allocated for this class.")
                    #     continue
                    
                    # Assign subject and update records
                    print(f"Assigning {subject_name} to class {class_name} on day {day}, hour {hour}.")
                    self.assign_subject(timetable, day, class_name, hour, subject_name, teachers_for_subject, "NORMAL", teacher_schedule)
                   
                                   
                    theory_hours_assigned[day][class_name][subject_name] = total_hours_day + 1
                    allocated_subjects[day][class_name].add(subject_name)
                    total_hours_day += 1  # Increment day total
                    hours_to_allocate -= 1  # Decrement the hours to allocate
                    
                    # Break if all hours have been allocated
                    if hours_to_allocate <= 0:
                        print(f"All required hours for {subject_name} have been allocated.")
                        break

                # Stop assigning if all needed hours have been allocated
                if hours_to_allocate <= 0:
                    break

            # Optional: Check if after allocation there are still unallocated hours
            if hours_to_allocate > 0:
                print(f"Warning: Unable to allocate all required hours for {subject_name} in {class_name}. Remaining hours to allocate: {hours_to_allocate}.")
        else:
            print(f"{subject_name} in {class_name} already has all required hours allocated.")

    
        
    def get_free_teacher_hours(self, teacher_schedule, teachers_for_subject):
        free_teacher_hours = {}

        for day in range(self.num_days):
            free_hours = set()  # Set to hold all free hours for the day
            for hour in range(self.num_hours):
                for teacher in teachers_for_subject:
                    if teacher not in self.teacher_schedule[day][hour]:  # Teacher is free
                        free_hours.add(hour)  # Add the hour to the set of free hours
                        break  # Exit the loop as we found at least one free teacher for this hour
            free_teacher_hours[day] = free_hours  # Assign the set of free hours for the day

        return free_teacher_hours

    def get_free_class_hours(self, timetable, class_name):
        free_class_hours = {}

        for day in range(self.num_days):
            free_hours = set()  # Set to hold all free hours for the class
            for hour in range(self.num_hours):
                if len(timetable[day][class_name][hour]) == 0:  # Class is free at this hour
                    free_hours.add(hour)  # Add the hour to the set of free hours
            free_class_hours[day] = free_hours  # Assign the set of free hours for the day

        return free_class_hours


    



    def assign_subject(self, timetable, day, class_name, hour, subject_name, teachers_for_subject, category, teacher_schedule):
        if category == "GROUP TEACHING":
            assigned_teachers = []
            for teacher in teachers_for_subject:
                if teacher not in self.teacher_schedule[day][hour]:  # Ensure no double booking
                    assigned_teachers.append(teacher)
                    self.teacher_schedule[day][hour].add(teacher)  # Mark teacher as assigned for this hour

            if assigned_teachers:
                timetable[day][class_name][hour].append((subject_name, assigned_teachers))
                return True  # Return True indicating the subject was assigned
            else:
                print(f"No available teachers for group teaching of {subject_name} in {class_name} on day {day}, hour {hour}.")
                return False  # Return False indicating assignment failed

        elif category == "NORMAL":
            if not any(subject[0] == subject_name for subject in timetable[day][class_name][hour]):
                teacher = random.choice(teachers_for_subject)
                if teacher not in self.teacher_schedule[day][hour]:  # Ensure no double booking
                    timetable[day][class_name][hour].append((subject_name, [teacher]))
                    self.teacher_schedule[day][hour].add(teacher)  # Mark teacher as assigned for this hour
                    return True  # Return True indicating the subject was assigned
                else:
                    print(f"Teacher {teacher} is already booked for {subject_name} in {class_name} on day {day}, hour {hour}.")
                    return False  # Return False indicating assignment failed
            else:
                print(f"{subject_name} is already assigned in {class_name} on day {day}, hour {hour}.")
                return False  # Return False indicating assignment failed




    def get_available_lab(self, day, hour):
        # Check available lab rooms for the specified day and hour
        for lab_name in self.lab_timetables.keys():
            if len(self.lab_timetables[lab_name][day][hour]) == 0 and len(self.lab_timetables[lab_name][day][hour + 1]) == 0:
                return lab_name
        return None

    def is_lab_available(self, lab_name, day, hour):
        return len(self.lab_timetables[lab_name][day][hour]) == 0

    def assign_lab(self, timetable, day, class_name, hour, subject_name, teachers_for_subject, lab_venue, allocated_subjects, teacher_schedule):
        # Store subject, teachers, and lab venue
        self.lab_count[class_name][subject_name]=len(teachers_for_subject)
        
        timetable[day][class_name][hour].append((subject_name, teachers_for_subject, lab_venue))  # Store all teachers and lab venue
        timetable[day][class_name][hour + 1].append((subject_name, teachers_for_subject, lab_venue))  # Assign for the next hour
        self.lab_timetables[lab_venue][day][hour].append((subject_name, teachers_for_subject))
        self.lab_timetables[lab_venue][day][hour + 1].append((subject_name, teachers_for_subject))
        allocated_subjects[day][class_name].add(subject_name)
        for teacher in teachers_for_subject:
            self.teacher_schedule[day][hour].add(teacher)
            self.teacher_schedule[day][hour + 1].add(teacher)

        return timetable
    
    def get_free_hours_timetable(self, timetable):
        free_hours = set()  # Set to store free hours

        for day in range(self.num_days):
            for class_name in self.classes:
                for hour in range(self.num_hours):
                    # If the hour is free (i.e., no subjects assigned)
                    if len(timetable[day][class_name][hour]) == 0:
                        free_hours.add((day, hour, class_name))  # Add the free slot to the set

        return free_hours
    

    
    def create_class_dataframes(self, timetable):
        all_class_dfs = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        for class_name in self.classes:
            data = {day: [] for day in days}

            for day in range(self.num_days):
                for hour in range(self.num_hours):
                    subjects = timetable[day][class_name][hour]
                    if subjects:
                        subject_info = []
                        for subject in subjects:
                            subject_short_name = shortsub.get(subject[0], subject[0])  # Short form of subject
                            teachers = ', '.join([short_teachers.get(teacher.strip(), teacher) for teacher in subject[1]])  # Short form of teachers
                            if len(subject) == 3:  # Lab
                                subject_info.append(f"{subject_short_name} (Lab - {subject[2]} by {teachers})")
                            else:  # Theory
                                subject_info.append(f"{subject_short_name} by {teachers}")

                        # Join subject info with new line for better readability
                        data[days[day]].append('\n'.join(subject_info))
                    else:
                        data[days[day]].append("Free")

            # Create DataFrame for this class
            df = pd.DataFrame(data)
            df.index = [f"Hour {hour + 1}" for hour in range(self.num_hours)]
            all_class_dfs[class_name] = df

            # Adjust cell sizes based on content
            self.adjust_dataframe_cells(df)

        return all_class_dfs

    def create_teacher_dataframes(self, timetable):
        all_teacher_dfs = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        # Collect all unique teachers from courses
        teachers = set()
        for class_data in self.courses.values():
            for category, subjects in class_data.items():
                for subject_info in subjects.values():
                    teachers.update(subject_info.get("teacher_incharge", []))

        teachers = teachers.intersection(set(short_teachers.keys()))

        # Initialize a timetable for each teacher
        for teacher in teachers:
            data = {day: [] for day in days}

            for day in range(self.num_days):
                for hour in range(self.num_hours):
                    subject_info = []
                    for class_name in self.classes:
                        subjects = timetable[day][class_name][hour]
                        for subject in subjects:
                            if teacher in subject[1]:  # If teacher is assigned
                                subject_short_name = shortsub.get(subject[0], subject[0])  # Short form of subject
                                subject_info.append(f"{subject_short_name} ({class_name})")

                    # Join subject info with new line for better readability
                    data[days[day]].append('\n'.join(subject_info) if subject_info else "Free")

            # Create DataFrame for this teacher
            df = pd.DataFrame(data)
            df.index = [f"Hour {hour + 1}" for hour in range(self.num_hours)]
            all_teacher_dfs[teacher] = df

            # Adjust cell sizes based on content
            self.adjust_dataframe_cells(df)

        return all_teacher_dfs

    def create_lab_dataframes(self, timetable):
        all_lab_dfs = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        for lab in self.lab_timetables.keys():
            data = {day: [] for day in days}

            for day in range(self.num_days):
                for hour in range(self.num_hours):
                    subjects_info = []
                    for class_name in self.classes:
                        subjects = timetable[day][class_name][hour]
                        for subject in subjects:
                            if isinstance(subject, tuple) and len(subject) == 3:  # Lab subject
                                subject_name = subject[0]
                                teachers_for_subject = subject[1]
                                lab_venue = subject[2]
                                subject_short_name = shortsub.get(subject_name, subject_name)

                                # Check if current lab matches the subject's lab
                                if lab_venue == lab:
                                    teachers = ', '.join([short_teachers.get(teacher.strip(), teacher) for teacher in teachers_for_subject])
                                    subjects_info.append(f"{subject_short_name} (Lab - {lab} by {teachers}) in {class_name}")

                    data[days[day]].append('\n'.join(subjects_info) if subjects_info else "Free")

            # Create DataFrame for this lab
            df = pd.DataFrame(data)
            df.index = [f"Hour {hour + 1}" for hour in range(self.num_hours)]
            all_lab_dfs[lab] = df

            # Adjust cell sizes based on content
            self.adjust_dataframe_cells(df)

        return all_lab_dfs

    def adjust_dataframe_cells(self, df):
        """ Adjust the cell size based on content for better display. """
        # Maximum length for columns based on content
        max_length = {col: max(df[col].astype(str).map(len).max(), len(col)) for col in df.columns}

        # Set a minimum width (for example, 35 characters) and maximize width
        for column in df.columns:
            max_length[column] = max(max_length[column], 35)  # Minimum width of 35 characters

            # Left justify each cell content
            df[column] = df[column].apply(lambda x: x.ljust(max_length[column]))

        # Also adjust the index (hour labels)
        max_index_length = max(df.index.astype(str).map(len).max(), len("Hour N"))
        df.index = df.index.map(lambda x: x.ljust(max_index_length))  # Left justify index labels




    
    def finalize_timetable(self, timetable, theory_hours_assigned, allocated_subjects, teacher_schedule):
        # For each class and subject, ensure all hours are allocated
        for class_name, class_data in self.courses.items():

                for subject_name, subject_info in class_data["NORMAL"].items():
                    normal_hours = subject_info["normal_hours"]
                    assigned_hours = sum(
                        theory_hours_assigned[day][class_name].get(subject_name, 0) for day in range(self.num_days)
                    )

                    # If the assigned hours are less than the required normal hours, allocate the missing hours
                    if assigned_hours < normal_hours:
                        print(f"Allocating missing hours for {subject_name} in {class_name}...")
                        self.allocate_missing_hours_for_subject(
                            class_name, subject_name, timetable, theory_hours_assigned, allocated_subjects, teacher_schedule
                    )
                        
    
    def style_excel_sheet(self,file_name, output_file_name):
        # Load the workbook
        workbook = openpyxl.load_workbook(file_name)

        # Define styles
        header_font = Font(bold=True, color="FFFFFF")  # White text
        header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")  # Blue background
        border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

        # Iterate over each sheet in the workbook
        for sheet in workbook.worksheets:
            # Adjust column widths and style headers
            for column in sheet.columns:
                max_length = 0
                column_letter = column[0].column_letter  # Get the column letter (e.g., 'A', 'B', 'C', etc.)
                
                for cell in column:
                    # Adjust maximum length for column width
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                    
                    # Apply borders to each cell
                    cell.border = border
                
                adjusted_width = (max_length + 2)  # Add a little extra space for padding
                sheet.column_dimensions[column_letter].width = adjusted_width  # Set the width

            # Style the header row (assumes headers are in the first row)
            for cell in sheet[1]:  # The first row (index 1)
                cell.font = header_font
                cell.fill = header_fill
                cell.border = border

        # Save the modified workbook
        workbook.save(output_file_name)  # Save it with the specified output filename

                        


        







if __name__ == "__main__":
    timetable_generator = TimetableGenerator(courses)
    timetable = timetable_generator.generate_timetable()

    # Create DataFrames for each class
    class_dataframes = timetable_generator.create_class_dataframes(timetable)

    # Create DataFrames for each teacher
    teacher_dataframes = timetable_generator.create_teacher_dataframes(timetable)

    lab_dataframes = timetable_generator.create_lab_dataframes(timetable)

    # Save each class DataFrame to separate sheets in an Excel file
    with pd.ExcelWriter("timetable.xlsx") as writer:
        for class_name, df in class_dataframes.items():
            df.to_excel(writer, sheet_name=class_name, index=True)
        
        for lab_name, df in lab_dataframes.items():
            df.to_excel(writer, sheet_name=lab_name, index=True)
    

    # Save teacher DataFrames to separate sheets
    with pd.ExcelWriter("teachertimetable.xlsx") as writer:
        for teacher_name, df in teacher_dataframes.items():
            df.to_excel(writer, sheet_name=teacher_name, index=True)
    
    timetable_generator.style_excel_sheet('timetable.xlsx', 'timetable.xlsx')
    timetable_generator.style_excel_sheet('teachertimetable.xlsx', 'teachertimetable.xlsx')
            
    print("Timetable saved to 'timetable.xlsx'.")
    
    

    # def record_assigned_classes(self):
    #     assigned_classes_record = {}
        
    #     for day in range(len(self.timetable)):  # Iterate over each day
    #         for class_name in self.timetable[day]:  # Iterate over each class on that day
    #             if class_name not in assigned_classes_record:
    #                 assigned_classes_record[class_name] = {}  # Initialize if class not already in record

    #             for hour in self.timetable[day][class_name]:  # Iterate over each hour
    #                 for entry in self.timetable[day][class_name][hour]:  # Get all entries in the timetable for that hour
    #                     if isinstance(entry, tuple) and len(entry) >= 1:
    #                         subject = entry[0]  # First element is the subject name
    #                         is_lab = 'Lab' in subject  # Check if this is a lab subject

    #                         # Initialize the subject in the record if it's not already there
    #                         if subject not in assigned_classes_record[class_name]:
    #                             assigned_classes_record[class_name][subject] = {'normal_hours': 0, 'lab_hours': 0}

    #                         # Increment the appropriate count for normal or lab hours
    #                         if is_lab:
    #                             assigned_classes_record[class_name][subject]['lab_hours'] += 1
    #                         else:
    #                             assigned_classes_record[class_name][subject]['normal_hours'] += 1
        
    #     return assigned_classes_record
    
    # def print_assigned_hours(self, assigned_hours):
    #     print("\nAssigned Hours Summary:")
    #     for class_name, subjects in assigned_hours.items():
    #         print(f"\nClass: {class_name}")
    #         print(f"{'Subject':<30}{'Normal Hours':<15}{'Lab Hours':<15}")
    #         print('-' * 60)
    #         for subject_name, hours in subjects.items():
    #             normal_hours = hours['normal_hours']
    #             lab_hours = hours['lab_hours']
    #             print(f"{subject_name:<30}{normal_hours:<15}{lab_hours:<15}")
    #         print('-' * 60)
            
    # def compare_assigned_with_expected(self, assigned_classes_record):
    #     discrepancies = {}
        
    #     # Iterate through each class and subject in the courses data to compare hours
    #     for class_name, class_data in self.courses.items():
    #         for category, subjects in class_data.items():
    #             for subject_name, subject_info in subjects.items():
    #                 expected_normal_hours = subject_info.get('normal_hours', 0)
    #                 expected_lab_hours = subject_info.get('lab_hours', 0)
                    
    #                 # Get the assigned hours from the recorded assigned_classes_record
    #                 assigned_normal_hours = assigned_classes_record.get(class_name, {}).get(subject_name, {}).get('normal_hours', 0)
    #                 assigned_lab_hours = assigned_classes_record.get(class_name, {}).get(subject_name, {}).get('lab_hours', 0)

    #                 # Check for discrepancies
    #                 if expected_normal_hours != assigned_normal_hours or expected_lab_hours != assigned_lab_hours:
    #                     discrepancies.setdefault(class_name, {}).setdefault(subject_name, {
    #                         'expected_normal_hours': expected_normal_hours,
    #                         'expected_lab_hours': expected_lab_hours,
    #                         'assigned_normal_hours': assigned_normal_hours,
    #                         'assigned_lab_hours': assigned_lab_hours,
    #                     })
        
    #     # Print the discrepancies
    #     if discrepancies:
    #         print("\nDiscrepancies Found Between Assigned and Expected Hours:")
    #         for class_name, subjects in discrepancies.items():
    #             print(f"\nClass: {class_name}")
    #             print(f"{'Subject':<30}{'Expected Normal':<20}{'Assigned Normal':<20}{'Expected Lab':<20}{'Assigned Lab':<20}")
    #             print('-' * 90)
    #             for subject_name, hours in subjects.items():
    #                 print(f"{subject_name:<30}{hours['expected_normal_hours']:<20}{hours['assigned_normal_hours']:<20}"
    #                     f"{hours['expected_lab_hours']:<20}{hours['assigned_lab_hours']:<20}")
    #             print('-' * 90)
    #     else:
    #         print("\nAll hours are correctly assigned as per the course requirements.")
    


    # def get_teachers_for_first_two_hours(self, timetable):
    #     teachers_first_two_hours = set()

    #     # Iterate over all days
    #     for day in range(self.num_days):
    #         # Focus only on the first two hours (Hour 0 and Hour 1)
    #         for hour in range(2):  
    #             # Check each class
    #             for class_name in self.classes:
    #                 subjects = timetable[day][class_name][hour]
    #                 # Check all subjects being taught during this hour
    #                 for subject in subjects:
    #                     teachers = subject[1]  # List of teachers for the subject
    #                     # Add each teacher to the set (avoids duplicates)
    #                     teachers_first_two_hours.update(teachers)

    #     return teachers_first_two_hours

    # def block_third_hour_for_teachers(self, timetable, teacher_schedule):
    #     # Get the set of teachers who are scheduled for the first two hours
    #     teachers_first_two_hours = self.get_teachers_for_first_two_hours(timetable)

    #     # Iterate over each day
    #     for day in range(self.num_days):
    #         # For each teacher scheduled in the first two hours
    #         for teacher in teachers_first_two_hours:
    #             # If teacher_schedule for the third hour (hour 2) doesn't contain "lunch"
    #             if "lunch" not in teacher_schedule[day][2]:  # Check if not already blocked
    #                 teacher_schedule[day][2] = {"lunch"}  # Overwrite the third hour with "lunch"
    #                 print(f"Blocked 3rd hour for {teacher} on day {day} as 'lunch'.")
    #             else:
    #                 print(f"3rd hour for {teacher} on day {day} is already blocked as 'lunch'.")

    #     return teacher_schedule  # Optional return to check changes externally
    
    
    
    # def generate_timetable(self):
    #     # Initialize timetable structure
    #     timetable = self.initialize_timetable()
    #     allocated_subjects, theory_hours_assigned, lab_assigned_per_day, teacher_schedule = self.initialize_tracking_structures()

    #     # Pre-assign subjects
    #     self.pre_assign_subjects(timetable)
            
    #     self.assign_elective_lab(timetable, allocated_subjects, lab_assigned_per_day, teacher_schedule)
    #     self.assign_elective_hours_single_section(timetable, allocated_subjects, teacher_schedule, "5CME")
    #     self.assign_lab_hours_multiple_electives(timetable, allocated_subjects, lab_assigned_per_day, teacher_schedule, "5CME")
        
    #     # # # Assign LCA subjects to the first two hours of the day
    #     self.assign_lca_and_lab_hours(timetable, allocated_subjects, lab_assigned_per_day)
       
    #     # Assign lab hours and theory hours
    #     self.assign_lab_hours(timetable, allocated_subjects, lab_assigned_per_day, teacher_schedule)
    #     # self.finalize_timetable(timetable, theory_hours_assigned, allocated_subjects, teacher_schedule)
    #     self.assign_theory_hours(timetable, allocated_subjects, theory_hours_assigned, teacher_schedule)
        
    #      #  #  # Assign all elective subjects at the same time for both sections A and B
    #     self.assign_elective_hours(timetable, allocated_subjects, teacher_schedule)
       
       
    #     self.timetable = timetable

    #     return timetable
    
    
    # fix eng and act
    
    


