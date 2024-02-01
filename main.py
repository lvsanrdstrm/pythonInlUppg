import spacy 
nlp = spacy.load('en_core_web_lg')

from spacy.matcher import Matcher


metam = open('books\metamorphosis.txt', 'r', encoding='utf8').read()
yellowp = open('books\yellowwallpaper.txt', 'r', encoding='utf8').read()

metamDoc = nlp(metam)
yellowpDoc = nlp(yellowp)

matcher = Matcher(nlp.vocab)

pattern = [{"TEXT": "wallpaper"}]
matcher.add("sun_pattern", [pattern])

matches = matcher(yellowpDoc)

# Extract matched spans from the text
matched_phrases = [yellowpDoc[start:end].text for match_id, start, end in matches]

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
# Add the pattern to the matcher
pattern = [{"TEXT": "iPhone"}, {"TEXT": "X"}]
matcher.add("IPHONE_PATTERN", [pattern])

# Process some text
doc = nlp("Upcoming iPhone X release date leaked")

# Call the matcher on the doc
matches = matcher(doc)'''