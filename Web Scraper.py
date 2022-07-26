
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
        widget.setFixedSize(1523, 796)
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

            self.clearTabs()

            keywords = self.ScrapeLineEdit.text().split(',')
            pages = self.ScraperSpinBox.value()
            time = self.ScrapeDropDownMenu.currentText()

            self.progressBar.setRange(0,0)

            self.googleRun = searchEngineThread()

            self.googleRun.keywords = keywords
            self.googleRun.pages = pages
            self.googleRun.time = time
            self.googleRun.baseurl = baseUrlGoogle
            self.ThreadActive = True

            self.googleRun.start()

            self.googleRun.data.connect(self.scrapingFinshed)
            self.googleRun.ThreadActive.connect(self.posterPage)
            self.googleRun.ThreadActive.connect(self.posterPageAfter)



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

        for i in range(len(self.data)):
            self.Twitter = QLabel()
            self.Twitter.setPixmap(tPixmap)
            self.Twitter.setAlignment(Qt.AlignCenter)

            self.Linkedin = QLabel()
            self.Linkedin.setPixmap(lPixmap)
            self.Linkedin.setAlignment(Qt.AlignCenter)

            self.table.setItem(i, 0, QTableWidgetItem(self.data[i][0]))
            self.table.setItem(i, 1, QTableWidgetItem(self.data[i][1]))
            self.table.setItem(i, 2, QTableWidgetItem(self.data[i][2]))
            self.table.setItem(i, 3, QTableWidgetItem(self.data[i][3]))
            self.table.setCellWidget(i, 4, self.Twitter)
            self.table.setCellWidget(i, 5, self.Linkedin)

        self.table.resizeColumnsToContents()
        return self.table

    def posterPage(self):
        self.progressBar.hide()
        widget.setFixedSize(1523, 796)
        widget.setCurrentIndex(widget.currentIndex() + 1)



    def clearTabs(self):
        self.poster = widget.widget(widget.currentIndex() + 1)
        self.tab = self.poster.findChild(QTabWidget, "PosterTab")

        totalTabs = self.tab.count()

        for i in range(totalTabs):
            self.tab.removeTab(0)

    def posterPageAfter(self):

        self.poster = widget.widget(widget.currentIndex())
        self.tab = self.poster.findChild(QTabWidget, "PosterTab")

        for i in range(self.tab.count()):
            self.tab.widget(i).cellClicked.connect(self.currentColumn)


    def currentColumn(self,row,column):
        title = self.tab.widget(self.tab.currentIndex()).item(row, headers.index("Title")).text()
        description = self.tab.widget(self.tab.currentIndex()).item(row, headers.index("Description")).text()
        link = self.tab.widget(self.tab.currentIndex()).item(row, headers.index("Link")).text()

        if column == headers.index("Twitter"):
            self.Twitter = TwitterPosterWindow()
            self.Twitter.PosterTwitter.setPlainText(f"{title}\n\n{link}")
            self.Twitter.show()

        if column == headers.index("Linkedin"):
            self.Linkedin = LinkedinPosterWindow()
            self.Linkedin.PosterLinkedin.setPlainText(f"{title}\n\n{description}\n\n{link}")
            self.Linkedin.show()


class PosterWindow(QDialog):
    def __init__(self):
        super(PosterWindow, self).__init__()
        loadUi('Windows/PosterMainWindow.ui',self)

        self.PosterBackArrowLabel.setPixmap(QPixmap('Images/left-arrow.png'))

        self.PosterBackArrowLabel.mousePressEvent = self.mainPage


    def mainPage(self, event):
        self.event = widget.setFixedSize(500, 800)
        self.event = widget.setCurrentIndex(widget.currentIndex() - 2)


class TwitterPosterWindow(QDialog):
    def __init__(self):
        super(TwitterPosterWindow, self).__init__()
        loadUi('Windows/TwitterPoster.ui',self)

        self.DateTimeEditTwiter.hide()

        self.QueueTwitterRadioButton.toggled.connect(self.dateTimeCheckTwitt)

        self.PosterTwitter.textChanged.connect(self.characterCounter)

    def dateTimeCheckTwitt(self,enabled):
        if enabled:
            self.DateTimeEditTwiter.show()
        else:
            self.DateTimeEditTwiter.hide()

    def characterCounter(self):
        characters = len(self.PosterTwitter.toPlainText())
        self.TwitterCharacterCounter.setText(f"{characters}/288")


class LinkedinPosterWindow(QDialog):
    def __init__(self):
        super(LinkedinPosterWindow, self).__init__()
        loadUi('Windows/LinkedinPoster.ui', self)

        self.DateTimeEditLinkedin.hide()

        self.QueueLinkedinRadioButton.toggled.connect(self.dateTimecheckLink)

    def dateTimecheckLink(self, enabled):
        if enabled:
            self.DateTimeEditLinkedin.show()
        else:
            self.DateTimeEditLinkedin.hide()

class searchEngineThread(QThread):

    keywords = pyqtSignal(list)
    pages = pyqtSignal(str)
    time = pyqtSignal(str)
    baseurl = pyqtSignal(str)
    data = pyqtSignal(list, str)
    ThreadActive = pyqtSignal(bool)



    def run(self):
        for keyword in self.keywords:
            googleSE = Google(self.time, keyword, self.pages, self.baseurl)
            googleSE = googleSE.Start()
            self.data.emit(googleSE, keyword)
        self.ThreadActive.emit(False)


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

try:
    sys.exit(app.exec())
except:
    print("exit")