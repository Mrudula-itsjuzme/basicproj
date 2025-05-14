import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import filedialog, simpledialog
import random

class BasicChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Chatbot")
        self.root.geometry("500x600")
        
        self.current_theme = "lightyellow"
        self.current_font = ("Arial", 12)
        self.themes = ["lightyellow", "lightblue", "lightgreen", "lightpink"]
        self.fonts = [("Arial", 12), ("Courier", 12), ("Times New Roman", 12), ("Comic Sans MS", 12)]

        # Welcome Screen
        self.show_welcome_screen()
        
        self.chat_log = scrolledtext.ScrolledText(self.root, bg=self.current_theme, wrap=tk.WORD, font=self.current_font)
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.entry_frame = tk.Frame(self.root, bg="lightblue")
        self.entry_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.entry_box = tk.Entry(self.entry_frame, font=self.current_font)
        self.entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message, bg="lightgreen", font=self.current_font)
        self.send_button.pack(side=tk.RIGHT, padx=5)
        
        self.entry_box.bind("<Return>", lambda event: self.send_message())
        
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save Chat", command=self.save_chat)
        self.file_menu.add_command(label="Clear Chat", command=self.clear_chat)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        
        self.theme_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Themes", menu=self.theme_menu)
        for theme in self.themes:
            self.theme_menu.add_command(label=theme, command=lambda t=theme: self.change_theme(t))
        
        self.font_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Fonts", menu=self.font_menu)
        for font_name, font_size in self.fonts:
            self.font_menu.add_command(label=f"{font_name} {font_size}", command=lambda fn=font_name, fs=font_size: self.change_font(fn, fs))
        
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_help)
        
        self.responses = {
            # Existing responses...
            "hi": "Hello! How can I assist you today?",
            "hello": "Hey there! What's up?",
            "hey": "Hi! What can I do for you?",
            "good morning": "Good morning! How can I help?",
            "good afternoon": "Good afternoon! What’s on your mind?",
            "good evening": "Good evening! How can I assist you?",
            "how are you?": "I'm just a bunch of code, but thanks for asking! How are you?",
            "what's up?": "Not much, just here to chat with you! What's up with you?",
            "how are things?": "Things are going great! How about you?",
            "what is your name?": "I'm your friendly chatbot created by a brilliant mind!",
            "who are you?": "I'm your chatbot buddy, here to chat and help you out!",
            "bye": "Goodbye! Have a great day!",
            "see you": "See ya! Take care!",
            "catch you later": "Later! Have a good one!",
            "what can you do?": "I can chat with you and keep you company! Ask me anything.",
            "what are your abilities?": "I can answer questions, tell jokes, and chat with you!",
            "tell me a joke": "Why don't scientists trust atoms? Because they make up everything!",
            "joke?": "Here's a joke: Why did the scarecrow win an award? Because he was outstanding in his field!",
            "make me laugh": "Why did the bicycle fall over? Because it was two-tired!",
            "what is the meaning of life?": "42, according to Douglas Adams. But really, it's up to you to decide!",
            "meaning of life?": "Some say it's 42. What do you think it is?",
            "what is your favorite color?": "I'm quite fond of #00FF00. It's a nice shade of green!",
            "favorite color?": "I love the color green, especially #00FF00!",
            "who created you?": "I was created by a genius who loves coding and chatbots!",
            "who made you?": "A brilliant coder brought me to life!",
            "do you like music?": "I don't have ears, but I think music is a wonderful expression of creativity.",
            "music?": "Music is amazing, even though I can't hear it!",
            "what is the capital of India?": "The capital of India is New Delhi.",
            "capital of India?": "New Delhi is the capital of India.",
            "tell me a fun fact": "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still edible!",
            "fun fact?": "Fun fact: A day on Venus is longer than a year on Venus!",
            "do you have a favorite book?": "I'm a big fan of 'Artificial Intelligence: A Modern Approach' by Stuart Russell and Peter Norvig.",
            "favorite book?": "I love 'Artificial Intelligence: A Modern Approach' by Stuart Russell and Peter Norvig.",
            # Space-related questions
            "what is the largest planet in our solar system?": "The largest planet in our solar system is Jupiter.",
            "largest planet?": "Jupiter is the biggest planet in our solar system.",
            "how many planets are in our solar system?": "There are eight planets in our solar system.",
            "planets in solar system?": "There are eight planets orbiting our Sun.",
            "what is a black hole?": "A black hole is a region of space where the gravitational pull is so strong that not even light can escape from it.",
            "black hole?": "A black hole has such strong gravity that nothing can escape from it, not even light!",
            "who was the first person to walk on the moon?": "The first person to walk on the moon was Neil Armstrong, on July 20, 1969.",
            "first moon landing?": "Neil Armstrong was the first person to walk on the moon in 1969.",
            "what is the milky way?": "The Milky Way is the galaxy that contains our Solar System. It's a barred spiral galaxy.",
            "milky way?": "The Milky Way is our home galaxy, a beautiful spiral of stars.",
            "how far is the sun from the earth?": "The average distance from the Earth to the Sun is about 93 million miles or 150 million kilometers.",
            "distance to the sun?": "It's around 93 million miles (or 150 million kilometers) from Earth to the Sun.",
            "what is a light year?": "A light year is the distance that light travels in one year, which is about 5.88 trillion miles or 9.46 trillion kilometers.",
            "light year?": "A light year is how far light travels in a year, roughly 5.88 trillion miles.",
            "what is the closest star to earth?": "The closest star to Earth is the Sun. The closest star outside our solar system is Proxima Centauri.",
            "closest star?": "The Sun is our nearest star. Beyond that, it's Proxima Centauri."
        }
    
    def show_welcome_screen(self):
        welcome_message = "Welcome to the Basic Chatbot!\n\nFeel free to ask me anything. I can tell jokes, answer questions, and more. Use the menu to change themes, fonts, and get help."
        messagebox.showinfo("Welcome", welcome_message)
    
    def change_theme(self, theme):
        self.current_theme = theme
        self.chat_log.config(bg=self.current_theme)
    
    def change_font(self, font_name, font_size):
        self.current_font = (font_name, font_size)
        self.entry_box.config(font=self.current_font)
        self.send_button.config(font=self.current_font)
        self.chat_log.config(font=self.current_font)
    
    def send_message(self):
        user_input = self.entry_box.get().strip()
        if user_input:
            self.entry_box.delete(0, tk.END)
            self.update_chat_log(f"You: {user_input}")
            response = self.get_response(user_input.lower())
            self.update_chat_log(f"Bot: {response}")
    
    def get_response(self, user_input):
        for key in self.responses:
            if user_input in key.lower():
                return self.responses[key]
        return "Sorry, I don't understand that."
    
    def update_chat_log(self, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"{message}\n")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.yview(tk.END)
    
    def save_chat(self):
        file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file:
            file.write(self.chat_log.get("1.0", tk.END))
            file.close()
    
    def clear_chat(self):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.delete("1.0", tk.END)
        self.chat_log.config(state=tk.DISABLED)
    
    def show_help(self):
        help_text = "I can answer the following questions:\n\n"
        for question in self.responses.keys():
            help_text += f"- {question}\n"
        messagebox.showinfo("Help", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = BasicChatbot(root)
    root.mainloop()
