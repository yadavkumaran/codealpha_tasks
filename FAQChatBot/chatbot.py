import json
from tkinter import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load FAQ data
with open("faq.json", "r") as file:
    faq_data = json.load(file)

questions = [item["question"] for item in faq_data]
answers = [item["answer"] for item in faq_data]

# Train TF-IDF model
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)


def send_message():
    user_input = entry_box.get().strip()

    if not user_input:
        return

    # Show user message
    chat_area.config(state=NORMAL)
    chat_area.insert(END, f"You: {user_input}\n")

    # Exit option
    if user_input.lower() == "exit":
        chat_area.insert(END, "Bot: Goodbye!\n\n")
        chat_area.config(state=DISABLED)
        entry_box.delete(0, END)
        return

    # Find best match
    user_vector = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vector, question_vectors)

    best_score = similarity.max()

    if best_score < 0.3:
        response = "Sorry, I don't know the answer."
    else:
        best_match = similarity.argmax()
        response = answers[best_match]

    # Show bot response
    chat_area.insert(END, f"Bot: {response}\n\n")
    chat_area.config(state=DISABLED)

    # Clear entry box
    entry_box.delete(0, END)

    # Auto-scroll
    chat_area.see(END)


# Main Window
root = Tk()
root.title("FAQ Chatbot")
root.geometry("700x500")
root.resizable(False, False)

# Heading
title = Label(
    root,
    text="FAQ Chatbot",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)

# Chat Area
chat_area = Text(
    root,
    width=80,
    height=20,
    font=("Arial", 11)
)
chat_area.pack(padx=10, pady=10)

chat_area.insert(
    END,
    "Bot: Hello! Ask me a question.\n\n"
)
chat_area.config(state=DISABLED)

# Bottom Frame
bottom_frame = Frame(root)
bottom_frame.pack(pady=10)

# Entry Box
entry_box = Entry(
    bottom_frame,
    width=50,
    font=("Arial", 12)
)
entry_box.grid(row=0, column=0, padx=10)

# Send Button
send_btn = Button(
    bottom_frame,
    text="Send",
    command=send_message,
    font=("Arial", 12),
    width=10
)
send_btn.grid(row=0, column=1)

# Enter Key Support
entry_box.bind(
    "<Return>",
    lambda event: send_message()
)

root.mainloop()