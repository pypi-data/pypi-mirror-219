from quick_topic.topic_interaction.main import *
from quickcsv.file import *

def get_categories(csv_file,category_field):
    list_item=read_csv(csv_file)
    list_ca=[]
    for item in list_item:
        if item[category_field] not in list_ca:
            list_ca.append(item[category_field])
    return list_ca

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

def gui_topic_interaction(
    # step 1: data file
    meta_csv_file = "datasets_paper/list_paper.csv",
    text_root = r"datasets_paper/raw_text",
    output_folder="results/topic_interaction",
    predefined_topic_file="predefined_topics.txt",
    category_field="category",
    time_field='PD',
    id_field='file_id',
    lang="en",
    stopwords_path="",
    num_topics: int = 6,
    num_pass: int = 10,
    num_words: int = 50,
    prefix_filename="",
        result_path=""
):
    # step2: jieba cut words file
    list_keywords_path = [

    ]

    label_names,list_topics=get_predefined_topics(predefined_topic_file=predefined_topic_file)

    # if any keyword is the below one, then the keyword is removed from our consideration
    filter_words = []

    # dictionaries
    list_category = get_categories(csv_file=meta_csv_file,category_field=category_field)
    print(list_category)

    # run shell
    run_topic_interaction(
        meta_csv_file=meta_csv_file,
        raw_text_folder=text_root,
        output_folder=f"{output_folder}/divided",
        list_category=list_category,  # a dictionary where each record contain a group of keywords
        stopwords_path=stopwords_path,
        weights_folder=f'{output_folder}/weights',
        list_keywords_path=list_keywords_path,
        label_names=label_names,
        list_topics=list_topics,
        filter_words=filter_words,
        # set field names
        tag_field=category_field,
        keyword_field="",  # ignore if keyword from csv exists in the text
        time_field=time_field,
        id_field=id_field,
        prefix_filename=prefix_filename,
        lang=lang,
        num_topics=num_topics,
        num_words=num_words,
        num_pass=num_pass,
        result_path=result_path
    )

