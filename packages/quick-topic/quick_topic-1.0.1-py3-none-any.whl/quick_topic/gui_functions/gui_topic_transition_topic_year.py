from quick_topic.topic_transition.transition_by_year_topic import *
from quick_topic.topic_transition.divide_by_year import *

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

def gui_topic_transition_topic_year(
    meta_csv_file = "datasets_paper/list_paper.csv",
    raw_text_folder = r"datasets_paper/raw_text",
        predefined_topic_file="",
        output_folder="",
        start_year=2010,
        end_year=2021,
        category_field="category",
        time_field='PD',
        id_field='file_id',
        lang="en",
        result_path="",
        show_figure=True,
        prefix_filename=""
           ):
    output_divided_folder = f"{output_folder}/divided_year"
    if not os.path.exists(output_divided_folder):
        os.mkdir(output_divided_folder)
    output_figure_folder = f"{output_folder}/figures"
    if not os.path.exists(output_figure_folder):
        os.mkdir(output_figure_folder)

    # Step 1: divide the dataset by year-month
    divide_by_year(
        meta_csv_file=meta_csv_file,
        raw_text_folder=raw_text_folder,
        output_folder=output_divided_folder,
        start_year=start_year,
        end_year=end_year,
        id_field=id_field,
        tag_field=category_field,
        time_field=time_field,
        prefix_filename=prefix_filename
    )

    label_names, list_topics = get_predefined_topics(predefined_topic_file=predefined_topic_file)

    for idx, keywords in enumerate(list_topics):
        label = label_names[idx]
        show_transition_by_year_topic(
            root_path=f"{output_folder}/divided_year",
            label=label,
            keywords=keywords,
            start_year=start_year,
            end_year=end_year,
            save_figure=True,
            figure_path=f'{output_folder}/figure_{label}.jpg',
            result_path=result_path,
            show_figure=show_figure
        )
