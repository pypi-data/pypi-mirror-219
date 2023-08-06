from quick_topic.topic_stat.stat_by_keyword import *
'''
    Stat sentence numbers by keywords
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

def gui_keyword_stat(
    meta_csv_file = 'datasets_paper/list_paper.csv',
    raw_text_folder = "datasets_paper/raw_text",
    predefined_topic_file="",
    id_field='file_id',
        result_path="",
        prefix_filename=""
):

    label_names,list_topics=get_predefined_topics(predefined_topic_file)


    list_dict = []

    for idx,the_keyword in enumerate(list_topics):
        r = stat_sentence_by_keywords(
            meta_csv_file=meta_csv_file,
            keywords=the_keyword,
            id_field=id_field,
            raw_text_folder=raw_text_folder,
            contains_keyword_in_sentence='',
            prefix_file_name=prefix_filename
        )
        list_dict.append(r)
        output_path=f"{result_path}/ks_{label_names[idx]}.csv"
        list_item=[]
        for k in r:
            list_item.append({
                "Keyword":k,
                "Frequency":r[k]
            })
        write_csv(output_path,list_item)

    print()
    list_all_words = []
    for dict in list_dict:
        for k in dict:
            if k not in list_all_words:
                list_all_words.append(k)

    #list_item=[]
    print("keyword\t" + "\t".join(label_names))
    for w in list_all_words:
        list_v = []
        for dict in list_dict:
            count = 0
            if w in dict.keys():
                count = dict[w]
            list_v.append(str(count))
        print(w + "\t" + "\t".join(list_v))
        model={
            "keyword":w
        }
        for idx,l in enumerate(label_names):
            model[l] = float(list_v[idx])
        #list_item.append(model)
    #return list_item


