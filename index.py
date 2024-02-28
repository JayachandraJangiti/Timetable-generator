import streamlit as st
import pdfkit
st.title("AUTOMATIC TIMETABLE GENERATOR")
classes = ['A', 'B', 'C', 'D', 'E']
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri',"Sat"]
periods = ['Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5', 'Period 6', 'Period 7']
subs_with_teachers=[]
subjects_with_teachers={}
c=0
# Initialize the timetable with empty slots
timetable = [[[None for period_index in range(len(periods))] for day_index in range(len(days))] for class_index in range(len(classes))]
#for finding credits of a subject
def find_credits(subject):
    for sub,cred in subjects_with_teachers[0].items():
        subj=""
        for i in sub:
            if i=="(":
                break
            else:
                subj+=i
        if subject==subj:
            return subjects_with_teachers[0][sub]
check=0
for i in range(len(classes)):
    st.subheader(f"Enter details about section-{classes[i]}")
    subjects_with_teachers[i]={}
    if i==0:
        number_of_subjects=st.number_input("enter number of subjects",min_value=0,max_value=10,key="i"+"10")
        j=0
        L=[]
        while(j<number_of_subjects):
            subject=st.text_input("Enter subject name",key=j+10)
            teacher=st.text_input(f"Enter Faculty name for {subject}",key=j+100)
            creds=st.number_input(f"Enter number of credits of {subject}",min_value=0,max_value=10,key=j+1000)
            string=subject+"("+teacher+")"
            subjects_with_teachers[i][string]=creds
            L+=[string]
            j+=1
        subs_with_teachers+=[L]
    else:
        L=[]
        for k in range(len(subs_with_teachers[0])):
            subject=""
            for char in subs_with_teachers[0][k]:
                if char=="(":
                    break
                else:
                    subject+=char
            KL=str(c)+"1000000"
            teacher=st.text_input(f"Enter teacher name for {subject}",key=KL)
            #st.write(K)
            c+=1
            string=subject+"("+teacher+")"
            L+=[string]
            subjects_with_teachers[i][string]=find_credits(subject)
            if i==len(classes)-1 and k==len(subs_with_teachers[0])-1:
                check=1
        subs_with_teachers+=[L]

# Initialize the timetable with empty slots
timetable = [[[None for period_index in range(len(periods))] for day_index in range(len(days))] for class_index in range(len(classes))]

#To check if a subject is already assigned on a specific day for a class
def is_subject_assigned(class_index, day_index, subject):
    for period in timetable[class_index][day_index]:
        if period ==subject:
                return True
    return False

#To check if a subject is assigned for any class in a specific period on a specific day
def is_subject_assigned_on_period(day_index, period_index, subject):
    for class_index in range(len(classes)):
        if timetable[class_index][day_index][period_index] ==subject:
            return True
    return False


#To check a particulat slot is assigned or not
def is_particular_slot_filled(class_index,day_index,period_index):
    if timetable[class_index][day_index][period_index]!=None:
        return True
    return False



#For findig next free slot
def find_next_free_period_index(class_index,day_index,ind,days_len):
      while(day_index<days_len):
            ind=ind%4
            while(ind<4):
                  if timetable[class_index][day_index][ind]==None:
                        return day_index,ind
                  ind+=1
            day_index+=1


#To find next free subject
def find_next_subject(class_index,count):
    while(True):
        if count<len(subs_with_teachers[0]):
            sub=subs_with_teachers[class_index][count]
            if subjects_with_teachers[class_index][sub]==0:
                count+=1
            else:
                return sub
        break

#finding teacher from subject
def find_teacher(subject):
    if subject!=None:
          start=0
          end=0
          for i in range(len(subject)):
              if subject[i]=="(":
                  start=i+1
              if subject[i]==")":
                  end=i
              teacher=subject[start:end]
          return teacher


#checking teacher is having other class
def is_teaching_other_class(day_index, period_index, teacher):
    sub_teacher=""
    for class_index in range(len(classes)):
        sub_teacher=find_teacher(timetable[class_index][day_index][period_index])
        if sub_teacher ==teacher:
            return True
    return False

#for checking all subjects are assigned or not
def check_all_are_assigned(subs):
    for subject, hours in subs.items():
        if hours!=0:
            return False
    return True

#finding the subject that is having problem in assigning it
def find_problem_subject(subs):
    for sub,hours in subs.items():
        if hours!=0:
            return sub
       
               
# Print the timetables
def generate_timetable(class_index):
      """for class_index in range(len(classes)):"""
      print("\t\t"+classes[class_index]+":-")
      print('Days', end='\t')
      for period in periods:
            print(period, end='\t')
      print()
      for day_index in range(len(days)):
              print(days[day_index], end='\t')
              for period_index in range(len(periods)):
                  print(timetable[class_index][day_index][period_index], end='\t')
              print()
      print()

"""
#Table for constraints
constraints=[["Teacher","Sub","Class","Day","Hour"]]
constraints+=[["Mr.SH","AI(Mr.SH)",0,0,0]]
subjects_with_teachers[0]["AI(Mr.SH)"]-=1
constraints+=[["Mr.SH","AI(Mr.SH)",1,0,1]]
subjects_with_teachers[1]["AI(Mr.SH)"]-=1
constraints+=[["Mr.SH","AI(Mr.SH)",1,1,0]]
subjects_with_teachers[1]["AI(Mr.SH)"]-=1
constraints+=[["Mr.SH","AI(Mr.SH)",2,1,1]]
subjects_with_teachers[2]["AI(Mr.SH)"]-=1

for row_index in range(1,len(constraints)):
    sub=constraints[row_index][1]
    timetable[constraints[row_index][2]][constraints[row_index][3]][constraints[row_index][4]]=sub

"""



# Assign subjects to the timetable
subject=""
teacher=""
flag=0
count=-1
#subject=subjects[count]
class_index=0
while(class_index<len(classes)):
    day_index=0
    while(day_index<len(days)):
        ind=0
        while(ind<4):#upto four hours 
                  count+=1
                  if subs_with_teachers[0]!=[]:#for streamlit
                      count%=len(subs_with_teachers[0])
                  if flag!=1 and subs_with_teachers[0]!=[]:#for streamlit
                      sub=subs_with_teachers[class_index][count]
                      if subjects_with_teachers[class_index][sub]!=0:
                          subject=sub
                      else:
                          subject=find_next_subject(class_index,count)
                  flag=0
                  period_index=ind
                  if subject!="":#for streamlit
                      teacher=find_teacher(subject)
                  #print("teacher=",teacher)
                  if teacher!="":
                      if not  is_particular_slot_filled(class_index,day_index,period_index) and not is_subject_assigned(class_index, day_index, subject) and not is_teaching_other_class(day_index, period_index, teacher):
                          if period_index<4:
                                timetable[class_index][day_index][period_index] = subject
                                subjects_with_teachers[class_index][sub]-=1
                      else:
                            if day_index!=5 and ind!=3:
                                day_index,period_index=find_next_free_period_index(class_index,day_index,ind,len(days))
                            if not  is_particular_slot_filled(class_index,day_index,period_index) and not is_subject_assigned(class_index, day_index, subject) and not is_teaching_other_class(day_index, period_index, teacher):
                                 if period_index<4:
                                    timetable[class_index][day_index][period_index] = subject
                                    subjects_with_teachers[class_index][sub]-=1
                      ind+=1
                     
        day_index+=1
    if check_all_are_assigned(subjects_with_teachers[class_index]):
        #generate_timetable(class_index)
        class_index+=1
    else:
        subject=find_problem_subject(subjects_with_teachers[class_index])
        flag=1
        day_index=0
        ind=0

"""
labs=["AI-lab","CNS-lab","DIP-lab"]
#Checking labs assigned
def is_lab_assigned(lab,day_index):
    for class_index in range(len(classes)):
        #print(timetable[class_index][day_index][-1])
        if timetable[class_index][day_index][-1]==lab:
            return True
    return False
       
   

#Assigning Labs
count=0
for class_index in range(len(classes)):
    day_index=0
    count=0
    while(day_index<len(days) and count<len(labs)):
        subject=labs[count]
        if not is_lab_assigned(subject,day_index):
            for period_index in range(4,len(periods)):
                timetable[class_index][day_index][period_index]=subject
            count+=1
            day_index+=2
        else:
            day_index+=1
        #generate_timetable(class_index)
       
        #print(day_index)
        day_index%=len(days)

"""
#Assign colors to the cells
cell_colors = [
    ['#fff5b7', '#ffd966', '#ffc61a', '#ffc61a', '#ffc61a', '#ffc61a', '#ffc61a'],
    ['#fff5b7', '#ffd966', '#ffc61a', '#ffc61a', '#ffc61a', '#ffc61a', '#ffc61a'],
    ['#fff5b7', '#ffd966', '#ffc61a', '#ffc61a', '#ffc61a', '#ffc61a', '#ffc61a'],
    ['#fff5b7', '#ffd966', '#ffc61a', '#ffc61a', '#ffc61a', '#ffc61a', '#ffc61a'],
    ['#fff5b7', '#ffd966', '#ffc61a', '#ffc61a', '#ffc61a', '#ffc61a', '#ffc61a'],
]

# Create a Streamlit app
#def main():
st.title("Timetable")

# Display the timetable for each class
for class_index in range(len(classes)):
    st.header(f"Class {classes[class_index]}")

    # Display the timetable as a table with colors using Markdown formatting
    markdown_table = f"<table style='border-collapse: collapse;'>"
    markdown_table += f"<tr style='background-color: #4c7db8; color: white;'>"
    markdown_table += f"<th>Days</th>"
    for period in periods:
        markdown_table += f"<th>{period}</th>"
    markdown_table += "</tr>"

    for day_index in range(len(days)):
        markdown_table += "<tr>"
        markdown_table += f"<td style='background-color: #4c7db8; color: white;'>{days[day_index]}</td>"
        for period_index in range(len(periods)):
            subject = timetable[class_index][day_index][period_index]
            color = cell_colors[class_index][period_index]
            if subject:
                markdown_table += f"<td style='background-color: {color}; color: black;'>{subject}</td>"
            else:
                markdown_table += f"<td style='background-color: {color};'></td>"
        markdown_table += "</tr>"


    markdown_table += "</table>"
    st.markdown(markdown_table, unsafe_allow_html=True)

if st.button('Download PDF'):
    html_content = st._repr_html()
    pdfkit.from_string(html_content, 'output.pdf')
    st.success('PDF downloaded successfully!')

