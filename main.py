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
  

def add_user_input():
    
# Example user input
    user_input = input("Enter a phrase to use as a pattern: ")
    
    # Tokenize user input using spaCy
    searchWordDoc = nlp(user_input)

    # Create pattern from user input
    pattern = [{"LOWER": token.lower_} for token in searchWordDoc]

    # Add pattern to the matcher
    matcher.add("user_pattern", [pattern])

def book_to_search():
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
    return doc_to_search                


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
    doc_to_search = book_to_search()
    
    add_user_input()            

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
    doc_to_search = book_to_search()

    characters = [ent.text for ent in doc_to_search.ents if str(ent.label_) == "PERSON"]
     

    print(characters)

    # create hash
    characterFreq = {}
    for c in characters:
        if c in characterFreq.keys():
            characterFreq[c] += 1
        else:
            characterFreq[c] = 1    

    print(characterFreq)   

     #måste slå ihop gregor, samsa och gregor samsa innan detta
    maxFreq = max(characterFreq.values())
    mostFreqChar = str([key for key, value in characterFreq.items() if value == maxFreq])
    mostFreqChar = mostFreqChar.strip("[]'")
    print(mostFreqChar)
    

    # Iterate through each sentence in the document
    for sent in doc_to_search.sents:
        descriptor = ""
        polarity = 0
        # Check if the sentence contains the most frequent character
        if mostFreqChar in sent.text and any(token.pos_ == "ADJ" for token in sent):
            for token in sent:
                if token.pos_ == "ADJ":
                    descriptor += token.text + ", "
                    polarity += token._.blob.polarity
            if 0 > polarity > -0.5:
                polarity = "A bit negative"
            elif polarity < -0.5:
                polarity = "Very, very negative"
            elif 0 < polarity < 0.5:
                polarity = "A bit positive"
            else:
                polarity = "Very positive! :D"    
            # Print the sentence if the most frequent character is found
            print("Matched character:", mostFreqChar)
            print("Descriptor:", descriptor)
            print("Sentence:", sent.text)
            print("Polarity:", polarity)
            print()
'''
    # Iterate through each sentence in the document
    for sent in doc_to_search.sents:
        highFreqSents = {}
        if mostFreqChar in sent.text and any(token.pos_ == "ADJ" for token in sent):
            highFreqSents[sent] += {token.pos_: +1}
        else:
            highFreqSents[sent] = 1    

        print(characterFreq)
'''


'''  försök att slå ihop gregor samsa med gregor och samsa-förekomster

    combined_counts = {}

    # Iterate over the dictionary
    for key, value in characterFreq.items():
        # Check if the key contains 'Samsa'
        if mostFreqChar in str(key):
            combined_counts[key] += value
        else:
            combined_counts[key] = value
       

    print(combined_counts)'''

   

''' # Normalisera listan
    for word in characterFreq.keys():
        characterFreq[word] = (characterFreq[word]/maxFreq) # n/max, 12/233
        
    print(characterFreq)    '''


''' första koden jag skrev som genererar fram och skriver ut alla personer.
   koden ovan är en list comprehension av detta
     for ent in doc_to_search.ents:
        if str(ent.label_) == "PERSON":
            print(ent.text, '\t',ent.label_)'''


def common_descriptions():
    doc_to_search = book_to_search()

    '''for token in doc_to_search:
        if token.pos_ == "ADJ":
            print(token.text, '\t', token.pos_)   '''   

    descriptor = [token for token in doc_to_search if token.pos_ == "ADJ"]
     

    
    

'''
måste slå ihop gregor, samsa och gregor samsa innan detta
maxFreq = max(descriptFreq.values())
mostFreqDescr = str([key for key, value in descriptFreq.items() if value == maxFreq])
print(mostFreqDescr)
'''





