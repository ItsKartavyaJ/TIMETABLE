

# # def print_courses_table(courses):
# #     # Print overall headers
# #     subig=["GRAPHICS AND ANIMATION","CYBER SECURITY"]
# #     classig=["1BCA B","3BCA B","5BCA B",]
# #     print(f"{'Class Name':<10} {'Subject Name':<40} {'Theory Hours':<15} {'Lab Hours':<10} {'Total Hours':<10}")
# #     print("=" * 85)

# #     # Initialize overall total hours
# #     grand_total_hours = 0

# #     # Iterate through each class
# #     for class_name, categories in courses.items():
# #         if class_name not in classig:
# #             total_hours_for_class = 0  # Reset total for the class
# #             # Print class header
# #             print(f"\n{class_name}")
# #             print("-" * 60)

# #             # Iterate through categories and subjects
# #             for category, subjects in categories.items():
# #                 for subject_name, details in subjects.items():
# #                     if subject_name not in subig: 
# #                         lab_hours = details.get('lab_hours', 0)
# #                         theory_hours = details.get('normal_hours', 0)
# #                         total_hours = lab_hours + theory_hours
# #                         total_hours_for_class += total_hours

# #                         # Print subject details
# #                         print(f"{subject_name:<40} {theory_hours:<15} {lab_hours:<10} {total_hours:<10}")

# #             # Print total for the class
# #             print(f"{'Total for ' + class_name:<40} {'':<15} {'':<10} {total_hours_for_class:<10}")
            
# #             # Update grand total
# #             grand_total_hours += total_hours_for_class

# #         # Print grand total for all classes
# #     print("=" * 85)
# #     print(f"{'Grand Total':<40} {'':<15} {'':<10} {grand_total_hours:<10}")

# # # Example usage
# # print_courses_table(courses)




# # Calculate total hours for each course
# TOTALHR = {}
# for course, details in courses.items():
#     total_hours = 0
#     for section, subjects in details.items():
#         elective_counted = False
#         for subject, info in subjects.items():
#             if "ELECTIVE" in section.upper() or "Elective" in section:
#                 if not elective_counted:
#                     total_hours += info.get("total_hours_per_week", 0)
#                     elective_counted = True
#             else:
#                 total_hours += info.get("total_hours_per_week", 0)
#     TOTALHR[course] = total_hours

# # Sort the courses by total hours in descending order
# courses = dict(sorted(courses.items(), key=lambda item: TOTALHR[item[0]], reverse=True))

# # Function to sort subjects by lab hours and normal hours
# def sort_subjects_by_lab_hours(courses):
#     for course, details in courses.items():
#         for section, subjects in details.items():
#             # Sort subjects by lab_hours (descending) and then by normal_hours (ascending)
#             sorted_subjects = sorted(
#                 subjects.items(),
#                 key=lambda item: (-item[1].get('lab_hours', 0), -item[1].get('normal_hours', float('inf')))
#             )
#             details[section] = {subject_name: info for subject_name, info in sorted_subjects}
#     return courses

# # Sort subjects within each course
# courses = sort_subjects_by_lab_hours(courses)

# CLASSES={k:None for k in courses.keys()}

courses = {
   "1BCA A": {
        # 
       "GROUP TEACHING": {
           "OBJECT ORIENTED PROGRAMMING USING C++": {
               "subject_code":"BCA102-1",
               "short_name":"OOP",
               "proposed_timing":"BATCH IV : 9.30am-3.30pm",
               "teacher_incharge": ["Dr SAGAYA AURELIA P"," Dr Chanti"],
               "normal_hours": 2,
               "lab_hours": 4,
               "total_hours_per_week": 6
            }
        },
      "NORMAL": {
        # 20hr/
       "PRINCIPLES OF SOFTWARE DEVELOPMENT – 1": {
           "subject_code":"BCA203-1",
           "short_name":"PSD",
           "teacher_incharge": ["Dr NISMON RIO R"],
           "normal_hours": 4,
           "lab_hours": 2,
           "total_hours_per_week": 6
        },
       "INTRODUCTION TO WEB TECHNOLOGY": {
           "subject_code":"BCA261-1",
           "short_name":"WT",
           "teacher_incharge": ["Dr KIRUBANAND V B"],
           "normal_hours": 2,
           "lab_hours": 2,
           "total_hours_per_week": 4
        },
       "MATHEMATICS": {
           "subject_code":"BCA101",
           "short_name":"MATHS",
           "teacher_incharge": ["xyz"],
           "normal_hours": 3,
           "lab_hours": 0,
           "total_hours_per_week": 3
        },
       "LIBRARY": {
               "subject_code":"LIB001",
               "short_name":"LIBRARY",
               "teacher_incharge": ["1bcaa"],
               "normal_hours": 2,
               "lab_hours": 0,
               "total_hours_per_week": 2
        }
    },

       "MDC": {
           "MDC": {
               "normal_hours": 3,
               "lab_hours": 0,
               "total_hours_per_week": 3,
                "teacher_incharge": ["mdc"],
            }
        },
       "HED": {
           "HED": {
               "normal_hours": 1,
               "lab_hours": 0,
               "total_hours_per_week": 1,
                "teacher_incharge": ["--"],
            }
        },
       "NOT MORNING":{},
       "language":{},
       "act":{}
        
    },
   "1BCA B": {
        # 20hr
       "GROUP TEACHING": {
           "OBJECT ORIENTED PROGRAMMING USING C++": {
               "subject_code":"BCA102-1",
               "short_name":"OOP",
               "proposed_timing":"BATCH IV : 9.30am-3.30pm",
               "teacher_incharge": ["Dr SARAVANAN KN","Dr LOKESHWARAN"],
               "normal_hours": 2,
               "lab_hours": 4,
               "total_hours_per_week": 6
            }
        },
       "NORMAL": {
           "PRINCIPLES OF SOFTWARE DEVELOPMENT – 1": {
               "subject_code":"BCA203-1",
               "short_name":"PSD",
               "teacher_incharge": ["Dr AROKIA PAUL RAJAN R"],
               "normal_hours": 4,
               "lab_hours": 2,
               "total_hours_per_week": 6
            },
           "INTRODUCTION TO WEB TECHNOLOGY": {
               "subject_code":"BCA261-1",
               "short_name":"WT",
               "teacher_incharge": ["Dr SANGEETHA GOVINDA"],
               "normal_hours": 2,
               "lab_hours": 2,
               "total_hours_per_week": 4
            },
           "MATHEMATICS": {
               "subject_code":"BCA101",
               "short_name":"MATHS",
               "teacher_incharge": ["temp"],
               "normal_hours": 3,
               "lab_hours": 0,
               "total_hours_per_week": 3
            },
           "LIBRARY": {
               "subject_code":"LIB001",
               "short_name":"LIB",
               "teacher_incharge": ["1bca b"],
               "normal_hours": 2,
               "lab_hours": 0,
               "total_hours_per_week": 2
                }
        },
       "MDC": {
           "MDC": {
               "normal_hours": 3,
               "lab_hours": 0,
               "total_hours_per_week": 3,
                "teacher_incharge": ["mdc"],
            }
        },
       "HED": {
           "HED": {
               "normal_hours": 1,
               "lab_hours": 0,
               "total_hours_per_week": 1
            }
        },
       "NOT MORNING":{},
       "language":{},
       "act":{}
    },
   "3BCA A": {
        # 17 hr
       "LCA": {
           "COMPUTER NETWORKS": {
               "subject_code":"BCA107-3",
               "short_name":"CN",
               "proposed_timing":"BATCH II : 7.30am - 12.30pm",
               "teacher_incharge": ["Dr SANDEEP J","Dr NISMON RIO R"],
               "normal_hours": 4,
               "lab_hours": 0,
               "total_hours_per_week": 4
            },
           "INTRODUCTION TO PYTHON": {
               "subject_code":"BCA263",
               "short_name":"PY",
               "teacher_incharge": ["Dr MOHANA PRIYA T","Dr VIJAY ARPUTHARAJ"],
               "normal_hours": 2,
               "lab_hours": 2,
               "total_hours_per_week": 4
            }
            
        },
       "NORMAL": {
           "OPERATING SYSTEM": {
               "subject_code":"BCA108-3",
               "short_name":"OS",
               "teacher_incharge": ["Dr ROHINI V"],
               "normal_hours": 3,
               "lab_hours": 0,
               "total_hours_per_week": 3
            },
           "MOBILE APPLICATIONS": {
               "subject_code":"BCA310-3",
               "short_name":"MA",
               "teacher_incharge": ["Dr Manasa"],
               "normal_hours": 3,
               "lab_hours": 2,
               "total_hours_per_week": 5
            },
           "LIBRARY": {
               "subject_code":"LIB001",
               "short_name":"LIBRARY",
               "teacher_incharge": ["3 bca a"],
               "normal_hours": 1,
               "lab_hours": 0,
               "total_hours_per_week": 1
        },
           "SUMMER INTERNSHIP": {
               "subject_code":"BCA484-3",
               "short_name":"INTERNSHIP",
               "teacher_incharge": ["3bca a si"],
               "normal_hours": 4,
               "lab_hours": 0,
               "total_hours_per_week": 4
            }
        },
      
       "HED": {
           "HED": {
               "normal_hours": 1,
               "lab_hours": 0,
               "total_hours_per_week": 1
            }
        },
       "language":{},
       "act":{}
        
    },
   "3BCA B": {
        # 17hr
       "LCA": {
           "COMPUTER NETWORKS": {
               "subject_code":"BCA107-3",
               "short_name":"CN",
               "proposed_timing":"BATCH II : 7.30am - 12.30pm",
               "teacher_incharge": ["Dr FABIOLA HAZEL POHRMEN","Dr CYNTHIA"],
               "normal_hours": 4,
               "lab_hours": 0,
               "total_hours_per_week": 4
            },
           "INTRODUCTION TO PYTHON": {
               "subject_code":"BCA263",
               "short_name":"PY",
               "teacher_incharge": ["Dr RESMI KR","Dr HUBERT SHANTHAN"],
               "normal_hours": 2,
               "lab_hours": 2,
               "total_hours_per_week": 4
            }
        },
       "NORMAL": {
           "OPERATING SYSTEM": {
               "subject_code":"BCA108-3",
               "short_name":"OS",
               "teacher_incharge": ["Dr AROKIA PAUL RAJAN R"],
               "normal_hours": 3,
               "lab_hours": 0,
               "total_hours_per_week": 3
            },
           "MOBILE APPLICATIONS": {
               "subject_code":"BCA310-3",
               "short_name":"MA",
               "teacher_incharge": ["Dr VINEETHA KR"],
               "normal_hours": 3,
               "lab_hours": 2,
               "total_hours_per_week": 5
            },
            "LIBRARY": {
               "subject_code":"LIB001",
               "short_name":"LIBRARY",
               "teacher_incharge": ["3 bca b"],
               "normal_hours": 1,
               "lab_hours": 0,
               "total_hours_per_week": 1},
             "SUMMER INTERNSHIP": {
               "subject_code":"BCA484-3",
               "short_name":"INTERNSHIP",
               "teacher_incharge": ["3bca b si"],
               "normal_hours": 4,
               "lab_hours": 0,
               "total_hours_per_week": 4
            }
        },
       
       "HED": {
           "HED": {
               "normal_hours": 1,
               "lab_hours": 0,
               "total_hours_per_week": 1
            }
        },
       "language":{},
       "act":{}
    },
       "5BCA A": {
        # 28 hr
       "NORMAL": {
           "MOBILE APPLICATIONS": {
               "subject_code":"BCA531",
               "short_name":"MA",
               "proposed_timing":"BATCH II : 7.30am - 12.30pm",
               "teacher_incharge": ["Dr VINEETHA KR"],
               "normal_hours": 4,
               "lab_hours": 4,
               "total_hours_per_week": 8
            },
           "COMPUTER NETWORKS": {
               "subject_code":"BCA532",
               "short_name":"CN",
               "teacher_incharge": ["Dr SMERA"],
               "normal_hours": 4,
               "lab_hours": 0,
               "total_hours_per_week": 4
            },
           "PROJECT-I": {
               "subject_code":"BCA581",
               "short_name":"PRJ",
               "teacher_incharge": ["Dr VIJAY ARPUTHARAJ"],
               "normal_hours": 2,
               "lab_hours": 2,
               "total_hours_per_week": 4
            },
        #    "LIBRARY": {
        #        "subject_code":"LIB001",
        #        "short_name":"LIBRARY",
        #        "teacher_incharge": ["5 bca a"],
        #        "normal_hours": 1,
        #        "lab_hours": 0,
        #        "total_hours_per_week": 1}
           
           
        },
       "ELECTIVE-I": {
           "GRAPHICS AND ANIMATION": {
               "subject_code":"BCA541B",
               "short_name":"GA",
               "teacher_incharge": ["Dr VIJAY ARPUTHARAJ"],
               "normal_hours": 4,
               "lab_hours": 4,
               "total_hours_per_week": 8
            },
           "BUSINESS INTELLIGENCE": {
               "subject_code":"BCA542",
               "short_name":"BI",
               "teacher_incharge": ["Dr NEWBEGIN"],
               "normal_hours": 4,
               "lab_hours": 4,
               "total_hours_per_week": 8
            },
        },
       "Elective-II":{
           "MULTIMEDIA APPLICATIONS": {
               "subject_code":"BCA543",
               "short_name":"MM",
               "teacher_incharge": ["Dr AMRUTHA"],
               "normal_hours": 4,
               "lab_hours": 0,
               "total_hours_per_week": 4
            },
           "CYBER SECURITY": {
               "subject_code":"BCA544",
               "short_name":"CS",
               "teacher_incharge": ["Dr CYNTHIA"],
               "normal_hours": 4,
               "lab_hours": 0,
               "total_hours_per_week": 4
            }
        },
       "act":{}
       
    },
   "5BCA B": {
        # 28hr
       "NORMAL": {
           "MOBILE APPLICATIONS": {
               "subject_code":"BCA531",
               "short_name":"MA",
               "proposed_timing":"BATCH II : 7.30am - 12.30pm",
               "teacher_incharge": ["Dr Manasa"],
               "normal_hours": 4,
               "lab_hours": 4,
               "total_hours_per_week": 8
            },
           "COMPUTER NETWORKS": {
               "subject_code":"BCA532",
               "short_name":"CN",
               "teacher_incharge": ["Dr RAINA"],
               "normal_hours": 4,
               "lab_hours": 0,
               "total_hours_per_week": 4
            },
           "PROJECT-I": {
               "subject_code":"BCA581",
               "short_name":"PRJ",
               "teacher_incharge": ["Dr SHAMINE"],
               "normal_hours": 2,
               "lab_hours": 2,
               "total_hours_per_week": 4
            },
        #    "LIBRARY": {
        #        "subject_code":"LIB001",
        #        "short_name":"LIBRARY",
        #        "teacher_incharge": ["5 bca b"],
        #        "normal_hours": 1,
        #        "lab_hours": 0,
        #        "total_hours_per_week": 1}
        },
       "ELECTIVE-I": {
           "GRAPHICS AND ANIMATION": {
               "subject_code":"BCA541B",
               "short_name":"GA",
               "teacher_incharge": ["Dr VIJAY ARPUTHARAJ"],
               "normal_hours": 4,
               "lab_hours": 4,
               "total_hours_per_week": 8
            },
           "BUSINESS INTELLIGENCE": {
               "subject_code":"BCA542",
               "short_name":"BI",
               "teacher_incharge": ["Dr NEWBEGIN"],
               "normal_hours": 4,
               "lab_hours": 4,
               "total_hours_per_week": 8
            },
        },
       "Elective-II":{
           "MULTIMEDIA APPLICATIONS": {
               "subject_code":"BCA543",
               "short_name":"MM",
               "teacher_incharge": ["Dr AMRUTHA"],
               "normal_hours": 4,
               "lab_hours": 0,
               "total_hours_per_week": 4
            },
           "CYBER SECURITY": {
               "subject_code":"BCA544",
               "short_name":"CS",
               "teacher_incharge": ["Dr CYNTHIA"],
               "normal_hours": 4,
               "lab_hours": 0,
               "total_hours_per_week": 4
            }
        },"act":{}
    },
    
    
   "1CM": {
        # 18hr
       "GROUP TEACHING": {
           "DIGITAL COMPUTER FUNDAMENTALS AND C PROGRAMMING": {
               "subject_code":"CSC101-1",
               "short_name":"DCF",
               "proposed_timing":"BATCH IV : 9.30am-3.30pm",
               "teacher_incharge": ["Dr SREEJA","Dr MANJUNATHA HIREMATH"],
               "normal_hours": 3,
               "lab_hours": 2,
               "total_hours_per_week": 5
            }
        },
       "NORMAL": {
           "WEB APPLICATION DEVELOPMENT": {
               "subject_code":"CSC161-1",
               "short_name":"WAD",
               "teacher_incharge": ["Dr MOHANA PRIYA T"],
               "normal_hours": 2,
               "lab_hours": 2,
               "total_hours_per_week": 4
            },
           "DATA ANALYSIS USING SPREADSHEET": {
               "subject_code":"CSC162-1",
               "short_name":"DAS",
               "teacher_incharge": ["Dr FABIOLA HAZEL POHRMEN"],
               "normal_hours": 2,
               "lab_hours": 2,
               "total_hours_per_week": 4
            },"LIBRARY": {
               "subject_code":"LIB001",
               "short_name":"LIBRARY",
               "teacher_incharge": ["1cm"],
               "normal_hours": 1,
               "lab_hours": 0,
               "total_hours_per_week": 1}
        },
       "MDC": {
           "MDC": {
               "normal_hours": 3,
               "lab_hours": 0,
               "total_hours_per_week": 3,
                "teacher_incharge": ["mdc"],
            }
        },
       "HED": {
           "HED": {
               "normal_hours": 1,
               "lab_hours": 0,
               "total_hours_per_week": 1,
                "teacher_incharge": ["--"],
            }
        },
       "NOT MORNING":{},
       "act":{},
       "language":{}
    },
   "3CM": {
        # 14hr
       "LCA": {
           "JAVA PROGRAMMING": {
               "subject_code":"CSC201-3C",
               "short_name":"JAVA",
               "proposed_timing":"BATCH II : 7.30am - 12.30pm",
               "teacher_incharge": ["Dr SREEJA","Dr MANJUNATHA HIREMATH"],
               "normal_hours": 3,
               "lab_hours": 2,
               "total_hours_per_week": 5
            }
        },
       "NORMAL": {
           "DATA ANALYSIS USING PYTHON": {
               "subject_code":"CSC262-3C",
               "short_name":"DAP",
               "teacher_incharge": ["Dr RAMAMURTHY B"],
               "normal_hours": 2,
               "lab_hours": 2,
               "total_hours_per_week": 4
            },
           "SUMMER INTERNSHIP": {
               "subject_code":"Not Mentioned",
               "short_name":"INTERNSHIP",
               "teacher_incharge": ["3cm si"],
               "normal_hours": 4,
               "lab_hours": 0,
               "total_hours_per_week": 4
            },"LIBRARY": {
               "subject_code":"LIB001",
               "short_name":"LIBRARY",
               "teacher_incharge": ["3cm"],
               "normal_hours": 1,
               "lab_hours": 0,
               "total_hours_per_week": 1}
        },
       "HED": {
           "HED": {
               "normal_hours": 1,
               "lab_hours": 0,
               "total_hours_per_week": 1,
                "teacher_incharge": ["--"],
            }
        },"act":{},
    },
    
   "1CS": {
        # 14hr
       "GROUP TEACHING": {
           "DIGITAL COMPUTER FUNDAMENTALS AND C PROGRAMMING": {
               "subject_code":"CSC101-1",
               "short_name":"DCF",
               "proposed_timing":"BATCH IV : 9.30am-3.30pm",
               "teacher_incharge": ["Dr SREEJA","Dr LOKESHWARAN"],
               "normal_hours": 3,
               "lab_hours": 2,
               "total_hours_per_week": 5
            }
        },
       "NORMAL": {
           "DATA ANALYSIS USING SPREADSHEET": {
               "subject_code":"CSC162-1",
               "short_name":"DAS",
               "teacher_incharge": ["Dr BEAULAH SOUNDARABAI P"],
               "normal_hours": 2,
               "lab_hours": 2,
               "total_hours_per_week": 4
            },"LIBRARY": {
               "subject_code":"LIB001",
               "short_name":"LIBRARY",
               "teacher_incharge": ["1cs"],
               "normal_hours": 1,
               "lab_hours": 0,
               "total_hours_per_week": 1}
        },
        "MDC": {
           "MDC": {
               "normal_hours": 3,
               "lab_hours": 0,
               "total_hours_per_week": 3,
                "teacher_incharge": ["mdc"],
            }
        },
       "HED": {
           "HED": {
               "normal_hours": 1,
               "lab_hours": 0,
               "total_hours_per_week": 1,
                "teacher_incharge": ["--"],
            }
        },
       "NOT MORNING":{},
       "act":{},
       "language":{}
    },
   "3CS": {
        # 10 hr
       "LCA": {
           "JAVA PROGRAMMING": {
               "subject_code":"CSC201-3C",
               "short_name":"JAVA",
               "proposed_timing":"BATCH II : 7.30am - 12.30pm",
               "teacher_incharge": ["Dr RESMI KR","Dr SARAVANAN KN"],
               "normal_hours": 3,
               "lab_hours": 2,
               "total_hours_per_week": 5
            }
        },
       "NORMAL": {
           "WEB APPLICATION DEVELOPMENT": {
               "subject_code":"CSC261-3C",
               "short_name":"WAD",
               "teacher_incharge": ["Dr BEAULAH SOUNDARABAI P"],
               "normal_hours": 2,
               "lab_hours": 2,
               "total_hours_per_week": 4
            },
           "SUMMER INTERNSHIP": {
               "subject_code":"Not Mentioned",
               "short_name":"INTERNSHIP",
               "teacher_incharge": ["3cs si"],
               "normal_hours": 4,
               "lab_hours": 0,
               "total_hours_per_week": 4
            },"LIBRARY": {
               "subject_code":"LIB001",
               "short_name":"LIBRARY",
               "teacher_incharge": ["3cm"],
               "normal_hours": 1,
               "lab_hours": 0,
               "total_hours_per_week": 1}
        },
       "HED": {
           "HED": {
               "normal_hours": 1,
               "lab_hours": 0,
               "total_hours_per_week": 1,
               "teacher_incharge": ["--"],
            }
        },"act":{},
    },
   "5CME": {
       "NORMAL": {
           "DATA ANALYTICS": {
               "subject_code":"CSC541A",
               "short_name":"DA",
               "proposed_timing":"BATCH IV : 9.30am - 3.30pm",
               "teacher_incharge": ["Dr AMRUTHA"],
               "normal_hours": 3,
               "lab_hours": 2,
               "total_hours_per_week": 5
            },"LIBRARY": {
               "subject_code":"LIB001",
               "short_name":"LIBRARY",
               "teacher_incharge": ["5cme"],
               "normal_hours": 1,
               "lab_hours": 0,
               "total_hours_per_week": 1}
            
        },
       "ELECTIVE-I": {
           "WEB TECHNOLOGY": {
               "subject_code":"CSC542B",
               "short_name":"WT",
               "teacher_incharge": ["Dr HUBERT SHANTHAN"],
               "normal_hours": 3,
               "lab_hours": 2,
               "total_hours_per_week": 5
            },
           "GRAPHICS AND ANIMATION": {
               "subject_code":"CSC542D",
               "short_name":"GA",
               "teacher_incharge": ["Dr Chanti"],
               "normal_hours": 3,
               "lab_hours": 2,
               "total_hours_per_week": 5
            }
        },
       "NOT MORNING":{}
        
    },
   "BCOM-I":{},
   "BCOM-II":{},
   "BCOM-III":{},
   
}

shortsub = {}

for classz, classinfo in courses.items():
    for category, subject_info in classinfo.items():
        for sub_name, sub_details in subject_info.items():
            if 'short_name' in sub_details:
                # Check if the subject name is not in shortsub
                if sub_name not in shortsub:
                    # print(f"Adding '{sub_name}' to shortsub with short name '{sub_details['short_name']}'")
                    # Add the subject name and its short name from sub_details to shortsub
                    shortsub[sub_name] = sub_details['short_name']

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
   "Dr RESMI KR":"RES",
   "Dr ROHINI V":"RV",
   "Dr SAGAYA AURELIA P":"SA",
   "Dr SANDEEP J":"SD",
   "Dr SANGEETHA GOVINDA":"SG",
   "Dr SARAVANAKUMAR K":"SK",
   "Dr SARAVANAN KN":"KNS",
   "Dr SHONY SEBASTIAN":"SS",
   "Dr SMITHA VINOD":"SV",
   "Dr SOMNATH SINHA":"SOM",
   "Dr SREEJA":"SR",
   "Dr SRIDEVI R":"SRI",
   "Dr SUDHAKAR":"SU",
   "Dr SURESH K":"KS",
   "Dr THIRUNAVUKKARASU V":"VT",
   "Dr VAIDHEHI V":"VV",
   "Dr VIJAY ARPUTHARAJ":"VA",
   "Dr VINEETHA KR":"VKR",
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

CLASSES_t={x:None for x in courses.keys() if x not in ["BCOM-I","BCOM-II","BCOM-III"]}

# Calculate total hours for each course
TOTALHR = {}

for course, details in courses.items():
    total_hours = 0
    for section, subjects in details.items():
        elective_counted = False
        
        for subject, info in subjects.items():
            if"ELECTIVE" in section.upper() or"Elective" in section:
                if not elective_counted:
                    total_hours += info.get("total_hours_per_week", 0)
                    elective_counted = True
            else:
                total_hours += info.get("total_hours_per_week", 0)
    
    TOTALHR[course] = total_hours
    


    
# Sort the courses by total hours in descending order
courses = dict(sorted(courses.items(), key=lambda item: TOTALHR[item[0]], reverse=True))
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

ele = [key for key in courses if"ELECTIVE-I" in courses[key] and"Elective-II" in courses[key]]

# Step 2: Retrieve subjects from both categories for those classes
ele_sub =list(set(
    subject
    for key in ele  # Iterate over identified classes
    for subject in courses[key]['ELECTIVE-I'].keys()  # Get the subjects for"ELECTIVE-I"
))

# print(ele_sub)


                
                # Strip spaces from each teacher's name and capitalize them
                

# import pprint
# pprint.pprint(lab_hr)
# print(sum(lab_hr.values()))

# pprint.pprint(th_hr)
# print(sum(th_hr.values()))


list1 = ["Dr KIRUBANAND V B", "Dr FABIOLA HAZEL POHRMEN", "Dr CYNTHIA"]

list2 = ["Dr SARAVANAKUMAR K", "Dr SANGEETHA GOVINDA", "Dr SMERA"]


list3 = ["Dr RAMAMURTHY B", "Dr AMRUTHA"]

# Converting all elements to upper case
# print(list1)
list1 = [name.upper() for name in list1]
list2 = [name.upper() for name in list2]
list3 = [name.upper() for name in list3]




            



# # Print sorted results
# for course, details in courses.items():
#     print(f"{course}: {TOTALHR[course]} hours")
#     for section, subjects in details.items():
#         for subject, info in subjects.items():
#             print(f"  {subject} - Total Hours: {info['total_hours_per_week']}")


def print_courses_table(courses):
    # Print overall headers
    print(f"{'Subject Name':<40} {'Theory Hours':<15} {'Lab Hours':<10} {'Total Hours':<10}")
    print("=" * 85)
    classig=["5BCA B","3BCA B","1BCA B","BCOM-II","BCOM-I","BCOM-III"]
    subig=["MDC","LIBRARY","HED","MATHEMATICS"]
    # Initialize overall total hours
    grand_total_hours = 0

    # Iterate through each class
    for class_name, categories in courses.items():
        total_hours_for_class = 0  # Reset total for the class
        if  class_name in classig:
            continue


        # Print class header
        print(f"\nclass name= {class_name}")
        print("-" * 85)

        # Iterate through categories and subjects
        for category, subjects in categories.items():
            for subject_name, details in subjects.items():
                if subject_name in  subig:
                    continue

                lab_hours = details.get('lab_hours', 0)
                theory_hours = details.get('normal_hours', 0)
                total_hours = lab_hours + theory_hours
                total_hours_for_class += total_hours

                # Print subject details
                print(f"{shortsub[subject_name]:<40} {theory_hours:<15} {lab_hours:<10} {total_hours:<10}")

        # Print total for the class
        print(f"{'Total for ' + class_name:<40} {'':<15} {'':<10} {total_hours_for_class:<10}")
        
        # Update grand total
        grand_total_hours += total_hours_for_class

    # Print grand total for all classes
    print("=" * 85)
    print(f"{'Grand Total':<40} {'':<15} {'':<10} {grand_total_hours:<10}")

# Example usage
print_courses_table(courses)

