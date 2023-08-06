import os
from gensim import corpora, models
import gensim
import re
import jieba
import jieba.posseg as pseg
from gensim.utils import  simple_preprocess
import spacy
import pandas as pd

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

def get_text_chinese(list_doc,stopwords_path,list_useful_words=None):
    stopwords=[]
    if os.path.exists(stopwords_path):
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

def LDA(field,list_doc,weights_path,list_keywods_path,stopwords_path,num_topics=6,num_words=50,num_pass=5,lang='zh',use_bigram=False,iteration=100,random_state=100,chunk_size=10):

    # ============ begin configure ====================
    NUM_TOPICS = num_topics
    NUM_WORDS = num_words
    FIG_V_NUM = 2
    FIG_H_NUM = 3
    WC_MAX_WORDS = 20
    NUM_PASS = num_pass
    # ============ end configure ======================


    # qc_write("results/result_expert.csv",list_result)
    texts=None
    if lang=='zh':

        for pp in list_keywods_path:
            print(pp)
            words=[w.strip() for w in open(pp,'r',encoding='utf-8').read().split("\n")]
            for w in words:
                jieba.add_word(w,1)
        texts=get_text_chinese(list_doc,stopwords_path=stopwords_path)
    else:
        texts=get_text_english(list_doc,use_bigram=use_bigram)



    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]

    # generate LDA model
    ldamodel = None

    if lang=='en':
        ldamodel = gensim.models.ldamodel.LdaModel(corpus,
                                                   num_topics=NUM_TOPICS,
                                                   id2word=dictionary,
                                                   passes=NUM_PASS,
                                                   random_state=random_state,
                                                   update_every=1,
                                                   chunksize=chunk_size,
                                                   alpha='symmetric',
                                                   iterations=iteration,
                                                   per_word_topics=True
                                                   )
    elif lang=='zh':
        ldamodel = gensim.models.ldamodel.LdaModel(corpus,
                                                   num_topics=NUM_TOPICS,
                                                   id2word=dictionary,
                                                   passes=NUM_PASS,
                                                   random_state=random_state,
                                                   update_every=1,
                                                   chunksize=chunk_size,
                                                   alpha='symmetric',
                                                   iterations=iteration,
                                                   per_word_topics=True
                                                   )

    # print keywords
    topics = ldamodel.print_topics(num_words=NUM_WORDS, num_topics=NUM_TOPICS)

    dict_topic_weights=get_topic_distribution(lda_model=ldamodel,corpus=corpus)
    # save keywords weights
    save_keywords_weights(field,topics,weights_path)
    # save topic weights
    save_topic_weights(field,dict_topic_weights,weights_path)

def save_topic_weights(field,weights,weights_path):
    f_out_w = open(f"{weights_path}/{field}_w.csv", 'w', encoding='utf-8')
    for k in weights:
        f_out_w.write(f"{k},{weights[k]}\n")
    f_out_w.close()

def save_keywords_weights(field,topics,weights_path):
    f_out_k=open(f"{weights_path}/{field}_k.csv",'w',encoding='utf-8')
    f_out_v = open(f"{weights_path}/{field}_v.csv", 'w', encoding='utf-8')
    for topic in topics:
        print(topic)
        topic_id=topic[0]
        list_keywords=[]
        list_weight=[]
        s=str(topic[1])
        for k in s.split("+"):
            fs=k.split("*")
            w=fs[0].strip()
            keyword=fs[1].replace("\"","").strip()
            # print(keyword,w)
            list_keywords.append(keyword)
            list_weight.append(str(w))
        # print(','.join(list_keywords))
        # print("total weight:",round(np.sum(list_weight,4)))
        f_out_k.write(','.join(list_keywords)+"\n")
        f_out_v.write(','.join(list_weight)+"\n")
    f_out_v.close()
    f_out_k.close()


def lda_by_tag_each(list_category,root_path,weights_path,list_keywords_path,stopwords_path,minimum_num_doc=15,num_topics=6,num_pass=5,num_words=50,lang='zh'):
    if not os.path.exists(weights_path):
        os.mkdir(weights_path)
    print("Building topic models...")
    for country in list_category:
        if country.strip()=="":
            continue
        list_doc = []

        if not os.path.exists(f"{root_path}/{country}"):
            continue
        for file in os.listdir(f"{root_path}/{country}"):
            text_file = f"{root_path}/{country}/{file}"
            if not os.path.exists(text_file):
                continue
            text = open(text_file, "r", encoding='utf-8').read()
            list_doc.append(text)
        if len(list_doc) >= minimum_num_doc:
            print(country,len(list_doc))
            LDA(country, list_doc,weights_path,list_keywords_path,stopwords_path,num_topics,num_words,num_pass,lang=lang)
        print()

def get_topic_distribution(lda_model,corpus):
    # Sentence Coloring of N Sentences
    def topics_per_document(model, corpus, start=0, end=1):
        corpus_sel = corpus[start:end]
        dominant_topics = []
        topic_percentages = []
        for i, corp in enumerate(corpus_sel):
            topic_percs, wordid_topics, wordid_phivalues = model[corp]
            dominant_topic = sorted(topic_percs, key=lambda x: x[1], reverse=True)[0][0]
            dominant_topics.append((i, dominant_topic))
            topic_percentages.append(topic_percs)
        return dominant_topics, topic_percentages

    dominant_topics, topic_percentages = topics_per_document(model=lda_model, corpus=corpus, end=-1)

    # Distribution of Dominant Topics in Each Document
    df = pd.DataFrame(dominant_topics, columns=['Document_Id', 'Dominant_Topic'])
    dominant_topic_in_each_doc = df.groupby('Dominant_Topic').size()
    df_dominant_topic_in_each_doc = dominant_topic_in_each_doc.to_frame(name='count').reset_index()


    # df_dominant_topic_in_each_doc.to_csv(output_folder + "/" + save_dominant_topic_file, encoding='utf-8')

    # Total Topic Distribution by actual weight
    topic_weightage_by_doc = pd.DataFrame([dict(t) for t in topic_percentages])
    df_topic_weightage_by_doc = topic_weightage_by_doc.sum().to_frame(name='count').reset_index()

    # df_topic_weightage_by_doc.to_csv(output_folder + "/" + save_topic_topic_weight, encoding='utf-8')
    total_weight=0
    for idx,row in df_topic_weightage_by_doc.iterrows():
        # print(row)
        index =row["index"]
        count=row["count"]
        total_weight+=count

    list_item={}
    for idx,row in df_topic_weightage_by_doc.iterrows():
        # print(row)
        index =row["index"]
        count=row["count"]
        # list_item[index]=round(count*1.0/total_weight,6)
        list_item[index]=count
    return list_item

