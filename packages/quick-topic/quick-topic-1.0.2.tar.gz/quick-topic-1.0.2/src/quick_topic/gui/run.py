import os
import pickle
import sys
import PyQt5
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QFileSystemModel, QTableWidgetItem
from quick_topic.gui.main import Ui_MainWindow
from quick_topic.gui_functions.gui_topic_interaction import *
from quick_topic.gui_functions.gui_topic_prevalence import *
from quick_topic.gui_functions.gui_topic_similarity import *
from quick_topic.gui_functions.gui_keywordstat import *
from quick_topic.gui_functions.gui_topic_modeling import *
from quick_topic.gui_functions.gui_topic_transition_topic_year import *
from quick_topic.gui_functions.gui_topic_trends import *
from quick_topic.gui_functions.gui_topic_trends_correlation import *
from quick_topic.gui_functions.gui_topic_transition_term_year import *
from quick_topic.gui_functions.gui_topic_explore import *
import pyqtgraph as pg

import ctypes
myappid = 'quick-topic-tool-gui' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        current_path = os.path.dirname(__file__)
        app_icon = QIcon(current_path+ "/qtt.png")
        self.setWindowIcon(app_icon)

        self.btnOpen.clicked.connect(self.select_file)
        self.btnBrowse.clicked.connect(self.select_folder)
        self.btnBrowseOutput.clicked.connect(self.select_output_folder)
        self.btnOpenTopic.clicked.connect(self.select_topic_file)
        self.btnOpenTrendsFile.clicked.connect(self.select_trends_file)
        self.btnRun.clicked.connect(self.run)
        self.btnOpenStopwords.clicked.connect(self.select_stopwords_file)
        self.btnKeywordsFile.clicked.connect(self.select_keywords_file)
        self.btnResult.clicked.connect(self.select_result_folder)
        self.btn_refresh_results.clicked.connect(self.show_result_folder)
        self.btnSaveConfig.clicked.connect(self.save_config_file_event)
        self.btnLoadConfig.clicked.connect(self.load_config_file_event)
        self.tv_result_files.doubleClicked.connect(self.tree_clicked)
        self.btnPlot.clicked.connect(self.plot)
        self.btn_clear_plot.clicked.connect(self.clear_plot)
        self.btn_bar.clicked.connect(self.plot_bar)
        self.btn_explore.clicked.connect(self.explore_topic)
        self.btn_select_chinese_font.clicked.connect(self.open_chinese_font_file)

        # self.table_show.selectedIndexes.connect(self.selected)
        # plot chart
        self.graphWidget = pg.PlotWidget()
        self.layout_plot.addWidget(self.graphWidget)

        #hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        #temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        # plot data: x, y values
        #self.graphWidget.plot(hour, temperature)
        self.graphWidget.setBackground('w')
        self.load_config()
        self.list_plot=[]

    def reset_plot_widget(self):
        self.layout_plot.removeWidget(self.graphWidget)
        self.graphWidget = pg.PlotWidget()
        self.layout_plot.addWidget(self.graphWidget)
        self.graphWidget.setBackground('w')

    def clear_plot(self):
        if self.list_plot != None and len(self.list_plot) != 0:
            for plot in self.list_plot:
                self.graphWidget.removeItem(plot)
                self.graphWidget.removeItem(self.graphWidget.getPlotItem())
        self.list_plot = []
        self.reset_plot_widget()

    def plot_bar(self):
        self.reset_plot_widget()
        index = self.table_show.selectedIndexes()
        chart_data = []
        list_cols = []
        list_value = []
        for i in index:
            row = i.row()
            col = i.column()
            value = self.data[row][col]
            if col not in list_cols:
                list_cols.append(col)
        for c in list_cols:
            list_v = []
            for i in index:
                row = i.row()
                col = i.column()
                value = self.data[row][col]
                if col == c:
                    list_v.append(value)
            list_value.append(list_v)
        print(list_cols)
        print(list_value)
        if len(list_cols) >= 2:
            # plot data: x, y values
            x_label = self.cols[list_cols[0]]
            y_label = self.cols[list_cols[1]]
            # plt=self.graphWidget.plot()
            self.graphWidget.setBackground('w')



            pen = pg.mkPen(color=(255, 0, 0))
            self.graphWidget.setTitle("Comparison analysis", color="b", size="10pt")
            styles = {'color': 'b', 'font-size': '10px'}
            self.graphWidget.setLabel('left', y_label, **styles)
            self.graphWidget.setLabel('bottom', x_label, **styles)
            self.graphWidget.addLegend()
            self.graphWidget.showGrid(x=True, y=True)
            self.list_plot = []
            if len(list_cols)==2:
                height=list_value[1]
                new_height=[]
                for h in height:
                    new_height.append(float(h))
                new_x=[]
                for idx,xx in enumerate(list_value[0]):
                    new_x.append(idx)
                bar_item = pg.BarGraphItem(x=new_x, height=new_height, width=1.0, brush='r')
                plot1=self.graphWidget.addItem(bar_item)

                self.list_plot.append(plot1)
            else:
                QMessageBox.about(self, "Tips", "Please select only two columns!")


    def plot(self):
        self.reset_plot_widget()
        index = self.table_show.selectedIndexes()
        chart_data=[]
        list_cols=[]
        list_value=[]
        for i in index:
            row=i.row()
            col=i.column()
            value=self.data[row][col]
            if col not in list_cols:
                list_cols.append(col)
        for c in list_cols:
            list_v=[]
            for i in index:
                row=i.row()
                col=i.column()
                value=self.data[row][col]
                if col==c:
                    list_v.append(float(value))
            list_value.append(list_v)
        print(list_cols)
        print(list_value)
        if len(list_cols)>=2:
            # plot data: x, y values
            x_label=self.cols[list_cols[0]]
            y_label=self.cols[list_cols[1]]
            # plt=self.graphWidget.plot()
            self.graphWidget.setBackground('w')

            pen = pg.mkPen(color=(255, 0, 0))
            self.graphWidget.setTitle("Trend analysis", color="b", size="15pt")
            styles = {'color': 'b', 'font-size': '10px'}
            self.graphWidget.setLabel('left', y_label, **styles)
            self.graphWidget.setLabel('bottom', x_label, **styles)
            self.graphWidget.addLegend()
            self.graphWidget.showGrid(x=True, y=True)
            self.list_plot=[]
            if len(list_cols)>=3:
                for i in range(1,len(list_cols)):
                    plot=self.graphWidget.plot(list_value[0], list_value[i], label=self.cols[list_cols[i]], pen=pen,  symbol='+')
                    self.list_plot.append(plot)
            else:
                plot=self.graphWidget.plot(list_value[0], list_value[1], label=self.cols[list_cols[1]],pen=pen, symbol='+')
                self.list_plot.append(plot)

    def open_chinese_font_file(self):
        path = QFileDialog.getOpenFileName(self, 'Load a chinese font file', '',
                                           'All Files (*.*)')
        if path != ('', ''):
            print("Load chinese file path : " + path[0])
            self.edit_chinese_font.setText(path[0])

    def save_config_file_event(self):
        path = QFileDialog.getSaveFileName(self, 'Save a config file', '',
                                           'All Files (*.*)')
        if path != ('', ''):
            print("Save file path : " + path[0])
            self.save_config_file(path[0])

    def load_config_file_event(self):
        path = QFileDialog.getOpenFileName(self, 'Load a config file', '',
                                           'All Files (*.*)')
        if path != ('', ''):
            print("Load file path : " + path[0])
            self.load_config_file(path[0])

    def select_file(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.*)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.edit_metafile.setText(path[0])

    def select_trends_file(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.*)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.edit_trends_file.setText(path[0])

    def select_topic_file(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.*)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.edit_predefined_topic.setText(path[0])

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Open a directory', '',)
        if folder != ('', ''):
            print("raw folder path : " + folder)
            self.edit_raw_folder.setText(folder)

    def select_result_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Open a directory', '',)
        if folder != ('', ''):
            print("result folder path : " + folder)
            self.edit_result_path.setText(folder)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Open a directory', '',)
        if folder != ('', ''):
            print("output folder path : " + folder)
            self.edit_output_path.setText(folder)

    def select_stopwords_file(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.*)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.edit_stopwords_file.setText(path[0])

    def select_keywords_file(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.*)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.edit_keywords_file.setText(path[0])

    def explore_topic(self):
        self.save_config()
        meta_csv_file = self.edit_metafile.text()
        print(meta_csv_file)
        raw_text_folder = self.edit_raw_folder.text()
        output_folder = self.edit_output_path.text()
        topic_file = self.edit_predefined_topic.text()
        category_field = self.field_category.text()
        id_field = self.field_id.text()
        time_field = self.field_time.text()
        lang = self.field_lang.text()
        num_topics = self.numTopics.value()
        num_words = self.numWords.value()
        stopwords_path = self.edit_stopwords_file.text()
        result_path = self.edit_result_path.text()
        prefix_filename = self.edit_prefix.text()

        target_folder = f"{output_folder}/topic_explore"
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)

        gui_topic_explore(
            meta_csv_file=meta_csv_file,
            raw_text_folder=raw_text_folder,
            output_folder=target_folder,
            stopwords_path=stopwords_path,
            lang=lang,
            num_topics=num_topics,
            num_words=num_words,
            prefix_filename=prefix_filename,
            n_rows=int(self.edit_rows.text()),
            n_cols=int(self.edit_cols.text()),
            max_records=int(self.edit_max_records.text()),
            chinese_font_file=self.edit_chinese_font.text()
        )

        QMessageBox.about(self, "Tips", "Finished!")


    def run_topic_interaction(self):

        QtCore.QCoreApplication.processEvents()

        meta_csv_file=self.edit_metafile.text()
        print(meta_csv_file)
        raw_text_folder=self.edit_raw_folder.text()
        output_folder=self.edit_output_path.text()
        topic_file=self.edit_predefined_topic.text()
        category_field=self.field_category.text()
        id_field=self.field_id.text()
        time_field=self.field_time.text()
        lang=self.field_lang.text()
        num_topics = self.numTopics.value()
        num_words = self.numWords.value()
        stopwords_path=self.edit_stopwords_file.text()
        result_path=self.edit_result_path.text()
        prefix_filename=self.edit_prefix.text()

        target_folder=f"{output_folder}/topic_interaction"
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)

        gui_topic_interaction(
            meta_csv_file=meta_csv_file,
            text_root=raw_text_folder,
            output_folder=target_folder,
            predefined_topic_file=topic_file,
            category_field=category_field,
            time_field=time_field,
            id_field=id_field,
            lang=lang,
            num_topics=num_topics,
            num_words=num_words,
            stopwords_path=stopwords_path,
            result_path=result_path,
            prefix_filename=prefix_filename
        )
        # QMessageBox.about(self, "Tips", "Finished!")

    def run_topic_prevalence(self):
        meta_csv_file = self.edit_metafile.text()
        raw_text_folder = self.edit_raw_folder.text()
        output_folder = self.edit_output_path.text()
        topic_file = self.edit_predefined_topic.text()
        category_field = self.field_category.text()
        id_field = self.field_id.text()
        time_field = self.field_time.text()
        lang = self.field_lang.text()
        start_year=self.numStartYear.value()
        end_year=self.numEndYear.value()
        num_topics = self.numTopics.value()
        num_words = self.numWords.value()
        stopwords_path = self.edit_stopwords_file.text()
        result_path=self.edit_result_path.text()
        prefix_filename = self.edit_prefix.text()

        target_folder = f"{output_folder}/topic_prevalence"
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)

        QtCore.QCoreApplication.processEvents()

        gui_topic_prevalence(
            meta_csv_file=meta_csv_file,
            text_root=raw_text_folder,
            output_folder=target_folder,
            predefined_topic_file=topic_file,
            category_field=category_field,
            time_field=time_field,
            id_field=id_field,
            lang=lang,
            start_year=start_year,
            end_year=end_year,
            num_topics=num_topics,
            num_words=num_words,
            stopwords_path=stopwords_path,
            result_path=result_path,
            prefix_filename=prefix_filename
        )

    def run_keyword_stat(self):

        QtCore.QCoreApplication.processEvents()
        result_path = self.edit_result_path.text()

        meta_csv_file = self.edit_metafile.text()
        raw_text_folder = self.edit_raw_folder.text()
        output_folder = self.edit_output_path.text()
        topic_file = self.edit_predefined_topic.text()
        id_field = self.field_id.text()
        prefix_filename = self.edit_prefix.text()

        target_folder = f"{output_folder}/keyword_stat"
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)

        gui_keyword_stat(
            meta_csv_file=meta_csv_file,
            raw_text_folder=raw_text_folder,
            predefined_topic_file=topic_file,
            id_field=id_field,
            result_path=result_path,
            prefix_filename=prefix_filename
        )

        # write_csv(f"{result_path}/ks_keywords.csv",list_item)

    def run_topic_modeling(self):

        QtCore.QCoreApplication.processEvents()

        meta_csv_file = self.edit_metafile.text()
        raw_text_folder = self.edit_raw_folder.text()
        output_folder = self.edit_output_path.text()
        topic_file = self.edit_predefined_topic.text()
        id_field = self.field_id.text()
        category_field = self.field_category.text()
        id_field = self.field_id.text()
        time_field = self.field_time.text()
        lang = self.field_lang.text()
        start_year = self.numStartYear.value()
        end_year = self.numEndYear.value()
        num_topics = self.numTopics.value()
        num_words = self.numWords.value()
        stopwords_path = self.edit_stopwords_file.text()
        prefix_filename = self.edit_prefix.text()

        target_folder = f"{output_folder}/topic_modeling"
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)

        gui_topic_modeling(
            meta_csv_file=meta_csv_file,
            raw_text_folder=raw_text_folder,
            output_folder=target_folder,
            id_field=id_field,
            category_field=category_field,
            num_topics=num_topics,
            num_words=num_words,
            stopwords_path=stopwords_path,
            lang=lang,
            prefix_filename=prefix_filename
        )

    def run_topic_transition_year(self):

        QtCore.QCoreApplication.processEvents()

        meta_csv_file = self.edit_metafile.text()
        raw_text_folder = self.edit_raw_folder.text()
        output_folder = self.edit_output_path.text()
        topic_file = self.edit_predefined_topic.text()
        id_field = self.field_id.text()
        category_field = self.field_category.text()
        id_field = self.field_id.text()
        time_field = self.field_time.text()
        lang = self.field_lang.text()
        start_year = self.numStartYear.value()
        end_year = self.numEndYear.value()
        result_path=self.edit_result_path.text()
        show_figure = self.cbDisplayFigure.isChecked()
        prefix_filename = self.edit_prefix.text()

        target_folder = f"{output_folder}/topic_transition"
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)

        gui_topic_transition_topic_year(
            meta_csv_file=meta_csv_file,
            raw_text_folder=raw_text_folder,
            predefined_topic_file=topic_file,
            output_folder=target_folder,
            start_year=start_year,
            end_year=end_year,
            category_field=category_field,
            time_field=time_field,
            id_field=id_field,
            lang=lang,
            result_path=result_path,
            show_figure=show_figure,
            prefix_filename=prefix_filename
        )

    def run_term_transition_year(self):

        QtCore.QCoreApplication.processEvents()

        meta_csv_file = self.edit_metafile.text()
        raw_text_folder = self.edit_raw_folder.text()
        output_folder = self.edit_output_path.text()
        topic_file = self.edit_predefined_topic.text()
        id_field = self.field_id.text()
        category_field = self.field_category.text()
        id_field = self.field_id.text()
        time_field = self.field_time.text()
        lang = self.field_lang.text()
        start_year = self.numStartYear.value()
        end_year = self.numEndYear.value()
        select_keywords_file=self.edit_keywords_file.text()
        result_path = self.edit_result_path.text()
        show_figure=self.cbDisplayFigure.isChecked()
        prefix_filename = self.edit_prefix.text()

        target_folder = f"{output_folder}/term_transition"
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)

        gui_term_transition_year(
            meta_csv_file=meta_csv_file,
            raw_text_folder=raw_text_folder,
            selected_keywords_file=select_keywords_file,
            output_folder=target_folder,
            start_year=start_year,
            end_year=end_year,
            time_field=time_field,
            id_field=id_field,
            tag_field=category_field,
            result_path=result_path,
            show_figure=show_figure,
            prefix_filename=prefix_filename
        )

    def run_topic_trends(self):
        meta_csv_file = self.edit_metafile.text()
        raw_text_folder = self.edit_raw_folder.text()
        output_folder = self.edit_output_path.text()
        topic_file = self.edit_predefined_topic.text()
        id_field = self.field_id.text()
        category_field = self.field_category.text()
        id_field = self.field_id.text()
        time_field = self.field_time.text()
        lang = self.field_lang.text()
        start_year = self.numStartYear.value()
        end_year = self.numEndYear.value()
        result_path = self.edit_result_path.text()
        prefix_filename = self.edit_prefix.text()

        target_folder = f"{output_folder}/topic_trends"
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)

        QtCore.QCoreApplication.processEvents()

        gui_topic_trends(
            meta_csv_file=meta_csv_file,
            raw_text_folder=raw_text_folder,
            predefined_topic_file=topic_file,
            output_folder=target_folder,
            minimum_year=start_year,
            time_field=time_field,
            id_field=id_field,
            prefix_filename=prefix_filename
        )

    def run_topic_trends_correlation(self):
        time_field = self.field_time.text()
        start_year = self.numStartYear.value()
        end_year = self.numEndYear.value()
        trends_file=self.edit_trends_file.text()
        label_names=self.edit_labelnames.text()
        result_path = self.edit_result_path.text()
        QtCore.QCoreApplication.processEvents()
        prefix_filename = self.edit_prefix.text()

        gui_tropic_trends_correlation(
            trends_file=trends_file,
            label_names_str=label_names,
            time_field=time_field,
            start_year=start_year,
            end_year=end_year,
            result_path=result_path,
            prefix_filename=prefix_filename
        )

    def run_topic_similarity(self):
        meta_csv_file = self.edit_metafile.text()
        raw_text_folder = self.edit_raw_folder.text()
        output_folder = self.edit_output_path.text()
        topic_file = self.edit_predefined_topic.text()
        category_field = self.field_category.text()
        id_field = self.field_id.text()
        time_field = self.field_time.text()
        lang = self.field_lang.text()
        start_year=self.numStartYear.value()
        end_year=self.numEndYear.value()
        num_topics=self.numTopics.value()
        num_words=self.numWords.value()
        result_path = self.edit_result_path.text()
        target_folder = f"{output_folder}/topic_similarity"
        prefix_filename = self.edit_prefix.text()
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)

        QtCore.QCoreApplication.processEvents()

        gui_topic_similarity(
            meta_csv_file=meta_csv_file,
            raw_text_folder=raw_text_folder,
            output_folder=target_folder,
            category_field=category_field,
            time_field=time_field,
            id_field=id_field,
            lang=lang,
            num_topics=num_topics,
            num_words=num_words,
            result_path=result_path,
            prefix_filename=prefix_filename
        )

    def save_config_file(self,filename):
        config_model = {
            "meta_csv_file": self.edit_metafile.text(),
            "raw_text_folder": self.edit_raw_folder.text(),
            "output_folder": self.edit_output_path.text(),
            "topic_file": self.edit_predefined_topic.text(),
            "category_field": self.field_category.text(),
            "id_field": self.field_id.text(),
            "time_field": self.field_time.text(),
            "lang": self.field_lang.text(),
            "start_year": self.numStartYear.value(),
            "end_year": self.numEndYear.value(),
            "num_topics": self.numTopics.value(),
            "num_words": self.numWords.value(),
            "trends_file": self.edit_trends_file.text(),
            "label_names": self.edit_labelnames.text(),
            "stopwords_file": self.edit_stopwords_file.text(),
            "keywords_file": self.edit_keywords_file.text(),
            "result_path": self.edit_result_path.text(),
            "show_figure": self.cbDisplayFigure.isChecked(),
            "prefix_filename":self.edit_prefix.text(),
            "n_rows":self.edit_rows.text(),
            "n_cols":self.edit_cols.text(),
            "max_records":self.edit_max_records.text(),
            "chinese_font_file":self.edit_chinese_font.text()
        }
        pickle.dump(config_model, open(filename, "wb"))

    def load_config_file(self,filename):
        if os.path.exists(filename):
            config_model=pickle.load(open(filename,"rb"))
            self.edit_metafile.setText(config_model["meta_csv_file"])
            self.edit_raw_folder.setText(config_model["raw_text_folder"])
            self.edit_output_path.setText(config_model["output_folder"])
            self.edit_predefined_topic.setText(config_model["topic_file"])
            self.field_category.setText(config_model["category_field"])
            self.field_id.setText(config_model["id_field"])
            self.field_lang.setText(config_model['lang'])
            self.field_time.setText(config_model['time_field'])
            if 'start_year' in config_model:
                self.numStartYear.setValue(config_model['start_year'])
            if 'end_year' in config_model:
                self.numEndYear.setValue(config_model['end_year'])
            if 'num_topics' in config_model:
                self.numTopics.setValue(config_model['num_topics'])
            if 'num_words' in config_model:
                self.numWords.setValue(config_model['num_words'])
            if 'trends_file' in config_model:
                self.edit_trends_file.setText(config_model['trends_file'])
            if 'label_names' in config_model:
                self.edit_labelnames.setText(config_model['label_names'])
            if 'stopwords_file' in config_model:
                self.edit_stopwords_file.setText(config_model['stopwords_file'])
            if 'keywords_file' in config_model:
                self.edit_keywords_file.setText(config_model['keywords_file'])
            if 'result_path' in config_model:
                self.edit_result_path.setText(config_model['result_path'])
            if 'show_figure' in config_model:
                self.cbDisplayFigure.setChecked(config_model['show_figure'])
            if 'prefix_filename' in config_model:
                self.edit_prefix.setText(config_model['prefix_filename'])
            if 'n_rows' in config_model:
                self.edit_rows.setText(config_model['n_rows'])
            if 'n_cols' in config_model:
                self.edit_cols.setText(config_model['n_cols'])
            if 'max_records' in config_model:
                self.edit_max_records.setText(config_model['max_records'])
            if 'chinese_font_file' in config_model:
                self.edit_chinese_font.setText(config_model['chinese_font_file'])
        else:
            print("Config file not exists")

    def save_config(self):
        self.save_config_file('quick_topic.config')

    def load_config(self):
        self.load_config_file('quick_topic.config')

    def display(self, s):
        if s=="start":
            # QMessageBox.about(self, "Info", "Working...")
            self.lbTip.setText("Working...")
        if s=="end":
            self.lbTip.setText("Finished")
            QMessageBox.about(self, "Info", "Finished!")
            self.show_result_folder()
        if s.startswith("error:"):
            self.lbTip.setText("Error")
            QMessageBox.warning(self, "Error",s)

    def run(self):
        QtCore.QCoreApplication.processEvents()
        self.save_config()
        if self.cbTI.isChecked():
            # self.run_topic_interaction()
            self.work = WorkThread()
            self.work.set_func(self.run_topic_interaction)
            self.work.start()
            self.work.trigger.connect(self.display)
        if self.cbTP.isChecked():
            # self.run_topic_prevalence()
            self.work = WorkThread()
            self.work.set_func(self.run_topic_prevalence)
            self.work.start()
            self.work.trigger.connect(self.display)
        if self.cbTS.isChecked():
            self.work = WorkThread()
            self.work.set_func(self.run_topic_similarity)
            self.work.start()
            self.work.trigger.connect(self.display)
        if self.cbKS.isChecked():
            self.work = WorkThread()
            self.work.set_func(self.run_keyword_stat)
            self.work.start()
            self.work.trigger.connect(self.display)
        if self.cbTM.isChecked():
            self.work = WorkThread()
            self.work.set_func(self.run_topic_modeling)
            self.work.start()
            self.work.trigger.connect(self.display)
        if self.cbTT.isChecked():
            self.work = WorkThread()
            self.work.set_func(self.run_topic_transition_year)
            self.work.start()
            self.work.trigger.connect(self.display)
        if self.cbTrends.isChecked():
            self.work = WorkThread()
            self.work.set_func(self.run_topic_trends)
            self.work.start()
            self.work.trigger.connect(self.display)
        if self.cbTTC.isChecked():
            self.work = WorkThread()
            self.work.set_func(self.run_topic_trends_correlation)
            self.work.start()
            self.work.trigger.connect(self.display)
        if self.cbTermT.isChecked():
            self.work = WorkThread()
            self.work.set_func(self.run_term_transition_year)
            self.work.start()
            self.work.trigger.connect(self.display)


    def show_result_folder(self):
        try:
            self.filemodel = QFileSystemModel()

            if self.edit_result_path.text()!="":
                self.filemodel.setRootPath(self.edit_result_path.text())

            else:
                self.filemodel.setRootPath('')

            # model.setRootPath('')
            self.tv_result_files.setModel(self.filemodel)
            self.tv_result_files.setRootIndex(self.filemodel.index(
                self.edit_result_path.text()
            ))
            self.tv_result_files.setAnimated(False)
            self.tv_result_files.setIndentation(20)
            self.tv_result_files.setSortingEnabled(True)
            for i in [1, 2, 3]:
                self.tv_result_files.setColumnHidden(i, True)
        except Exception as err:
            print(err)

    def tree_clicked(self, Qmodelidx):
        if self.filemodel!=None:
            # print(self.filemodel.filePath(Qmodelidx))
            # print(self.filemodel.fileName(Qmodelidx))
            # print(self.filemodel.fileInfo(Qmodelidx))
            self.lb_selected_file.setText(f"Selected File: {self.filemodel.fileName(Qmodelidx)}")
            self.selected_result_file_path=self.filemodel.filePath(Qmodelidx)
            if self.selected_result_file_path.endswith('.csv'):
                try:
                    list_item=read_csv(self.selected_result_file_path)
                    self.cols=list(list_item[0].keys())
                    data=[]
                    for item in list_item:
                        line=[]
                        for k in item:
                            line.append(item[k])
                        data.append(line)
                    self.data=data
                    #data_model=TableModel(data)
                    #for idx,c in enumerate(cols):
                    #    data_model.setHeaderData(idx+1, Qt.Horizontal, c)
                    print("cols: ",self.cols)
                    self.table_show.clear()
                    self.table_show.setColumnCount(len(self.cols))
                    self.table_show.setRowCount(len(list_item))
                    self.table_show.setHorizontalHeaderLabels(self.cols)
                    for idx,item in enumerate(list_item):
                        for idx1,k in enumerate(list(item.keys())):
                            newItem = QTableWidgetItem(item[k])
                            self.table_show.setItem(idx, idx1, newItem)
                    # self.table_show.setModel(data_model)
                except Exception as err:
                    print(err)

from PyQt5.QtCore import Qt
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class WorkThread(QThread):
    trigger = pyqtSignal(str)

    def __int__(self):
        super(WorkThread, self).__init__()

    def set_func(self,func):
        self.func=func

    def run(self):

        try:
            self.trigger.emit("start")
            QtCore.QCoreApplication.processEvents()
            self.func()
            self.trigger.emit("end")
        except Exception as err:
            print('Error: ',err)
            self.trigger.emit("error:"+str(err))

def main():
    app = QApplication(sys.argv)

    current_path = os.path.dirname(__file__)
    print("current path = ",current_path)
    app_icon = QIcon(current_path+"/qtt.png")
    app.setWindowIcon(app_icon)

    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()