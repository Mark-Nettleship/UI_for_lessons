# Imports

from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import datetime
import subprocess
import pyautogui
import time
import pyperclip
import webbrowser
import os
from tkinter.messagebox import showinfo
from itertools import islice
from tktooltip import ToolTip
from Topics_and_Qs import *

# Finding path

absolute_path = os.path.dirname(__file__)
students_folder = "Students\\"
student_folder_path = os.path.join(absolute_path, students_folder)

print(student_folder_path)

# Identifying day for shift

now = datetime.datetime.now()
shift = now.strftime('%A')
print("Shift = " + str(shift))

students = []

'''
match shift:
    
    case "Monday":
        students = ["Emma Johnson", "Marcus Chen", "Olivia Rodriguez", "Liam Patel", "Sophia Nguyen"]
    case "Tuesday":
        students = ["Noah Smith", "Isabella Brown", "Ethan Gonzalez", "Mia Kumar", "Elijah Thompson"]
    case "Wednesday":
        students = ["Ava Martinez", "Oliver Wilson", "Charlotte Lee", "Lucas Davis", "Amelia Garcia"]
    case "Thursday":
        students = [ "Olivia Rodriguez", "Liam Patel", "Sophia Nguyen", "Noah Smith", "Isabella Brown", "Ethan Gonzalez"]
    case "Friday":
        students = ["Mia Kumar", "Elijah Thompson", "Ava Martinez", "Oliver Wilson", "Charlotte Lee", "Lucas Davis", "Amelia Garcia"]
    case "Saturday":
        students = ["Lucas Davis", "Amelia Garcia", "Olivia Rodriguez"]
    case "Sunday":
        students = ["Emma Johnson", "Marcus Chen", "Mia Kumar", "Elijah Thompson","Ava Martinez", "Oliver Wilson"]

'''
if (shift == "Monday"):
    students = ["Emma Johnson", "Marcus Chen", "Olivia Rodriguez", "Liam Patel", "Sophia Nguyen"]
elif (shift == "Tuesday"):
    students = ["Noah Smith", "Isabella Brown", "Ethan Gonzalez", "Mia Kumar", "Elijah Thompson"]
elif (shift == "Wednesday"):
    students = ["Ava Martinez", "Oliver Wilson", "Charlotte Lee", "Lucas Davis", "Amelia Garcia"]
elif (shift == "Thursday"):
    students = [ "Olivia Rodriguez", "Liam Patel", "Sophia Nguyen", "Noah Smith", "Isabella Brown", "Ethan Gonzalez"]
elif (shift == "Friday"):
    students = ["Mia Kumar", "Elijah Thompson", "Ava Martinez", "Oliver Wilson", "Charlotte Lee", "Lucas Davis", "Amelia Garcia"]
elif (shift == "Saturday"):
    students = ["Lucas Davis", "Amelia Garcia", "Olivia Rodriguez"]
elif (shift == "Sunday"):
    students = ["Emma Johnson", "Marcus Chen", "Mia Kumar", "Elijah Thompson","Ava Martinez", "Oliver Wilson"]


# Create window

root = tk.Tk()

root.title("Lesson dashboard")

# Set to full screen with toolbar visible

root.state('zoomed')

# Organising topic list

alphabetical_topic_list = sorted(topic_list)

for i in range(0,len(alphabetical_topic_list), 2):
    try:
        a = topic_list.index(alphabetical_topic_list[i])
    except:
        print("Problem with :" + str(alphabetical_topic_list[i]))
        continue

# Creating frames and scrollbars

frames = []

frame=Frame(root, relief=GROOVE, bd=2, padx=10, pady=10)
frame.pack(side = TOP, padx=10, pady=(50, 0), expand=TRUE)

frames.append(frame)

for i in range(2,6):
    frame=Frame(root, relief=GROOVE, bd=2, padx=10, pady=10)
    frame.pack(side = LEFT, fill=BOTH, padx=10, pady=50, expand=TRUE)
    frames.append(frame)

var = tk.Variable(value=students)
var2 = tk.Variable(value=alphabetical_topic_list)

listbox = tk.Listbox(
    frames[1],
    listvariable=var,
    height=15,
    selectmode=tk.SINGLE,
    exportselection=0
    )

listbox2 = tk.Listbox(
    frames[2],
    listvariable=var2,
    height=50,
    width=25,
    selectmode=tk.SINGLE,
    exportselection=0
    )

scrollbar= Scrollbar(frames[2])

scrollbar.pack(side=RIGHT, fill='y')

scrollbar2= Scrollbar(frames[3])

scrollbar2.pack(side=RIGHT, fill='y')

listbox2.config(yscrollcommand = scrollbar.set)

scrollbar.config(command=listbox2.yview)

# Selection functions

def student_selection(event):
    global selected_student
    selected_indices = listbox.curselection()
    selected_student = [listbox.get(i) for i in selected_indices]
    selected_student = str(selected_student).strip('\'[]\'')

listbox.bind('<<ListboxSelect>>', student_selection)

def topic_selection(event):
    global selected_topic
    global topic_qs
    T.delete(1.0, END)
    selected_indices = listbox2.curselection()
    selected_topic = [listbox2.get(i) for i in selected_indices]
    selected_topic = str(selected_topic).strip('\'[]\'')
    topic_number = topic_list.index(selected_topic)
    
    T.insert(tk.END, (all_qs[topic_number * 5]) + "\n")
    T.insert(tk.END, (all_qs[(topic_number * 5)+1]) + "\n")
    T.insert(tk.END, (all_qs[(topic_number * 5)+2]) + "\n")
    T.insert(tk.END, (all_qs[(topic_number * 5)+3]) + "\n")
    T.insert(tk.END, (all_qs[(topic_number * 5)+4]) + "\n")

listbox2.bind('<<ListboxSelect>>', topic_selection)

def all_student_selection(event):
    global selected_student
    selected_indices = listbox3.curselection()
    selected_student = [listbox3.get(i) for i in selected_indices]
    selected_student = str(selected_student).strip('\'[]\'')

# Making 'Plan for today' file

plan_path = r'C:\Users\markn\Desktop\UI\Students\Plans'
plan_file = open(plan_path + '\\' + now.strftime('%d %b %Y %p') + '.txt', "a")

# Opening correct files, adding today's date, and adding info to 'Plan for today' file
    
email_text1 = '\nIt was great to see you today.\nHere are the notes from our lesson'
email_text1a = '\nIt was great to see you today.'
email_text1b = '\nHere are the notes from our lesson'
email_text2 = 'I am sending you our topic for .'
email_text3 = 'I look forward to seeing you.\nKind regards,\nMark\n'
email_text4 = '--------------------\n\n'
email_text5 = 'NOTES\n\n'
email_text6 = 'NEXT TIME:'

def prepare_notes():

    path = student_folder_path

    for i in students:
        name = str(i)
        split_name = name.split()
        first_name = split_name[0]
        try:
            f = open(student_folder_path + i + '.txt', encoding='utf-8',errors='replace')
            lines = f.readlines()
        except:
            input("There was a problem.")
        try:
            last_line = lines[-1]
            plan_file.write(i + ': ' + '\n\n' + last_line + '\n\n' + '--------------' + '\n\n')
        except:
            print('File was blank.')
        subprocess.Popen(['C:\\Program Files\\Windows NT\\Accessories\\WordPad.exe', path + i + '.txt'])
        window = pyautogui.getWindowsWithTitle(i)
        time.sleep(1)
        fw = pyautogui.getActiveWindow()
        fw.maximize()
        pyautogui.click(500,500)
        pyautogui.hotkey('ctrl', 'end')
        pyautogui.write(['enter'])
        pyautogui.write(['enter'])
        pyautogui.write('-----------------------')
        pyautogui.write(['enter'])
        pyautogui.write(['enter'])
        pyautogui.write(now.strftime('%A %d %B %Y'))
        pyautogui.write(['enter'])
        pyautogui.write(['enter'])
        pyautogui.write('-----------------------')
        pyautogui.write(['enter'])
        pyautogui.write(['enter'])
        pyautogui.write(email_text5)
        time.sleep(0.5)
        pyautogui.write(email_text4)
        time.sleep(0.5)
        pyautogui.write(email_text6)
        time.sleep(0.5)
        fw.minimize()
    plan_file.write("-----------------------\n\n")
    plan_file.write("Student names: \n\n")
    for i in students:
        plan_file.write(i + "\n")
    plan_file.close()
    subprocess.Popen(['C:\\Program Files\\Windows NT\\Accessories\\WordPad.exe', plan_path + '\\' + now.strftime('%d %b %Y %p') + '.txt'])

# Show a list discussion topics that the selected student has already done

def esl_discussion():
    T.delete(1.0, END)
    try:
        selected_student
    except NameError:
        pyautogui.alert('Please select a student.')
    else:
        f = open(student_folder_path + str(selected_student).strip('\'[]\'') + '.txt', encoding='utf-8', errors='replace')
        lines = f.readlines()

        done = []
        for i in lines:
            if ("discussion" in i.lower()):
                done.append(i[11:75].rstrip() + '\n')        
        done = sorted(done)
        for i in done:
                T.insert(tk.END, i)
                
        T.insert(tk.END, "\n\n----------------Finished----------------\n\n")


# Find "nice" phrases the student has used. To be used when writing progress reports

def find_nice():

    T.delete(1.0, END)
    try:
        selected_student
    except NameError:
        pyautogui.alert('Please select a student.')
    f = open(student_folder_path + str(selected_student).strip('\'[]\'') + '.txt', encoding='utf-8')
    lines = f.readlines()
    T.insert(tk.END, "These are some nice phrases that " + str(selected_student) + " has used in our lessons so far:")
    T.insert(tk.END, "\n\n")

    done = []
    for i in lines:
            if ("<--- Nice!" in i):
                done.append(i)
                    
    done = sorted(done)

    for i in done:
            T.insert(tk.END, i)
    T.insert(tk.END, "\n\n")        

    
    T.insert(tk.END, "\n\n----------------End of nice things----------------\n\n")


# Opening IMS files

imsLinks = {'Emma Johnson': 'https://docs.google.com/spreadsheets/d/1Z1wVB7HzWrlkl05Uddg0xROeVePFHhR0-btm9D093nc/edit?usp=drive_link',
            'Marcus Chen': 'https://docs.google.com/spreadsheets/d/1RXZwitlzu0YM6_sjT7ygLMaRwKnfzQcqm8xg7d3HDl0/edit?usp=drive_link',
            'Olivia Rodriguez': 'https://docs.google.com/spreadsheets/d/1a56vljewAS5zLICoqLp-IfT4tnrLyJlQgn_nsTA2XGo/edit?usp=drive_link',
            'Liam Patel': 'https://docs.google.com/spreadsheets/d/1AALuvTgez4X4o1neAzz8NFN00qMfCcNlo1JvuogPTIM/edit?usp=drive_link',
            'Sophia Nguyen': 'https://docs.google.com/spreadsheets/d/1IMQx_vC3Ma6tLejuUYn84PL791EAyLDktmn8vkCVeDU/edit?usp=drive_link',
            'Noah Smith': 'https://docs.google.com/spreadsheets/d/1qgSFuk2QUIGg6vnb4eghLleg-O1EWsE6PS4Diuu2w58/edit?usp=drive_link',
            'Isabella Brown': 'https://docs.google.com/spreadsheets/d/1NkHyT-S1Null4J-qv8At5ocdGmJBwiCnjhoO3u3q7gM/edit?usp=drive_link',
            'Ethan Gonzalez': 'https://docs.google.com/spreadsheets/d/1F2HY2CG2LLKqxwS1rSyh8AxWhC35HQCzYV0ti9v8yqM/edit?usp=drive_link',
            'Mia Kumar': 'https://docs.google.com/spreadsheets/d/1-0qn0mWdR78kGXwbY58ssyGPCamGdD6mD2nnfmE-mnc/edit?usp=drive_link',
            'Elijah Thompson': 'https://docs.google.com/spreadsheets/d/1d06ywMtVKX-pJfuSLEXyJRBoldN9BcQ7QI_JnsXvvwo/edit?usp=drive_link',
            'Ava Martinez': 'https://docs.google.com/spreadsheets/d/1g812dp7-k_uwqeXFDTVLUbWgDDSMsZwjSYbIBUfcBBc/edit?usp=drive_link',
            'Oliver Wilson': 'https://docs.google.com/spreadsheets/d/1tTz5WbVDiWzOgWzmzlyTia259B9FBM7eY28kxVr3_ww/edit?usp=drive_link',
            'Charlotte Lee': 'https://docs.google.com/spreadsheets/d/1U21T4YXzyzR8Xsq4VPyPRLcD2eT9Na2753OK0wt5FG0/edit?usp=drive_link',
            'Lucas Davis': 'https://docs.google.com/spreadsheets/d/1DuRCHWqvXJltjKZfKeVNEREP8f02Z5VtoywEC-NWcF0/edit?usp=drive_link',
            'Amelia Garcia': 'https://docs.google.com/spreadsheets/d/1dvyvPPmx44Ed6948t3zxPb4lo0jgjr5cNUQJ7q0jwqA/edit?usp=drive_link',
}

def open_ims():

    webbrowser.open(imsLinks[selected_student])

# Sort all students alphabetically by first name

sorted_students = dict(sorted(imsLinks.items()))

all_students = []

for key in sorted_students:
    key = str(key).strip("'")
    all_students.append(key)
    
var3 = tk.Variable(value=all_students)

listbox3 = tk.Listbox(
    frames[4],
    listvariable=var3,
    height=50,
    width=25,
    selectmode=tk.SINGLE,
    exportselection=0
    )

listbox3.config(yscrollcommand = scrollbar2.set)

scrollbar2.config(command=listbox3.yview)

listbox3.bind('<<ListboxSelect>>', all_student_selection)

# Notes cleaner - Deletes unneccesary line breaks and message data from most recent lesson notes

def clean_notes():

    start_line = []
    finish_line = []
    notes_to_copy = ""
    try:
        selected_student
    except NameError:
        pyautogui.alert('Please select a student.')
    f = open(student_folder_path + str(selected_student).strip('\'[]\'') + '.txt', encoding='utf-8', errors='replace')
    for line_no, line in enumerate(f):
        if "Notes" in line or "NOTES" in line:
            start_line.append(line_no)
        elif "---------" in line:
            finish_line.append(line_no)
        else:
            continue
    start_point = int(start_line[-1])
    end_point = int(finish_line[-1])
    if start_point > end_point:
        start_point = int(start_line[-2])
    f.seek(0)
    content = f.readlines()
    for i in range(start_point, end_point):    
        notes_to_copy += content[i]
    T.delete(1.0, END)
    pyperclip.copy(notes_to_copy) 
    rawNotes = pyperclip.paste()
    lines = rawNotes.splitlines()
    with open("clean_notes.txt", "w") as newNotes:
        for j in range(len(lines)):
            if (("NOTES:") not in lines[j]) and (("You  to  Everyone") not in lines[j]) and (("You 0") not in lines[j]) and (("You 1") not in lines[j]) and (("From Me") not in lines[j]) and (("Notes from first") not in lines[j]) and (lines[j] != ""):
                newNotes.write(lines[j] + "\n")
    newNotes.close()
    beautifulNotes = open("clean_notes.txt", "r").read()
    pyperclip.copy(beautifulNotes)
    T.insert(tk.END, ("\nSuccess! Notes cleaned. Ready to paste\n\n"))
    T.insert(tk.END, ("\nNotes preview: \n\n"))
    time.sleep(.02)
    pyautogui.click(1000,500)
    pyautogui.hotkey('ctrl', 'end')
    pyautogui.write(['enter'])
    pyautogui.hotkey('ctrl','v')
    
# Write email to student with notes from today's lesson and the topic for the next lesson

def add_email_to_txt_file():
    try:
        window = pyautogui.getWindowsWithTitle(selected_student)[0].minimize()
        window = pyautogui.getWindowsWithTitle(selected_student)[0].maximize()
    except:
        pyautogui.alert("Student's file will be opened.")
        f = open(student_folder_path + selected_student + '.txt', encoding='utf-8',errors='replace')
        subprocess.Popen(['C:\\Program Files\\Windows NT\\Accessories\\WordPad.exe', student_folder_path + selected_student + '.txt'])
        time.sleep(2)
    pyautogui.click(500,500)
    pyautogui.hotkey('ctrl', 'end')
    pyautogui.write(['enter'])
    pyautogui.write(['enter'])
    pyautogui.write('-----------------------')
    pyautogui.write(['enter'])
    pyautogui.write(['enter'])
    pyautogui.write(now.strftime('%A %d %B %Y'))
    pyautogui.write(['enter'])
    pyautogui.write(['enter'])
    pyautogui.write('-----------------------')
    pyautogui.write(['enter'])
    pyautogui.write(['enter'])
    pyautogui.hotkey('ctrl','v')
    pyautogui.write('\n\n')
        
def email_templates():
    try:
        selected_student
    except:
        pyautogui.alert("Please select a student.")
    f = open(student_folder_path + str(selected_student).strip('\'[]\'') + '.txt', encoding='utf-8', errors='replace')
    email_text2 = 'I am sending you our topic for '
    selected_indices = listbox2.curselection()
    selected_topic = [listbox2.get(i) for i in selected_indices]
    selected_topic = str(selected_topic).strip('\'[]\'')
    try:
        topic_number = topic_list.index(selected_topic)
    except:
        pyautogui.alert("Please select a topic.")
    qs = [all_qs[(topic_number * 5)],all_qs[(topic_number * 5)+1],all_qs[(topic_number * 5)+2],all_qs[(topic_number * 5)+3],all_qs[(topic_number * 5)+4]]
    ok_count=0
    problem_qs = []
    for q in qs:
        f.seek(0)
        if q not in f.read():
            print(q + " - Not done yet.")
            ok_count += 1
        else:
            problem_qs.append(q)

    if ok_count == 5:
        first_name_email = selected_student.split()
        first_name_email = first_name_email[0]
        fw = pyautogui.getActiveWindow()
        fw.maximize()
        pyautogui.click(1000,495)
        T.delete(1.0, END)
        pyautogui.write("Hello " + first_name_email + ".")
        pyautogui.write(email_text1a)
        pyautogui.write(email_text1b)
        pyperclip.copy(':')
        pyautogui.hotkey('ctrl','v')
        pyautogui.write(['enter'])
        pyautogui.write(['enter'])
        beautifulNotes = open("clean_notes.txt", "r").read()
        pyautogui.write(beautifulNotes)
        pyautogui.write(['enter'])
        d = next_lesson_date.get("1.0", "end-1c")
        email_text2 = email_text2 + str(d) + "."
        pyautogui.write(email_text2)
        pyautogui.write(['enter'])
        pyautogui.write("In our next lesson, we will talk about " + str(selected_topic).lower() + ". To prepare, please think about the following questions")
        pyperclip.copy(':')
        pyautogui.hotkey('ctrl','v')
        pyautogui.write(['enter'])
        pyautogui.write(['enter'])
        pyautogui.write(all_qs[topic_number * 5] + "\n")
        pyautogui.write(all_qs[(topic_number * 5)+1] + "\n")
        pyautogui.write(all_qs[(topic_number * 5)+2] + "\n")
        pyautogui.write(all_qs[(topic_number * 5)+3] + "\n")
        pyautogui.write(all_qs[(topic_number * 5)+4] + "\n")
        pyautogui.write(['enter'])
        pyautogui.write(email_text3)
        pyautogui.write(['enter'])
        pyautogui.hotkey('ctrl','a')
        pyautogui.hotkey('ctrl','c')
        pyautogui.write(['down'])
        pyautogui.write(['enter'])
        pyautogui.write(['enter'])
        pyautogui.write('-----------------------------------\n\n')
        pyautogui.write("Email draft completed. \n\nIf it looks good, click 'Copy to txt file' to add it to the student's file.")
    else:
        string_list = [str(element) for element in problem_qs]
        delimiter = "\n\n"
        result_string = delimiter.join(string_list)
        msg = 'You have already done some of these questions with this student.\n\nFound the following questions in their text file: \n\n' + result_string
        pyautogui.alert(msg)
    
def open_txt_file():
    try:
        selected_student
    except:
        pyautogui.alert("Please select a student.")
    f = open(student_folder_path + selected_student + '.txt', encoding='utf-8',errors='replace')
    subprocess.Popen(['C:\\Program Files\\Windows NT\\Accessories\\WordPad.exe', student_folder_path + selected_student + '.txt'])

# IMS entry - Opens IMS file and copies lesson info in correct format to paste 

def ims_entry():
    try:
        selected_student
    except:
        pyautogui.alert("Please select a student.")
        return
    if (var3.get() == 1):
        tl = "Discussion: " + this_lesson.get("1.0", "end-1c")
        hw = "Prep for " + next_lesson.get("1.0", "end-1c")
        nl = "Discussion: " +  next_lesson.get("1.0", "end-1c")
    else:
        tl = this_lesson.get("1.0", "end-1c")
        hw = homework.get("1.0", "end-1c")
        nl = next_lesson.get("1.0", "end-1c")
    entry = tl + " / HW - " + hw + " / RF - " + nl
    this_lesson.delete('1.0', END)
    homework.delete('1.0', END)
    next_lesson.delete('1.0', END)
    i = "student name from selection"
    try:
        window = pyautogui.getWindowsWithTitle(selected_student)[0].minimize()
        window = pyautogui.getWindowsWithTitle(selected_student)[0].maximize()
    except:
        pyautogui.alert("Student's file will be opened.")
        open(student_folder_path + selected_student + '.txt', encoding='utf-8',errors='replace')
        subprocess.Popen(['C:\\Program Files\\Windows NT\\Accessories\\WordPad.exe', student_folder_path + selected_student + '.txt'])
    time.sleep(1)
    pyautogui.click(500,500)
    pyautogui.hotkey('ctrl', 'end')
    pyautogui.write(['enter'])
    pyautogui.write("NEXT TIME")
    pyperclip.copy(':')
    pyautogui.hotkey('ctrl','v')
    selected_indices = listbox2.curselection()
    selected_topic = [listbox2.get(i) for i in selected_indices]
    selected_topic = str(selected_topic).strip('\'[]\'')
    pyautogui.write(" Discussion")
    pyperclip.copy(': ')
    pyautogui.hotkey('ctrl','v')
    pyautogui.write(selected_topic)
    T.insert(tk.END, ("\nSuccess! \n\n" + entry + " copied to clipboard."))
    pyperclip.copy(entry)
    time.sleep(1)
    open_ims()
    
    
# Textboxes

T = Text(frames[3], height=15, width = 70, wrap=WORD)
T.pack(side = RIGHT, fill=BOTH, expand=TRUE)
this_lesson = Text(frames[1], height=1, width = 25)
homework = Text(frames[1], height=1, width = 25)
next_lesson = Text(frames[1], height=1, width = 25)
next_lesson_date = Text(frames[1], height=1, width = 25)

ToolTip(T, msg='Output from buttons will be shown here', delay=0.5)
ToolTip(this_lesson, msg='Enter what the student did today', delay=0.5)
ToolTip(homework, msg='Enter student\'s homework', delay=0.5)
ToolTip(next_lesson, msg='Enter the topic of the student\'s next lesson', delay=0.5)
ToolTip(next_lesson_date, msg='Enter the date of the student\'s next lesson', delay=0.5)

# Checkbox

var3 = tk.IntVar()

chk = tk.Checkbutton(frames[1], text="ESL Discussion?", variable=var3, onvalue=1, offvalue=0)

# Buttons

btn = Button(frames[0], text = "Prepare notes", fg = "blue", padx=10, pady=10, height= 1, width = 15, command=prepare_notes)
btn.pack(side="left", fill="x")
btn2 = Button(frames[0], text = "Open IMS", fg = "blue", padx=10, pady=10, height= 1, width = 15, command=open_ims)
btn2.pack(side="left", fill="x")
btn3 = Button(frames[0], text = "Open txt file", fg = "blue", padx=10, pady=10, height= 1, width = 15, command=open_txt_file)
btn3.pack(side="left", fill="x")
btn4 = Button(frames[0], text = "ESL Discussion", fg = "blue", padx=10, pady=10, height= 1, width = 15, command=esl_discussion)
btn4.pack(side="left", fill="x")
btn5 = Button(frames[0], text = "Note cleaner", fg = "blue", padx=10, pady=10, height= 1, width = 15, command=clean_notes)
btn5.pack(side="left", fill="x")
btn6 = Button(frames[0], text = "Find \"Nice!\"", fg = "blue", padx=10, pady=10, height= 1, width = 15, command=find_nice)
btn6.pack(side="left", fill="x")
btn7 = Button(frames[0], text = "IMS entry", fg = "blue", padx=10, pady=10, height= 1, width = 15, command=ims_entry)
btn7.pack(side="left", fill="x")
btn8 = Button(frames[0], text = "Draft email", fg = "blue", padx=10, pady=10, height= 1, width = 15, command=email_templates)
btn8.pack(side="left", fill="x")
btn9 = Button(frames[0], text = "Copy to txt file", fg = "blue", padx=10, pady=10, height= 1, width = 15, command=add_email_to_txt_file)
btn9.pack(side="left", fill="x")


ToolTip(btn, msg='1. Open notes files for today\'s students\n2. Add today\'s date and note section to end of student\'s text file \n3. Create text doc with list of today\'s students and lesson goals', delay=0.5)
ToolTip(btn2, msg='Open the IMS file\nfor the selected student', delay=0.5)
ToolTip(btn3, msg='Opens the text file for the selected student.', delay=0.5)
ToolTip(btn4, msg='Show which discussion topics\nthe selected student has done', delay=0.5)
ToolTip(btn5, msg='Delete unneccesary line breaks\nand message data from the selected \nstudent\'s most recent lesson\'s notes', delay=0.5)
ToolTip(btn6, msg='For reports: List nice phrases\nthe student has used', delay=0.5)
ToolTip(btn7, msg='Add goal of next lesson to student\'s text file\nand open their IMS file. Lesson info can\nbe pasted from the clipboard', delay=0.5)
ToolTip(btn8, msg='Draft an email to the selected student\nincluding the notes from today\'s \nlesson and topic for next time', delay=0.5)
ToolTip(btn9, msg='Copies the drafted email to clipboard and \npastes it at the bottom of the student\'s text file.', delay=0.5)
ToolTip(btn3, msg='Opens the text file for the selected student.', delay=0.5)

ToolTip(listbox, msg='Shows today\'s students in order of lesson time\n(First lesson at the top, last lesson at the bottom)', delay=0.5)
ToolTip(listbox2, msg='Shows discussion topics to use in lessons\n(Click a topic to show the questions)', delay=0.5)
ToolTip(listbox3, msg='Shows all students \nin alphabetical order', delay=0.5)
ToolTip(chk, msg='Click this if you used a standard discussion topic. \nThe "homework" section will be filled in automatically.', delay=0.5)

# Lesson info entry boxes

tl_label = Label(frames[1], text = "This lesson:")
hw_label = Label(frames[1], text = "Homework:")
nl_label = Label(frames[1], text = "Next lesson:")
d_label= Label(frames[1], text = "Next lesson date:")

todaySS = Label(frames[1], text = str(shift) + ":").pack(side = TOP)
numberTodayS = Label(frames[1], text = ("\nYou have ") + str(len(students)) + " students today.").pack(side = TOP)
topicListLabel = Label(frames[2], text = "Topics:").pack(side = TOP)
allStudentsListLabel = Label(frames[4], text = "All students:").pack(side = TOP)

listbox.pack(side = TOP, expand=TRUE)
chk.pack(side = TOP)
tl_label.pack(side = TOP)
this_lesson.pack(side = TOP)
hw_label.pack(side = TOP)
homework.pack(side = TOP)
nl_label.pack(side = TOP)
next_lesson.pack(side = TOP)
d_label.pack(side = TOP)
next_lesson_date.pack(side = TOP)
listbox2.pack(side = LEFT, expand=TRUE)
listbox3.pack(side = LEFT, expand=TRUE)

# Execute Tkinter
root.mainloop()
