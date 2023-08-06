from quick_topic.topic_visualization.topic_modeling_pipeline import *

def gui_topic_explore(
    meta_csv_file = "../g20_news1/datasets/list_g20_news.csv",
    raw_text_folder = f"../g20_news1/datasets/raw_text",
    stopwords_path = "../datasets/stopwords/hit_stopwords.txt",
    chinese_font_file = "../g20_news/utils/fonts/SimHei.ttf",
    output_folder="",
    num_topics = 4,
    num_words = 10,
    n_rows = 2,
    n_cols = 4,
    max_records = 100,
    lang="zh",
    prefix_filename=""
):

    result_output_folder = f"{output_folder}/topic{num_topics}"

    if not os.path.exists(result_output_folder):
        os.mkdir(result_output_folder)

    run_topic_modeling_pipeline(
        meta_csv_file=meta_csv_file,
        raw_text_folder=raw_text_folder,
        stopwords_path=stopwords_path,
        top_record_num=max_records,
        chinese_font_file=chinese_font_file,
        num_topics=num_topics,
        num_words=num_words,
        n_rows=n_rows,
        n_cols=n_cols,
        result_output_folder=result_output_folder,
        load_existing_models=False,
        lang=lang,
        prefix_filename=prefix_filename
    )
