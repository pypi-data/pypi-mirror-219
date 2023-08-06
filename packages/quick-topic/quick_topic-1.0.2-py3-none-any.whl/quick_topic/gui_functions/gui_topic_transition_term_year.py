from quick_topic.topic_transition.transition_by_year_term import *
from quick_topic.topic_transition.divide_by_year import *
'''
    Estimate the topic transition over time
'''

def gui_term_transition_year(
    meta_csv_file="datasets_paper/list_paper.csv",
    raw_text_folder = r"datasets_paper/raw_text",
        output_folder="results/topic_transition",
        selected_keywords_file="",
        start_year=2010,
        end_year=2021,
        id_field='file_id',
        tag_field='category',
        time_field='PY',
        result_path="",
        show_figure=True,
        prefix_filename=""
):

    output_divided_folder = f"{output_folder}/divided_year"
    output_figure_folder = f"{output_folder}/figures"
    select_keywords=[w.strip() for w in open(selected_keywords_file,'r',encoding='utf-8').readlines()]

    # Step 1: divide the dataset by year-month
    divide_by_year(
        meta_csv_file=meta_csv_file,
        raw_text_folder=raw_text_folder,
        output_folder=output_divided_folder,
        start_year=start_year,
        end_year=end_year,
        id_field=id_field,
        tag_field=tag_field,
        time_field=time_field,
        prefix_filename=prefix_filename
    )

    # Step 2: analyze the divided datasets
    '''
    list_all_range = [
        [[2010, 2015], [2016, 2021]],
        [[2011, 2017], [2018, 2021]],
        [[2009, 2017], [2018, 2021]],
        [[2011, 2016], [2017, 2021]],
        [[2017, 2018], [2019, 2021]],
        [[2009, 2014], [2015, 2021]],
        [[2009, 2014], [2015, 2021]],
        [[2009, 2015], [2016, 2021]],
        [[2008, 2011], [2012, 2015], [2016, 2021]],
        [[2011, 2016], [2017, 2021]],
        [[2009, 2012], [2013, 2016], [2017, 2021]],
        [[2009, 2015], [2016, 2021]]
    ]
    '''
    list_all_range = None

    show_transition_by_year_term(
        root_path=output_divided_folder,
        select_keywords=select_keywords,
        list_all_range=list_all_range,
        output_figure_folder=output_figure_folder,
        start_year=start_year,
        end_year=end_year,
        result_path=result_path,
        show_figure=show_figure
    )
