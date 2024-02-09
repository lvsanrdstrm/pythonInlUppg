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

# denna funktion kallar jag på när användaren får välja bok att söka i
def book_to_search():
    # en loop så jag kan hantera felinput och kontrollera när koden ska sluta execute
    while True:
        # användarinput som loopen baseras på
        to_search = input("Do you want to search through Metamorphosis by Franz Kafka or The Yellow Wallpaper by Charlotte Perkins? M/Y:  ").lower()
        # if-sats som hanterar input m, val av bok
        if to_search == "m":
            # assignar nlp-dokumentet metamDoc till doc_to_search
            doc_to_search = metamDoc
            # avslutar loopen
            break
        # elif-sats som hanterar input y, val av bok
        elif to_search == "y":
            # assignar nlp-dokumentet yellowpDoc till doc_to_search
            doc_to_search = yellowpDoc    
            #avlutar loopen
            break
        #else-sats som hanterar felinput
        else:
            print("Invalid entry. M for Metamorphosis and Y for The Yellow Wallpaper.")
            # eftersom det inte är någon break här executas koden i loopen om från början
    #funktionen returnerar variabeln doc_to_search med användarens valda bok assignad till den        
    return doc_to_search  

# funktion som jag kan återanvända i slutet på huvudfunktionerna, mest för att menyn inte automatiskt ska poppa upp i botten
# men också så användaren faktiskt kan välja att köra igen om den vill
# den tar inparameter där jag skickar in namnet på funktionen där end-funktionen körs så det är den som börjar om
def end_of_function(current_function_name):
    # en loop så jag kan hantera felinput och kontrollera när koden ska sluta execute
    while True:
        # användarinput som loopen baseras på
        now_what = input("Press B when/if you want to return to the menu. Press A if you want to start over. A/B:  ").lower()
        # denna del hanterar val b, stänger nuvarande funktion och går tillbaka till menyn
        if now_what == "b":
            print("Okay. Bye!")
            print("----------------------")
            break
        # denna del hanterar val a, kör samma funktion igen
        elif now_what == "a":
            # inparametern som är namnet på funktionen end-funktionen körs i
            current_function_name()
            break
        # hanterar felinput och kör om loopen
        else:
            print("Invalid entry. Y for Yes or N for No.")
            print("----------------------")    

   
# funktion som har huvudfunktionaliteten i frisöksfunktionen
def search_any_book():
    # assignar doc_to_search resultatet på bokväljar-funktionen ovan
    doc_to_search = book_to_search()

    # denna kod har jag gjort för att jag ville använda bokens fulla namn, 
    #så här hämtar jag det baserat på vilken bok användaren valde i boksökfunktionen
    if doc_to_search == metamDoc:
        book = "Metamorphosis"
    elif doc_to_search == yellowpDoc:
        book = "The Yellow Wallpaper"
    
    # kallar på user-inputfunktionen så användaren väljer sökord
    add_user_input()            

    # kör matchern med användarens valda sökord på det valda nlp-dokumentet/boken
    matches = matcher(doc_to_search)
   
   # list som jag sparar träffmeningarna i
    matched_phrase_sentence = []

    # loopar igenom matchningarna
    for match_id, start, end in matches:
        #skapar variabeln matched_phrase och assignar sökträffens förekomst i söktexten i textform
        matched_phrase = doc_to_search[start:end].text
        # itererar igenom meningarna i söktexten 
        for sent in doc_to_search.sents:
            # letar efter träffar genom att se om sökordet start och slut är inom någon menings start och slut
            # (när jag skrev denna kod arbetade jag utifrån att användaren skulle kunna söka på fraser men jag släppte det)
            # (det är ju inte nödvändigt med start och end på detta sätt när det bara är ett ord)
            if start >= sent.start and end <= sent.end:
                # assignar meningar med sökträffar till variabeln matced_sentence
                matched_sentence = sent.text
                # appendar en dictionary med sökträff som key och mening som value till listan matched_phrase_sentence
                matched_phrase_sentence.append({"phrase": matched_phrase, "sentence": matched_sentence})
    
    #printar bokens namn, här kommer if/else-koden i början på denna kod till användning
    print("----------------------")
    print("Book:", book)
    print("----------------------")

    # if-sats som hanterar om det inte finns matchningar.
    if matched_phrase_sentence:
        # printar sökfrasen, kändes inte nödvändigt att printa den med varje mening
        print("Matched phrase:", matched_phrase_sentence[0]["phrase"])
        print("----------------------")
        #itererar igenom träffarna och printar meningarna
        for match in matched_phrase_sentence:
            print("Sentence:", match["sentence"])
            print("----------------------")
    else:
        #om det inte finns någon träff printar den detta
        print("No matched phrases found.")
    
    #denna tar bort patternet från matchern så sökorden inte kommer med till nästa gång matchern körs
    matcher.remove("user_pattern")

    #kallar end-funktionen med namnet på nuvarande funktion som inparameter
    while end_of_function(search_any_book):
        break

# en funktion som hanterar sentiment-analysen av ett specifikt dokument, gjorde såhär så ja kan återanvända det
    # mostFrewChar är optional eftersom den bara används i common_character-funktionen
def sentiment_process_document(doc_to_process, doc_name, mostFreqChar = None):
    # här kör jag try/except för att hantera om det inte finns några matchningar
    try:
        # skapar variabeln matches som assignas resultatet på att matchern körs på det valda dokumentet
        matches = matcher(doc_to_process)
        if not matches:
            # the error som raises och mitt egna meddelande som skrivs ut om det sker
            raise ValueError("No matches found in the document.")
        #skapar lista där sökträffarna sparas
        matched_phrase_sentence = []
        #itererar igenom matchningarna
        for match_id, start, end in matches:
            # skapar matched_phrase och assignar sökträffen
            matched_phrase = doc_to_process[start:end].text
            #itererar igenom meningarna i söktexten
            for sent in doc_to_process.sents:
                # om sökträffens start och slut är inom söktextens start och slut
                if start >= sent.start and end <= sent.end:
                    # ... så assignas meningen till matched_sentence
                    matched_sentence = sent.text
                    # och variablen polarity assignas polarity-värdet spacytextblob räknar ut baserat på meningen
                    polarity = sent._.blob.polarity
                    # för varje träff skapas en klassinstans av sentimentsent
                    match = SentimentSent(doc_name, matched_phrase, matched_sentence, polarity, mostFreqChar=mostFreqChar)
                    # ... och det objektet  läggs sedan till listan 
                    matched_phrase_sentence.append(match)
         # den listan returneras av funktionen           
        return matched_phrase_sentence 
    # detta är koden som körs om det inte finns någon match 
    except ValueError as e:
        print(e)
        return []
        
# gjorde en funktion som översätter polarity-resultatet som är float-form till text
    
def translate_polarity(polarity):
    # if/elif/else-kod som hanterar olika värden på polarity och assignar värde till text_polarity baserat på floaten
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
    # funktionen returnerar polarityn översatt till text
    return text_polarity 

# funktionen som innehåller huvudfunktionaliteten till emotional tone-analysen på fritextsök
def sentiment_search():
    # kallar funktionen som genererar sökord/pattern baserat på user input
    add_user_input()
    
    # kallar funktionen som gör sentimentanalys på dokumenten
    # först metamorphosis som sparas i en variabel med passande namn
    metam_matched_phrase_sentence = sentiment_process_document(metamDoc, "Metamorphosis")

    # sedan yellow wallpaper som sparas i variabel med passande namn
    yellowp_matched_phrase_sentence = sentiment_process_document(yellowpDoc, "The Yellow Wallpaper")
    
    # slår ihop träffarna i en variabel
    all_matches = metam_matched_phrase_sentence + yellowp_matched_phrase_sentence
    
    # skapar dictionary där alla träffmeningar sparas som key/value-par dokument/polarity
    doc_polarities = {}
    # dictionary som består av två key/value-par där jag sparar avg polarity för ett dokuments alla meningar
    compare_polarities = {}

    # itererar igenom sökträffmeningarna
    for match in all_matches:
        # och skapar ett key/value-par i compare_polarities där dokumentet är key
        if match.doc not in doc_polarities:
            doc_polarities[match.doc] = []
        # lägger till varje menings polarity-score i listan som är value i dictionaryn
        doc_polarities[match.doc].append(match.polarity)
    
    # itererar igenom dictionaryn
    for doc, polarities in doc_polarities.items():
        # och räknar ut average polarity
        avg_polarity = sum(polarities) / len(polarities)
        # och lägger till average polarity i en ny dictionary där dokumentnamnet igen är key
        compare_polarities[doc] = avg_polarity
        # kör sedan funktionen som omvandlar polarity-floatern till text
        avg_polarity = translate_polarity(avg_polarity) 
        # här skriver den ut de två böckernas avg_polarity tillsammans med titelt
        print("----------------------")
        print("Book:", doc)
        print("Average emotional tone in sentences with your search word:", avg_polarity)
        
    # skapar variabeln och assignar keyn med maxvärde från compare_polarities, 
        #key=compare_polarities.get ser till att det baseras på keyns value
    max_polarity_doc = max(compare_polarities, key=compare_polarities.get)
    min_polarity_doc = min(compare_polarities, key=compare_polarities.get)
    
    # printar en sammanfattning/förklaring av resultatet
    print("----------------------")
    print(f"Based on the sentences with your search word, {min_polarity_doc} has a more negative emotional tone than {max_polarity_doc}.")
    print("----------------------")

    #denna tar bort patternet från matchern så sökorden inte kommer med till nästa gång matchern körs
    matcher.remove("user_pattern")    
    
        
       # loop som hanterar om användaren vill se sökträffmeningarna eller ej 
    while True:
        print_sentences = input("Would you like to see the sentences the emotional tone analysis was based on? Y/N: ").lower()
        # id-sats som hanterar om användaren säger ja
        if print_sentences == "y":
            # itererar igenom träffarna
            for match in all_matches:
                # översätter polarity-scoren till text
                match.polarity = translate_polarity(match.polarity)
                # och printar träffarna en och en med titel, sökord, meningen och polarity-score
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

    # kallar funktionen där användaren får välja att avsluta eller fortsätta
    while end_of_function(sentiment_search):
        break

# funktionen som innehåller huvudfunktionaliteten för emotional search baserad på huvudkaraktär
def common_characters():
    # kallar på funktionen där användaren får välja bok
    doc_to_search = book_to_search()

    # assignar book ett värde baserat på valt dokument
    if doc_to_search == metamDoc:
        book = "Metamorphosis"
    elif doc_to_search == yellowpDoc:
        book = "The Yellow Wallpaper"  

    # list comprehension som itererar igenom alla entities och sorterar ut alla som är personer
    characters = [ent.text for ent in doc_to_search.ents if str(ent.label_) == "PERSON"]
    
    # skapar dictionary där characters och deras förekomster sparas för att kunna räkna ut vilken som nämns oftast
    characterFreq = {}
    # itererar igenom alla element i characters, alltså alla personnamn i boken
    for c in characters:
        # om karaktären finns i listan så ökar valuen till 1, för varje gång ett namn förekommer i träffarna ökar siffran
        if c in characterFreq.keys():
            characterFreq[c] += 1
        # om karaktären förekommer för första gången skapar key/value-paret med karaktären som key och får value 1
        else:
            characterFreq[c] = 1    

    # karaktären som har högst value, alltså nämns oftast i boken, assignas till max (valuen, inte keyn)
    maxFreq = max(characterFreq.values())
    # här assignas keyn till valuen med högst värde till variabeln (med list comprehension) och görs om till string i samma veva
    mostFreqChar = str([key for key, value in characterFreq.items() if value == maxFreq])
    # tar bort klamrar och ' från stringen
    mostFreqChar = mostFreqChar.strip("[]'")
    
    # kallar på funktionen som skapar pattern till matchern, tar vanligaste karaktären som inparameter
    create_pattern(mostFreqChar)
    # kallar funktionen som gör emotional tone-analys
    char_matches = sentiment_process_document(doc_to_search, book, mostFreqChar)

    #skapar dicitonary där sökträffarna och dess polarity sparas som key/value-par
    char_polarities = {}
    
    # itererar igenom träffarna
    for match in char_matches:
        # om karaktären inte redan finns i dictionaryn skapar key/value-paret med en tom lista som value
        #och sökträffmeningen som key
        if match.mostFreqChar not in char_polarities:
            char_polarities[match.mostFreqChar] = []
        # om karaktären redan finns med läggs meningens polarity till i listan
        char_polarities[match.mostFreqChar].append(match.polarity)
    
    #itererar igenom dictionaryn som skapades ovan
    for mostFreqChar, polarities in char_polarities.items():
        # och räknar ut avg_polarity
        avg_polarity = sum(polarities) / len(polarities)
        # och översätter resultatet till text
        avg_polarity = translate_polarity(avg_polarity) 
        
    # skriver ut vanligaste karaktären och boktiteln tillsammans med avg polarity
    print("----------------------")
    print(f"The most frequent character in {book} is {mostFreqChar}")
    print(f"The average emotional tone in sentences where {mostFreqChar} occur is {avg_polarity}")
    print("----------------------")
    
    # loop som hanterar om användaren vill se meningarna analysen baseras på
    while True:
        print_sentences = input("Would you like to see a selection of the sentences the analysis was based on? Y/N: ").lower()
       # om ja
        if print_sentences == "y":
            # så itererar den igenom träffarna, översätter polarityn och skriver ut informationen
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
   

# funktionen jag har börjat skriva som ska hantera emotional analys baserat på adjektiv
def common_descriptors():
    # kallar på sökbokväljarfunktionen
    doc_to_search = book_to_search()
   
    # list comprehension som itererar ut alla ord som är adjektiv och sparar i listan descriptor
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