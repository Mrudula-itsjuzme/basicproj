import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import random
import datetime

class EnhancedChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Chatbot")

        # Initialize responses and settings
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
            "no": "Alright, if you need anything, just let me know! 😊",
            "astronomy": "Do you have any specific astronomy questions? I can answer some interesting facts about the universe! 🌌"
        }
        
        self.astronomy_questions = {
            "What is the largest planet in our solar system?": "Jupiter",
            "Which planet is known as the Red Planet?": "Mars",
            "What is the closest star to Earth?": "The Sun",
            "Which planet has the most moons?": "Saturn",
            "What is the name of our galaxy?": "The Milky Way",
            "What is the name of the first human to walk on the moon?": "Neil Armstrong",
            "What are the rings of Saturn made of?": "Ice and rock particles",
            "What is the name of the phenomenon when the moon blocks the sun?": "Solar eclipse",
            "What is the hottest planet in our solar system?": "Venus",
            "How many planets are in our solar system?": "Eight",
            "What is a black hole?": "A region of space where gravity is so strong that nothing, not even light, can escape from it.",
            "What is the name of the space telescope that took the famous Hubble Deep Field image?": "Hubble Space Telescope",
            "What causes the phases of the moon?": "The varying angles from which we see the moon's surface lit by the sun.",
            "What is the name of the second-largest planet in our solar system?": "Saturn",
            "Which planet is known for its extensive ring system?": "Saturn",
            "What is a supernova?": "An explosion of a star at the end of its life cycle.",
            "What are the two main types of galaxies?": "Spiral and elliptical",
            "What is the name of the largest volcano in the solar system?": "Olympus Mons on Mars",
            "What is the name of the boundary around a black hole beyond which nothing can escape?": "Event horizon",
            "What causes the seasons on Earth?": "The tilt of Earth's axis relative to its orbit around the sun.",
            "What is the most abundant element in the universe?": "Hydrogen",
            "How far is the Earth from the Sun?": "Approximately 93 million miles or 150 million kilometers",
            "What is the speed of light?": "About 299,792 kilometers per second (186,282 miles per second)",
            "What is the name of the first artificial satellite launched into space?": "Sputnik 1",
            "What is dark matter?": "A form of matter that does not emit light or energy, making it invisible and detectable only through its gravitational effects.",
            "What is the Kuiper Belt?": "A region of the solar system beyond Neptune that contains many small, icy bodies.",
            "What is the name of the first manned mission to land on the moon?": "Apollo 11",
            "What is the Great Red Spot?": "A massive storm on Jupiter",
            "What is a neutron star?": "The remnant of a supernova explosion, composed almost entirely of neutrons.",
            "How many stars are in the Milky Way galaxy?": "Estimated to be between 100 billion and 400 billion",
            "What is the name of the phenomenon when a planet passes in front of a star?": "Transit",
            "What is the name of our solar system's central star?": "The Sun",
            "What is the primary source of energy for the Sun?": "Nuclear fusion",
            "What is an exoplanet?": "A planet that orbits a star outside our solar system.",
            "What is the name of the comet that is visible from Earth approximately every 76 years?": "Halley's Comet",
            "What is the name of the galaxy closest to the Milky Way?": "Andromeda Galaxy",
            "What is a quasar?": "An extremely luminous active galactic nucleus powered by a supermassive black hole.",
            "What is the name of the largest asteroid in the asteroid belt?": "Ceres",
            "What is the name of the first spacecraft to land on the moon?": "Luna 2"
        }
        
        self.custom_responses = {}
        self.history = []
        self.personality = "friendly"
        self.current_font = "Arial"
        self.current_size = 12
        self.current_theme = "Light"
        self.user_profiles = {"default": {"theme": "Light", "font": "Arial", "size": 12, "personality": "friendly"}}
        self.current_profile = "default"
        self.story_stage = 0
        self.current_quiz = None
        self.quiz_questions = {
            "What is the capital of France?": ["Paris", "Rome", "Berlin"],
            "Which planet is known as the Red Planet?": ["Mars", "Earth", "Jupiter"]
        }
        self.language = "English"
        self.astronomy_facts = [
            "The Milky Way galaxy is about 100,000 light-years in diameter.",
            "A day on Venus is longer than a year on Venus.",
            "There are more stars in the universe than grains of sand on all of Earth's beaches.",
            "The largest volcano in the solar system is Olympus Mons on Mars.",
            "Neutron stars are so dense that a sugar-cube-sized amount of their material would weigh about 100 million tons on Earth."
        ]
        
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
        self.file_menu.add_command(label="Load Previous Chat", command=self.load_chat)
        self.file_menu.add_command(label="Clear Chat", command=self.clear_chat)
        self.file_menu.add_command(label="Show History", command=self.show_history)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.settings_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Change Font Size", command=self.change_text_size)
        self.settings_menu.add_command(label="Change Personality", command=self.change_personality)
        self.settings_menu.add_command(label="Change Theme", command=self.change_theme)
        self.settings_menu.add_command(label="Change Font", command=self.change_font)
        self.settings_menu.add_command(label="Start Story", command=lambda: self.send_message("start story"))
        self.settings_menu.add_command(label="Start Quiz", command=lambda: self.send_message("start quiz"))
        self.settings_menu.add_command(label="Show Random Fact", command=self.show_random_fact)
        self.settings_menu.add_command(label="Show Daily Fact", command=self.show_daily_fact)
        self.settings_menu.add_command(label="Show Daily Challenge", command=self.show_daily_challenge)
        self.settings_menu.add_command(label="Change Language", command=self.change_language)
        self.settings_menu.add_command(label="Switch Profile", command=self.switch_profile)
        self.settings_menu.add_command(label="Astronomy Facts", command=self.show_astronomy_fact)
        self.settings_menu.add_command(label="Change Text Size", command=self.change_text_size)

    def show_welcome_screen(self):
        welcome_message = (
            "Welcome to the Enhanced Chatbot!\n\n"
            "You can ask me questions about various topics, tell me to tell jokes, start quizzes, and more! 😄\n"
            "To get started, type your message below or choose an option from the menu."
        )
        self.update_chat_log(f"Bot: {welcome_message}")

    def update_chat_log(self, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"{message}\n")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.yview(tk.END)
        
    def send_message(self):
        user_input = self.entry_box.get().strip().lower()
        if user_input:
            self.update_chat_log(f"You: {self.format_text(user_input)}")
            response = self.get_response(user_input)
            self.update_chat_log(f"Bot: {response}")
            self.history.append(f"You: {user_input}\nBot: {response}\n")
            self.entry_box.delete(0, tk.END)

    def get_response(self, user_input):
        if user_input in self.responses:
            return self.responses[user_input]
        elif user_input in self.custom_responses:
            return self.custom_responses[user_input]
        elif "start story" in user_input:
            return self.start_story()
        elif "start quiz" in user_input:
            return self.start_quiz()
        elif "quiz" in user_input:
            return self.start_quiz()
        elif "joke" in user_input:
            return "Why did the scarecrow win an award? Because he was outstanding in his field! 😂"
        elif "hello" in user_input or "hi" in user_input or "hey" in user_input or "good morning" in user_input:
            return self.responses["hello"]
        elif "thanks" in user_input or "thank you" in user_input:
            return self.responses["thanks"]
        elif "goodbye" in user_input:
            return self.responses["goodbye"]
        elif "weather" in user_input:
            return self.responses["weather"]
        elif "news" in user_input:
            return self.responses["news"]
        elif "astronomy" in user_input:
            return "Sure! Ask me any astronomy question or type 'random fact' for a fun astronomy fact."
        elif "random fact" in user_input:
            return self.show_random_fact()
        elif "daily fact" in user_input:
            return self.show_daily_fact()
        elif "daily challenge" in user_input:
            return self.show_daily_challenge()
        elif "language" in user_input:
            return self.change_language()
        elif "profile" in user_input:
            return self.switch_profile()
        elif "history" in user_input:
            self.show_history()
        elif "change theme" in user_input:
            self.change_theme()
        elif "change font" in user_input:
            self.change_font()
        elif self.current_quiz and user_input:
            return self.check_answer(user_input)
        elif "story" in user_input:
            return self.start_story()
        elif "quiz" in user_input:
            return self.start_quiz()
        else:
            return "I'm not sure how to respond to that. Try asking something else! 🤔"

    def start_story(self):
        stories = [
            "Once upon a time in a faraway land, there was a chatbot who loved to talk. The end!",
            "A long time ago, in a digital realm, a chatbot became friends with everyone it met."
        ]
        return random.choice(stories)

    def save_chat(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write("".join(self.history))

    def load_chat(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.history = file.readlines()
            self.chat_log.config(state=tk.NORMAL)
            self.chat_log.delete(1.0, tk.END)
            self.chat_log.insert(tk.END, "".join(self.history))
            self.chat_log.config(state=tk.DISABLED)

    def clear_chat(self):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.delete(1.0, tk.END)
        self.chat_log.config(state=tk.DISABLED)
        self.history.clear()

    def show_history(self):
        history_text = "\n".join(self.history) if self.history else "No chat history available."
        messagebox.showinfo("Chat History", history_text)

    def change_text_size(self):
        size = simpledialog.askinteger("Change Text Size", "Enter new font size (e.g., 12, 14, 16):")
        if size:
            self.current_size = size
            self.chat_log.config(font=(self.current_font, self.current_size))
            self.entry_box.config(font=(self.current_font, self.current_size))
            self.send_button.config(font=(self.current_font, self.current_size))

    def change_personality(self):
        personality = simpledialog.askstring("Change Personality", "Choose a personality: friendly, sassy")
        if personality in ["friendly", "sassy"]:
            self.personality = personality

    def change_theme(self):
        themes = ["Light", "Dark", "Blue"]
        theme = simpledialog.askstring("Change Theme", f"Choose a theme from: {', '.join(themes)}")
        if theme in themes:
            self.current_theme = theme
            if theme == "Light":
                self.chat_log.config(bg="lightgrey")
                self.root.config(bg="white")
            elif theme == "Dark":
                self.chat_log.config(bg="black", fg="white")
                self.root.config(bg="black")
            elif theme == "Blue":
                self.chat_log.config(bg="lightblue")
                self.root.config(bg="lightblue")
            self.entry_box.config(bg=self.chat_log.cget("bg"), fg=self.chat_log.cget("fg"))
            self.send_button.config(bg=self.chat_log.cget("bg"), fg=self.chat_log.cget("fg"))

    def change_font(self):
        fonts = ["Arial", "Courier", "Times New Roman", "Comic Sans MS"]
        font = simpledialog.askstring("Change Font", f"Choose a font from: {', '.join(fonts)}")
        if font in fonts:
            self.current_font = font
            self.chat_log.config(font=(self.current_font, self.current_size))
            self.entry_box.config(font=(self.current_font, self.current_size))
            self.send_button.config(font=(self.current_font, self.current_size))

    def start_quiz(self):
        self.current_quiz = random.choice(list(self.quiz_questions.keys()))
        choices = "\n".join(self.quiz_questions[self.current_quiz])
        return f"Quiz Time! {self.current_quiz}\nOptions: {choices}"

    def check_answer(self, user_input):
        correct_answers = {
            "What is the capital of France?": "paris",
            "Which planet is known as the Red Planet?": "mars"
        }
        if user_input == correct_answers[self.current_quiz]:
            self.current_quiz = None
            return "Correct! 🎉"
        else:
            return "Incorrect. Try again! 😕"

    def get_astronomy_fact(self):
        return random.choice(self.astronomy_facts)

    def show_astronomy_fact(self):
        fact = self.get_astronomy_fact()
        self.update_chat_log(f"Bot: Did you know? {fact}")

    def show_random_fact(self):
        facts = [
            "Honey never spoils.",
            "Octopuses have three hearts.",
            "There are more stars in the universe than grains of sand on all the Earth's beaches."
        ]
        fact = random.choice(facts)
        self.update_chat_log(f"Bot: Did you know? {fact}")

    def show_daily_fact(self):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        daily_facts = {
            "2024-07-24": "The shortest war in history lasted just 38-45 minutes between Britain and Zanzibar.",
            "2024-07-23": "Honey never spoils; archeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible.",
        }
        fact = daily_facts.get(today, "No daily fact available for today.")
        self.update_chat_log(f"Bot: Daily Fact: {fact}")

    def show_daily_challenge(self):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        challenge = self.daily_challenges.get(today, "No daily challenge available for today.")
        self.update_chat_log(f"Bot: Daily Challenge: {challenge}")

    def change_language(self):
        languages = ["English", "Spanish", "French", "German"]
        language = simpledialog.askstring("Change Language", f"Choose a language from: {', '.join(languages)}")
        if language in languages:
            self.language = language
            self.update_chat_log(f"Bot: Language changed to {self.language}")

    def switch_profile(self):
        profile = simpledialog.askstring("Switch Profile", "Enter profile name:")
        if profile:
            if profile not in self.user_profiles:
                self.user_profiles[profile] = {
                    "theme": "Light",
                    "font": "Arial",
                    "size": 12,
                    "personality": "friendly"
                }
            self.current_profile = profile
            self.update_chat_log(f"Bot: Switched to profile {self.current_profile}")

    def format_text(self, text):
        if self.personality == "sassy":
            return f"Well, well, look who decided to chat. {text}"
        else:
            return text

    def display_help(self):
        help_text = (
            "Available commands:\n"
            "1. 'hello', 'hi', 'hey', 'good morning' - Greeting messages\n"
            "2. 'joke' - Get a joke\n"
            "3. 'story' - Get a random story\n"
            "4. 'quiz' - Start a quiz\n"
            "5. 'weather' - Get a weather forecast (not available)\n"
            "6. 'news' - Get news updates (not available)\n"
            "7. 'thanks', 'thank you' - Express gratitude\n"
            "8. 'goodbye' - End the chat\n"
            "9. 'astronomy' - Ask astronomy-related questions\n"
            "10. 'change theme' - Change chat theme\n"
            "11. 'change font' - Change chat font\n"
            "12. 'change font size' - Change font size\n"
            "13. 'change personality' - Change chatbot personality\n"
            "14. 'random fact' - Get a random fact\n"
            "15. 'daily fact' - Get a daily fact\n"
            "16. 'daily challenge' - Get a daily challenge\n"
            "17. 'change language' - Change chatbot language\n"
            "18. 'switch profile' - Switch user profile\n"
            "19. 'show history' - Show chat history\n"
            "20. 'save chat' - Save chat to a file\n"
            "21. 'load chat' - Load chat from a file\n"
            "22. 'clear chat' - Clear the chat log\n"
            "23. 'show astronomy facts' - Show astronomy facts\n"
        )
        self.update_chat_log(f"Bot: {help_text}")

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = EnhancedChatbot(root)
    root.mainloop()
