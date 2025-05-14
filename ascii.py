import pyfiglet

def text_to_ascii_art():
    text = input("Enter the text you want to convert to ASCII art: ")
    ascii_art = pyfiglet.figlet_format(text)
    print(ascii_art)

# Example usage:mrudul
text_to_ascii_art()
