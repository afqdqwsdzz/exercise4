import nltk
from nltk.corpus import gutenberg
from gensim import corpora, models
import pyLDAvis.gensim.models


nltk.download('gutenberg')
alice = gutenberg.raw('carroll-alice.txt')


alice_sentences = nltk.sent_tokenize(alice)
alice_words = [nltk.word_tokenize(sentence) for sentence in alice_sentences]
alice_words = [[word.lower() for word in sentence if word.isalpha()] for sentence in alice_words]


dictionary = corpora.Dictionary(alice_words)
corpus = [dictionary.doc2bow(sentence) for sentence in alice_words]


lda_model = models.LdaModel(corpus, num_topics=5, id2word=dictionary)


pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.models.prepare(lda_model, corpus, dictionary)
pyLDAvis.display(vis)
