from quick_topic.topic_interaction.divide_by_tag import *
from quick_topic.topic_interaction.lda_by_tag_each import *
from quick_topic.topic_interaction.interaction_among_tag import *

def run_topic_interaction(meta_csv_file,raw_text_folder, output_folder,list_category,stopwords_path,weights_folder,list_keywords_path,
    label_names,list_topics,filter_words,
                          tag_field="tag",
                          keyword_field="keyword",
                          time_field="time",
                          id_field="Id",
                          prefix_filename="",
                          num_topics=6,
                          num_pass=10,
                          num_words=50,
                          lang='zh',
                          minimum_num_doc_in_lda=15,
                          skip_date=False,
                          skip_step_1=False,
                          result_path=""
                          ):
    # step 1
    if not skip_step_1:
        divide_by_tag(
            meta_csv_file=meta_csv_file,
            raw_text_folder=raw_text_folder,
            output_folder=output_folder,
            list_category=list_category,
            tag_field = tag_field,
            keyword_field= keyword_field,
            time_field = time_field,
            id_field =id_field,
            prefix_filename=prefix_filename,
            skip_date=skip_date
        )

    # step 2

    lda_by_tag_each(
        list_category=list_category,
        root_path=output_folder,
        weights_path=weights_folder,
        list_keywords_path=list_keywords_path,
        stopwords_path=stopwords_path,
        num_topics=num_topics,
        num_pass=num_pass,
        num_words=num_words,
        lang=lang,
        minimum_num_doc=minimum_num_doc_in_lda
    )
    # step 3


    # run analysis for weights and interaction analysis
    result_topic_weights,result_top_keywords,result_interaction = interaction_among_tag(
        list_category=list_category,
        weights_folder=weights_folder,
        label_names=label_names,
        list_topics=list_topics,
        filter_keywords=filter_words
    )

    # save results
    if result_path!="" and os.path.exists(result_path):
        write_csv(f"{result_path}/ti_topic_weights.csv",result_topic_weights)
        write_csv(f"{result_path}/ti_top_keywords.csv",result_top_keywords)
        write_csv(f"{result_path}/ti_topic_interaction.csv",result_interaction)


