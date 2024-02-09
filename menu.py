import main

run = True
while run:
  answer = input("\nMenu\n"
                 "\n Welcome to EmotionSearch2000."
                 "\n This program allows you to explore the emotional tone of two books through different variables."
                 "\n    Your choices are as follows:"
                 "\n 1. Free search."
                 "\n    Search Metamorphosis or The Yellow Wallpaper with your chosen search word."
                 "\n    EmotionSearch2000 will print the sentences where your search word occurs, without emotional tone analysis."
                 "\n 2. Emotional tone analysis based on your search word."
                 "\n    Search both books with your chosen search word."
                 "\n    EmotionSearch2000 will make an emotional tone comparison of the sentence results."
                 "\n 3. Emotional tone analysis based on the most common character in your book of choice."
                 "\n   EmotionSearch2000 will return the name of the most common character in your chosen book"
                 "\n   and print an emotional tone-analysis of the sentences where the character occur."
                 "\n    You can then choose to see the sentences the analysis is based on."
                  # denna fungerar inte som den ska än
                 "\n 4. Ask EmotionSearch2000 about the most common descriptive words in the books."
                 "\n Q. Shut down EmotionSearch2000"
                   "\n-> ").strip()
  match answer.lower():
        case "1":
          print("Entering free search mode. You first choose book and then search word.") 
          main.search_any_book()
        case "2":
          print("Entering emotional tone-mode.") 
          main.sentiment_search()
        case "3":
          print("Entering character search-mode")
          main.common_characters()
        case "4":
          print("Entering descriptor search-mode")
          main.common_descriptors()
        case "q":
          print("Shutting down EmotionSearch2000")
          run = False
        case _:
          print(f"'{answer}' is not an option. Choose between 1-4 or Q!")

