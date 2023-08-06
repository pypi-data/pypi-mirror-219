from gensim import  models
from quick_topic.topic_interaction.lda_by_tag_each import *
from quickcsv.file import *
import pickle
def build_lda_model(list_doc,num_topics=6,num_words=50,num_pass=5,list_term_file=None,stopwords_path="",save_name="topic",output_folder="output",lang='zh',
                    random_state=100,
                    chunk_size=10,
                    iteration=100,
                    list_useful_words=None
                    ):

    # ============ begin configure ====================
    NUM_TOPICS = num_topics
    NUM_WORDS = num_words
    FIG_V_NUM = 2
    FIG_H_NUM = 3
    WC_MAX_WORDS = 20
    NUM_PASS = num_pass
    # ============ end configure ======================
    if list_term_file!=None:
        for file in list_term_file:
            jieba.load_userdict(file)

    # qc_write("results/result_expert.csv",list_result)
    stopwords=[]
    if stopwords_path!="":
        stopwords = [w.strip() for w in open(stopwords_path, 'r', encoding='utf-8').readlines()
                     if w.strip() != ""]

    # load data
    # dict_dataset=pickle.load(open("datasets/weibo_vae_dataset_prepared_with_domain.pickle", "rb"))

    # compile sample documents into a list
    # doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]

    texts = None
    if lang == 'zh':
        for pp in list_term_file:
            jieba.load_userdict(pp)
        texts = get_text_chinese(list_doc, stopwords_path=stopwords_path,list_useful_words=list_useful_words)
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

    model_folder = output_folder + "/model"
    if not os.path.exists(model_folder):
        os.mkdir(model_folder)

    ldamodel.save(model_folder + "/ldamodel.model")

    pickle.dump(texts, open(model_folder + "/texts.pickle", "wb"))

    ## list_topic_weights=get_topic_weights(ldamodel=ldamodel,corpus=corpus)

    # print keywords
    topics = ldamodel.print_topics(num_words=NUM_WORDS, num_topics=NUM_TOPICS)

    save_keywords_weights(output_folder,save_name,topics)

    dict_topic_weights=get_topic_distribution(ldamodel,corpus)

    save_topic_weights(save_name,dict_topic_weights,output_folder)

    ## return list_topic_weights'
    return []

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


def save_topic_weights(field,weights,weights_path):
    f_out_w = open(f"{weights_path}/{field}_w.csv", 'w', encoding='utf-8')
    for k in weights:
        f_out_w.write(f"{k},{weights[k]}\n")
    f_out_w.close()

def save_keywords_weights(output_folder,field,topics):
    print(field)
    f_out_k=open(f"{output_folder}/{field}_k.csv",'w',encoding='utf-8')
    f_out_v = open(f"{output_folder}/{field}_v.csv", 'w', encoding='utf-8')
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
    print()

def build_lda_models(meta_csv_file,raw_text_folder,tag_field="area",id_field="fileId",
                     prefix_filename="text_",list_term_file=None,stopwords_path="",
                     output_folder="results/topic_modeling",
                    num_topics=6,num_words=50,num_pass=5,
                     lang='zh',
                     min_doc_num=10
                     ):

    #meta_csv_file = "datasets/list_country.csv"
    #raw_text_folder = "datasets/raw_text"

    dict_country = {}
    list_item = read_csv(meta_csv_file)

    for item in list_item:
        area = item[tag_field]
        if area.strip()=="":
            continue
        id = item[id_field]
        text_path = f'{raw_text_folder}/{prefix_filename}{id}.txt'
        if not os.path.exists(text_path):
            continue
        text = read_text(text_path)
        if text.strip() == "":
            continue
        if area in dict_country:
            dict_country[area].append(text)
        else:
            dict_country[area] = [text]

    for country in dict_country:
        if len(dict_country[country])<min_doc_num:
            continue
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        build_lda_model(
            list_doc=dict_country[country],
            output_folder=output_folder,
            stopwords_path=stopwords_path,
            save_name=country,
            list_term_file=list_term_file,
            num_pass=num_pass,
            num_topics=num_topics,
            num_words=num_words,
            lang=lang
        )
    return list(dict_country.keys())

def get_topic_weights(ldamodel, corpus):
    # Init output
    list_topic_dist=[]
    # sent_topics_df = pd.DataFrame()
    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                model={
                    "topic_num":int(topic_num),
                    "topic_percent":round(prop_topic,4),
                    "topic_keywords":topic_keywords
                }
                list_topic_dist.append(model)
                # sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    # sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']
    # Add original text to the end of the output
    # contents = df
    # sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return list_topic_dist