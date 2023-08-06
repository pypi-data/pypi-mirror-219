from quick_topic.topic_modeling.lda import build_lda_models
from quick_topic.topic_similarity.topic_similarity_by_category import *
import os
'''
    Estimate topic similarity between two groups of LDA topics
'''

def gui_topic_similarity(
        meta_csv_file="datasets_paper/list_paper.csv",
        raw_text_folder="datasets_paper/raw_text",
        output_folder="",
        category_field="category",
        time_field='PD',
        id_field='file_id',
        lang="en",
        num_topics=6,
        num_words=50,
        num_pass=10,
        result_path='',
        prefix_filename=''
):


    list_term_file = [
        ]

    stop_words_path = ""

    topic_output_folder = f"{output_folder}/topics"

    if not os.path.exists(topic_output_folder):
        os.mkdir(topic_output_folder)

    list_category = build_lda_models(
        meta_csv_file=meta_csv_file,
        raw_text_folder=raw_text_folder,
        output_folder=topic_output_folder,
        list_term_file=list_term_file,
        stopwords_path=stop_words_path,
        prefix_filename=prefix_filename,
        num_topics=num_topics,
        num_words=num_words,
        num_pass=num_pass,
        tag_field=category_field,
        id_field=id_field,
        lang=lang
    )

    # Step 2: estimate similarity



    # keywords_file="../datasets/keywords/carbon2.csv"

    estimate_topic_similarity(
        list_topic=list_category,
        topic_folder=topic_output_folder,
      #  list_keywords_file=keywords_file,
        lang=lang,
        result_path=result_path
    )


