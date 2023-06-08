import names
import random
student_num = 750
admin_num = 10
student_cs = 600
tutor_num = 20
student_requests_num = 10
tutor_request_num = 100
tutor_cs = 50
t_xp = 200
ttr = 100
ser = 100
courses = ['GEN_CHEM1','ANATOMY','AP_PHYSICS','AP_PSYCH',
           'AP_CALC_BC','AP_CALC_AB','AP_GOV',
           'AP_US_HISTORY','AP_WORLD_HISTORY']
course_num = len(courses)
pos_times = ['7:00_AM','8:00_AM','9:00_AM','10:00_AM','11:00_AM','12:00_PM','1:00_PM','2:00_PM','3:00_PM','4:00_PM','5:00_PM','6:00_PM','7:00_PM']
def main():
    course_ids = random.sample(range(10000,99999),course_num)
    courses1 = random.sample(courses,k = course_num)

    course_offerings = tuple(zip(course_ids,courses1))


    course_dict= dict(zip(course_ids,courses1))
    cid_zip = dict(zip(courses1,course_ids))

    tutor_names = []
    i = 0
    while i < tutor_num:
        j = names.get_first_name().upper()
        k = names.get_last_name().upper()
        if j + ' ' + k not in tutor_names:
            tutor_names.append(j.upper() + '_' + k.upper())
            i += 1
        else:
            pass

    tutor_ids = random.sample(range(1000,9999),k = tutor_num)
    tutor_emails = [x.split('_')[0].lower() + f'{random.randint(1,9)}' * random.randint(0,2) + x.split('_')[1].lower()  + '@gmail.com' for x in tutor_names]


    tutor_name_em = dict(zip(tutor_names,tutor_emails))

    tutors_info = tuple(zip(tutor_ids,tutor_names,tutor_emails))
    tut_tup = tuple(zip(tutor_names,tutor_ids))

    tut_avail = random.choices(tutor_ids,k = 2*course_num)

    tut_courses = random.choices(courses,k = 2*course_num)

    tut_fin = tuple(zip(tut_avail,tut_courses))[:course_num]



    student_ids = random.choices(range(2000000000,2100000000),k = student_num)

    student_names = []
    i = 0
    while i < student_num:
        j = names.get_first_name()
        k = names.get_last_name()
        if j + ' ' + k not in tutor_names + student_names:
            i+=1
            student_names.append(j.upper() + '_' + k.upper())
        else:
            pass

    student_emails = [x.split('_')[0].lower() + f'{random.randint(1,9)}' * random.randint(0,2) + x.split('_')[1].lower()  + '@gmail.com' for x in student_names]

    student_info = tuple(zip(student_ids,student_names,student_emails))


    admin_names = []
    i = 0
    while i < admin_num:
        name = names.get_first_name()
        l_name = names.get_last_name()
        if name + '_' + l_name not in admin_names + tutor_names + student_names:
            admin_names.append(name + '_' + l_name)
            i+= 1
        else:
            pass

    admin_emails = [x.split('_')[0].lower() + f'{random.randint(1,9)}' * random.randint(0,2) + x.split('_')[1].lower()  + '@gmail.com' for x in admin_names]

    administrators = tuple(zip(admin_names,admin_emails))


    xp_ids = random.choices(tutor_ids,k = t_xp*2)
    xp_slots = []
    k = 0
    while k < t_xp * 2:
        ind = random.randint(0,len(pos_times) - 3)
        time1 = pos_times[ind]
        time2 = pos_times[ind + 2]

        xp_slots.append(time1 + '-' + time2)
        k+=1
        
    xp_cids = random.choices(course_ids,k = t_xp*2)

    xp_exp = [course_dict[x] for x in xp_cids]

    tutor_availability = tuple(set(tuple(zip(xp_ids,xp_slots,xp_cids,xp_exp))))[:t_xp]

    tutors_course = tuple(set(tuple(zip([x[0] for x in tutor_availability],[x[2] for x in tutor_availability],[course_dict[x] for x in xp_cids]))[:tutor_cs]))


    # print(tutors_course)
    student_tutors = tuple(zip(random.choices(student_ids,k = student_cs),[x[1] for x in tutors_course],[x[0] for x in tutors_course]))

    tutor_teaching_request = tuple(set(tuple(zip(xp_ids[t_xp:t_xp + ttr],xp_slots[t_xp:t_xp + ttr],xp_cids[t_xp:t_xp + ttr]))))





    student_enrollment_request = tuple(zip(random.sample(student_ids,k = student_cs),[x[2] for x in tutor_availability[tutor_cs:tutor_cs + ser]],[x[1] for x in tutor_availability[tutor_cs:tutor_cs + ser]],[x[0] for x in tutor_availability[tutor_cs:tutor_cs + ser]]))

    full_str = []
    for table in [('course_offerings',course_offerings),('tutor_availability',tutor_availability),('student_enrollment_request',student_enrollment_request),('tutor_teaching_request',tutor_teaching_request),('administrator',administrators),('student_info',student_info),('student_tutors',student_tutors),('tutors_info',tutors_info),('tutors_courses',tutors_course)]:
        for ex in table[1]:
            st = ""
            for val in ex:
                try:
                   st += f" {int(val)}" 
                except Exception:
                    st += f" {val}"
            full_str.append(f"{table[0]}" + st)
    lst = '\n'.join(full_str)

    # lst = '\n'.join(full_str)
    text_file = open("auto_mock_data.txt", "w")
    n = text_file.write(lst)
    text_file.close()
if __name__ == '__main__':
    main()
main()