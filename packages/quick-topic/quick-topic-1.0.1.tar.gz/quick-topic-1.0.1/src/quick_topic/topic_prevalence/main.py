from quick_topic.topic_prevalence.divide_per_year import *
from quick_topic.topic_prevalence.lda_per_year import *
from quick_topic.topic_prevalence.trends_per_year import *

def run_topic_prevalence(meta_csv_file,raw_text_folder,save_root_folder, list_keywords_path,stop_words_path,start_year,end_year,label_names,list_topics,
    tag_field="tag",
    time_field="time",
    id_field="Id",
    prefix_filename="",
    num_topics=6,
    num_words=50,
    num_pass=5,
    lang='zh'
                         ):
    # step 1
    if not os.path.exists(save_root_folder):
        os.mkdir(save_root_folder)
    target_folder = f"{save_root_folder}/target"
    get_news_by_year(meta_csv_file=meta_csv_file, raw_text_folder=raw_text_folder, output_folder=target_folder,
                     group_by=tag_field,
                     id_field=id_field,
                     time_field=time_field,
                     prefix_filename=prefix_filename
                     )

    # Step 2
    do_lda_per_year(start_year=start_year, end_year=end_year,
                    yearly_data_folder=f'{save_root_folder}/target',
                    save_topic_weight_folder=f'{save_root_folder}/weights',
                    list_keywords_path=list_keywords_path,
                    stopwords_path=stop_words_path,
                    num_topics=num_topics,
                    num_words=num_words,
                    num_pass=num_pass,
                lang=lang
                    )

    # step 3

    return get_trends(
        start_year=start_year,
        end_year=end_year,
        label_names=label_names,
        list_topics=list_topics,
        root_path=f"{save_root_folder}/weights"
    )

