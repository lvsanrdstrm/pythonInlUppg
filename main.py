import spacy 
nlp = spacy.load('en_core_web_lg')

from spacy.matcher import Matcher


metam = open('books\metamorphosis.txt', 'r', encoding='utf8').read()
yellowp = open('books\yellowwallpaper.txt', 'r', encoding='utf8').read()

metamDoc = nlp(metam)
yellowpDoc = nlp(yellowp)

matcher = Matcher(nlp.vocab)


 


'''
# Add the pattern to the matcher
pattern = [{"TEXT": "iPhone"}, {"TEXT": "X"}]
matcher.add("IPHONE_PATTERN", [pattern])

# Process some text
doc = nlp("Upcoming iPhone X release date leaked")

# Call the matcher on the doc
matches = matcher(doc)'''