import numpy as np
from collections import OrderedDict
import os
from quickcsv.file import *
# topic files
def load_topic_file(output_folder, topic_name,top=10):
    dict_keyword_weights={}
    k_lines = open(f"{output_folder}/{topic_name}_k.csv", 'r', encoding='utf-8').readlines()
    v_lines = open(f"{output_folder}/{topic_name}_v.csv", 'r', encoding='utf-8').readlines()
    w_lines = open(f"{output_folder}/{topic_name}_w.csv", 'r', encoding='utf-8').readlines()
    if len(w_lines)!=len(k_lines) or len(w_lines)!=len(v_lines):
        return {}
    dict_keyword=OrderedDict()
    for idx, item in enumerate(k_lines):
        fs_k = item.strip().split(",")
        fs_v = v_lines[idx].strip().split(",")
        topic_weight=float(w_lines[idx].strip().split(",")[1])
        for kid, k in enumerate(fs_k):
            weight = float(fs_v[kid])
            keyword = k
            #if keyword not in list_all_words:
            #    list_all_words.append(keyword)
            if keyword not in dict_keyword_weights.keys():
                dict_keyword_weights[keyword] = [topic_weight * weight]
            else:
                dict_keyword_weights[keyword].append(topic_weight * weight)
    for k in dict_keyword_weights:
        dict_keyword[k]=np.sum(dict_keyword_weights[k])
    dict_keyword = OrderedDict(sorted(dict_keyword.items(), key=lambda obj: obj[1], reverse=True))
    # get top key words
    top_keywords=list(dict_keyword.keys())[:top]
    list_keyword_weight=[]
    for t in top_keywords:
        list_keyword_weight.append(np.sum(dict_keyword[t]))
    dict_kw={}
    for t in top_keywords:
        dict_kw[t]=np.sum(dict_keyword[t])

    return dict_kw

def get_sim(list_w1,list_w2):
    from strsimpy.cosine import Cosine
    cosine = Cosine(2)
    s0 = ' '.join(list_w1)
    s1 = ' '.join(list_w2)
    p0 = cosine.get_profile(s0)
    p1 = cosine.get_profile(s1)
    sim=cosine.similarity_profiles(p0, p1)
    # print()
    return sim

def get_cosine_sim(list1,list2):
    from scipy import spatial
    result = 1 - spatial.distance.cosine(list1, list2)
    return result

def get_cosine_sim_by_dicts(dict1,dict2):
    # print(dict1)
    # print(dict2)
    list_words=[]
    list_weights1=[]
    list_weights2 = []
    for k1 in dict1:
        if k1 not in list_words:
            list_words.append(k1)
    for k1 in dict2:
        if k1 not in list_words:
            list_words.append(k1)
    # print(list_words)
    for idx,k in enumerate(list_words):
        if k in dict1.keys():
            list_weights1.append(float(dict1[k]))
        else:
            list_weights1.append(0)

    for idx,k in enumerate(list_words):
        if k in dict2:
            list_weights2.append(float(dict2[k]))
        else:
            list_weights2.append(0)
    return get_cosine_sim(list_weights1,list_weights2)


def estimate_topic_similarity(list_topic,topic_folder,list_keywords_file="",topN=30,lang='zh',result_path=''):
    print()
    list_item=[]
    print("Category-Pair\tTopic-Similarity")
    for i in range(0, len(list_topic) - 1):
        for j in range(i + 1, len(list_topic)):
            topic1 = list_topic[i]
            topic2 = list_topic[j]
            topic1_file = f"{topic_folder}/{topic1}_k.csv"
            topic2_file = f"{topic_folder}/{topic2}_k.csv"
            if not os.path.exists(topic1_file) or not os.path.exists(topic2_file):
                continue
            dict1 = load_topic_file(topic_folder, topic1, top=topN)
            dict2 = load_topic_file(topic_folder, topic2, top=topN)
            if len(list(dict1.keys()))==0 or len(list(dict1.keys()))==0:
                continue
            # sim=get_sim(dicts[i],dicts[j])
            sim = get_cosine_sim_by_dicts(dict1, dict2)

            print(f"({topic1},{topic2})\t{round(sim, 4)}")
            list_item.append({
                'Category Pair':f"({topic1},{topic2})",
                'Topic Similarity':round(sim, 4)
            })

    # print(get_sim(dict_g20,dict_industry))
    # print(get_sim(dict_g20,dict_company))
    # print(get_sim(dict_g20,dict_weibo))
    if result_path!="" and os.path.exists(result_path):
        write_csv(result_path+"/ts_similarity.csv",list_item)




