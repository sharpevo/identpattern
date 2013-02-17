
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui_main import Ui_MainWindow
from lib import identicon


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):

        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        #self.icon_count = 3
        self.generate_icon()

    def generate_icon(self):
        #self.icon, self.canvas = identicon.generate_icon(self.icon_count)
        self.icon, self.canvas = identicon.generate_icon()
        self.update_view()

    def update_view(self):
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap("canvas.png"))
        self.graphicsView.setScene(scene)
        self.graphicsView.show()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_N:
            self.generate_icon()
        if key == Qt.Key_J:
            self.increase_icon()
            #self.icon.save("element.png", 'PNG')

        QMainWindow.keyPressEvent(self, event)



if __name__ == "__main__":


    #app = QApplication(sys.argv)

    #grview = QGraphicsView()
    #scene = QGraphicsScene()


    #app = QApplication(sys.argv)
    #main_window = MainWindow()

    #scene.addPixmap(QPixmap('pic.jpg'))
    #grview.setScene(scene)

    #grview.show()

    #sys.exit(app.exec_())
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

