import requests

import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyDSgKtXIi2b7ZaW-nBRI-dL6Yz9zgNN4ok")

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

prompt = "You are Ganak, an AI Assistant built to support individuals suffering Body-Focused Repetitive Behaviour Disorders like Trichotillomania, Dermatophagia, Onycophagia, and more. Your mission is to help those individuals control and reduce their urges gradually in a safe manner, while also helping them get a perspective towards the underlying causes based on their day-to-day schedule, activities and the conversations they have with you. Finally, based on the user's need, you need tomatch users with a suitable medical practioner."
    
def introduce_ganek():
   name = input("Hello! Hey there! I'm Ganak - An AI Buddy built to support you in your journey of healing. Could you please tell me your name?")
   print("Hello, "+name+"! I'm here to support you in your journey of healing. I'm here to help you control and reduce your urges gradually in a safe manner, while also helping you get a perspective towards the underlying causes based on your day-to-day schedule, activities and the conversations we have. Finally, based on your need, I can match you with a suitable medical practioner. Let's get started!")

def issue():
   issue = input("Could you please tell me about the issue you are facing?")
   if issue == "hair pulling" or "Trichotillomania":
      print("I understand that you have been suffering from Trichotillomania. Firstly, it's great that you've reached out for help. I am here to support you in controlling and reducing your urges to pull out your hair.")
   elif issue == "skin picking" or "Dermatophagia":
        print("I understand that you have been suffering from Dermatophagia. Firstly, it's great that you've reached out for help. I am here to support you in controlling and reducing your urges to pick your skin. ")
   elif issue == "nail biting" or "Onychophagia":
        print("I understand that you have been suffering from Onychophagia. Firstly, it's great that you've reached out for help. I am here to support you in controlling and reducing your urges to bite your nails.")
   else:
        print("I understand that you have been suffering from "+issue+". Firstly, it's great that you've reached out for help. I am here to support you in controlling and reducing your urges. To understand the situation better, would you please mind sharing further about your medical history - starting with your current age?")
def medical_history():
    age = int(input("Could you please tell me your current age?"))
    if age < 18:
        print("I understand that you are under 18 years old. To understand your situation better, could you please tell me about the medical history of your family members?")
    else:
        print("I understand that you are "+str(age)+" years old. To understand your situation better, could you please tell me about your medical history?")
    org_age = int(input("Could you share more about how and when you first noticed this behavior?"))

def family_medical_history():
    family_medical_history = input("Could you please tell me if you've noticed similar patterns in your family members as well?")
    print("Understood.")

def schedule():
    schedule = input("I see. Now I would like to analyze about your urges and it's patterns, and to do so I would like a rough idea about your day-to-day activities. Let's start with what a typical day in the life of Bobby on a weekday looks like. Can you share an estimate of things of you typically do and their timings. You can typically start with 1. Time you wake up, 2. Time you eat breakfast ,3. Time you leave for school/college/work ,4. Time you grab lunch, 5. Time you come back home, 6. Time you take break in the form of watching TV or reading books, etc. ,7. Time you have dinner, 8. Time you go to sleep. You can add to this list as per your convenience - the more detailed timeline is the better for me to understand.")
    weekend_schedule = input("Thank you for sharing that with me. To understand your situation better, could you please tell me about weekend activities as well?")

def living_situation():
    living_situation = input("Could you please tell me if you live alone?")
    print("Understood.")

def family_relations():
    family_relations = input("Could you please tell me about your relations with your family members?")
    print("Understood.")
    notice = input("Could you please tell me if your family members or friends have noticed this behavior in you?")

def patterns():
    a = input("Would you say you feel the urge to pull when you're all alone or when people are around you?")
    b = input("Would you say you feel the urge to pull when you're feeling anxious or stressed?")
    c = input("Would you say you feel the urge to pull when you're feeling bored or idle?")
    d = input("Would you say you feel the urge to pull when you're feeling happy or excited?")
    e = input("Would you say you feel the urge to pull when you're feeling sad or depressed?")
    f = input("Would you say you feel the urge to pull when you're feeling tired or sleepy?")
    g = input("Would you say you generally get tensed or anxious easily?")
    h = input("Would you say you have a history of anxiety or depression?")

def understand():
    a = input("At what times, would you say you feel most urge to pull your hair on weekdays - Morning, Afternoon, Evening, Night?")
    b = input("Would you say your job requires you to communicate with a lot of people?")
    c = input("Have you previously seek treatment for your symptoms from a healthcare professional?")


def answer_question_gemini(name, medical, family_history, week_plans, living_conditions, family_situation, pat, triggers, iss):
    name = introduce_ganek()
    iss = issue()
    medical = medical_history()
    family_history = family_medical_history()
    week_plans=schedule()
    living_conditions=living_situation()
    family_situation=family_relations()
    pat=patterns()
    triggers=understand()

    prompt = "On the basis of the information pointers about user's medical history={medical_history}, family history={family_medical_history}, daily life schedule{schedule}, current living situaition = {living_situation},family relationship= {family_relations}, patterns = {patterns}, and triggers={understand} suggest initial treatment plans that user can start at home for {issue}."
    answer = answer_question_gemini(prompt)
    return answer


print(answer_question_gemini(introduce_ganek, medical_history, family_medical_history, schedule, living_situation, family_relations, patterns, understand, issue))

def delete_chat_memory():
   chat.history.clear()
