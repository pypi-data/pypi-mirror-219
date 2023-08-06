import pickle
import re, numpy as np, pandas as pd
from pprint import pprint
import os
import jieba.posseg as pseg
import gensim, spacy, logging, warnings
import gensim.corpora as corpora
from gensim.utils import lemmatize, simple_preprocess
from gensim.models import CoherenceModel
import matplotlib
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import matplotlib.colors as mcolors

matplotlib.rcParams['font.family'] = 'SimHei'
# NLTK Stop words
warnings.filterwarnings("ignore",category=DeprecationWarning)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

'''
  Step 1: Load dataset
'''
def load_dataset(meta_csv_file,raw_text_folder,prefix_filename='',id_field='fileId',text_field='text'):
    df = pd.read_csv(meta_csv_file)
    df = df[[id_field]]

    fileIds = df[id_field].values
    list_text = []
    for fileId in fileIds:
        text_path = f"{raw_text_folder}/{prefix_filename}{fileId}.txt"
        if not os.path.exists(text_path):
            text = ""
        else:
            text = open(text_path, encoding='utf-8').read()
        list_text.append(text)

    df[text_field] = list_text
    print(df.head())
    return df

# Step 2: word segmentation
def word_segmentation(df,stopwords_path="",text_field='text',top_record_num=-1):
    stopwords = []

    if stopwords_path != "":
        stopwords = [w.strip() for w in open(stopwords_path, 'r', encoding='utf-8').readlines()
                     if w.strip() != ""]

    def sent_to_words(doc):
        list_words = pseg.cut(doc)
        list_w = []
        for w, f in list_words:
            if f in ['n', 'nr', 'ns', 'nt', 'nz', 'vn', 'nd', 'nh', 'nl', 'i']:
                if w not in stopwords and len(w) != 1:
                    list_w.append(w)
        return list_w

    # Convert to list
    data = df[text_field].values.tolist()
    if top_record_num!=-1:
        data=data[:top_record_num]

    data_words = []
    for text in data:
        words = sent_to_words(text)
        data_words.append(words)
        print(words)

    print(data_words[:1])
    return data_words

def word_segmentation_english(df,stopwords_path="",text_field='text',top_record_num=-1,min_count=5,threshold=100,user_postags=None):
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english')
    if top_record_num!=-1:
        df=df.head(n=top_record_num)
    def sent_to_words(sentences):
        for sent in sentences:
            sent = re.sub('\S*@\S*\s?', '', sent)  # remove emails
            sent = re.sub('\s+', ' ', sent)  # remove newline chars
            sent = re.sub("\'", "", sent)  # remove single quotes
            sent = gensim.utils.simple_preprocess(str(sent), deacc=True)
            # print(sent)
            yield (sent)

            # Convert to list

    data = df[text_field].values.tolist()
    data_words = list(sent_to_words(data))

    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words, min_count=min_count, threshold=threshold)  # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=threshold)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    # allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']
    allowed_postags=['NOUN']
    if user_postags!=None:
        allowed_postags=user_postags

    # !python3 -m spacy download en  # run in terminal once
    def process_words(texts, stop_words=stop_words, allowed_postags=allowed_postags):
        """Remove Stopwords, Form Bigrams, Trigrams and Lemmatization"""
        texts = [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]
        texts = [bigram_mod[doc] for doc in texts]
        texts = [trigram_mod[bigram_mod[doc]] for doc in texts]
        texts_out = []
        nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
        for sent in texts:
            doc = nlp(" ".join(sent))
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        # remove stopwords once more after lemmatization
        texts_out = [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts_out]
        return texts_out

    data_ready = process_words(data_words)  # processed Text Data!
    return data_ready

'''
  Step 3: build LDA
'''
def build_lda(data_words,num_topics=10,num_pass=10):
    # Create Dictionary
    id2word = corpora.Dictionary(data_words)

    # Create Corpus: Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in data_words]

    # Build LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=num_topics,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=10,
                                                passes=num_pass,
                                                alpha='symmetric',
                                                iterations=100,
                                                per_word_topics=True)

    pprint(lda_model.print_topics(num_topics=num_topics))
    return lda_model,corpus,id2word

'''
  Step 4: What is the Dominant topic and its percentage contribution in each document
'''
def get_dominant_topics_in_each_document(lda_model,corpus,data_words,
                                         output_folder="",
                                         save_topic_sentence_keywords='topic_sentence_keywords.csv',
                                         save_dominant_topic="dominant_topic_in_each_document.csv"
                                         ):
    def format_topics_sentences(ldamodel=None, corpus=corpus, texts=None):
        # Init output
        sent_topics_df = pd.DataFrame()

        # Get main topic in each document
        for i, row_list in enumerate(ldamodel[corpus]):
            row = row_list[0] if ldamodel.per_word_topics else row_list
            # print(row)
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = ldamodel.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    sent_topics_df = sent_topics_df.append(
                        pd.Series([int(topic_num), round(prop_topic, 4), topic_keywords]), ignore_index=True)
                else:
                    break
        sent_topics_df.columns = ['Dominant_Topic', 'Percent_Contribution', 'Topic_Keywords']

        # Add original text to the end of the output
        contents = pd.Series(texts)
        sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
        return sent_topics_df

    df_topic_sents_keywords = format_topics_sentences(ldamodel=lda_model, corpus=corpus, texts=data_words)

    df_topic_sents_keywords.to_csv(output_folder+"/"+save_topic_sentence_keywords, encoding='utf-8')

    # Format
    df_dominant_topic = df_topic_sents_keywords.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Percent_Contribution', 'Keywords', 'Text']

    df_dominant_topic.to_csv(output_folder+"/"+save_dominant_topic, encoding='utf-8')

    print(df_dominant_topic.head(10))

    return df_topic_sents_keywords,df_dominant_topic

'''
  Step 5: get the most representative sentence for each topic
'''
def get_most_representative_sentences(df_topic_sents_keywords,output_folder="",save_file="most_representative_sentence.csv"):
    # Display setting to show more characters in column
    pd.options.display.max_colwidth = 100

    sent_topics_sorteddf_mallet = pd.DataFrame()
    sent_topics_outdf_grpd = df_topic_sents_keywords.groupby('Dominant_Topic')

    for i, grp in sent_topics_outdf_grpd:
        sent_topics_sorteddf_mallet = pd.concat([sent_topics_sorteddf_mallet,
                                                 grp.sort_values(['Percent_Contribution'], ascending=False).head(1)],
                                                axis=0)

    # Reset Index
    sent_topics_sorteddf_mallet.reset_index(drop=True, inplace=True)

    # Format
    sent_topics_sorteddf_mallet.columns = ['Topic_Num', "Topic_Percent_Contribution", "Keywords", "Representative_Text"]

    # Show
    print(sent_topics_sorteddf_mallet.head(10))

    sent_topics_sorteddf_mallet.to_csv(output_folder+"/"+save_file, encoding='utf-8')
    return sent_topics_sorteddf_mallet

'''
  Step 6: get frequency distribution of word counts in documents
'''
def show_freq_distribution(df_dominant_topic,show_figure=True,n_rows=2,n_cols=2,font_size=10,dpi=160,save_figure=False,output_folder="",pause_figure=3):
    doc_lens = [len(d) for d in df_dominant_topic.Text]

    # Plot
    plt.figure(
        # figsize=(16, 7),
               dpi=dpi)
    plt.hist(doc_lens, bins=1000, color='navy')
    plt.text(750, 100, "Mean   : " + str(round(np.mean(doc_lens))))
    plt.text(750, 90, "Median : " + str(round(np.median(doc_lens))))
    plt.text(750, 80, "Stdev   : " + str(round(np.std(doc_lens))))
    plt.text(750, 70, "1%ile    : " + str(round(np.quantile(doc_lens, q=0.01))))
    plt.text(750, 60, "99%ile  : " + str(round(np.quantile(doc_lens, q=0.99))))

    plt.gca().set(xlim=(0, 1000), ylabel='Number of Documents', xlabel='Document Word Count')
    plt.tick_params(size=font_size)
    plt.xticks(np.linspace(0, 1000, 9))
    plt.title('Distribution of Document Word Counts', fontdict=dict(size=font_size))
    if save_figure:
        plt.savefig(f"{output_folder}/document_word_counts_distribution.jpg",dpi=dpi)
    if show_figure:
        plt.show()
    else:
        plt.show(block=False)
        plt.pause(pause_figure)
        plt.close()

    import seaborn as sns
    import matplotlib.colors as mcolors
    # cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]  # more colors: 'mcolors.XKCD_COLORS'
    cols = [color for name, color in mcolors.XKCD_COLORS.items()]

    fig, axes = plt.subplots(n_rows, n_cols,
                             # figsize=(16, 14),
                             dpi=dpi, sharex=True, sharey=True)

    for i, ax in enumerate(axes.flatten()):
        df_dominant_topic_sub = df_dominant_topic.loc[df_dominant_topic.Dominant_Topic == i, :]
        doc_lens = [len(d) for d in df_dominant_topic_sub.Text]
        ax.hist(doc_lens, bins=1000, color=cols[i])
        ax.tick_params(axis='y', labelcolor=cols[i], color=cols[i])
        sns.kdeplot(doc_lens, color="black", shade=False, ax=ax.twinx())
        ax.set(xlim=(0, 1000), xlabel='Document Word Count')
        ax.set_ylabel('Number of Documents', color=cols[i])
        ax.set_title('Topic: ' + str(i), fontdict=dict(size=font_size, color=cols[i]))

    fig.tight_layout()
    fig.subplots_adjust(top=0.90)
    plt.xticks(np.linspace(0, 1000, 9))
    fig.suptitle('Distribution of Document Word Counts by Dominant Topic', fontsize=font_size)
    if save_figure:
        plt.savefig(f"{output_folder}/document_word_counts_distribution_by_dominant_topic.jpg",dpi=dpi)
    if show_figure:
        plt.show()
    else:
        plt.show(block=False)
        plt.pause(3)
        plt.close()

'''
  Step 7: Word Clouds
'''
def show_word_clouds(lda_model,num_topics=10,  num_words=20, stopwords_path="",n_rows=2,n_cols=2,chinese_font_path="",font_size=10,
                     max_words=20,width=2500,height=1800,max_font_size=200,show_figure=True,save_figure=True,output_folder="",dpi=160,pause_figure=3):
    stopwords = []

    if stopwords_path != "":
        stopwords = [w.strip() for w in open(stopwords_path, 'r', encoding='utf-8').readlines()
                     if w.strip() != ""]

    # 1. Wordcloud of Top N words in each topic


    cols = [color for name, color in mcolors.XKCD_COLORS.items()]  # more colors: 'mcolors.XKCD_COLORS'

    cloud=None
    if chinese_font_path=="":
        cloud = WordCloud(stopwords=stopwords,
                          background_color='white',
                          width=width,
                          height=height,
                          max_words=max_words,
                          colormap='tab10',
                          color_func=lambda *args, **kwargs: cols[i],
                          prefer_horizontal=1.0,

                          )
    else:
        cloud = WordCloud(stopwords=stopwords,
                                  background_color='white',
                                  width=width,
                                  height=height,
                                  max_words=max_words,
                                  colormap='tab10',
                                  color_func=lambda *args, **kwargs: cols[i],
                                  prefer_horizontal=1.0,
                                  font_path=chinese_font_path,

                                  )

    topics = lda_model.show_topics(num_topics=num_topics, num_words=num_words,formatted=False)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(10, 10), sharex=True, sharey=True)
    print("len of axes: ",len(axes.flatten()))
    print("len of topcis: ",len(topics))
    for i, ax in enumerate(axes.flatten()):
        fig.add_subplot(ax)
        topic_words = dict(topics[i][1])
        cloud.generate_from_frequencies(topic_words, max_font_size=max_font_size)
        plt.gca().imshow(cloud)
        plt.gca().set_title('Topic ' + str(i), fontdict=dict(size=font_size))
        plt.gca().axis('off')

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.axis('off')
    plt.margins(x=0, y=0)
    plt.tight_layout()
    if save_figure:
        plt.savefig(output_folder+"/wordcloud.jpg",dpi=dpi)
    if show_figure:
        plt.show()
    else:
        plt.show(block=False)
        plt.pause(pause_figure)
        plt.close()

'''
  Step 8: show word counts of topic keywords
'''
def show_word_counts_of_topic_keywords(lda_model,data_words,num_words=20,num_topics=10,output_folder="", save_topic_keyword_important='topic_keyword_importance.csv',
                                       font_size=8,dpi=160,n_rows=2,n_cols=2,show_figure=True,rotation=30,pause_figure=3
                                       ):
    from collections import Counter
    topics = lda_model.show_topics(num_topics=num_topics, num_words=num_words, formatted=False)
    data_flat = [w for w_list in data_words for w in w_list]
    counter = Counter(data_flat)

    out = []
    for i, topic in topics:
        for word, weight in topic:
            out.append([word, i, weight, counter[word]])

    df = pd.DataFrame(out, columns=['word', 'topic_id', 'importance', 'word_count'])

    df.to_csv(output_folder+"/"+save_topic_keyword_important, encoding='utf-8')

    # Plot Word Count and Weights of Topic Keywords
    fig, axes = plt.subplots(n_rows, n_cols,
                             # figsize=(16, 10),
                             sharey=True, dpi=dpi)
    cols = [color for name, color in mcolors.XKCD_COLORS.items()]
    for i, ax in enumerate(axes.flatten()):
        ax.bar(x='word', height="word_count", data=df.loc[df.topic_id == i, :], color=cols[i], width=0.5, alpha=0.3,
               label='Word Count')
        ax_twin = ax.twinx()
        ax_twin.bar(x='word', height="importance", data=df.loc[df.topic_id == i, :], color=cols[i], width=0.2,
                    label='Weights')
        ax.set_ylabel('Word Count', color=cols[i],fontdict=dict(size=font_size))

        # ax_twin.set_ylim(0, 0.030)
        # ax.set_ylim(0, 3500)
        ax.set_title('Topic: ' + str(i), color=cols[i],fontdict=dict(size=font_size))
        ax.tick_params(axis='y', left=False)
        ax.set_xticklabels(df.loc[df.topic_id == i, 'word'], rotation=rotation, horizontalalignment='right',fontsize=font_size)

        ax.legend(loc='upper left')
        ax_twin.legend(loc='upper right')

    fig.tight_layout(w_pad=2)
    fig.suptitle('Word Count and Importance of Topic Keywords', fontsize=font_size, y=1.05)
    if show_figure:
        plt.show()
    else:
        plt.show(block=False)
        plt.pause(pause_figure)
        plt.close()

'''
 Step 9: show sentence charts colored by topic
'''
def show_sentence_chart(lda_model, corpus, start = 0, end = 13,font_size=8,show_figure=True,pause_figure=3,save_figure=True,output_folder="",dpi=160):
    from matplotlib.patches import Rectangle
    corp = corpus[start:end]
    mycolors = [color for name, color in mcolors.XKCD_COLORS.items()]

    fig, axes = plt.subplots(end - start, 1,
                             figsize=(20, (end - start) * 0.95), dpi=160)
    axes[0].axis('off')
    for i, ax in enumerate(axes):
        if i > 0:
            corp_cur = corp[i - 1]
            topic_percs, wordid_topics, wordid_phivalues = lda_model[corp_cur]
            word_dominanttopic = [(lda_model.id2word[wd], topic[0]) for wd, topic in wordid_topics]
            ax.text(0.01, 0.5, "Doc " + str(i - 1) + ": ", verticalalignment='center',
                    fontsize=font_size, color='black', transform=ax.transAxes, fontweight=700)

            # Draw Rectange
            topic_percs_sorted = sorted(topic_percs, key=lambda x: (x[1]), reverse=True)
            ax.add_patch(Rectangle((0.0, 0.05), 0.99, 0.90, fill=None, alpha=1,
                                   color=mycolors[topic_percs_sorted[0][0]], linewidth=2))

            word_pos = 0.06
            for j, (word, topics) in enumerate(word_dominanttopic):
                if j < 14:
                    ax.text(word_pos, 0.5, word,
                            horizontalalignment='left',
                            verticalalignment='center',
                            fontsize=font_size, color=mycolors[topics],
                            transform=ax.transAxes, fontweight=700)
                    word_pos += .009 * len(word)  # to move the word for the next iter
                    ax.axis('off')
            ax.text(word_pos, 0.5, '. . .',
                    horizontalalignment='left',
                    verticalalignment='center',
                    fontsize=font_size, color='black',
                    transform=ax.transAxes)

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.suptitle('Sentence Topic Coloring for Documents: ' + str(start) + ' to ' + str(end - 2), fontsize=font_size, y=0.95,
                 fontweight=700)
    plt.tight_layout()
    if save_figure:
        plt.savefig(output_folder+"/sentence_chart.jpg",dpi=dpi)
    if show_figure:
        plt.show()
    else:
        plt.show(block=False)
        plt.pause(pause_figure)
        plt.close()

'''
  show the most discussed topics
'''
def show_most_discussed_topics(lda_model,corpus,num_topics=10,num_words=20, output_folder="",
                               save_dominant_topic_file='distribution_of_dominant_topics_in_each_document.csv',
                               save_topic_topic_weight='total_topic_distribution_by_actual_weight.csv',
                               save_top_keywords_in_topic='topN_words_in_each_topic.csv',
                               max_words_num=20

                               ):
    # Sentence Coloring of N Sentences
    def topics_per_document(model, corpus, start=0, end=1):
        corpus_sel = corpus[start:end]
        dominant_topics = []
        topic_percentages = []
        for i, corp in enumerate(corpus_sel):
            topic_percs, wordid_topics, wordid_phivalues = model[corp]
            dominant_topic = sorted(topic_percs, key=lambda x: x[1], reverse=True)[0][0]
            dominant_topics.append((i, dominant_topic))
            topic_percentages.append(topic_percs)
        return (dominant_topics, topic_percentages)

    dominant_topics, topic_percentages = topics_per_document(model=lda_model, corpus=corpus, end=-1)

    # Distribution of Dominant Topics in Each Document
    df = pd.DataFrame(dominant_topics, columns=['Document_Id', 'Dominant_Topic'])
    dominant_topic_in_each_doc = df.groupby('Dominant_Topic').size()
    df_dominant_topic_in_each_doc = dominant_topic_in_each_doc.to_frame(name='count').reset_index()

    df_dominant_topic_in_each_doc.to_csv(output_folder+"/"+save_dominant_topic_file, encoding='utf-8')

    # Total Topic Distribution by actual weight
    topic_weightage_by_doc = pd.DataFrame([dict(t) for t in topic_percentages])
    df_topic_weightage_by_doc = topic_weightage_by_doc.sum().to_frame(name='count').reset_index()

    df_topic_weightage_by_doc.to_csv(output_folder+"/"+ save_topic_topic_weight, encoding='utf-8')

    # Top 3 Keywords for each Topic
    topic_top3words = [(i, topic) for i, topics in lda_model.show_topics(num_topics=num_topics,num_words=num_words, formatted=False)
                       for j, (topic, wt) in enumerate(topics) if j < max_words_num]

    df_top3words_stacked = pd.DataFrame(topic_top3words, columns=['topic_id', 'words'])
    df_top3words = df_top3words_stacked.groupby('topic_id').agg(', '.join)
    df_top3words.reset_index(level=0, inplace=True)

    df_top3words.to_csv(output_folder+"/"+save_top_keywords_in_topic, encoding='utf-8')

    return df_dominant_topic_in_each_doc,df_topic_weightage_by_doc,df_top3words

'''
  step 11: show_topic_distribution
'''
def show_topic_distribution(df_dominant_topic_in_each_doc,df_topic_weightage_by_doc,df_top3words,font_size=10,dpi=120,show_figure=True,
                            save_figure=True,output_path="",pause_figure=3):
    # Let’s visualize the clusters of documents in a 2D space using t-SNE (t-distributed stochastic neighbor embedding) algorithm.
    from matplotlib.ticker import FuncFormatter

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2,
                                   # figsize=(10, 4),
                                   dpi=dpi, sharey=True)

    # Topic Distribution by Dominant Topics
    ax1.bar(x='Dominant_Topic', height='count', data=df_dominant_topic_in_each_doc, width=.5, color='firebrick')
    ax1.set_xticks(range(df_dominant_topic_in_each_doc.Dominant_Topic.unique().__len__()))
    # tick_formatter = FuncFormatter(lambda x, pos: 'Topic ' + str(x)+ '\n' + df_top3words.loc[df_top3words.topic_id==x, 'words'].values[0])
    # ax1.xaxis.set_major_formatter(tick_formatter)
    ax1.set_title('Number of Documents by Dominant Topic', fontdict=dict(size=font_size))
    ax1.set_ylabel('Number of Documents')
    # ax1.set_ylim(0, 1000)

    # Topic Distribution by Topic Weights
    ax2.bar(x='index', height='count', data=df_topic_weightage_by_doc, width=.5, color='steelblue')
    ax2.set_xticks(range(df_topic_weightage_by_doc.index.unique().__len__()))
    # ax2.xaxis.set_major_formatter(tick_formatter)
    ax2.set_title('Number of Documents by Topic Weightage', fontdict=dict(size=font_size))

    if save_figure:
        plt.savefig(output_path+"/topic_distribution.jpg",dpi=dpi)
    if show_figure:
        plt.show()
    else:
        plt.show(block=False)
        plt.pause(pause_figure)
        plt.close()

'''
  Step 12: 
'''

def show_tsne(lda_model,corpus,num_topics=4,output_folder=""):
    # Get topic weights and dominant topics ------------
    from sklearn.manifold import TSNE

    from bokeh.plotting import figure, output_file, save
    output_file(filename=output_folder+"/tsne.html", title="Static HTML file")

    # Get topic weights
    topic_weights = []
    for i, row_list in enumerate(lda_model[corpus]):
        topic_weights.append([w for i, w in row_list[0]])

    # Array of topic weights
    arr = pd.DataFrame(topic_weights).fillna(0).values

    # Keep the well separated points (optional)
    arr = arr[np.amax(arr, axis=1) > 0.35]

    # Dominant topic number in each doc
    topic_num = np.argmax(arr, axis=1)

    # tSNE Dimension Reduction
    tsne_model = TSNE(n_components=2, verbose=1, random_state=0, angle=.99, init='pca')
    tsne_lda = tsne_model.fit_transform(arr)

    # Plot the Topic Clusters using Bokeh
    # n_topics = 6
    mycolors = np.array([color for name, color in mcolors.XKCD_COLORS.items()])
    plot = figure(title="t-SNE Clustering of {} LDA Topics".format(num_topics),
                  plot_width=900, plot_height=700)
    plot.scatter(x=tsne_lda[:, 0], y=tsne_lda[:, 1], color=mycolors[topic_num])
    from bokeh.io import export_png

    # export_png(plot, filename=output_folder+"/tsne.png")

    # show(plot, output_file=output_folder+"/tsne.html", browser='windows-default',new='tab')
    save(plot)

'''
 step 13: pyLDAvis
'''
def show_pyLDAvis(lda_model,corpus,output_folder="",save_file="pyLDAvis.html"):
    import pyLDAvis.gensim_models
    # pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary=lda_model.id2word)
    pyLDAvis.save_html(vis, output_folder+'/'+save_file)

def run_topic_modeling_pipeline(
## data
    meta_csv_file = "../../../examples/g20_news1/datasets/list_g20_news.csv",
    raw_text_folder = f"../../../examples/g20_news1/datasets/raw_text",
    stopwords_path = "../../../examples/datasets/stopwords/hit_stopwords.txt",
    ## output
    result_output_folder = "../../../examples/g20_news1/test_output6",
    ## parameters
    chinese_font_file = "../../../examples/g20_news/utils/fonts/SimHei.ttf",
    num_topics = 6,
        num_words=20,
    n_rows = 2,
    n_cols = 3,
    max_words_in_wordcloud = 30,
    save_figure = True,
    show_figure = False,
    top_record_num = 1000,  # -1 means all data
    pause_figure=3,
    load_existing_models=False,
        lang='en',
        prefix_filename="",
        id_field="fileId",
        text_field="text",
        num_pass=10
):

    lda_model_file = result_output_folder + "/lda.model"
    corpus_model_file = result_output_folder + "/corpus.model"
    id2word_model_file = result_output_folder + "/id2word.model"
    data_words_file=result_output_folder+"/data_words.model"
    lda_model=None
    corpus=None
    id2word=None
    data_words=None
    if load_existing_models:
        lda_model=pickle.load(open(lda_model_file,'rb'))
        corpus = pickle.load(open(corpus_model_file, 'rb'))
        id2word = pickle.load(open(id2word_model_file, 'rb'))
        data_words=pickle.load(open(data_words_file,'rb'))
    else:
        # step 1:
        df = load_dataset(meta_csv_file=meta_csv_file, raw_text_folder=raw_text_folder,prefix_filename=prefix_filename,id_field=id_field,text_field=text_field)
        # step 2:
        data_words=None

        if lang=='zh':
            data_words = word_segmentation(df, stopwords_path=stopwords_path, top_record_num=top_record_num)
        elif lang=='en':
            data_words=word_segmentation_english(df, stopwords_path=stopwords_path, top_record_num=top_record_num)
        else:
            raise Exception("lang is not valid!")

        # step 3:
        lda_model, corpus, id2word = build_lda(data_words, num_topics=num_topics,num_pass=num_pass)
        pickle.dump(lda_model,open(lda_model_file,'wb'))
        pickle.dump(corpus,open(corpus_model_file,"wb"))
        pickle.dump(id2word,open(id2word_model_file,"wb"))
        pickle.dump(data_words,open(data_words_file,"wb"))

    if not os.path.exists(lda_model_file):
        lda_model.save(lda_model_file)
    # step 4:
    df_sentence, df_dominant_topic = get_dominant_topics_in_each_document(lda_model=lda_model, corpus=corpus,
                                                                          data_words=data_words,
                                                                          output_folder=result_output_folder)
    # step 5:
    sent_topics_sorteddf_mallet = get_most_representative_sentences(df_sentence, output_folder=result_output_folder)
    # step 6:
    show_freq_distribution(df_dominant_topic, show_figure=show_figure, n_rows=n_rows, n_cols=n_cols,
                           save_figure=save_figure, output_folder=result_output_folder,pause_figure=pause_figure)
    # step 7:
    show_word_clouds(lda_model, num_topics=num_topics, num_words=num_words, n_rows=n_rows, n_cols=n_cols, stopwords_path=stopwords_path,
                     chinese_font_path=chinese_font_file, max_words=max_words_in_wordcloud,
                     show_figure=show_figure, save_figure=save_figure, output_folder=result_output_folder,pause_figure=pause_figure)
    # step 8:
    show_word_counts_of_topic_keywords(lda_model,data_words,num_topics=num_topics,num_words=num_words, output_folder=result_output_folder, n_rows=n_rows, n_cols=n_cols,
                                       show_figure=show_figure,pause_figure=pause_figure)
    # step 9:
    show_sentence_chart(lda_model, corpus, start=0, end=9, show_figure=show_figure,save_figure=save_figure,pause_figure=pause_figure,output_folder=result_output_folder)
    # step 10:
    a, b, c = show_most_discussed_topics(lda_model, corpus, output_folder=result_output_folder)
    # step 11:
    show_topic_distribution(df_dominant_topic_in_each_doc=a, df_topic_weightage_by_doc=b, df_top3words=c,
                            output_path=result_output_folder, show_figure=show_figure,
                            save_figure=save_figure,pause_figure=pause_figure)
    # step 12:
    show_tsne(lda_model=lda_model, corpus=corpus, output_folder=result_output_folder, num_topics=num_topics)
    # step 13:
    show_pyLDAvis(lda_model=lda_model, corpus=corpus, output_folder=result_output_folder, save_file='pyLDAvis.html')

if __name__=="__main__":

    num_topics=8
    num_words=20
    n_rows=2
    n_cols=4
    max_records=-1
    result_output_folder=f"../../../examples/g20_news1/test_outputs/topic{num_topics}"

    if not os.path.exists(result_output_folder):
        os.mkdir(result_output_folder)
    run_topic_modeling_pipeline(top_record_num=max_records,
                                num_topics=num_topics,
                                num_words=num_words,
                                n_rows=n_rows,n_cols=n_cols,
                                result_output_folder = result_output_folder,
                                load_existing_models=False
                               )
