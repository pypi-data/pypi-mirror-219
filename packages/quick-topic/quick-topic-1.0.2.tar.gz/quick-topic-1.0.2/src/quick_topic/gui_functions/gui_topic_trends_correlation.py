import os.path

from quick_topic.topic_trends_correlation.topic_trends_correlation_two import *
'''
    Estimate the correlation among trends
'''

def gui_tropic_trends_correlation(
    trends_file = "results/topic_trends/trends_fulltext.csv",
    label_names_str = "Knowledge,Socialization,Digitalization,Intelligence",
        start_year=2010,
        end_year=2021,
        time_field='Time',
        show_figure=False,
        result_path='',
        prefix_filename=''
):
    label_names=label_names_str.split(",")
    label_names=[l.strip() for l in label_names]

    list_result = []
    list_line = []
    for i in range(0, len(label_names) - 1):
        for j in range(i + 1, len(label_names)):
            label1 = label_names[i]
            label2 = label_names[j]
            result = estimate_topic_trends_correlation_single_file(
                trend_file=trends_file,
                selected_field1=label1,
                selected_field2=label2,
                start_year=start_year,
                end_year=end_year,
                show_figure=show_figure,
                time_field=time_field
            )

            line = f"({label1},{label2})\t{result['pearson'][0]}\t{result['pearson'][1]}"
            list_line.append(line)
            list_result.append({
                "Comparison":f"({label1},{label2})",
                "Pearson-stat":result['pearson'][0],
                "Pearson-p-value":result['pearson'][1]
            })

            print()

    print("Correlation analysis results:")
    print("Pair\tPearson-Stat\tP-value")
    for line in list_line:
        print(line)

    if result_path!="" and os.path.exists(result_path):
        write_csv(result_path+"/ttc_trends.csv",list_result)


if __name__=="__main__":
    gui_tropic_trends_correlation(
        trends_file='D:/UIBE科研/国自科青年/开源项目/quick-topic/examples/metaverse_tweets/topic_analysis/results2/topic_trends/trends_fulltext.csv',
        label_names_str='Knowledge, Digitalization,Socialization,Intelligence'
    )