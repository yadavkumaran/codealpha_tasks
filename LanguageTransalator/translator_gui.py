from tkinter import *
from tkinter import ttk
from deep_translator import GoogleTranslator
from gtts import gTTS
import os


# Function
def translate_text():
    try:
        text = input_text.get("1.0", END)

        target_lang = language_dict[language_var.get()]

        translated = GoogleTranslator(
            source='auto',
            target=target_lang
        ).translate(text)

        output_text.delete("1.0", END)
        output_text.insert(END, translated)

    except Exception as e:
        output_text.delete("1.0", END)
        output_text.insert(END, f"Error: {e}")

def copy_text():
    translated = output_text.get("1.0", END)
    root.clipboard_clear()
    root.clipboard_append(translated)

def speak_text():
    try:
        text = output_text.get("1.0", END).strip()

        if not text:
            return

        lang = language_dict[language_var.get()]

        tts = gTTS(text=text, lang=lang)

        tts.save("speech.mp3")

        os.system("start speech.mp3")

    except Exception as e:
        print("Speech Error:", e)

# Window
root = Tk()
root.title("Language Translator")
root.geometry("800x700")

# Heading
title = Label(
    root,
    text="Language Translator",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)

# Input Label
Label(root, text="Enter Text").pack()

# Input Box
input_text = Text(root, height=8, width=60)
input_text.pack(pady=10)

# Languages
language_dict = {
    "Tamil": "ta",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Russian": "ru"
}

language_var = StringVar()
language_var.set("Tamil")

dropdown = ttk.Combobox(
    root,
    textvariable=language_var,
    values=list(language_dict.keys()),
    state="readonly"
)

dropdown.pack(pady=10)

# Button
Button(
    root,
    text="Translate",
    command=translate_text,
    font=("Arial", 12)
).pack(pady=10)
Button(
    root,
    text="Copy",
    command=copy_text,
    font=("Arial", 12)
).pack(pady=5)
Button(
    root,
    text="Speak",
    command=speak_text,
    font=("Arial", 12)
).pack(pady=5)
# Output Label
Label(root, text="Translated Text").pack()

# Output Box
output_text = Text(root, height=8, width=60)
output_text.pack(pady=10)

root.mainloop()