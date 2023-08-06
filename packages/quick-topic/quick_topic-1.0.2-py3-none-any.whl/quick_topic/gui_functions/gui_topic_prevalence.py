from quick_topic.topic_prevalence.main import *
'''
    Estimate yearly topic prevalence trends over topics
'''

def get_predefined_topics(predefined_topic_file):
    lines=open(predefined_topic_file,'r',encoding='utf-8').readlines()
    list_label=[]
    list_topics=[]
    for line in lines:
        line=line.strip()
        label_name=line.split(":")[0]
        keywords=line.split(":")[1].split(";")
        list_label.append(label_name)
        list_topics.append(keywords)
    return list_label,list_topics

def gui_topic_prevalence(
        meta_csv_file = "datasets_paper/list_paper.csv",
        text_root = r"datasets_paper/raw_text",
        output_folder="results/topic_prevalence",
        predefined_topic_file="",
        start_year=2010,
        end_year = 2021,
        category_field="category",
        time_field='PD',
        id_field='file_id',
        lang="en",
        num_topics=6,
        num_words=50,
        num_pass=10,
        stopwords_path="",
        result_path="",
        prefix_filename=""
):


    # word segmentation data files
    list_keywords_path = [

        ]

    # date range for analysis


    # used topics
    # set predefined topic labels
    label_names, list_topics = get_predefined_topics(predefined_topic_file)

    # run-all

    list_tp_keyword,list_tp_topics=run_topic_prevalence(
        meta_csv_file=meta_csv_file,
        raw_text_folder=text_root,
        save_root_folder=output_folder,
        list_keywords_path=list_keywords_path,
        stop_words_path=stopwords_path,
        start_year=start_year,
        end_year=end_year,
        label_names=label_names,
        list_topics=list_topics,
        tag_field=category_field,
        time_field=time_field,
        id_field=id_field,
        prefix_filename=prefix_filename,
        lang=lang,
        num_topics=num_topics,
        num_words=num_words,
        num_pass=num_pass,

    )

    # print('result: ',list_tp_topics)
    # print('result: ',list_tp_keyword)

    if result_path!="" and os.path.exists(result_path):
        write_csv(f"{result_path}/list_tp_keywords.csv",list_tp_keyword)
        write_csv(f"{result_path}/list_tp_topics.csv", list_tp_topics)