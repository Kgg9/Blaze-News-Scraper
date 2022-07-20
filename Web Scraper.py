
# Imports needed to make the project run
import sys
from SearchEngines.Google import Google
from Tools import GetCSV
import Images
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import*

baseUrlGoogle = "https://www.google.com/search?q=&source=lnms&tbm=nws"
headers = ["Title",
           "Description",
           "Publication Date (Relative To When Scraper Was Run)",
           "Link",
           "Twitter",
           "Linkedin",
           "Queue"
           ]

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('Windows/MainWindow.ui',self)
        self.MainWindowLogo.setPixmap(QPixmap('Images/blaze.png'))


        self.ScraperPushButton.clicked.connect(self.ScrapperPage)
        self.PosterPushButton.clicked.connect(self.PosterPage)

    def ScrapperPage(self):
        widget.setFixedSize(600,800)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def PosterPage(self):
        widget.setFixedSize(1500, 800)
        widget.setCurrentIndex(widget.currentIndex() + 2)


class ScraperMainWindow(QDialog):
    def __init__(self):
        super(ScraperMainWindow, self).__init__()
        loadUi('Windows/ScraperMainWindow.ui',self)



        self.BackArrowLabel.setPixmap(QPixmap('Images/left-arrow.png'))
        self.BackArrowLabel.mousePressEvent = self.mainPage

        self.ScraperErrorMessage.hide()

        self.progressBar.setTextVisible(False)
        self.progressBar.hide()

        self.ScrapePushButton.clicked.connect(self.scrapeButton)

    def mainPage(self, event):
        self.event = widget.setFixedSize(500, 800)
        self.event = widget.setCurrentIndex(widget.currentIndex() -1 )

    def scrapeButton(self):

        if (not self.ScrapeGoogleRadioButton.isChecked() or self.ScrapeLineEdit.text() == ''):
            self.ScraperErrorMessage.show()
        else:
            self.ScraperErrorMessage.hide()
            self.progressBar.show()


            keywords = self.ScrapeLineEdit.text().split(',')
            pages = self.ScraperSpinBox.value()
            time = self.ScrapeDropDownMenu.currentText()

            self.progressBar.setRange(0,0)

            self.googleRun = searchEngineThread()

            self.googleRun.keywords = keywords
            self.googleRun.pages = pages
            self.googleRun.time = time
            self.googleRun.baseurl = baseUrlGoogle

            self.googleRun.start()
            self.googleRun.finish.connect(self.scrapingFinshed)

    def scrapingFinshed(self, newsArticles, keyword):
        self.poster = widget.widget(widget.currentIndex()+1)
        self.tab = self.poster.findChild(QTabWidget,"PosterTab").addTab(self.tableMaker(newsArticles),keyword)

    def tableMaker(self, data):
        self.data = [tup for group in data for tup in group]
        self.table = QTableWidget()

        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(len(headers))

        self.table.setHorizontalHeaderLabels(headers)

        tPixmap = QPixmap("Images/twitter.png")
        lPixmap = QPixmap("Images/linkedin.png")
        cPixmap = QPixmap("Images/schedule.png")


        for i in range(len(self.data)):
            self.Twitter = QLabel()
            self.Twitter.setPixmap(tPixmap)
            self.Twitter.setAlignment(Qt.AlignCenter)

            self.Linkedin = QLabel()
            self.Linkedin.setPixmap(lPixmap)
            self.Linkedin.setAlignment(Qt.AlignCenter)

            self.Calender = QLabel()
            self.Calender.setPixmap(cPixmap)
            self.Calender.setAlignment(Qt.AlignCenter)

            self.table.setItem(i, 0, QTableWidgetItem(self.data[i][0]))
            self.table.setItem(i, 1, QTableWidgetItem(self.data[i][1]))
            self.table.setItem(i, 2, QTableWidgetItem(self.data[i][2]))
            self.table.setItem(i, 3, QTableWidgetItem(self.data[i][3]))
            self.table.setCellWidget(i, 4, self.Twitter)
            self.table.setCellWidget(i, 5, self.Linkedin)
            self.table.setCellWidget(i, 6, self.Calender)


        self.table.resizeColumnsToContents()
        return self.table





class PosterWindow(QDialog):
    def __init__(self):
        super(PosterWindow, self).__init__()
        loadUi('Windows/PosterMainWindow.ui',self)

        self.setFixedSize(self.width(),self.height())

        self.PosterBackArrowLabel.setPixmap(QPixmap('Images/left-arrow.png'))

        self.PosterBackArrowLabel.mousePressEvent = self.mainPage

    def mainPage(self, event):
        self.event = widget.setFixedSize(500, 800)
        self.event = widget.setCurrentIndex(widget.currentIndex() - 2)




class searchEngineThread(QThread):

    keywords = pyqtSignal(list)
    pages = pyqtSignal(str)
    time = pyqtSignal(str)
    baseurl = pyqtSignal(str)
    finish = pyqtSignal(list, str)

    def run(self):
        for keyword in self.keywords:
            googleSE = Google(self.time, keyword, self.pages, self.baseurl)
            googleSE = googleSE.Start()
            self.finish.emit(googleSE, keyword)















app = QApplication(sys.argv)

widget = QtWidgets.QStackedWidget()
mainWindow = MainWindow()
scraperWindow = ScraperMainWindow()
posterWindow = PosterWindow()
widget.addWidget(mainWindow)
widget.addWidget(scraperWindow)
widget.addWidget(posterWindow)
widget.setFixedSize(500,800)
widget.show()

#
# for keyword in keywords:
#     googleSE = Google(time,keyword,10,url)
#     GetCSV.get_CSV(googleSE.Start(),keyword,time)

try:
    sys.exit(app.exec())
except:
    print("exit")