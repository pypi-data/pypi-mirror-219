from quick_topic.topic_trends.trends_by_year_fulltext import *
'''
    Get time trends of numbers of documents containing topic keywords with full text.
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

def gui_topic_trends(
        meta_csv_file='',
        raw_text_folder='',
        output_folder='',
        predefined_topic_file="",
        minimum_year=2010,
        id_field='file_id',
        time_field='PY',
        prefix_filename=""
):

    label_names,list_topics=get_predefined_topics(predefined_topic_file)

    # call function to show trends of number of documents containing topic keywords each year-month
    show_year_trends_with_fulltext(
        meta_csv_file=meta_csv_file,
        list_topics=list_topics,
        label_names=label_names,
        save_result_path=f"{output_folder}/topic_trends.csv",
        minimum_year=minimum_year,
        raw_text_path=raw_text_folder,
        id_field=id_field,
        time_field=time_field,
        prefix_filename=prefix_filename
    )
