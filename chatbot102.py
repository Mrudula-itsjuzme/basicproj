import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import random
import datetime

class BasicChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Chatbot")

        # Initial responses
        self.responses = {
            "hi": "Hello! How can I assist you today? 😊",
            "hello": "Hi there! How can I help you? 👋",
            "good morning": "Good morning! 🌞 What can I do for you today?",
            "hey": "Hey! What’s up? 😎",
            "joke": "Why did the chicken cross the road? To get to the other side! 😂",
            "story": "Once upon a time, there was a chatbot who loved telling stories. 📖",
            "quiz": "Ready for a quiz? Brace yourself! 😎",
            "weather": "I don't have a weather forecast, but it's always sunny in my world! ☀️",
            "news": "I'm not up-to-date with the news, but I can tell you a joke! 😂",
            "goodbye": "See you later! 👋",
            "help": "I can answer questions, tell jokes, and more! Just ask! 😊",
            "thanks": "You're welcome! 😊",
            "yes": "Great! What else can I help you with? 😊",
            "no": "Alright, if you need anything, just let me know! 😊"
        }

        # Custom responses and settings
        self.custom_responses = {}
        self.history = []
        self.personality = "friendly"
        self.current_font = "Arial"
        self.current_size = 12
        self.quiz_questions = {
            "What is the capital of France?": ["Paris", "Rome", "Berlin"],
            "Which planet is known as the Red Planet?": ["Mars", "Earth", "Jupiter"]
        }
        self.current_quiz = None
        self.story_stage = 0

        self.setup_ui()
        self.show_welcome_screen()

    def setup_ui(self):
        self.chat_log = tk.Text(self.root, state=tk.DISABLED, bg="lightgrey", font=(self.current_font, self.current_size))
        self.chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(fill=tk.X, padx=10, pady=5)

        self.entry_box = tk.Entry(self.entry_frame, font=(self.current_font, self.current_size))
        self.entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message, font=(self.current_font, self.current_size))
        self.send_button.pack(side=tk.RIGHT)

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save Chat", command=self.save_chat)
        self.file_menu.add_command(label="Clear Chat", command=self.clear_chat)
        self.file_menu.add_command(label="Show History", command=self.show_history)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.settings_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Change Font Size", command=self.change_text_size)
        self.settings_menu.add_command(label="Change Personality", command=self.change_personality)
        self.settings_menu.add_command(label="Start Story", command=lambda: self.send_message("start story"))
        self.settings_menu.add_command(label="Start Quiz", command=lambda: self.send_message("start quiz"))
        self.settings_menu.add_command(label="Show Random Fact", command=self.show_random_fact)
        self.settings_menu.add_command(label="Show Daily Fact", command=self.show_daily_fact)

        self.help_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Show Help", command=self.show_help)

    def show_welcome_screen(self):
        current_hour = datetime.datetime.now().hour
        if current_hour < 12:
            greeting = "Good morning! Welcome to the Enhanced Chatbot!"
        elif 12 <= current_hour < 18:
            greeting = "Good afternoon! Welcome to the Enhanced Chatbot!"
        else:
            greeting = "Good evening! Welcome to the Enhanced Chatbot!"
        welcome_message = f"{greeting}\n\nFeel free to ask me anything. I can tell jokes, answer questions, and more. Use the menu for options! 😊"
        messagebox.showinfo("Welcome", welcome_message)

    def get_response(self, user_input):
        if self.story_stage == 0:
            if "start story" in user_input.lower():
                self.story_stage = 1
                return "Once upon a time, there was a chatbot who wanted to explore the world. What happened next? Type 'continue' to find out."
            return self.custom_responses.get(user_input.lower(), self.responses.get(user_input.lower(), "Sorry, I don't understand that."))
        elif self.story_stage == 1:
            if "continue" in user_input.lower():
                self.story_stage = 2
                return "The chatbot met a wise old wizard. The wizard offered three magical gifts. Type 'gift 1', 'gift 2', or 'gift 3' to choose."
            return self.custom_responses.get(user_input.lower(), self.responses.get(user_input.lower(), "Sorry, I don't understand that."))
        elif self.story_stage == 2:
            if "gift 1" in user_input.lower():
                return "The chatbot chose gift 1: a magic wand that grants one wish. The end!"
            elif "gift 2" in user_input.lower():
                return "The chatbot chose gift 2: a magical map to unknown lands. The end!"
            elif "gift 3" in user_input.lower():
                return "The chatbot chose gift 3: a potion of eternal youth. The end!"
            return self.custom_responses.get(user_input.lower(), self.responses.get(user_input.lower(), "Sorry, I don't understand that."))
        elif "quiz" in user_input.lower():
            return self.start_quiz()
        elif self.current_quiz and user_input.lower() in self.quiz_questions[self.current_quiz]:
            return self.check_answer(user_input.lower())
        else:
            return self.custom_responses.get(user_input.lower(), self.responses.get(user_input.lower(), "Sorry, I don't understand that."))

    def send_message(self, event=None):
        user_input = self.entry_box.get()
        if user_input:
            self.update_chat_log(f"You: {user_input}")
            response = self.get_response(user_input)
            self.update_chat_log(f"Bot: {self.format_text(response)}")
            self.entry_box.delete(0, tk.END)

    def update_chat_log(self, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.yview(tk.END)
        self.history.append(message)  # Save message to history

    def save_chat(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, "w") as file:
                file.write(self.chat_log.get("1.0", tk.END))

    def clear_chat(self):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.delete("1.0", tk.END)
        self.chat_log.config(state=tk.DISABLED)
        self.history = []

    def show_history(self):
        history_message = "\n".join(self.history)
        messagebox.showinfo("Conversation History", history_message)

    def change_text_size(self):
        size = simpledialog.askinteger("Change Font Size", "Enter new font size:", minvalue=8, maxvalue=36)
        if size:
            self.current_size = size
            self.chat_log.config(font=(self.current_font, self.current_size))
            self.entry_box.config(font=(self.current_font, self.current_size))
            self.send_button.config(font=(self.current_font, self.current_size))

    def change_personality(self):
        personality = simpledialog.askstring("Change Personality", "Enter new personality (friendly/sassy):")
        if personality in ["friendly", "sassy"]:
            self.personality = personality

    def show_random_fact(self):
        facts = [
            "Bananas are berries, but strawberries aren't.",
            "A group of flamingos is called a 'flamboyance.'",
            "There are more stars in the universe than grains of sand on all the Earth's beaches.",
        ]
        fact = random.choice(facts)
        messagebox.showinfo("Random Fun Fact", fact)

    def show_daily_fact(self):
        daily_facts = [
            "Did you know? Honey never spoils.",
            "Fact: A day on Venus is longer than a year on Venus.",
            "Did you know? An octopus has three hearts.",
        ]
        today = datetime.date.today().day
        fact = daily_facts[today % len(daily_facts)]
        messagebox.showinfo("Daily Fact", fact)

    def start_quiz(self):
        self.current_quiz = random.choice(list(self.quiz_questions.keys()))
        options = self.quiz_questions[self.current_quiz][1:]
        random.shuffle(options)
        options = [self.quiz_questions[self.current_quiz][0]] + options
        options_text = ", ".join(options)
        return f"Quiz Time! {self.current_quiz}\nOptions: {options_text}"

    def check_answer(self, answer):
        correct_answer = self.quiz_questions[self.current_quiz][0]
        if answer == correct_answer:
            return "Correct! 🎉"
        return "Oops, that's not right. 😢"

    def format_text(self, text):
        if self.personality == "sassy":
            return text.upper() + " 😏"
        return text

    def show_help(self):
        help_text = (
            "Here's how you can interact with me:\n"
            "- Hi, hello, hey, good morning (greetings)\n"
            "- Joke (ask for a joke)\n"
            "- Story (start a story)\n"
            "- Quiz (start a quiz)\n"
            "- Weather (ask for weather)\n"
            "- News (ask for news)\n"
            "- Goodbye (end the chat)\n"
            "- Help (show this help)\n"
            "- Thanks, yes, no (polite responses)\n"
            "\nEnjoy chatting with me! 😄"
        )
        messagebox.showinfo("Help", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = BasicChatbot(root)
    root.mainloop()
