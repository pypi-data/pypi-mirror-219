from negate import Negator

negator = Negator(fail_on_unsupported=False)

while True:
    sentence = input("Sentence: ")
    ns = negator.negate_sentence(sentence)
    print(ns)

