import random
import pandas as pd
from data import courses, short_teachers, shortsub, elective_classes,CLASSES

class TimetableGenerator:
    def __init__(self, courses, num_days=6, num_hours=8):
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

        self.assign_elective_hours_single_section(timetable, allocated_subjects, teacher_schedule, "5CME")
        self.assign_lab_hours_multiple_electives(timetable, allocated_subjects, lab_assigned_per_day, teacher_schedule, "5CME")
       
        # Assign lab hours and theory hours
        self.assign_lab_hours(timetable, allocated_subjects, lab_assigned_per_day, teacher_schedule)
        self.assign_theory_hours(timetable, allocated_subjects, theory_hours_assigned, teacher_schedule)
        
        self.timetable = timetable

        return timetable
        

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
            self.assign_hed(timetable, class_name)
            self.assign_mdc(timetable, class_name)
            self.assign_lunch(timetable, class_name)
            self.block_hours(timetable, class_name)

    def assign_hed(self, timetable, class_name):
        """Pre-assign 'HED' to the 5th hour for all classes."""
        if 'HED' in self.courses[class_name]:
            timetable[0][class_name][4].append(("HED", ["Dr. John Doe"]))  # 5th hour

    def assign_mdc(self, timetable, class_name):
        """Pre-assign 'MDC' to specific hours if the class has it."""
        if 'MDC' in self.courses[class_name]:  # Check if "MDC" exists for this class
            for hour in range(2, 4):  # 3rd and 4th hours on day 1
                timetable[1][class_name][hour].append(("MDC", ["Dr. Jane Smith"]))
            # Pre-assign "MDC" to the 2nd hour on day 4
            timetable[3][class_name][1].append(("MDC", ["Dr. Jane Smith"]))  # 2nd hour on day 4

    def assign_lunch(self, timetable, class_name):
        """Assign lunch based on the 'NOT MORNING' key."""
        for day in range(self.num_days):
            if day == 5:  # Skip Saturday
                continue
            if "NOT MORNING" in self.courses[class_name]:
                timetable[day][class_name][5].append(("LUNCH", ["-"]))  # 6th hour for lunch
            else:
                timetable[day][class_name][2].append(("LUNCH", ["-"]))  # 3rd hour for lunch

    def block_hours(self, timetable, class_name):
        """Block hours based on the 'NOT MORNING' key."""
        # Block the first two hours for classes with "NOT MORNING"
        if "NOT MORNING" in self.courses[class_name]:
            for hour in range(2):  # First two hours
                for day in range(self.num_days):
                    timetable[day][class_name][hour].append(("BLOCKED", ["-"]))  # Blocked hours

        # Block all hours after the 5th for classes without "NOT MORNING"
        if "NOT MORNING" not in self.courses[class_name]:
            for hour in range(6, len(timetable[0][class_name])):  # Start from the 6th hour
                for day in range(self.num_days):
                    timetable[day][class_name][hour].append(("BLOCKED", ["-"]))  # Blocked hours




    def assign_lca_and_lab_hours(self, timetable, allocated_subjects, lab_assigned_per_day):
        for class_name in self.classes:
            if 'LCA' in self.courses[class_name]:  # Check if LCA exists for this class
                lca_subjects = self.courses[class_name]['LCA']

                for subject_name, subject_info in lca_subjects.items():
                    # Now, handle lab hours
                    lab_hours = subject_info["lab_hours"]
                    teachers_for_subject = subject_info["teacher_incharge"]
                    assigned_lab_hours = 0

                    for day in range(self.num_days):
                        if assigned_lab_hours >= lab_hours:
                            break
                        if not lab_assigned_per_day[day][class_name]:
                            if (len(timetable[day][class_name][0]) == 0 and len(timetable[day][class_name][1]) == 0):
                                if all(teacher not in self.teacher_schedule[day][0] for teacher in teachers_for_subject):
                                    lab_venue = self.get_available_lab(day, 0)
                                    if lab_venue and self.is_lab_available(lab_venue, day, 0):
                                        self.assign_lab(timetable, day, class_name, 0, subject_name, teachers_for_subject, lab_venue, allocated_subjects, self.teacher_schedule)
                                        lab_assigned_per_day[day][class_name] = True
                                        assigned_lab_hours += 2
                                        break

                    # Assign normal LCA hours
                    required_hours = subject_info["normal_hours"]
                    assigned_lca_hours = 0

                    for day in range(self.num_days):
                        if assigned_lca_hours >= required_hours:
                            break

                        # Check if LCA can be assigned in the first two hours
                        for hour in range(2):  # Only check the first two hours (0 and 1)
                            teachers_for_lca = subject_info["teacher_incharge"]
                            # Ensure both hours are free and teachers are available
                            if (len(timetable[day][class_name][hour]) == 0 and 
                                    len(timetable[day][class_name][hour + 1]) == 0 and
                                    all(teacher not in self.teacher_schedule[day][hour] and teacher not in self.teacher_schedule[day][hour + 1]
                                        for teacher in teachers_for_lca)):
                                
                                # Assign the LCA subject for two consecutive hours
                                timetable[day][class_name][hour].append((subject_name, teachers_for_lca))
                                timetable[day][class_name][hour + 1].append((subject_name, teachers_for_lca))

                                # Mark the teachers as busy for these hours
                                for teacher in teachers_for_lca:
                                    self.teacher_schedule[day][hour].add(teacher)
                                    self.teacher_schedule[day][hour + 1].add(teacher)

                                # Increment the assigned LCA hours by 2
                                assigned_lca_hours += 2
                                break  # Move to the next day after assigning 2 consecutive hours

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
            teacher_schedule[day][hour].add(teacher)
            return True
        return False

    def assign_elective_hours(self, timetable, allocated_subjects, teacher_schedule):
        theory_hours_assigned = {day: {class_name: {} for class_name in self.courses.keys()} for day in range(self.num_days)}
    #     for class_name, class_data in self.courses.items():
    # if class_name == "5BCA A":
    #     for category, subjects in class_data.items():
    #         elective_subjects = list(subjects.keys())
    #         if len(elective_subjects) < 2:
    #             continue  # Skip if less than 2 subjects

    #         subject1_name = elective_subjects[0]
    #         subject1_info = subjects[subject1_name]
    #         subject2_name = elective_subjects[1]
    #         subject2_info = subjects[subject2_name]

    #         normal_hours1 = subject1_info["normal_hours"]
    #         normal_hours2 = subject2_info["normal_hours"]
    #         teachers_for_subject1 = subject1_info["teacher_incharge"]
    #         teachers_for_subject2 = subject2_info["teacher_incharge"]

    #         assigned_theory_hours1 = 0
    #         assigned_theory_hours2 = 0

    #         while assigned_theory_hours1 < normal_hours1 or assigned_theory_hours2 < normal_hours2:
    #             for day in range(self.num_days):
    #                 total_hours1_A = theory_hours_assigned[day]["5BCA A"].get(subject1_name, 0)
    #                 total_hours1_B = theory_hours_assigned[day]["5BCA B"].get(subject1_name, 0)
    #                 total_hours2_A = theory_hours_assigned[day]["5BCA A"].get(subject2_name, 0)
    #                 total_hours2_B = theory_hours_assigned[day]["5BCA B"].get(subject2_name, 0)

    #                 # Check availability for both subjects
    #                 if (total_hours1_A < 2 and total_hours1_B < 2 and 
    #                     total_hours2_A < 2 and total_hours2_B < 2 and 
    #                     subject1_name not in allocated_subjects[day]["5BCA A"] and 
    #                     subject1_name not in allocated_subjects[day]["5BCA B"] and 
    #                     subject2_name not in allocated_subjects[day]["5BCA A"] and 
    #                     subject2_name not in allocated_subjects[day]["5BCA B"]):

    #                     for hour in range(self.num_hours):
    #                         if (len(timetable[day]["5BCA A"][hour]) == 0 and 
    #                             len(timetable[day]["5BCA B"][hour]) == 0):
                                
    #                             # Check if teachers are free for both subjects
    #                             if (all(teacher not in teacher_schedule[day][hour] for teacher in teachers_for_subject1) and 
    #                                 all(teacher not in teacher_schedule[day][hour] for teacher in teachers_for_subject2)):
                                    
    #                                 # Assign subject1 for 5BCA A
    #                                 if assigned_theory_hours1 < normal_hours1:
    #                                     if self.assign_elective_subject(timetable, day, "5BCA A", hour, subject1_name, teachers_for_subject1, teacher_schedule):
    #                                         theory_hours_assigned[day]["5BCA A"][subject1_name] = total_hours1_A + 1
    #                                         allocated_subjects[day]["5BCA A"].add(subject1_name)
    #                                         assigned_theory_hours1 += 1

    #                                 # Assign subject1 for 5BCA B
    #                                 if assigned_theory_hours1 < normal_hours1:
    #                                     if self.assign_elective_subject(timetable, day, "5BCA B", hour, subject1_name, teachers_for_subject1, teacher_schedule):
    #                                         theory_hours_assigned[day]["5BCA B"][subject1_name] = total_hours1_B + 1
    #                                         allocated_subjects[day]["5BCA B"].add(subject1_name)
    #                                         assigned_theory_hours1 += 1

    #                                 # Assign subject2 for 5BCA A
    #                                 if assigned_theory_hours2 < normal_hours2:
    #                                     if self.assign_elective_subject(timetable, day, "5BCA A", hour, subject2_name, teachers_for_subject2, teacher_schedule):
    #                                         theory_hours_assigned[day]["5BCA A"][subject2_name] = total_hours2_A + 1
    #                                         allocated_subjects[day]["5BCA A"].add(subject2_name)
    #                                         assigned_theory_hours2 += 1

    #                                 # Assign subject2 for 5BCA B
    #                                 if assigned_theory_hours2 < normal_hours2:
    #                                     if self.assign_elective_subject(timetable, day, "5BCA B", hour, subject2_name, teachers_for_subject2, teacher_schedule):
    #                                         theory_hours_assigned[day]["5BCA B"][subject2_name] = total_hours2_B + 1
    #                                         allocated_subjects[day]["5BCA B"].add(subject2_name)
    #                                         assigned_theory_hours2 += 1
                                    
    #                                 break  # Exit for loop if assignments are made

    #                 if assigned_theory_hours1 >= normal_hours1 and assigned_theory_hours2 >= normal_hours2:
    #                     break

        for class_name, class_data in self.courses.items():
            if class_name in ["5BCA A"]:
                for category, subjects in class_data.items():
                    if  category in ["ELECTIVE-I","Elective-II"]:
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
                                total_hours1_A = theory_hours_assigned[day]["5BCA A"].get(subject1_name, 0)
                                total_hours1_B = theory_hours_assigned[day]["5BCA B"].get(subject1_name, 0)
                                total_hours2_A = theory_hours_assigned[day]["5BCA A"].get(subject2_name, 0)
                                total_hours2_B = theory_hours_assigned[day]["5BCA B"].get(subject2_name, 0)

                                # Check availability for both subjects
                                if (total_hours1_A < 2 and total_hours1_B < 2 and 
                                    total_hours2_A < 2 and total_hours2_B < 2 and 
                                    subject1_name not in allocated_subjects[day]["5BCA A"] and 
                                    subject1_name not in allocated_subjects[day]["5BCA B"] and 
                                    subject2_name not in allocated_subjects[day]["5BCA A"] and 
                                    subject2_name not in allocated_subjects[day]["5BCA B"]):

                                    for hour in range(self.num_hours):
                                        if (len(timetable[day]["5BCA A"][hour]) == 0 and 
                                            len(timetable[day]["5BCA B"][hour]) == 0):
                                            
                                            # Check if teachers are free for both subjects
                                            if (all(teacher not in teacher_schedule[day][hour] for teacher in teachers_for_subject1) and 
                                                all(teacher not in teacher_schedule[day][hour] for teacher in teachers_for_subject2)):
                                                
                                                # Assign both subjects for both classes
                                                if assigned_theory_hours1 < normal_hours1:
                                                    if self.assign_elective_subject(timetable, day, "5BCA A", hour, subject1_name, teachers_for_subject1, teacher_schedule) and self.assign_elective_subject(timetable, day, "5BCA B", hour, subject1_name, teachers_for_subject1, teacher_schedule):
                                                        
                                                        theory_hours_assigned[day]["5BCA A"][subject1_name] = total_hours1_A + 1
                                                        allocated_subjects[day]["5BCA A"].add(subject1_name)
                                                        theory_hours_assigned[day]["5BCA B"][subject1_name] = total_hours1_B + 1
                                                        allocated_subjects[day]["5BCA B"].add(subject1_name)
                                                        assigned_theory_hours1 += 1

                                                

                                                if assigned_theory_hours2 < normal_hours2:
                                                    if self.assign_elective_subject(timetable, day, "5BCA A", hour, subject2_name, teachers_for_subject2, teacher_schedule) and self.assign_elective_subject(timetable, day, "5BCA B", hour, subject2_name, teachers_for_subject2, teacher_schedule):

                                                        theory_hours_assigned[day]["5BCA A"][subject2_name] = total_hours2_A + 1
                                                        allocated_subjects[day]["5BCA A"].add(subject2_name)
                                                        theory_hours_assigned[day]["5BCA B"][subject2_name] = total_hours2_B + 1
                                                        allocated_subjects[day]["5BCA B"].add(subject2_name)
                                                        assigned_theory_hours2 += 1

                                                break  # Exit for loop if assignments are made

                                    if assigned_theory_hours1 >= normal_hours1 and assigned_theory_hours2 >= normal_hours2:
                                        break
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
                                    if (all(teacher not in teacher_schedule[day][hour] for teacher in teachers_for_subject1) and
                                        all(teacher not in teacher_schedule[day][hour] for teacher in teachers_for_subject2)):
                                        
                                        # Assign subject 1
                                        if assigned_theory_hours1 < normal_hours1:
                                            self.assign_elective_subject(timetable, day, class_name, hour, subject1_name, teachers_for_subject1, teacher_schedule)
                                            theory_hours_assigned[day][class_name][subject1_name] = total_hours1 + 1
                                            allocated_subjects[day][class_name].add(subject1_name)
                                            assigned_theory_hours1 += 1

                                        # Assign subject 2
                                        if assigned_theory_hours2 < normal_hours2:
                                            self.assign_elective_subject(timetable, day, class_name, hour, subject2_name, teachers_for_subject2, teacher_schedule)
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
                                if (all(teacher not in teacher_schedule[day][hour] for teacher in teachers_for_subject1) and
                                    all(teacher not in teacher_schedule[day][hour] for teacher in teachers_for_subject2)):
                                    
                                    lab_venue1 = self.get_available_lab(day, hour)
                                    lab_venue2 = self.get_available_lab(day, hour)  # Assuming same lab for both subjects
                                    
                                    if lab_venue1 and self.is_lab_available(lab_venue1, day, hour):
                                        # Assign lab for both subjects in the same hour
                                        self.assign_lab(timetable, day, class_name, hour, subject1_name, teachers_for_subject1, lab_venue1, allocated_subjects, teacher_schedule)
                                        self.assign_lab(timetable, day, class_name, hour, subject2_name, teachers_for_subject2, lab_venue2, allocated_subjects, teacher_schedule)
                                        
                                        lab_assigned_per_day[day][class_name] = True
                                        assigned_lab_hours1 += 2  # Increment for subject 1
                                        assigned_lab_hours2 += 2  # Increment for subject 2
                                        break  # Exit the loop to re-evaluate lab assignments

                    if assigned_lab_hours1 >= lab_hours1 and assigned_lab_hours2 >= lab_hours2:
                        break  # Exit if all lab hours have been assigned

    def assign_elective_lab(self, timetable, allocated_subjects, lab_assigned_per_day, teacher_schedule):
        for class_name, class_data in self.courses.items():
            if class_name in ['5BCA A']:
                for category, subjects in class_data.items():
                    if category == "ELECTIVE-I":
                        for subject_name, subject_info in subjects.items():
                            lab_hours = subject_info["lab_hours"]
                            teachers_for_subject = subject_info["teacher_incharge"]
                            assigned_lab_hours = 0

                            for day in range(self.num_days):
                                if assigned_lab_hours >= lab_hours:
                                    break
                                if subject_name not in allocated_subjects[day][class_name] and not lab_assigned_per_day[day][class_name]:
                                    for hour in range(self.num_hours - 1):  # Ensure space for two hours
                                        if (len(timetable[day]["5BCA A"][hour]) == 0 and 
                                            len(timetable[day]["5BCA A"][hour + 1]) == 0 and 
                                            len(timetable[day]["5BCA B"][hour]) == 0 and 
                                            len(timetable[day]["5BCA B"][hour + 1]) == 0):

                                            if all(teacher not in teacher_schedule[day][hour] for teacher in teachers_for_subject):
                                                lab_venue = self.get_available_lab(day, hour)
                                                lab_venue2 = self.get_available_lab(day, hour)
                                                if lab_venue and lab_venue2 and self.is_lab_available(lab_venue, day, hour) and self.is_lab_available(lab_venue2, day, hour):
                                                    self.assign_lab(timetable, day, "5BCA A", hour, subject_name, teachers_for_subject, lab_venue, allocated_subjects, teacher_schedule)
                                                    self.assign_lab(timetable, day, "5BCA B", hour, subject_name, teachers_for_subject, lab_venue2, allocated_subjects, teacher_schedule)
                                                    lab_assigned_per_day[day]["5BCA A"] = True
                                                    lab_assigned_per_day[day]["5BCA B"] = True
                                                    assigned_lab_hours += 2
                                                    break

                                                    
    def assign_lab_hours(self, timetable, allocated_subjects, lab_assigned_per_day, teacher_schedule):
            lab_venues = ["BCA Lab", "MCA Lab", "BSc Lab"]

            for class_name, class_data in self.courses.items():
                for category, subjects in class_data.items():
                    if category not in ["LCA", "ELECTIVE-I", "ELECTIVE-II","HED","MDC"]:
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
                                                if all(teacher not in teacher_schedule[day][hour] for teacher in teachers_for_subject):
                                                    lab_venue = self.get_available_lab(day, hour)
                                                    if lab_venue and self.is_lab_available(lab_venue, day, hour):
                                                        self.assign_lab(timetable, day, class_name, hour, subject_name, teachers_for_subject, lab_venue, allocated_subjects, teacher_schedule)
                                                        lab_assigned_per_day[day][class_name] = True
                                                        assigned_lab_hours += 2
                                                        break
    
    def assign_theory_hours(self, timetable, allocated_subjects, theory_hours_assigned, teacher_schedule):
        for class_name, class_data in self.courses.items():
            for category, subjects in class_data.items():
                if category not in ["LCA", "ELECTIVE-I", "ELECTIVE-II", "HED", "MDC"]:
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
                                            if any(teacher not in teacher_schedule[day][hour] for teacher in teachers_for_subject):
                                                self.assign_subject(timetable, day, class_name, hour, subject_name, teachers_for_subject, category, teacher_schedule)
                                                theory_hours_assigned[day][class_name][subject_name] = total_hours + 1
                                                allocated_subjects[day][class_name].add(subject_name)
                                                assigned_theory_hours += 1  # Increment assigned hours
                                                break  # Move to the next subject

                                    if assigned_theory_hours >= normal_hours:
                                        break  # Exit the loop once normal hours are assigned

                            # Check if the exact number of required theory hours was assigned
                            if assigned_theory_hours != normal_hours:
                                self.allocate_missing_hours( timetable, theory_hours_assigned, allocated_subjects, teacher_schedule)
                                # print(f"Warning: Could not assign the exact number of theory hours for {subject_name} in {class_name}. Assigned: {assigned_theory_hours}, Required: {normal_hours}")


    def allocate_missing_hours(self, timetable, theory_hours_assigned, allocated_subjects, teacher_schedule):
        for class_name, class_data in self.courses.items():
            for category, subjects in class_data.items():
                if category  in ["NORMAL"]:
                    for subject_name, subject_info in subjects.items():
                        normal_hours = subject_info["normal_hours"]
                        assigned_hours = sum(theory_hours_assigned[day][class_name].get(subject_name, 0) for day in range(self.num_days))

                        # Check if assigned hours are less than normal hours
                        if assigned_hours < normal_hours:
                            hours_to_allocate = normal_hours - assigned_hours
                            # print(f"Allocating additional {hours_to_allocate} hours for {subject_name} in {class_name}")

                            # Attempt to allocate the missing hours
                            for day in range(self.num_days):
                                total_hours = theory_hours_assigned[day][class_name].get(subject_name, 0)

                                for hour in range(self.num_hours):
                                    if total_hours < 2 and subject_name not in allocated_subjects[day][class_name] and len(timetable[day][class_name][hour]) == 0:
                                        teachers_for_subject = subject_info["teacher_incharge"]
                                        
                                        # Check if at least one teacher is available
                                        if any(teacher not in teacher_schedule[day][hour] for teacher in teachers_for_subject):
                                            # Assign the first available teacher
                                            available_teacher = next(teacher for teacher in teachers_for_subject if teacher not in teacher_schedule[day][hour])
                                            
                                            self.assign_subject(timetable, day, class_name, hour, subject_name, [available_teacher], category, teacher_schedule)
                                            theory_hours_assigned[day][class_name][subject_name] = total_hours + 1
                                            allocated_subjects[day][class_name].add(subject_name)
                                            hours_to_allocate -= 1  # Decrement the hours to allocate
                                            
                                            if hours_to_allocate <= 0:
                                                break  # Exit if all required hours have been allocated
                                if hours_to_allocate <= 0:
                                    break  # Exit if all required hours have been allocated

                    # Optional: Check if after allocation there are still unallocated hours
                    if assigned_hours + (normal_hours - assigned_hours) > normal_hours:
                        print(f"Warning: Unable to allocate all required hours for {subject_name} in {class_name}")


    def assign_subject(self, timetable, day, class_name, hour, subject_name, teachers_for_subject, category, teacher_schedule):
        if category == "GROUP TEACHING":
            assigned_teachers = []
            for teacher in teachers_for_subject:
                if teacher not in teacher_schedule[day][hour]:  # Ensure no double booking
                    assigned_teachers.append(teacher)
                    teacher_schedule[day][hour].add(teacher)  # Mark teacher as assigned for this hour

            if assigned_teachers:
                timetable[day][class_name][hour].append((subject_name, assigned_teachers))
                return True  # Return True indicating the subject was assigned
            else:
                print(f"No available teachers for group teaching of {subject_name} in {class_name} on day {day}, hour {hour}.")
                return False  # Return False indicating assignment failed

        elif category == "NORMAL":
            if not any(subject[0] == subject_name for subject in timetable[day][class_name][hour]):
                teacher = random.choice(teachers_for_subject)
                if teacher not in teacher_schedule[day][hour]:  # Ensure no double booking
                    timetable[day][class_name][hour].append((subject_name, [teacher]))
                    teacher_schedule[day][hour].add(teacher)  # Mark teacher as assigned for this hour
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
        timetable[day][class_name][hour].append((subject_name, teachers_for_subject, lab_venue))  # Store all teachers and lab venue
        timetable[day][class_name][hour + 1].append((subject_name, teachers_for_subject, lab_venue))  # Assign for the next hour
        self.lab_timetables[lab_venue][day][hour].append((subject_name, teachers_for_subject))
        self.lab_timetables[lab_venue][day][hour + 1].append((subject_name, teachers_for_subject))
        allocated_subjects[day][class_name].add(subject_name)
        for teacher in teachers_for_subject:
            teacher_schedule[day][hour].add(teacher)
            teacher_schedule[day][hour + 1].add(teacher)

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
                        subject_info = ""
                        for subject in subjects:
                            subject_short_name = shortsub.get(subject[0], subject[0])  # Get the short form of the subject
                            teachers = ', '.join([short_teachers.get(teacher.strip(), teacher) for teacher in subject[1]])  # Get short forms of teachers
                            if len(subject) == 3:  # Lab
                                subject_info += f"{subject_short_name} (Lab - {subject[2]} by {teachers}) | "
                            else:  # Theory
                                subject_info += f"{subject_short_name} by {teachers} | "
                        data[days[day]].append(subject_info.strip("| "))
                    else:
                        data[days[day]].append("Free")

            # Create DataFrame for this class
            df = pd.DataFrame(data)
            df.index = [f"Hour {hour + 1}" for hour in range(self.num_hours)]
            all_class_dfs[class_name] = df

            # Adjust column width based on content for better cell size
            max_length = {col: max(df[col].astype(str).map(len).max(), len(col)) for col in df.columns}
            for column in df.columns:
                df[column] = df[column].apply(lambda x: x.ljust(max_length[column]))

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


        # Initialize a timetable for each teacher
        for teacher in teachers:
            data = {day: [] for day in days}

            for day in range(self.num_days):
                for hour in range(self.num_hours):
                    subject_info = []
                    # Check each class to see if this teacher is assigned during this hour
                    for class_name in self.classes:
                        subjects = timetable[day][class_name][hour]
                        for subject in subjects:
                            if teacher in subject[1]:  # If teacher is assigned
                                subject_short_name = shortsub.get(subject[0], subject[0])  # Get short form of the subject
                                subject_info.append(f"{subject_short_name} ({class_name})")  # Show which class is being taught
                    if subject_info:
                        data[days[day]].append(', '.join(subject_info))
                    else:
                        data[days[day]].append("Free")

            # Create DataFrame for this teacher
            df = pd.DataFrame(data)
            df.index = [f"Hour {hour + 1}" for hour in range(self.num_hours)]
            all_teacher_dfs[teacher] = df

            # Adjust column width based on content for better cell size
            max_length = {col: max(df[col].astype(str).map(len).max(), len(col)) for col in df.columns}
            for column in df.columns:
                df[column] = df[column].apply(lambda x: x.ljust(max_length[column]))

        return all_teacher_dfs



    def create_lab_dataframes(self, timetable):
        all_lab_dfs = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        # Initialize a timetable for each lab
        for lab in self.lab_timetables.keys():
            data = {day: [] for day in days}

            for day in range(self.num_days):
                for hour in range(self.num_hours):
                    subjects_info = []
                    
                    # Check each class to see which subjects are assigned in the current lab during this hour
                    for class_name in self.classes:
                        subjects = timetable[day][class_name][hour]
                        
                        # Check if the subject is a lab subject assigned to the current lab
                        for subject in subjects:
                            if isinstance(subject, tuple) and len(subject) == 3:  # Assuming subject is stored as a tuple
                                subject_name = subject[0]
                                teachers_for_subject = subject[1]
                                lab_venue = subject[2]

                                # Get the short form of the subject name
                                subject_short_name = shortsub.get(subject_name, subject_name)  # Get short form

                                # Ensure that the current lab matches the lab assigned to the subject
                                if lab_venue == lab:
                                    teachers = ', '.join([short_teachers.get(teacher.strip(), teacher) for teacher in teachers_for_subject])
                                    subjects_info.append(f"{subject_short_name} (Lab - {lab} by {teachers}) in {class_name}")

                    # Append information or "Free" if no lab subjects are assigned
                    if subjects_info:
                        data[days[day]].append(', '.join(subjects_info))
                    else:
                        data[days[day]].append("Free")

            # Create DataFrame for this lab
            df = pd.DataFrame(data)
            df.index = [f"Hour {hour + 1}" for hour in range(self.num_hours)]
            all_lab_dfs[lab] = df

            # Adjust column width based on content for better cell size
            max_length = {col: max(df[col].astype(str).map(len).max(), len(col)) for col in df.columns}
            for column in df.columns:
                df[column] = df[column].apply(lambda x: x.ljust(max_length[column]))
        

        return all_lab_dfs
    
    

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




    



if __name__ == "__main__":
    timetable_generator = TimetableGenerator(courses)
    timetable = timetable_generator.generate_timetable()

    # Call the record_assigned_classes function from timetable_generator, not from timetable
    # assigned_classes_record = timetable_generator.record_assigned_classes()
    
    # # Compare assigned hours with expected hours
    # timetable_generator.compare_assigned_with_expected(assigned_classes_record)
    
    # Print the assigned hours in a formatted way
    # timetable_generator.print_assigned_hours(assigned_classes_record)

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
            
    print("Timetable saved to 'timetable.xlsx'.")
