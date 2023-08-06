import sys
sys.path.append('../../src/')

import os
from gensim import corpora, models
import gensim
import re
import jieba.posseg as pseg
from gensim.utils import  simple_preprocess
import spacy

def get_text_english(text,min_count=5,threshold=100,use_bigram=False):
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english')
    def sent_to_words(sentences):
        for sent in sentences:
            sent = re.sub('\S*@\S*\s?', '', sent)  # remove emails
            sent = re.sub('\s+', ' ', sent)  # remove newline chars
            sent = re.sub("\'", "", sent)  # remove single quotes
            sent = gensim.utils.simple_preprocess(str(sent), deacc=True)
            # print(sent)
            yield (sent)

            # Convert to list
    data_words = list(sent_to_words(text))

    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words, min_count=min_count,
                                   threshold=threshold)  # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=threshold)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    # allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']
    allowed_postags = ['NOUN']

    # !python3 -m spacy download en  # run in terminal once
    def process_words(texts, stop_words=stop_words, allowed_postags=None):
        """Remove Stopwords, Form Bigrams, Trigrams and Lemmatization"""
        texts = [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]
        texts = [bigram_mod[doc] for doc in texts]
        texts = [trigram_mod[bigram_mod[doc]] for doc in texts]
        texts_out = []
        nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
        for sent in texts:
            doc = nlp(" ".join(sent))
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        # remove stopwords once more after lemmatization
        texts_out = [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts_out]
        return texts_out

    data_ready = process_words(data_words,stop_words=stop_words,allowed_postags=allowed_postags)  # processed Text Data!
    return data_ready

def get_text_chinese(list_doc,stopwords_path=None,list_useful_words=None):
    stopwords=[]
    if stopwords_path!=None and os.path.exists(stopwords_path):
        stopwords = [w.strip() for w in open(stopwords_path, 'r', encoding='utf-8').readlines()
                 if w.strip() != ""]

    # load data
    # dict_dataset=pickle.load(open("datasets/weibo_vae_dataset_prepared_with_domain.pickle", "rb"))

    # compile sample documents into a list
    # doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]

    doc_set = []
    for doc in list_doc:
        # list_words=jieba.cut(doc,cut_all=False)
        list_words = pseg.cut(doc)
        list_w = []
        for w, f in list_words:
            if f in ['n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'nsf', 'ns', 'nt', 'nz', 'nl', 'ng', 'v', 'vn', 'vd', 'nd',
                     'nh', 'nl', 'i', 'x', 'a', 'ad']:
                if w not in stopwords and len(w) != 1:
                    if list_useful_words != None:
                        if w in list_useful_words:
                            list_w.append(w)
                    else:
                        list_w.append(w)

        # print(list_w)
        doc_set.append(list_w)

    # list for tokenized documents in loop
    texts = []

    # loop through document list
    for tokens in doc_set:
        # clean and tokenize document string

        # stem tokens
        # stemmed_tokens = [p_stemmer.stem(i) for i in tokens]

        # add tokens to list
        texts.append(tokens)
    return texts