from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from TitleTableView.TitleTable import TitleTableWindow
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from startupView.startup import startupWindow
from articleContentView.articleContent import articleContentWindow
import WHO.WHOMAIN
from BBC.BBC_Main import BBCWindow
from VirusCrawler.VirusCrawlerUImod import Flight


class ViewController:
    def __init__(self):
        self.bbc = BBCWindow()
        self.bbc.goBackToStartupSignal.connect(self.loadStartup)

    def loadBBC(self):
        self.bbc.update()
        self.bbc.show()

    def loadArticleContent(self,dictory):
        self.articleContentWindow= articleContentWindow()
        self.articleContentWindow.goBackToTitleTableSignal.connect(self.loadTitleTable)
        self.articleContentWindow.show()
        self.articleContentWindow.label_title.setText(dictory['article_title'])
        #self.articleContentWindow.label_good.setText(dictory['good'])
        self.articleContentWindow.label_boo.setText(str(dictory['boo']))
        self.articleContentWindow.label_date.setText(dictory['date'])
        url='<a href=\"'+dictory['url'] + '\"> ' + dictory['url'] + '</a>'
        print(url)
        self.articleContentWindow.label_url.setText(url)
        self.articleContentWindow.label_url.linkActivated.connect(self.link)
        #self.articleContentWindow.label_url .setText('<a href="http://stackoverflow.com/">Stackoverflow/</a>')
        self.articleContentWindow.label_author.setText(dictory['author'])
        self.articleContentWindow.textBrowser.setHtml(dictory['content'])


    def link(self, linkStr):
        QDesktopServices.openUrl(QUrl(linkStr))
    def loadTitleTable(self):
        self.TitleTableWindow=TitleTableWindow()

        self.TitleTableWindow.goBackToStartupSignal.connect(self.loadStartup)
        self.TitleTableWindow.callArticleContent.connect(self.loadArticleContent)
        self.TitleTableWindow.show()
    def loadStartup(self):
        self.startupWindow=startupWindow()
        self.startupWindow.goToTitleTableSignal.connect(self.loadTitleTable)
        self.startupWindow.goToWHO.connect(self.loadWHO)
        self.startupWindow.goToTitleTableSignalFromBBC.connect(self.loadBBC)
        self.startupWindow.goToFlightInfoSignal.connect(self.loadFlightInfo)
        self.bbc.processRun()
        self.startupWindow.show()

    def loadWHO(self):
        self.WHOWindow=WHO.WHOMAIN.MainWindow()
        self.WHOWindow.goBackToStartupSignal.connect(self.loadStartup)
        self.WHOWindow.show()
    def loadFlightInfo(self):
        self.flightWindow=Flight()
        self.flightWindow.goBackToStartupSignal.connect(self.loadStartup)
        self.flightWindow.show()
    '''
    def addMenu(self):
        self.menuUI=startupView.testUI.Ui_MainWindow()
        self.menuUI.setupUi(self.articleContentWindow)
    '''



if __name__ == '__main__':
    def myExitHandler():
        print("Close BBC WebCrawl")
        import multiprocessing
        for t in multiprocessing.active_children():
            t.terminate()
#            t.close()

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(myExitHandler)
    view = ViewController()
    view.loadStartup()
    sys.exit(app.exec_())

