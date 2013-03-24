import time
import shutil
import os.path
import tempfile
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
        self.probar.hide()

        self.history = CommandStack(MAX_HISTORY)
        self.icon_path = os.path.join(tempfile.gettempdir(), "icon.png")
        self.canvas_path = os.path.join(tempfile.gettempdir(), "canvas.png")
        self.tb_collection.setColumnCount(1)
        self.load_collection(init=True)
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
        scene_icon.addPixmap(QPixmap(self.icon_path))
        self.gv_icon.setScene(scene_icon)
        scene_canvas = QGraphicsScene()
        scene_canvas.addPixmap(QPixmap(self.canvas_path))
        self.gv_canvas.setScene(scene_canvas)
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

    def export_file(self, file_type="jpg"):

        if not os.path.exists(file_type):
            os.mkdir(file_type)

        timestamp = time.strftime("%Y_%m_%d")
        dst_name = "%s-%s.%s" % (timestamp, self.hashcode, file_type)
        dst_path = os.path.join(file_type, dst_name)
        tmp_name = "export.%s" % file_type
        tmp_path = os.path.join(tempfile.gettempdir(), tmp_name)

        shutil.copyfile(tmp_path, dst_path)
        self.statusbar.showMessage("Save %s file to %s" % (file_type, dst_path))

    def load_collection(self,init=False):

        if init:
            self.show()
        self.thread = Load_Collection(self)
        self.thread.partDone.connect(self.update_probar)
        self.thread.procDone.connect(self.finish_probar)
        self.thread.run()

    def update_bar(self,val):
        if self.probar.isHidden():
            self.probar.show()
        self.probar.setValue(val)

    def finish_bar(self):
        self.lb_probar.hide()
        self.probar.hide()


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
            self.export_file("eps")
        if key == Qt.Key_G:
            self.export_file("jpg")

        QMainWindow.keyPressEvent(self, event)



if __name__ == "__main__":

    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

