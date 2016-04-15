import re, collections

def words(text):
    w = [t.strip('\n') for t in text]
    w = ' '.join(w).split(' ')
    return w

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

def edits1(word, alphabet):
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in s if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
    inserts    = [a + c + b     for a, b in s for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word, NWORDS, alphabet):
    return set(e2 for e1 in edits1(word, alphabet) for e2 in edits1(e1, alphabet) if e2 in NWORDS)

def known(words, NWORDS):
    return set(w for w in words if w in NWORDS)

def correct(word):
    NWORDS = train(words(file("ForSpellChecking.txt").readlines()))
    alphabet = 'abcdefghijklmnopqrstuvwxyz_ '
    candidates = known([word], NWORDS) or known(edits1(word, alphabet), NWORDS) or    known_edits2(word, NWORDS, alphabet) or [word]
    return max(candidates, key=NWORDS.get)

if __name__ == "__main__":
    word = raw_input("Enter a string: ")
    print correct(word)
