import os
from quickcsv.file import *
from collections import OrderedDict
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


def create_keyword_distribution(root_path, keyword,save_figure=False,list_range=None,start_year=2000,end_year=2021,output_figure_folder="",
                                min_total_num=10,maximum_rate_if_meet_min_num=0.8,font_size=16,style="seaborn-deep",
y_label='Share of document',x_label='Year'
                                ):
    matplotlib.rcParams.update({'font.size': font_size})
    plt.style.use(style)

    topic_keywords = [keyword]

    label_name = '-'.join(topic_keywords)

    dict_year_month_rate = OrderedDict()

    for year in range(start_year, end_year+1):
        for month in range(1, 13):
            month_str=str(month)
            if month<10:
                month_str="0"+month_str
            year_month = f"{year}-{month_str}"
            year_month_folder = f"{root_path}/{year}-{month_str}"
            if not os.path.exists(year_month_folder):
                continue
            total_num = 0
            keyword_num = 0
            for country in os.listdir(year_month_folder):
                country_folder = f"{year_month_folder}/{country}"
                for file in os.listdir(country_folder):
                    text_file = f"{country_folder}/{file}"
                    text = read_text(text_file)
                    # print(text)
                    total_num += 1
                    has_keyword = False
                    for k in topic_keywords:
                        if k in text:
                            has_keyword = True
                            break
                    if has_keyword:
                        keyword_num += 1
            keyword_rate = round(keyword_num * 1.0 / total_num, 4)
            if total_num < min_total_num and keyword_rate > maximum_rate_if_meet_min_num:
                keyword_rate = 0
                continue
            dict_year_month_rate[year_month] = keyword_rate
    dict_year_month_rate = OrderedDict(sorted(dict_year_month_rate.items(), key=lambda obj: obj[0], reverse=False))
    print()
    print(f"Year\t{label_name}Share of document")
    x = []
    y = []
    for year_month in dict_year_month_rate:
        rate = dict_year_month_rate[year_month]
        print(f"{year_month}\t{rate}")
        x.append(year_month)
        y.append(rate)

    show_scatter(label_name, x, y,save_figure=save_figure,list_range=list_range,output_figure_folder=output_figure_folder,x_label=x_label,y_label=y_label)

def get_sub_plot(min,max,x,y):
    ys=[]
    xs=[]

    for idx,year_month in enumerate(x):
        year=year_month.split("-")[0]
        if int(year)>=min and int(year)<=max:
            xs.append(year_month)
            ys.append(y[idx])

    y_mean=np.mean(ys)
    for idx,y in enumerate(ys):
        ys[idx]=y_mean
    return xs,ys

def show_scatter(title,x,y,save_figure=False,list_range=None,output_figure_folder="",y_label='Share of document',x_label='Year'):

    import numpy as np
    dates = [pd.to_datetime(d) for d in x]
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    # plt.xlim(left=2000,right=2021)
    # plt.ylim(bottom=0)
    plt.scatter(dates, y)
    if list_range!=None:
        for rr in list_range:
            # sub plot
            x1,y1=get_sub_plot(rr[0],rr[1],x,y)
            # print(x1)
            # print(y1)
            plt.plot([pd.to_datetime(d) for d in x1],y1,color='r')

    if save_figure:
        if output_figure_folder!="":
            plt.savefig(f"{output_figure_folder}/{title}.jpg",dpi=300)
    # plt.show()
    plt.clf()

def show_transition_by_year_month_term(root_path,select_keywords,start_year,end_year,list_all_range=None,output_figure_folder="",
min_total_num=10,maximum_rate_if_meet_min_num=0.8,font_size=16,y_label='Share of document',x_label='Year'
                                       ):
    if output_figure_folder!="":
        if not os.path.exists(output_figure_folder):
            os.mkdir(output_figure_folder)

    for idx, k in enumerate(select_keywords):
        rr=None
        if list_all_range!=None:
            rr = list_all_range[idx]
        create_keyword_distribution(root_path=root_path, keyword=k, save_figure=True, list_range=rr,start_year=start_year,end_year=end_year,output_figure_folder=output_figure_folder,
                                    min_total_num=min_total_num, maximum_rate_if_meet_min_num=maximum_rate_if_meet_min_num, font_size=font_size,
                                    x_label=x_label,y_label=y_label
                                    )
