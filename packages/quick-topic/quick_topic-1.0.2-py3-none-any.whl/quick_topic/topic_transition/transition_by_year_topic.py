import os
from quickcsv.file import *
from collections import OrderedDict
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.pyplot as plt
import matplotlib

def show_transition_by_year_topic(root_path,label,keywords,start_year,end_year,min_total_num=10,maximum_rate_if_meet_min_num=0.8,font_size=16,
                                  style="seaborn-deep",save_figure=False,figure_path="",result_path="",show_figure=True):
    matplotlib.rcParams.update({'font.size': font_size})
    plt.style.use(style)

    dict_year_rate = OrderedDict()

    for year in range(start_year, end_year+1):
        year_folder = f"{root_path}/{year}"
        if not os.path.exists(year_folder):
            continue
        total_num = 0
        keyword_num = 0
        for country in os.listdir(year_folder):
            country_folder = f"{year_folder}/{country}"
            for file in os.listdir(country_folder):
                text_file = f"{country_folder}/{file}"
                text = read_text(text_file)
                # print(text)
                total_num += 1
                has_keyword = False
                for k in keywords:
                    if k in text:
                        has_keyword = True
                        break
                if has_keyword:
                    keyword_num += 1
        keyword_rate = round(keyword_num * 1.0 / total_num, 4)
        if total_num < min_total_num and keyword_rate > maximum_rate_if_meet_min_num:
            keyword_rate = 0
        dict_year_rate[year] = keyword_rate


    def show_scatter(title, x, y,save_figure=False,output_path=""):
        # dates = [pd.to_datetime(d) for d in x]
        plt.title(title)
        plt.xlabel("Year")
        plt.ylabel("Share of document")
        plt.scatter(x, y)
        if save_figure:
            plt.savefig(output_path,dpi=300)
        plt.show()

    dict_year_rate = OrderedDict(sorted(dict_year_rate.items(), key=lambda obj: obj[0], reverse=False))
    print()
    print(f"Year\t{label} Percent")
    x = []
    y = []
    list_item=[]
    for year in dict_year_rate:
        rate = dict_year_rate[year]
        print(f"{year}\t{rate}")
        x.append(year)
        y.append(rate)
        model={
            "Year":year,
            "Percent":rate
        }
        list_item.append(model)
    if result_path != "" and os.path.exists(result_path):
        result_tt_folder=result_path+"/topic_transition"
        if not os.path.exists(result_tt_folder):
            os.mkdir(result_tt_folder)
        write_csv(f'{result_tt_folder}/tt_{label}.csv', list_item)
    if show_figure:
        show_scatter(label, x, y,save_figure,output_path=figure_path)
