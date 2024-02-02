import main

run = True
while run:
  answer = input("\nMenu\n"
                 "\n Welcome to LitSearch2000."
                 "\n This program allows you to search two sources for matches on your chosen search phrase."
                 "\n The result will be ordered according to accuracy."
                  "\n1. Enter search word and search through Metamorphosis for matches(temporarily)."
                  "\n2. Print sentences with the word wallpaper."
                  "\nQ. Shut down LitSearch2000"
                   "\n-> ").strip()
  match answer.lower():
        case "1":
            print("Enter search word.")
            # länka till funktion i main där input sker
            main.add_user_input()
        case "2":    
            print("Printing sentences with the word wallpaper")
            main.get_wallpaper_sentences()
        case "q":
            print("Shutting down LitSearch2000")
            run = False
        case _:
            print(f"'{answer}' is not an option. Choose between 1-2 or Q!")

