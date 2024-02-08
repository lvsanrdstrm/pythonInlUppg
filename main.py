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
    def __init__(self, doc, phrase, sentence, polarity):
        self.doc = doc
        self.phrase = phrase
        self.sentence = sentence
        self.polarity = polarity



            
def add_user_input():
    user_input = input("Enter a phrase to use as a pattern: ")
    searchWordDoc = nlp(user_input)
    
    
    pattern = [{"LOWER": token.lower_} for token in searchWordDoc]
    matcher.add("user_pattern", [pattern])

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

    
    for match in matched_phrase_sentence:
        print("Book:", book)
        print("Matched phrase:", match["phrase"])
        print("Sentence:", match["sentence"])
        print("----------------------")
   

    matcher.remove("user_pattern")

    while True:
        now_what = input("Press B when/if you want to return to the menu. Press A if you want to start over.").lower()
        if now_what == "b":
            print("Okay. Bye!")
            print("----------------------")
            return
        elif now_what == "a":
            search_any_book()
        else:
            print("Invalid entry. Y for Yes or N for No.")
            print("----------------------")

def sentiment_search():
    
    add_user_input()
    
    metam_matches = matcher(metamDoc)
    
    metam_matched_phrase_sentence = []
   
    for match_id, start, end in metam_matches:
        matched_phrase = metamDoc[start:end].text
        for sent in metamDoc.sents:
            if start >= sent.start and end <= sent.end:
                matched_sentence = sent.text
                polarity = sent._.blob.polarity
                match = SentimentSent("Metamorphosis", matched_phrase, matched_sentence, polarity)
                metam_matched_phrase_sentence.append(match)
                

    yellowp_matches = matcher(yellowpDoc)
    
    yellowp_matched_phrase_sentence = []
   
    for match_id, start, end in yellowp_matches:
        matched_phrase = yellowpDoc[start:end].text
        for sent in yellowpDoc.sents:
            if start >= sent.start and end <= sent.end:
                matched_sentence = sent.text
                polarity = sent._.blob.polarity
                match = SentimentSent("The Yellow Wallpaper", matched_phrase, matched_sentence, polarity)
                yellowp_matched_phrase_sentence.append(match)
                
    
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
        if 0 > avg_polarity > -0.5:
                avg_polarity = "A bit negative emotional tone."
        elif avg_polarity < -0.5:
            avg_polarity = "Negative emotional tone."
        elif 0 < avg_polarity < 0.5:
            avg_polarity = "A bit positive emotional tone."
        else:
            avg_polarity = "Very positive emotional tone! :D"  
        print("----------------------")
        print("Book:", doc)
        print("Average emotional tone in sentences with your search word:", avg_polarity)
        

    max_polarity_doc = max(compare_polarities, key=compare_polarities.get)
    min_polarity_doc = min(compare_polarities, key=compare_polarities.get)
    
    print("----------------------")
    print(f"Based on the sentences with your search word, {max_polarity_doc} has a more positive emotional tone than {min_polarity_doc}.")
    print("----------------------")

    matcher.remove("user_pattern")    
    
    
    while True:
        print_sentences = input("Would you like to see all the sentences that contain your search word? Y/N: ").lower()
        if print_sentences == "y":
            for match in all_matches:
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
    
    while True:
        now_what = input("Press B when/if you want to return to the menu. Press A if you want to start over. A/B:  ").lower()
        if now_what == "b":
            print("Okay. Bye!")
            print("----------------------")
            return
        elif now_what == "a":
            sentiment_search()
        else:
            print("Invalid entry. Y for Yes or N for No.")
            print("----------------------")

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
                    if 0 > polarity > -0.5:
                        polarity = "A bit negative"
                    elif polarity < -0.5:
                        polarity = "Very, very negative"
                    elif 0 < polarity < 0.5:
                        polarity = "A bit positive"
                    else:
                        polarity = "Very positive! :D"    
                    
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

    while True:
        now_what = input("Press B when/if you want to return to the menu. Press A if you want to start over.").lower()
        if now_what == "b":
            print("Okay. Bye!")
            print("----------------------")
            return
        elif now_what == "a":
            common_characters()
        else:
            print("Invalid entry. Y for Yes or N for No.")
            print("----------------------")       
   


def common_descriptors():
    doc_to_search = book_to_search()

    '''for token in doc_to_search:
        if token.pos_ == "ADJ":
            print(token.text, '\t', token.pos_)   '''   

    descriptor = [token for token in doc_to_search if token.pos_ == "ADJ"]
    print(descriptor)
     
     #denna vill jag göra en frequent-analys på
    while True:
        now_what = input("Press B when/if you want to return to the menu. Press A if you want to start over.").lower()
        if now_what == "b":
            print("Okay. Bye!")
            print("----------------------")
            return
        elif now_what == "a":
            common_descriptors()
        else:
            print("Invalid entry. Y for Yes or N for No.")
            print("----------------------")

    
    



