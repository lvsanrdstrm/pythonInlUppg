import spacy 
from spacy.matcher import Matcher
from spacytextblob.spacytextblob import SpacyTextBlob



nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('spacytextblob')



metam = open('books\metamorphosis.txt', 'r', encoding='utf8').read()
yellowp = open('books\yellowwallpaper.txt', 'r', encoding='utf8').read()


metamDoc = nlp(metam)
yellowpDoc = nlp(yellowp)


matcher = Matcher(nlp.vocab)

# skapade en class för att jag längre ner genererar data som jag ville spara på smidigt sätt, 
#räckte inte med tex dictionary som jag jobbat med mkt annars
class SentimentSent:
    def __init__(self, doc, phrase, sentence, polarity, mostFreqChar = None):
        self.doc = doc
        self.phrase = phrase
        self.sentence = sentence
        self.polarity = polarity
        self.mostFreqChar = mostFreqChar

    # här har jag brutit ur kod som skapar ett pattern till matchern från add_user_input för att jag
        #ville återanvända matcher-kod till character-funktionen.
def create_pattern(search_word):
    # skapar variabeln searchworddoc och assignar funktionsinputen i form av nlp-doc
    searchWordDoc = nlp(search_word)
    
    #skapar variabeln patter och assignar den de individuella orden i searchworddoc, alltå antingen användarens input eller vanligaste karaktären
    pattern = [{"LOWER": token.lower_} for token in searchWordDoc]
    # här läggs the pattern till matchern
    matcher.add("user_pattern", [pattern])

    # funktion jag kallar på när användaren väljer eget sökord     
def add_user_input():
    # skapar variabeln user_input som jag assignar användarens svar på prompten
    user_input = input("Enter a word to use as a pattern: ")
    # kallar på funktionen create_pattern och kör user input som parameter så att jag får ett pattern in i matchern med sökordet
    create_pattern(user_input)

def book_to_search():
    while True:
        to_search = input("Do you want to search through Metamorphosis by Franz Kafka or The Yellow Wallpaper by Charlotte Perkins? M/Y:  ").lower()
        if to_search == "m":
            doc_to_search = metamDoc
            break
        elif to_search == "y":
            doc_to_search = yellowpDoc    
            break
        else:
            print("Invalid entry. M for Metamorphosis and Y for The Yellow Wallpaper.")
    return doc_to_search  

def end_of_function(current_function_name):
    while True:
        now_what = input("Press B when/if you want to return to the menu. Press A if you want to start over.").lower()
        if now_what == "b":
            print("Okay. Bye!")
            print("----------------------")
            break
        elif now_what == "a":
            current_function_name()
            break
        else:
            print("Invalid entry. Y for Yes or N for No.")
            print("----------------------")    

    return doc_to_search  

def end_of_function(current_function_name):
    while True:
        now_what = input("Press B when/if you want to return to the menu. Press A if you want to start over.").lower()
        if now_what == "b":
            print("Okay. Bye!")
            print("----------------------")
            break
        elif now_what == "a":
            current_function_name()
            break
        else:
            print("Invalid entry. Y for Yes or N for No.")
            print("----------------------")    

   

def search_any_book():
    doc_to_search = book_to_search()

    if doc_to_search == metamDoc:
        book = "Metamorphosis"
    elif doc_to_search == yellowpDoc:
        book = "The Yellow Wallpaper"
    
    add_user_input()            

    matches = matcher(doc_to_search)
   
    matched_phrase_sentence = []

    for match_id, start, end in matches:
        matched_phrase = doc_to_search[start:end].text
        for sent in doc_to_search.sents:
            if start >= sent.start and end <= sent.end:
                matched_sentence = sent.text
                matched_phrase_sentence.append({"phrase": matched_phrase, "sentence": matched_sentence})

    print("----------------------")
    print("Book:", book)
    print("----------------------")

    if matched_phrase_sentence:
        print("Matched phrase:", matched_phrase_sentence[0]["phrase"])
        print("----------------------")

        for match in matched_phrase_sentence:
            print("Sentence:", match["sentence"])
            print("----------------------")
    else:
        print("No matched phrases found.")
    print("----------------------")
    print("Book:", book)
    print("----------------------")

    if matched_phrase_sentence:
        print("Matched phrase:", matched_phrase_sentence[0]["phrase"])
        print("----------------------")

        for match in matched_phrase_sentence:
            print("Sentence:", match["sentence"])
            print("----------------------")
    else:
        print("No matched phrases found.")
        print("----------------------")
        
   
        
   
    matcher.remove("user_pattern")

    while end_of_function(search_any_book):
        break


def sentiment_process_document(doc_to_process, doc_name, mostFreqChar = None):
    try:
        matches = matcher(doc_to_process)
        if not matches:
            raise ValueError("No matches found in the document.")
        
        matched_phrase_sentence = []
        for match_id, start, end in matches:
            matched_phrase = doc_to_process[start:end].text
            for sent in doc_to_process.sents:
                if start >= sent.start and end <= sent.end:
                    matched_sentence = sent.text
                    polarity = sent._.blob.polarity
                    match = SentimentSent(doc_name, matched_phrase, matched_sentence, polarity, mostFreqChar=mostFreqChar)
                    matched_phrase_sentence.append(match)
        return matched_phrase_sentence  
    except ValueError as e:
        print(e)
        return []
        

def translate_polarity(polarity):
    if 0 > polarity >= -0.5:
        text_polarity = "A bit negative emotional tone."
    elif polarity < -0.5:
        text_polarity = "Very negative emotional tone... :'("
    elif 0 < polarity < 0.5:
        text_polarity = "A bit positive emotional tone."
    elif polarity == 0:
        text_polarity = "Neutral emotional tone."
    else:
        text_polarity = "Very positive emotional tone! :D" 
    return text_polarity 


def sentiment_search():
    
    add_user_input()
    
    metam_matched_phrase_sentence = sentiment_process_document(metamDoc, "Metamorphosis")

    yellowp_matched_phrase_sentence = sentiment_process_document(yellowpDoc, "The Yellow Wallpaper")
    metam_matched_phrase_sentence = sentiment_process_document(metamDoc, "Metamorphosis")

    yellowp_matched_phrase_sentence = sentiment_process_document(yellowpDoc, "The Yellow Wallpaper")
    
    all_matches = metam_matched_phrase_sentence + yellowp_matched_phrase_sentence
    
   
    doc_polarities = {}
    compare_polarities = {}

    
    for match in all_matches:
        if match.doc not in doc_polarities:
            doc_polarities[match.doc] = []
        doc_polarities[match.doc].append(match.polarity)
    
    for doc, polarities in doc_polarities.items():
        avg_polarity = sum(polarities) / len(polarities)
        compare_polarities[doc] = avg_polarity
        avg_polarity = translate_polarity(avg_polarity) 
        avg_polarity = translate_polarity(avg_polarity) 
        print("----------------------")
        print("Book:", doc)
        print("Average emotional tone in sentences with your search word:", avg_polarity)
        

    max_polarity_doc = max(compare_polarities, key=compare_polarities.get)
    min_polarity_doc = min(compare_polarities, key=compare_polarities.get)
    
    print("----------------------")
    print(f"Based on the sentences with your search word, {min_polarity_doc} has a more negative emotional tone than {max_polarity_doc}.")
    print(f"Based on the sentences with your search word, {min_polarity_doc} has a more negative emotional tone than {max_polarity_doc}.")
    print("----------------------")

    matcher.remove("user_pattern")    
    
        
        
    while True:
        print_sentences = input("Would you like to see the sentences the emotional tone analysis was based on? Y/N: ").lower()
        print_sentences = input("Would you like to see the sentences the emotional tone analysis was based on? Y/N: ").lower()
        if print_sentences == "y":
            for match in all_matches:
                match.polarity = translate_polarity(match.polarity)
                match.polarity = translate_polarity(match.polarity)
                print("Document:", match.doc)
                print("Matched phrase:", match.phrase)
                print("Sentence:", match.sentence)
                print("Emotional tone for the sentence:", match.polarity)
                print("----------------------")
            break
        elif print_sentences == "n":
            print("You certainly don't have to. Bye!")
            print("----------------------") 
            break
        else:
            print("Invalid entry. Y for Yes or N for No.")
            print("----------------------")
    
    while end_of_function(sentiment_search):
        break

def common_characters():
    doc_to_search = book_to_search()

    characters = [ent.text for ent in doc_to_search.ents if str(ent.label_) == "PERSON"]
    
    if doc_to_search == metamDoc:
        book = "Metamorphosis"
    elif doc_to_search == yellowpDoc:
        book = "The Yellow Wallpaper"    
    
    characterFreq = {}
    for c in characters:
        if c in characterFreq.keys():
            characterFreq[c] += 1
        else:
            characterFreq[c] = 1    

         
    maxFreq = max(characterFreq.values())
    mostFreqChar = str([key for key, value in characterFreq.items() if value == maxFreq])
    mostFreqChar = mostFreqChar.strip("[]'")
    
    create_pattern(mostFreqChar)
    char_matches = sentiment_process_document(doc_to_search, book, mostFreqChar)

    char_polarities = {}
        
    for match in char_matches:
        if mostFreqChar not in char_polarities:
            char_polarities[match.mostFreqChar] = []
        char_polarities[match.mostFreqChar].append(match.polarity)
    
    for mostFreqChar, polarities in char_polarities.items():
        avg_polarity = sum(polarities) / len(polarities)
        avg_polarity = translate_polarity(avg_polarity) 
        
    
    print("----------------------")
    print(f"The most frequent character in {book} is {mostFreqChar}")
    print(f"The average emotional tone in sentences where {mostFreqChar} occur is {avg_polarity}")
    print("----------------------")
    
    while True:
        print_sentences = input("Would you like to see a selection of the sentences the analysis was based on? Y/N: ").lower()
        if print_sentences == "y":
            for match in char_matches:
                match.polarity = translate_polarity(match.polarity)
                print("Document:", match.doc)
                print("Most frequent character:", match.phrase)
                print("Sentence:", match.sentence)
                print("Emotional tone for the sentence:", match.polarity)
                print("----------------------")
            break
        elif print_sentences == "n":
            print("You certainly don't have to.")   
            break
        else:
            print("Invalid entry. Y for Yes or N for No.")

    matcher.remove("user_pattern")   

    while end_of_function(common_characters):
        break      
   


def common_descriptors():
    doc_to_search = book_to_search()

    '''for token in doc_to_search:
        if token.pos_ == "ADJ":
            print(token.text, '\t', token.pos_)   '''   

    descriptor = [token for token in doc_to_search if token.pos_ == "ADJ"]
    print(descriptor)
     
     #denna vill jag göra en frequent-analys på
    while end_of_function(common_descriptors):
        break
    
    
'''originalfunktionen där både karaktär och descriptor är med. gör om den så jag håller isär karaktär och descriptor
def common_characters():
    doc_to_search = book_to_search()

    characters = [ent.text for ent in doc_to_search.ents if str(ent.label_) == "PERSON"]
    
    if doc_to_search == metamDoc:
        book = "Metamorphosis"
    elif doc_to_search == yellowpDoc:
        book = "The Yellow Wallpaper"    
    
    characterFreq = {}
    for c in characters:
        if c in characterFreq.keys():
            characterFreq[c] += 1
        else:
            characterFreq[c] = 1    

         
    maxFreq = max(characterFreq.values())
    mostFreqChar = str([key for key, value in characterFreq.items() if value == maxFreq])
    mostFreqChar = mostFreqChar.strip("[]'")

       
    print("----------------------")
    print(f"The most frequent character in {book} is {mostFreqChar}")
    print("----------------------")
    
    while True:
        print_sentences = input("Would you like to get a emotional tone analysis of the descriptors associated with the character? Y/N: ").lower()
        if print_sentences == "y":
            for sent in doc_to_search.sents:
                descriptor = ""
                polarity = 0
                
                if mostFreqChar in sent.text and any(token.pos_ == "ADJ" for token in sent):
                    for token in sent:
                        if token.pos_ == "ADJ":
                            descriptor += token.text + ", "
                            polarity += token._.blob.polarity
                    polarity = translate_polarity(polarity)    
                    
                    print("Matched character:", mostFreqChar)
                    print("----------------------")
                    print("Descriptor:", descriptor)
                    print("----------------------")
                    print("Sentence:", sent.text)
                    print("----------------------")
                    print("Polarity:", polarity)
                    print()
            break
        elif print_sentences == "n":
            print("You certainly don't have to.")   
            break
        else:
            print("Invalid entry. Y for Yes or N for No.")

    while end_of_function(common_characters):
        break '''     
   

""" från sentence search
print("----------------------")
    print("Book:", book)
    print("Matched phrase:", matched_phrase_sentence[0]["phrase"]) 
    print("----------------------")

    for match in matched_phrase_sentence:
        print("Sentence:", match["sentence"])
        print("----------------------")"""

"""originella koden från slutet av sentiment analysis, jag testar printa df istället
while True:
        print_sentences = input("Would you like to see all the sentences that contain your search word? Y/N: ").lower()
        if print_sentences == "y":
            for match in all_matches:
                match.polarity = translate_polarity(match.polarity)
                print("Document:", match.doc)
                print("Matched phrase:", match.phrase)
                print("Sentence:", match.sentence)
                print("Emotional tone for the sentence:", match.polarity)
                print("----------------------")
            break
        elif print_sentences == "n":
            print("You certainly don't have to. Bye!")
            print("----------------------") 
            break
        else:
            print("Invalid entry. Y for Yes or N for No.")
            print("----------------------")"""