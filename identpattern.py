
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui_main import Ui_MainWindow
from lib.identicon import identicon
from lib.commandstack.commandstack import CommandStack

MAX_HISTORY = 10
class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):

        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        #self.icon_count = 3
        self.history = CommandStack(MAX_HISTORY)
        self.generate_icon()

    def generate_icon(self):
        """generate icon and add hash code to history"""

        self.generate_icon_by_code(0)
        #self.history.add_item(self.hashcode)

    def generate_icon_by_code(self, code):
        self.hashcode = identicon.generate_icon(code)
        if not code:
            self.history.add_item(self.hashcode)
        self.update_view()

    def update_view(self):
        self.make_label()
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap("icon.png"))
        self.gv_icon.setScene(scene)
        scene.addPixmap(QPixmap("canvas.png"))
        self.gv_canvas.setScene(scene)
        #self.graphicsView.show()

    def make_label(self):
        label_list = []
        for item in self.history.item_list:
            if self.hashcode == item:
                item = "<font color='blue'>%s</font>" % self.hashcode
            else:
                item = str(item)
            label_list.append(item)
        self.lb_icon.setText("<br/>".join(label_list))

    def generate_icon_in_history_backward(self):
        self.history.move_cursor_backward()

        self.generate_icon_by_code(self.history.get_item())

    def generate_icon_in_history_forward(self):
        self.history.move_cursor_forward()
        self.generate_icon_by_code(self.history.get_item())

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_J:
            if self.history.cursor == len(self.history.item_list) - 1:
                self.generate_icon()
            else:
                self.generate_icon_in_history_forward()
        if key == Qt.Key_K:
            self.generate_icon_in_history_backward()
        if key == Qt.Key_Q:
            self.close()
        if key == Qt.Key_S:
            pass

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

