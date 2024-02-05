import spacy 
nlp = spacy.load('en_core_web_lg')

from spacy.matcher import Matcher


metam = open('books\metamorphosis.txt', 'r', encoding='utf8').read()
yellowp = open('books\yellowwallpaper.txt', 'r', encoding='utf8').read()

metamDoc = nlp(metam)
yellowpDoc = nlp(yellowp)

matcher = Matcher(nlp.vocab)
  

def add_user_input():
    
# Example user input
    user_input = input("Enter a phrase to use as a pattern: ")
    
    # Tokenize user input using spaCy
    searchWordDoc = nlp(user_input)

    # Create pattern from user input
    pattern = [{"LOWER": token.lower_} for token in searchWordDoc]

    # Add pattern to the matcher
    matcher.add("user_pattern", [pattern])


def search_metam(): 
    add_user_input()
    # Perform matching
    matches = matcher(metamDoc)

    # iterate through the sentences and check if start and end of phrase in in sentence
    matched_phrase_sentence = []

    for match_id, start, end in matches:
        matched_phrase = metamDoc[start:end].text
        for sent in metamDoc.sents:
            if start >= sent.start and end <= sent.end:
                matched_sentence = sent.text
                matched_phrase_sentence.append({"phrase": matched_phrase, "sentence": matched_sentence})

    # Print the result
    for match in matched_phrase_sentence:
        print("Matched phrase:", match["phrase"])
        print("Sentence:", match["sentence"])
        print()


    matcher.remove("user_pattern")       

def search_yellowp():
    add_user_input()

    matches = matcher(yellowpDoc)


    # iterate through the sentences and check if start and end of phrase in in sentence
    matched_phrase_sentence = []

    for match_id, start, end in matches:
        matched_phrase = yellowpDoc[start:end].text
        for sent in yellowpDoc.sents:
            if start >= sent.start and end <= sent.end:
                matched_sentence = sent.text
                matched_phrase_sentence.append({"phrase": matched_phrase, "sentence": matched_sentence})

    # Print the result
    for match in matched_phrase_sentence:
        print("Matched phrase:", match["phrase"])
        print("Sentence:", match["sentence"])
        print()

    matcher.remove("user_pattern")   

def search_any_book():
    add_user_input()

    to_search = input("Do you want to search through Metamorphosis by Franz Kafka or The Yellow Wallpaper by Charlotte Perkins? M/Y:  ").lower()
    while True:
        if to_search == "m":
            print("You chose Metamorphosis.")
            doc_to_search = metamDoc
            break
        elif to_search == "y":
            print("You chose The Yellow Wallpaper.")
            doc_to_search = yellowpDoc    
            break
        else:
            print("Invalid entry. M for Metamorphosis and Y for The Yellow Wallpaper.")

    matches = matcher(doc_to_search)
    # iterate through the sentences and check if start and end of phrase in in sentence
    matched_phrase_sentence = []

    for match_id, start, end in matches:
        matched_phrase = doc_to_search[start:end].text
        for sent in doc_to_search.sents:
            if start >= sent.start and end <= sent.end:
                matched_sentence = sent.text
                matched_phrase_sentence.append({"phrase": matched_phrase, "sentence": matched_sentence})

    # Print the result
    for match in matched_phrase_sentence:
        print("Matched phrase:", match["phrase"])
        print("Sentence:", match["sentence"])
        print()
   

    matcher.remove("user_pattern")

def common_characters():
    to_search = input("Do you want to search through Metamorphosis by Franz Kafka or The Yellow Wallpaper by Charlotte Perkins? M/Y:  ").lower()
    while True:
            if to_search == "m":
                doc_to_search = metamDoc
                break
            elif to_search == "y":
                doc_to_search = yellowpDoc    
                break
            else:
                print("Invalid entry. M for Metamorphosis and Y for The Yellow Wallpaper.")

    for ent in doc_to_search.ents:
        if str(ent.label_) == "PERSON":
            print(ent.text, '\t',ent.label_)

def common_descriptions():
    to_search = input("Do you want to search through Metamorphosis by Franz Kafka or The Yellow Wallpaper by Charlotte Perkins? M/Y:  ").lower()
    while True:
            if to_search == "m":
                doc_to_search = metamDoc
                break
            elif to_search == "y":
                doc_to_search = yellowpDoc    
                break
            else:
                print("Invalid entry. M for Metamorphosis and Y for The Yellow Wallpaper.")

    for token in doc_to_search:
        if token.pos_ == "ADJ":
            print(token.text, '\t', token.pos_)      

'''
def asking_mode():
    print("You will be able to ask about the main characters, the most common locations and the most common descriptive word of the books.")
    question1 = input("Do you want to get information about the most mentioned characters? Y/N: ").lower()
    if question1 == "y":
        common_characters()
        question2 = input("Do you want to get information about the most mentioned locations? Y/N: ").lower()
        if question2 == "y":
            common_locations()
        else:
            print("Skipping most common locations-information.")
    else:
        print("Skipping most common characters-information.")'''
    






'''
# Extract matched spans from the text
    matched_phrases = [yellowpDoc[start:end].text for match_id, start, end in matches]

# Add the pattern to the matcher
pattern = [{"TEXT": "iPhone"}, {"TEXT": "X"}]
matcher.add("IPHONE_PATTERN", [pattern])

# Process some text
doc = nlp("Upcoming iPhone X release date leaked")

# Call the matcher on the doc
matches = matcher(doc)'''

''' to_search = input("Do you want to search through Metamorphosis by Franz Kafka or The Yellow Wallpaper by Charlotte Perkins? M/Y:  ").lower()
while True:
        if to_search == "m":
            doc_to_search = metamDoc
            break
        elif to_search == "y":
            doc_to_search = yellowpDoc    
            break
        else:
            print("Invalid entry. M for Metamorphosis and Y for The Yellow Wallpaper.")'''