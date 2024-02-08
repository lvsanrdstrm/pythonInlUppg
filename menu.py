import main

run = True
while run:
  answer = input("\nMenu\n"
                 "\n Welcome to EmotionSearch2000."
                 "\n This program allows you to search two sources for matches on your chosen search phrase."
                 "\n 1. Free search."
                 "\n    Search Metamorphosis or The Yellow Wallpaper with your chosen search word."
                 "\n    EmotionSearch2000 will print the sentences where your search word occurs."
                 "\n 2. Emotional tone analysis"
                 "\n    Search both books with your chosen search phrase."
                 "\n    EmotionSearch2000 will make an emotional tone comparison of the sentence results."
                 "\n 3. Common character-search."
                 "\n   EmotionSearch2000 will return the name of the most common character in your chosen book"
                 "\n   and print example sentences and emotional tone-analysis of the descriptors associated with the character."
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
          #ska denna verkligen vara med?
          main.common_descriptors()
        case "q":
          print("Shutting down EmotionSearch2000")
          run = False
        case _:
          print(f"'{answer}' is not an option. Choose between 1-4 or Q!")

