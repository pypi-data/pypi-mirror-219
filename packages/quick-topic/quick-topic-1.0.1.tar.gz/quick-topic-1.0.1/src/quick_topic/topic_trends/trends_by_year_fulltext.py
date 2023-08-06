import os

from quickcsv.file import *
from collections import OrderedDict

def show_year_trends_with_fulltext(
        meta_csv_file='../information_extraction2/datasets/list_g20_news_all_clean.csv',
        id_field="FileId",
        time_field="PublishTime",
        # opinion_path="../information_extraction2/datasets/list_g20_leaders_opinion.csv",
        # opinion_field="opinion",
        # opinion_id_field="file_id",
        list_topics=None,
        label_names=None,
        save_result_path="",
        minimum_year=2019,
        raw_text_path= r"g20_news_processed",
        prefix_filename=""
):
    # load dataset
    list_g20_news_final = qc_read(csv_path=meta_csv_file)

    dict_opinion_year = {}

    N = len(list_g20_news_final)
    for idx, item in enumerate(list_g20_news_final):
        # print(f"{idx+1}/{N}")
        file_id = item[id_field]
        year = item[time_field]
        if year=="":
            continue
        if int(year) < minimum_year:
            continue

        dict_opinion_year[file_id] = year

    list_item = qc_read(meta_csv_file)

    list_dict_topic=[]

    for the_keyword in list_topics:
        dict_keywords = OrderedDict()
        list_keywords=[]
        for item in list_item:
            file_id = item[id_field]
            # print(item["file_id"])
            text_path = raw_text_path + f"\\{prefix_filename}" + file_id + ".txt"
            if not os.path.exists(text_path):
                continue
            opinion = read_text(text_path)
            # opinion = get_text_with_leaders(opinion)

            # print(opinion)
            for k in the_keyword:
                if k in opinion:
                    # print(opinion)
                    list_keywords.append(item)
                    get_trend(dict_opinion_year,dict_keywords, file_id)
                    break
        # print(list_keywords)
        list_dict_topic.append(dict_keywords)

    # year-month trends
    list_dict_topic[0] = OrderedDict(sorted(list_dict_topic[0].items(), key=lambda obj: obj[0], reverse=False))

    # show_time_trend(dict_energy)
    show_time_trends(
        labels=label_names,
        list_dict_trends=list_dict_topic,
        output_trends_file=save_result_path
    )

def get_trend(dict_opinion_year,dict_num,file_id):
    year = ""
    if file_id in dict_opinion_year:
        year = dict_opinion_year[file_id]
    if year == "":
        return
    if year in dict_num:
        if file_id not in dict_num[year]:
            dict_num[year].append(file_id)

    else:
        dict_num[year] = []
        dict_num[year].append(file_id)
    return dict_num

def get_trend_total(dict_opinion_year_month,dict_economics,file_id):
    year_month = ""
    if file_id in dict_opinion_year_month:
        year_month = dict_opinion_year_month[file_id]
    if year_month == "":
        return
    if year_month in dict_economics:
        dict_economics[year_month].append(file_id)
    else:
        dict_economics[year_month] = []
        dict_economics[year_month].append(file_id)
    return dict_economics

def show_time_trend(dict_trend):
    print("Year\tDocument frequency")
    for k in dict_trend:
        print(f"{k}\t{len(dict_trend[k])}")

def show_time_trends(labels,list_dict_trends,output_trends_file):
    list_item=[]

    print("Time\t"+"\t".join(labels))
    for k in list_dict_trends[0]:
        ls = f"{k}\t"
        model = {
            "Time": k
        }
        for idx,dict_trend in enumerate(list_dict_trends):
            if k in dict_trend:
                ls+=f"{len(dict_trend[k])}\t"
                model[labels[idx]]=len(dict_trend[k])
            else:
                model[labels[idx]] = 0
                ls+="0\t"
        list_item.append(model)
        print(ls)
    qc_write(output_trends_file,list_item)

