import time
import shutil
import os.path
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
        scene_icon = QGraphicsScene()
        scene_icon.addPixmap(QPixmap("icon.png"))
        self.gv_icon.setScene(scene_icon)
        scene_canvas = QGraphicsScene()
        scene_canvas.addPixmap(QPixmap("canvas.png"))
        self.gv_canvas.setScene(scene_canvas)
        #self.graphicsView.show()
        self.statusbar.clearMessage()

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

    def export_EPS(self):
        output_folder = "EPS"
        timestamp = time.strftime("%Y_%m_%d")
        eps_file = "%s-%s.eps" % (timestamp, self.hashcode)
        eps_path = os.path.join(output_folder, eps_file)
        shutil.copyfile("export.eps", eps_path)
        self.statusbar.showMessage("Save EPS file to %s" % eps_file)

    def export_JPG(self):
        output_folder = "JPG"
        timestamp = time.strftime("%Y_%m_%d")
        jpg_file = "%s-%s.jpg" % (timestamp, self.hashcode)
        jpg_path = os.path.join(output_folder, jpg_file)
        shutil.copyfile("export.jpg", jpg_path)
        self.statusbar.showMessage("Save JPEG file to %s" % jpg_path)


    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_J:
            #print self.history.cursor, len(self.history.item_list) - 1
            if self.history.cursor >= len(self.history.item_list) - 1:
                self.generate_icon()
            else:
                self.generate_icon_in_history_forward()
        if key == Qt.Key_K:
            self.generate_icon_in_history_backward()
        if key == Qt.Key_Q:
            self.close()
        if key == Qt.Key_S:
            self.export_EPS()
        if key == Qt.Key_G:
            self.export_JPG()

        QMainWindow.keyPressEvent(self, event)



if __name__ == "__main__":

    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

