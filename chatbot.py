import random
import nltk
from nltk.corpus import words
import os

nltk.download('words')
nltk.download('punkt')

pip install psycopg2
import psycopg2

def create_conn():
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    return conn
#def create_conn():
#    conn = psycopg2.connect( host="localhost",
#                                    database="school",
#                                    user="postgres",
 #                                   password="KARAN1996")
 #   return conn

def create_table():
    conn = create_conn()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user_info (name text, age integer, city text)")
    conn.commit()
    conn.close()

def save_user_info(name, age, city):
    conn = create_conn()
    c = conn.cursor()
    c.execute(f"INSERT INTO user_info(name, age, city) VALUES ('{name}',{age},'{city}')")
    conn.commit()
    conn.close()

def chatbot():
    print("Hello, I'm a chatbot. How can I help you today?")
    words = set(nltk.corpus.words.words())
    user_info = {}
    while True:
        user_input = input("You: ")
        if user_input == "hi" or user_input == "hello":
            print("Chatbot: Hello there!")
        elif user_input == "bye":
            print("Chatbot: Bye! Have a great day.")
            break
        elif user_input.lower() in words:
            print("Chatbot: I'm sorry, I don't understand what you're trying to say.")
        elif "my name is" in user_input:
            name = user_input.split("is")[-1].strip()
            print(f"Chatbot: Nice to meet you, {name}!")
            user_info["name"] = name
        elif "my age is" in user_input:
            age = int(user_input.split("is")[-1].strip())
            print(f"Chatbot: Okay, got it. You're {age} years old.")
            user_info["age"] = age
        elif "I live in" in user_input:
            city = user_input.split("in")[-1].strip()
            print(f"Chatbot: Okay, got it. You live in {city}.")
            user_info["city"] = city
        elif user_input == "save my information":
            if "name" in user_info and "age" in user_info and "city" in user_info:
                save_user_info(user_info["name"], user_info["age"], user_info["city"])
                print("Chatbot: Your information has been saved.")
            else:
                print("Chatbot: You need to tell me your name, age, and city first.")
        else:
            print("Chatbot: " + random.choice(["Interesting!", "Okay.", "I see.", "Okay, I understand."]))

create_table()
chatbot()