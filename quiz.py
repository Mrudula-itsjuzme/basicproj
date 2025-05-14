import random

def sassy_quiz():
    questions = [
        {
            "question": "What's the capital of England?",
            "options": ["London", "Manchester", "Liverpool", "Birmingham"],
            "answer": "London",
            "sassy_remarks": [
                "Nice one, Einstein.",
                "Seriously? It's the big smoke, darling.",
                "Oh honey, do you even geography?"
            ]
        },
        {
            "question": "Who painted the Mona Lisa?",
            "options": ["Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso", "Michelangelo"],
            "answer": "Leonardo da Vinci",
            "sassy_remarks": [
                "Brush up on your art history, honey.",
                "That's a masterpiece of a wrong answer.",
                "Not quite. Think Italian Renaissance!"
            ]
        },
        {
            "question": "Which mammal can fly?",
            "options": ["Bat", "Dolphin", "Elephant", "Kangaroo"],
            "answer": "Bat",
            "sassy_remarks": [
                "Spot on, bat-tastic!",
                "Correct, but don't get too carried away.",
                "Bats are soaring, unlike your guesses."
            ]
        }
    ]
    
    score = 0
    
    print("Salutations, darling! Welcome to the Quiz!")
    print("Answer the following questions with style:")
    
    for i, question in enumerate(questions, start=1):
        print(f"\nQuestion {i}: {question['question']}")
        print("Options:")
        for option in question['options']:
            print("-", option)
        
        user_answer = input("Your answer: ")
        
        if user_answer.lower() == question['answer'].lower():
            print("Correct! You've got it right!")
            score += 1
        elif user_answer.capitalize() not in [option.capitalize() for option in question['options']]:
            print("Nice try, but that's not one of the options.")
            sassy_remark = random.choice(question['sassy_remarks'])
            print(f"{sassy_remark}")
        else:
            sassy_remark = random.choice(question['sassy_remarks'])
            print(f"Wrong answer! {sassy_remark}")
    
    print(f"\nWell done, love! You scored {score} out of {len(questions)}. Until next time, keep that sass alive!")
    
sassy_quiz()
