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

    matches = matcher(metamDoc)
    
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

    

def search_metam(): 
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

def search_yellowp():
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

def get_wallpaper_sentences():
    pattern = [{"TEXT": "wallpaper"}]
    matcher.add("sun_pattern", [pattern])

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