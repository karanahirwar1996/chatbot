def chatbot():
    print("Hello, I'm a chatbot. How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input == "hi" or user_input == "hello":
            print("Chatbot: Hello there!")
        elif user_input == "bye":
            print("Chatbot: Bye! Have a great day.")
            break
        else:
            print("Chatbot: " + random.choice(["Interesting!", "Okay.", "I see.", "Okay, I understand."]))

chatbot()
