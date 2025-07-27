from colorama import init, Fore, Style

init(autoreset=True)

# =========================
# Utility Print Functions
# =========================
def print_narration(text):
    print(Fore.WHITE + Style.BRIGHT + text)

def print_dialog(text):
    print(Fore.CYAN + Style.BRIGHT + text)

def print_choice(text):
    print(Fore.YELLOW + Style.BRIGHT + text)

# =========================
# Character Definition
# =========================

class MainCharacter:
    def __init__(self):
        self.name = "Sam Carter"
        self.occupation = "Private Detective"
        self.background = (
            "It's the year 1951. You are former catholic priest, and the best investigator in New York, with a reputation for solving the unsolvable, and supernatural. \n"
            "You've been sent to the isolated town of Ashwood to investigate a string of bizarre missing persons reports. \n"
            "All the victims were last seen at a peculiar coffee shop on the edge of town. \n"
            "The townsfolk whisper about the owner, Mr. Blackwood, but no one dares speak openly.\n"
            "You sense something lurking beneath the surface of this case.\n"
        )
        self.case = (
            "The disappearances are strange as there are constant sightings of the victims in reflections or mirrors. "
            "and strange indecipherable symbols found in the town among many other bizarre occurrences around the town as a whole. "
            "Your only solid lead: the coffee shop and its enigmatic owner."
        )

    def introduce(self):
        print_narration(f"You are {self.name}, a {self.occupation}.")
        print_narration(self.background)
        print_narration(f"Current case: {self.case}\n \n \n ")
 
# =========================
# Setting and Introduction
# =========================
def intro():
    print_narration("Welcome to 'Ashwood: A Lovecraftian detective game'.\n")
    print_narration("This is a text-based horror game. Your choices will uncover the truth—or drive you mad.\n \n \n ")
    print_narration("A cold mist clings to the empty streets despite the midday sun sitting high in the sky of an overcast day, as you approach the Blackwood Coffee House. \n"
                    "The sign above the door flickers and creaks in the low wind, and the windows are dingy and fogged, hiding whatever lies within.\n")
    print_narration("You step inside. The air is thick with the scent of coffee and sweets.\n")
    print_narration("The owner, Mr. Blackwood, stands behind the counter, his eyes dark and downcast. \n"
                    "A handful of patrons sit scattered about, each lost in their own world, their faces pale, drawn and just a bit off.\n")

# =========================
# Characters
# =========================
def greet_barista():
    print_dialog('Mr. Blackwood: "Welcome, Detective. May I offer you something... special?"\n')
    print_narration("how did he know my proffestion?")



# =========================
# Actions and Choices
# =========================
def scene_entry_choice():
    used = set()
    while True:
        print_narration("What will you do first?")
        if "1" not in used:
            print_choice("  1. Observe the coffee shop and its patrons.")
        if "2" not in used:
            print_choice("  2. Talk to a nervous-looking patron in the corner.")
        if "3" not in used:
            print_choice("  3. Ignore everyone and sit at a table to watch.")
        if "4" not in used:
            print_choice("  4. Take action: Approach Mr. Blackwood at the counter.\n")
        choice = input(Fore.YELLOW + Style.BRIGHT + "Choose your action (1-4): " + Style.RESET_ALL)
        if choice in used or choice not in {"1", "2", "3", "4"}:
            print(Fore.RED + "Invalid or already chosen option. Please try again.\n")
            continue
        if choice == "1":
            print_narration("\nYou scan the room. The wallpaper peels in strange, swirling patterns. "
                            "A clock ticks backwards above the door. The patrons avoid your gaze, their hands trembling as they sip their drinks and eat their food.\n")
            used.add("1")
        elif choice == "2":
            print_narration("\nYou approach the patron. They flinch at your presence, eyes darting to the shadows.")
            print_dialog('"Don\'t drink the coffee," they whisper, voice trembling. "It shows you things... things you can\'t forget."\n')
            used.add("2")
        elif choice == "3":
            print_narration("\nYou sit at a table, pretending to read a newspaper. "
                            "You feel the weight of unseen eyes upon you.\n")
            used.add("3")
        elif choice == "4":
            print_narration("\nYou stride to the counter. Mr. Blackwood's smile is thin and knowing. "
                            "His fingers drum a rhythm you can't quite place on the polished wood.\n")
            greet_barista()
            break  # Only progress when Action is chosen

def menu_interaction():
    used = set()
    drinks = {
        "1": "Abyssal Brew",
        "2": "Eldritch Espresso",
        "3": "Haunted Mocha",
        "4": "Spectral Cappuccino"
    }
    chosen_drink = None
    print_narration("Mr. Blackwood hands you a menu. The letters are sloppy, and nearly unreadable but somehow you understand them, and the items names are strange and unsettling.\n")
    while True:
        if "1" not in used:
            print_choice("  1. Observe the menu more closely.")
        if "2" not in used:
            print_choice("  2. Talk to Mr. Blackwood about the strange occurrences.")
        if "3" not in used:
            print_choice("  3. Ignore the menu and refuse to order anything.")
        if "4" not in used:
            print_choice("  4. Take action: Order from the menu.\n")
        choice = input(Fore.YELLOW + Style.BRIGHT + "What will you do? (1-4): " + Style.RESET_ALL)
        if choice in used or choice not in {"1", "2", "3", "4"}:
            print(Fore.RED + "Invalid or already chosen option. Please try again.\n")
            continue
        if choice == "1":
            print_narration("\nYou study the menu. The letters are sloppy like a child's handwriting. "
                            "You see a symbol that matches those found at the crime scenes.\n")
            used.add("1")
        elif choice == "2":
            print_narration("\nYou ask Mr. Blackwood about the strange occurrences. "
                            "You notice a flicker of something in his eyes. He remains silent and gestures to the menu again.\n")
            used.add("2")
        elif choice == "3":
            print_narration("\nYou refuse to order. Mr. Blackwood's smile fades, and the room grows colder. "
                            "A shadow flickers at the edge of your vision.\n")
            used.add("3")
        elif choice == "4":
            print_narration("\nYou decide to order a drink. The menu reads:")
            for key, drink in drinks.items():
                print_choice(f"  {key}. {drink}")
            while True:
                drink_choice = input(Fore.YELLOW + Style.BRIGHT + "Which drink will you order? (1-4): " + Style.RESET_ALL)
                if drink_choice in drinks:
                    chosen_drink = drinks[drink_choice]
                    print_narration(f"\nYou order the {chosen_drink}. Mr. Blackwood nods and prepares your drink.\n")
                    break
                else:
                    print(Fore.RED + "Invalid drink choice. Please try again.\n")
            break  # Only progress when Action is chosen
    return chosen_drink

def supernatural_event(chosen_drink):
    used = set()
    print_narration("The lights flicker. and the scent of coffee momentarily shifts to something more rotten.")
    print_narration("A low hum vibrates through the floorboards. The patrons' faces sink then return to normal but still unnerving.")
    print_narration("Mr. Blackwood watches you, his eyes reflecting a light that seems to come from nowhere.\n")
    if chosen_drink:
        print_narration(f"As you sip your {chosen_drink}, a chill runs down your spine. The taste is otherworldly, and you feel reality bending at the edges.\n")
    while True:
        print_narration("What will you do?")
        if "1" not in used:
            print_choice("  1. Observe the unnatural shadows.")
        if "2" not in used:
            print_choice("  2. Talk to the nearest patron about the strange occurrences.")
        if "3" not in used:
            print_choice("  3. Ignore the strangeness and focus on your investigation notes.")
        if "4" not in used:
            print_choice("  4. Take action: Demand answers from Mr. Blackwood.\n")
        choice = input(Fore.YELLOW + Style.BRIGHT + "Choose your action (1-4): " + Style.RESET_ALL)
        if choice in used or choice not in {"1", "2", "3", "4"}:
            print(Fore.RED + "Invalid choice. Please try again.\n")
            continue
        if choice == "1":  # Observe
            print_narration("\nYou stare into the shadows. seemingly nothing is amiss yet your gaze is still drawn with a sense of urgency. "
                            "A cold unease settles over you causing a shiver.\n")
            used.add("1")
        elif choice == "2":  # Talk
            print_narration("\nYou whisper to a patron. They clutch your arm, desperate. "
                            "\"The coffee binds us. We can't leave. Not while it still remembers us.\"\n")
            used.add("2")
        elif choice == "3":  # Ignore
            print_narration("\nYou try to focus on your notes, but the ink runs and forms cryptic warnings: "
                            "\"IT SEES YOU.\"\n")
            used.add("3")
        elif choice == "4":  # Action
            print_narration("\nYou inquire of Mr. Blackwood for answers. He leans in, his voice a whisper: "
                            "\"The shop is greater than you know. It hungers we are all its prey.\"\n"
                            "You feel a confusion by his bizarre words.\n"
                            "You realize he will tell you no more as he returns to his task.")
            break  # Only progress when Action is chosen

def climax():
    used = set()
    print_narration("Suddenly, the world lurches the room tilts a sense of vertigo and movement downward. however you immediately return to normal, as if nothing happened except a headache behind your eyes remains.")
    print_narration("The shadows flicker at the edges of your vision once again as if trying to get your attention.")
    print_narration("You look out the window. The street is empty, the mist thicker than before.")
    print_narration("You blink—and the coffee shop is normal again. Patrons chat quietly. Mr. Blackwood polishes a cup, smiling as if nothing happened.")
    print_narration("But you know something is terribly wrong. You stagger outside into the parking lot with nothing but more questions.\n")
    while True:
        if "1" not in used:
            print_choice("  1. Observe from outside, searching for more clues.")
        if "2" not in used:
            print_choice("  2. Talk to a local about the shop's history.")
        if "3" not in used:
            print_choice("  3. Ignore your fear and try to leave town.")
        if "4" not in used:
            print_choice("  4. Take action: Go back inside and confront the truth.\n")
        choice = input(Fore.YELLOW + Style.BRIGHT + "What will you do? (1-4): " + Style.RESET_ALL)
        if choice in used or choice not in {"1", "2", "3", "4"}:
            print(Fore.RED + "Invalid choice. Please try again.\n")
            continue
        if choice == "1":  # Observe
            print_narration("\nYou watch from outside. The windows darken, and for a moment you see your own reflection—smiling back with someone else's eyes.\n")
            used.add("1")
        elif choice == "2":  # Talk
            print_narration("\nYou find a strange old woman nearby. She whispers, \"The shop was built on cursed ground. It feeds on the lost and forgotten, trapping them inside.\"\n")
            used.add("2")
        elif choice == "3":  # Ignore
            print_narration("\nYou try to leave, but every road leads you back to the coffee shop. The curse will not let you go.\n")
            used.add("3")
        elif choice == "4":  # Action
            print_narration("\nYou step back inside. The shop is unchanged, but the eyes of every patron follow you. "
                            "You sense the story is far from over.\n"
                            "Mr. Blackwood's smile widens as he sees you return, his eyes glinting with a dark knowledge.\n"
                            "A sense of dread fills you as you realize the shop is a trap, and you are its latest victim.\n")
            # Only show outro after Action is chosen
            print("\nAs you stand in the shop, the truth of Ashwood settles over you like a shroud.")
            print("Some doors, once opened, can never be closed. The coffee shop waits for its next visitor...")
            print(Fore.CYAN + Style.BRIGHT + "Thank you for playing Ashwood: A Lovecraftian detective game!")
            print("I hope you enjoyed the game and the story!")
            print("FIN")
            break



# =========================
# Main Game Flow
# =========================
def main():
    detective = MainCharacter()
    detective.introduce()
    intro()
    scene_entry_choice()
    chosen_drink = menu_interaction()
    supernatural_event(chosen_drink)
    climax()

if __name__ == "__main__":
    main()

