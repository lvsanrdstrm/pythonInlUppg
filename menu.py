import main

run = True
while run:
  answer = input("\nMenu\n"
                 "\n Welcome to LitSearch2000."
                 "\n This program allows you to search two sources for matches on your chosen search phrase."
                # "\n The result will be ordered according to accuracy."
                  "\n1. Search Metamorphosis with your chosen search phrase."
                  "\n2. Search The Yellow Wallpaper with your chosen search phrase."
                  "\n3. Search Metamorphosis or The Yellow Wallpaper with your chosen search phrase."
                  "\n4. Ask LitSearch2000 about the most common characters in the books."
                  "\n5. Ask LitSearch2000 about the most common descriptive words in the books."
                  "\nQ. Shut down LitSearch2000"
                   "\n-> ").strip()
  match answer.lower():
        case "1":
          print("Welcome to Metamorphosis-search")
          main.search_metam()  
        case "2":
          print("Welcome to The Yellow Wallpaper-search") 
          main.search_yellowp()
        case "3":
          print("Here you can search any of the books.") 
          main.search_any_book()
        case "4":
          print("Entering asking-mode")
          main.common_characters()
        case "5":
          main.common_descriptions()
        case "q":
          print("Shutting down LitSearch2000")
          run = False
        case _:
          print(f"'{answer}' is not an option. Choose between 1-4 or Q!")

