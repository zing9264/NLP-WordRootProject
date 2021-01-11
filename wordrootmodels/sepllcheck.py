from spellchecker import SpellChecker

spell = SpellChecker()

# find those words that may be misspelled

print(spell.known(['al','as']))

misspelled = spell.unknown( ['al'])

for word in misspelled:
    # Get the one `most likely` answer
    print(spell.correction(word))
    # Get a list of `likely` options
    print(spell.candidates(word))
