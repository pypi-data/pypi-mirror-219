import os
from gensim import corpora, models
import gensim
from quickcsv.file import *
import jieba
import jieba.posseg as pseg
import numpy as np
from quick_topic.topic_interaction.lda_by_tag_each import get_text_english,get_text_chinese
import pandas as pd

def LDA( year,list_doc,save_topic_weights_folder,list_keywords_path,stop_words_path,
    # ============ begin configure ====================
    NUM_TOPICS = 10,
    NUM_WORDS = 50,
    FIG_V_NUM = 2,
    FIG_H_NUM = 3,
    WC_MAX_WORDS = 20,
    NUM_PASS = 5,
         lang='zh',
         random_state=100,
         chunk_size=10,
         iteration=100
    # ============ end configure ======================
         ):

    if list_keywords_path!=None:
        for keyword_path in list_keywords_path:
            jieba.load_userdict(keyword_path)

    # qc_write("results/result_expert.csv",list_result)
    stopwords=[]
    if os.path.exists(stop_words_path):
        stopwords = [w.strip() for w in open(stop_words_path, 'r', encoding='utf-8').readlines()
                 if w.strip() != ""]

    # load data
    # dict_dataset=pickle.load(open("datasets/weibo_vae_dataset_prepared_with_domain.pickle", "rb"))

    # compile sample documents into a list
    # doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]

    texts = None
    if lang == 'zh':
        for pp in list_keywords_path:
            jieba.load_userdict(pp)
        texts = get_text_chinese(list_doc, stopwords_path=stop_words_path)
    else:
        texts = get_text_english(list_doc)

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]

    ldamodel=None
    # generate LDA model
    if lang == 'en':
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
    elif lang == 'zh':
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

    save_keywords_weights(str(year),topics,weights_path=save_topic_weights_folder)

    dict_topic_weights = get_topic_distribution(lda_model=ldamodel, corpus=corpus)

    save_topic_weights(str(year),dict_topic_weights,weights_path=save_topic_weights_folder)

def save_topic_weights(field,weights,weights_path):
    f_out_w = open(f"{weights_path}/{field}_w.csv", 'w', encoding='utf-8')
    for k in weights:
        f_out_w.write(f"{k},{weights[k]}\n")
    f_out_w.close()

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


def save_keywords_weights(field,weights,weights_path):
    if not os.path.exists(weights_path):
        os.mkdir(weights_path)
    f_out_k=open(f"{weights_path}/{field}_k.csv",'w',encoding='utf-8')
    f_out_v = open(f"{weights_path}/{field}_v.csv", 'w', encoding='utf-8')
    for topic in weights:
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

def do_lda_per_year(start_year,end_year, yearly_data_folder = "results/news_by_year",
                    save_topic_weight_folder="results/topic_weights",list_keywords_path=None,
                    stopwords_path="hit_stopwords.txt",
                    num_topics=6,
                    num_words=50,
                    num_pass=5,
                    lang='zh'
                    ):
    print("Building topic model per year...")
    for year in range(start_year, end_year+1):
        year_folder = f"{yearly_data_folder}/{year}"
        list_doc = []
        if not os.path.exists(year_folder):
            continue
        for country in os.listdir(year_folder):
            for file in os.listdir(os.path.join(year_folder, country)):
                text_path = f"{year_folder}/{country}/{file}"
                if not os.path.exists(text_path):
                    continue
                # print(country,file)
                if '.txt' not in file:
                    continue
                text = open(text_path, "r", encoding='utf-8').read()
                list_doc.append(text)
        print(f"{year}'s news count: ", len(list_doc))
        LDA(year, list_doc,save_topic_weight_folder,list_keywords_path,stopwords_path,NUM_TOPICS=num_topics,NUM_WORDS=num_words,NUM_PASS=num_pass,lang=lang)
        print()

