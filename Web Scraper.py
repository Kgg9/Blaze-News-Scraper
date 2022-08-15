# Imports needed to make the project run
import sys
from SearchEngines.Google import Google
from Tools.LinkedinAccountPost import LinkedinAccountPoster
from Tools.TwitterAccountPost import TwitterAccountPost
import Images
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import*
from apscheduler.schedulers.background import BackgroundScheduler
from tzlocal import get_localzone



baseUrlGoogle = "https://www.google.com/search?q=&source=lnms&tbm=nws"

headers = ["Title",
           "Description",
           "Publication Date (Relative To When Scraper Was Run)",
           "Link",
           "Twitter",
           "Linkedin",
           ]

queuedHeaders = ["Title",
                 "Platform",
                 "Date",
                 "Time",
                 "Cancel"]

newsArtcilesLoction = []
queuedArticles = []

linkedinLogin = ['Silverfrost8@gmail.com','AwAw!234','https://www.linkedin.com/company/35598172/admin/']
twitterLogin = ['Kartikeyg910','AwAw!@#$']

sched = BackgroundScheduler(timezone = get_localzone())
sched.start()

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('Windows/MainWindow.ui',self)
        self.MainWindowLogo.setPixmap(QPixmap('Images/blaze.png'))


        self.ScraperPushButton.clicked.connect(self.ScrapperPage)
        self.PosterPushButton.clicked.connect(self.PosterPage)
        self.AccountsPushButton.clicked.connect(self.AccountsPage)
        self.QueuedPushButton.clicked.connect(self.QueuedPage)


    def ScrapperPage(self):
        widget.setFixedSize(scraperWidth,scraperHeight)
        widget.setCurrentIndex(widget.indexOf(scraperWindow))

    def PosterPage(self):
        widget.setFixedSize(posterWidth,posterHeight)
        widget.setCurrentIndex(widget.indexOf(posterWindow))

    def QueuedPage(self):
        widget.setFixedSize(queuedWidth,queuedHeight)
        widget.setCurrentIndex(widget.indexOf(queued))

    def AccountsPage(self):
        widget.setFixedSize(accountsWidth,accountsHeight)
        widget.setCurrentIndex(widget.indexOf(accounts))
        widget.findChild(QPushButton,'AccountsErrorMessage').hide()

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
        self.event = widget.setFixedSize(mainWidth,mainHeight)
        self.event = widget.setCurrentIndex(widget.indexOf(mainWindow))

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
        self.poster = widget.widget(widget.indexOf(posterWindow))
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
        widget.setFixedSize(posterWidth, posterHeight)
        widget.setCurrentIndex(widget.indexOf(posterWindow))


    def clearTabs(self):
        self.poster = widget.widget(widget.indexOf(posterWindow))
        self.tab = self.poster.findChild(QTabWidget, "PosterTab")

        totalTabs = self.tab.count()

        for i in range(totalTabs):
            self.tab.removeTab(0)

    def posterPageAfter(self):

        self.poster = widget.widget(widget.indexOf(posterWindow))
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
        self.event = widget.setFixedSize(mainWidth,mainHeight)
        self.event = widget.setCurrentIndex(widget.indexOf(mainWindow))


class Queued(QDialog):
    def __init__(self):
        super(Queued, self).__init__()
        loadUi("Windows/QueueWindow.ui",self)

        self.QueueBackArrowLabel.setPixmap(QPixmap('Images/left-arrow.png'))

        self.QueueBackArrowLabel.mousePressEvent = self.mainPage

        self.QueuedTableWidget.setColumnCount(len(queuedHeaders))
        self.QueuedTableWidget.setHorizontalHeaderLabels(queuedHeaders)

        self.QueuedTableWidget.cellClicked.connect(self.queueCancel)

    def queueCancel(self,row,column):
        item = self.QueuedTableWidget.cellWidget(row,column)
        color = item.palette().color(QtGui.QPalette.Background).name()

        if column == queuedHeaders.index("Cancel") and color!='#a8a8a8':

            title = self.QueuedTableWidget.item(row,queuedHeaders.index("Title")).text()
            platform = self.QueuedTableWidget.item(row,queuedHeaders.index("Platform")).text()
            date = self.QueuedTableWidget.item(row,queuedHeaders.index("Date")).text()
            time = self.QueuedTableWidget.item(row,queuedHeaders.index("Time")).text()

            jobId = queuedArticles.index((title,row,date,time,platform))

            print(queuedArticles)

            sched.remove_job(str(jobId))

            self.QueuedTableWidget.hideRow(row)




    def mainPage(self, event):
        self.event = widget.setFixedSize(mainWidth, mainHeight)
        self.event = widget.setCurrentIndex(widget.indexOf(mainWindow))

class Accounts(QDialog):
    def __init__(self):
        super(Accounts, self).__init__()
        loadUi('Windows/Accounts.ui',self)

        self.AccountsBackArrowLabel.setPixmap(QPixmap('Images/left-arrow.png'))
        self.AccountsBackArrowLabel.mousePressEvent = self.mainPage

        self.LinkedinSaveButton.clicked.connect(self.linkAccountInfo)
        self.TwitterSaveButton.clicked.connect(self.tweetAccountInfo)

    def mainPage(self,event):
        self.event = widget.setFixedSize(mainWidth,mainHeight)
        self.event = widget.setCurrentIndex(widget.indexOf(mainWindow))

    def linkAccountInfo(self):
        self.AccountsErrorMessage.hide()

        linkedinLogin.clear()

        linkedinLogin.append(self.LinkedinUsernameBox.text())
        linkedinLogin.append(self.LinkedinPasswordBox.text())
        linkedinLogin.append(self.LinkedinCompanyUrlBox.text())

        if "" in linkedinLogin:
            self.AccountsErrorMessage.show()

    def tweetAccountInfo(self):
        self.AccountsErrorMessage.hide()

        twitterLogin.clear()

        twitterLogin.append(self.TwitterUsernameBox.text())
        twitterLogin.append(self.TwitterPasswordBox.text())

        if "" in twitterLogin:
            self.AccountsErrorMessage.show()


class TwitterPosterWindow(QDialog):
    def __init__(self):
        super(TwitterPosterWindow, self).__init__()
        loadUi('Windows/TwitterPoster.ui',self)

        self.DateTimeEditTwiter.setMinimumDateTime(QDateTime.currentDateTime())

        self.DateTimeEditTwiter.hide()

        self.QueueTwitterRadioButton.toggled.connect(self.dateTimeCheckTwitt)

        self.PosterTwitter.textChanged.connect(self.characterCounter)

        self.TwitterPosterButton.clicked.connect(self.postTwitter)


    def dateTimeCheckTwitt(self,enabled):
        if enabled:
            self.DateTimeEditTwiter.show()
        else:
            self.DateTimeEditTwiter.hide()

    def characterCounter(self):
        characters = len(self.PosterTwitter.toPlainText())
        self.TwitterCharacterCounter.setText(f"{characters}/288")

    def postTwitter(self):

        self.poster = widget.widget(widget.indexOf(posterWindow))
        self.tab = self.poster.findChild(QTabWidget, "PosterTab")

        currentTab = self.tab.currentIndex()
        currentRow = self.tab.widget(currentTab).currentRow()

        title = self.tab.widget(currentTab).item(currentRow, 0).text()

        newsArtcilesLoction.append((title, currentTab, currentRow))

        if self.QueueTwitterRadioButton.isChecked():
            queuedTableMaker(self,"Twitter")
        else:
            self.twitterPostRun = TwitterPosterMech(self.PosterTwitter.toPlainText())
            self.twitterPostRun.start()
            self.twitterPostRun.finished.connect(lambda: self.tweetPostRunAfter(title))


    def tweetPostRunAfter(self,title):
        self.poster = widget.widget(widget.indexOf(posterWindow))
        self.tab = self.poster.findChild(QTabWidget, "PosterTab")

        qDate = self.DateTimeEditTwiter.dateTime().toString("yyyy-MM-dd")
        qTime = self.DateTimeEditTwiter.dateTime().toString("hh:mm:00 ap")

        currentTab = [tups[1] for tups in newsArtcilesLoction if tups[0]==title]
        currentRow = [tups[2] for tups in newsArtcilesLoction if tups[0]==title]

        for tuple in queuedArticles:
            if (tuple[0] == title and tuple[2] == qDate and tuple[3] == qTime and tuple[4]=="Twitter"):

                self.queued = widget.widget(widget.indexOf(queued))
                self.qTable = self.queued.findChild(QTableWidget, "QueuedTableWidget")

                for i in range(len(queuedHeaders)-1):
                    self.qTable.item(tuple[1],i).setBackground(QColor("#bbeebb"))

                self.qTable.cellWidget(tuple[1], queuedHeaders.index("Cancel")).setStyleSheet(
                    "background-color:#A8A8A8")


        for i in range(len(headers) - 2):
            self.tab.widget(currentTab[0]).item(currentRow[0], i).setBackground(QColor("Yellow"))

        self.tab.widget(currentTab[0]).cellWidget(currentRow[0], headers.index("Twitter")).setStyleSheet(
            "background-color:Yellow")

        # self.close()

    def twitterCompRun(self,title):
        self.twitterPostRun = TwitterPosterMech(self.PosterTwitter.toPlainText())
        self.twitterPostRun.start()
        self.tweetPostRunAfter(title)


class LinkedinPosterWindow(QDialog):
    def __init__(self):
        super(LinkedinPosterWindow, self).__init__()
        loadUi('Windows/LinkedinPoster.ui', self)

        self.DateTimeEditLinkedin.setMinimumDateTime(QDateTime.currentDateTime())
        self.DateTimeEditLinkedin.hide()

        self.QueueLinkedinRadioButton.toggled.connect(self.dateTimecheckLink)
        self.LinkedinPosterButton.clicked.connect(self.postLinkedin)

    def dateTimecheckLink(self, enabled):
        if enabled:
            self.DateTimeEditLinkedin.show()
        else:
            self.DateTimeEditLinkedin.hide()

    def postLinkedin(self):

        self.poster = widget.widget(widget.indexOf(posterWindow))
        self.tab = self.poster.findChild(QTabWidget, "PosterTab")

        currentTab = self.tab.currentIndex()
        currentRow = self.tab.widget(currentTab).currentRow()

        title = self.tab.widget(currentTab).item(currentRow, 0).text()

        newsArtcilesLoction.append((title, currentTab, currentRow))

        if self.QueueLinkedinRadioButton.isChecked():
           queuedTableMaker(self,"Linkedin")
        else:
            self.linkPostRun = LinkedinPosterMech(self.PosterLinkedin.toPlainText())

            self.linkPostRun.start()
            self.linkPostRun.finished.connect(lambda: self.linkPostRunAfter(title))

    def linkPostRunAfter(self,title):
        self.poster = widget.widget(widget.indexOf(posterWindow))
        self.tab = self.poster.findChild(QTabWidget, "PosterTab")

        qDate = self.DateTimeEditLinkedin.dateTime().toString("yyyy-MM-dd")
        qTime = self.DateTimeEditLinkedin.dateTime().toString("hh:mm:00 ap")

        currentTab = [tups[1] for tups in newsArtcilesLoction if tups[0] == title]
        currentRow = [tups[2] for tups in newsArtcilesLoction if tups[0] == title]

        for tuple in queuedArticles:
            if (tuple[0] == title and tuple[2] == qDate and tuple[3] == qTime and tuple[4] == "Linkedin"):

                self.queued = widget.widget(widget.indexOf(queued))
                self.qTable = self.queued.findChild(QTableWidget, "QueuedTableWidget")

                for i in range(len(queuedHeaders) - 1):
                    self.qTable.item(tuple[1], i).setBackground(QColor("#bbeebb"))

                self.qTable.cellWidget(tuple[1], queuedHeaders.index("Cancel")).setStyleSheet(
                    "background-color:#A8A8A8")

        for i in range(len(headers) - 2):
            self.tab.widget(currentTab[0]).item(currentRow[0], i).setBackground(QColor("Yellow"))

        self.tab.widget(currentTab[0]).cellWidget(currentRow[0], headers.index("Linkedin")).setStyleSheet(
            "background-color:Yellow")

        # self.close()

    def linkedinCompRun(self,title):
        self.linkPostRun = LinkedinPosterMech(self.PosterLinkedin.toPlainText())

        self.linkPostRun.start()
        self.linkPostRunAfter(title)


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

class LinkedinPosterMech(QThread):

    def __init__(self,textData):
        super().__init__()

        self.username = linkedinLogin[0]
        self.password = linkedinLogin[1]
        self.companyUrl = linkedinLogin[2]
        self.textData = textData

    def run(self):
        linkPost = LinkedinAccountPoster(self.username,self.password,self.companyUrl,self.textData)
        linkPost.linkedinRun()

class TwitterPosterMech(QThread):
    def __init__(self, textData):
        super().__init__()

        self.username = twitterLogin[0]
        self.password = twitterLogin[1]
        self.textData = textData

    def run(self):
        tweetPost = TwitterAccountPost(self.username,self.password,self.textData)
        tweetPost.postTweet()

def queuedTableMaker(self, type):
    self.datetime24,qDate,qTime,title,run = "","","","",""

    if type=='Twitter':
        self.dateTime24 = self.DateTimeEditTwiter.dateTime().toPyDateTime()

        qDate = self.DateTimeEditTwiter.dateTime().toString("yyyy-MM-dd")
        qTime = self.DateTimeEditTwiter.dateTime().toString("hh:mm:00 ap")


        title = self.PosterTwitter.toPlainText()
        title = title.split('\n')[0]

        run = self.twitterCompRun

    if type == "Linkedin":
        self.dateTime24 = self.DateTimeEditLinkedin.dateTime().toPyDateTime()

        qDate = self.DateTimeEditLinkedin.dateTime().toString("yyyy-MM-dd")
        qTime = self.DateTimeEditLinkedin.dateTime().toString("hh:mm:00 ap")

        title = self.PosterLinkedin.toPlainText()
        title = title.split('\n')[0]

        run = self.linkedinCompRun

    self.queued = widget.widget(widget.indexOf(queued))
    self.qTable = self.queued.findChild(QTableWidget, "QueuedTableWidget")

    rowPosition = self.qTable.rowCount()
    queuedArticles.append((title, rowPosition, qDate, qTime,type))

    sched.add_job(run, 'date', args=[title],misfire_grace_time=60, run_date=self.dateTime24, id=str(queuedArticles.index((title, rowPosition, qDate, qTime,type))))

    changePixmap = QPixmap("Images/schedule.png")
    change = QLabel()
    change.setPixmap(changePixmap)
    change.setAlignment(Qt.AlignCenter)

    cancelPixmap = QPixmap("Images/cancel.png")
    cancel = QLabel()
    cancel.setPixmap(cancelPixmap)
    cancel.setAlignment(Qt.AlignCenter)

    self.qTable.insertRow(rowPosition)

    self.qTable.setItem(rowPosition, 0, QTableWidgetItem(title))
    self.qTable.setItem(rowPosition, 1, QTableWidgetItem(type))
    self.qTable.setItem(rowPosition, 2, QTableWidgetItem(qDate))
    self.qTable.setItem(rowPosition, 3, QTableWidgetItem(qTime))
    self.qTable.setCellWidget(rowPosition, 4, cancel)

    self.qTable.resizeColumnsToContents()


app = QApplication(sys.argv)

widget = QtWidgets.QStackedWidget()

mainWindow = MainWindow()
scraperWindow = ScraperMainWindow()
posterWindow = PosterWindow()
accounts = Accounts()
queued = Queued()

widget.addWidget(mainWindow)
widget.addWidget(scraperWindow)
widget.addWidget(posterWindow)
widget.addWidget(queued)
widget.addWidget(accounts)


mainWidth = mainWindow.width()
mainHeight = mainWindow.height()

scraperWidth = scraperWindow.width()
scraperHeight = scraperWindow.height()

posterWidth = posterWindow.width()
posterHeight = posterWindow.height()

accountsWidth = accounts.width()
accountsHeight = accounts.height()

queuedWidth = queued.width()
queuedHeight = queued.height()

widget.setFixedSize(mainWidth,mainHeight)

widget.show()

try:
    sys.exit(app.exec())
except:
    print("exit")