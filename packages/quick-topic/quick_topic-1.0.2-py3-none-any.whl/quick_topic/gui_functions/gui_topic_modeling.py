from quick_topic.topic_modeling.lda import *
from quickcsv.file import *
import os

def gui_topic_modeling(
    meta_csv_file = "datasets_paper/list_paper.csv",
    raw_text_folder = "datasets_paper/raw_text",
    output_folder="",
    category_field='category',
    id_field='file_id',
    stopwords_path="",
    num_topics: int = 6,
    num_pass: int = 10,
    num_words: int = 50,
    lang='en',
    prefix_filename=""
):
    dict_country = {}
    list_item = read_csv(meta_csv_file)

    for item in list_item:
        area = item[category_field]
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

    list_term_file = [

    ]


    for country in dict_country:
        list_topic_weight = build_lda_model(
            list_doc=dict_country[country],
            output_folder=output_folder,
            stopwords_path=stopwords_path,
            save_name=country,
            list_term_file=list_term_file,
            lang=lang,
            num_topics=num_topics,
            num_words=num_words,
            num_pass=num_pass
        )
        print(list_topic_weight)
        # for topic in list_topic_weight:
        #    for k in topic:
        #        print(f"{topic['topic_num']}\t{topic['topic_percent']}\t{topic['topic_keywords']}")
        # print()

