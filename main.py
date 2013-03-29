import time
import shutil
import os
import tempfile
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui_main import Ui_MainWindow
from lib.identicon import identicon
from lib.commandstack.commandstack import CommandStack

MAX_HISTORY = 10
class MainWindow(QMainWindow, Ui_MainWindow):
    anim = pyqtSignal()

    def __init__(self, parent = None):

        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.scene_icon = QGraphicsScene()
        self.probar.hide()
        #self.gv_canvas.setBackgroundBrush(QBrush(QColor("#fdf6e3"), Qt.SolidPattern))
        gradient = QRadialGradient(0,0, 600, 0,0)
        gradient.setColorAt(0, QColor("#00aaaa"))
        gradient.setColorAt(1, QColor("#eeeeee"))
        self.gv_canvas.setBackgroundBrush(QBrush(gradient))
        self.history = CommandStack(MAX_HISTORY)
        self.icon_path = os.path.join(tempfile.gettempdir(), "icon.png")
        self.canvas_path = os.path.join(tempfile.gettempdir(), "canvas.png")
        self.tb_collection.setColumnCount(1)
        self.load_collection(init=True)
        self.generate_icon()


    def generate_icon(self, code=0, hist=False, ui=True):
        self.code = identicon.generate_icon(code)

        if not code or hist: # add history only if code = 0
            self.update_hist()
        if ui:
            self.update_ui()

    def update_hist(self):
        self.history.add_item(self.code)

    def update_ui(self):
        self.make_label()
        self.pix = QPixmap(self.icon_path)
        self.scene_icon.clear()
        self.scene_icon.addPixmap(self.pix)
        self.gv_icon.setScene(self.scene_icon)
        self.statusbar.clearMessage()
        self.animation()

    def animation(self):
        """
        OutElastic: Quick tiled;
        InOutElastic: centered then tiled;"""

        mode = 10
        count = mode * mode

        scene = QGraphicsScene(-350, -350, 700, 700)
        items = []
        for i in range(count):
            item = Pixmap(self.pix)
            item.pixmap_item.setOffset(-self.pix.width() / 2, -self.pix.height() / 2)
            item.pixmap_item.setZValue(i)
            items.append(item)
            scene.addItem(item.pixmap_item)

        self.gv_canvas.setScene(scene)

        self.group = QParallelAnimationGroup()
        for i, item in enumerate(items):
            anim = QPropertyAnimation(item, "pos")
            anim.setStartValue(QPointF(-self.pix.width()/2, -self.pix.height()/2))
            anim.setEndValue(QPointF(((i%mode)-mode/2)*self.pix.width() + self.pix.width()/2,
                    ((i//mode)-mode/2)*self.pix.height() + self.pix.height()/2))
            anim.setDuration(750+i*25)
            #anim.setDuration(1500)
            anim.setEasingCurve(QEasingCurve.InOutBack)
            self.group.addAnimation(anim)
        self.group.start()

    def make_label(self):
        label_list = []
        for item in self.history.item_list:
            if self.code == item:
                item = "<font color='blue'>%s</font>" % self.code
            else:
                item = str(item)
            label_list.append(item)
        count = MAX_HISTORY - len(label_list)
        label_list.append("<br/>" * count)
        self.lb_icon.setText("<br/>".join(label_list))

    def generate_icon_in_history_backward(self):
        self.history.move_cursor_backward()
        self.generate_icon(code=self.history.get_item())

    def generate_icon_in_history_forward(self):
        self.history.move_cursor_forward()
        self.generate_icon(code=self.history.get_item())

    def export_file(self, file_type="jpg"):

        if not os.path.exists(file_type):
            os.mkdir(file_type)

        timestamp = time.strftime("%Y_%m_%d")
        dst_name = "%s-%s.%s" % (timestamp, self.code, file_type)
        dst_path = os.path.join(file_type, dst_name)
        tmp_name = "export.%s" % file_type
        tmp_path = os.path.join(tempfile.gettempdir(), tmp_name)

        shutil.copyfile(tmp_path, dst_path)
        self.statusbar.showMessage("Save %s file to %s" % (file_type, dst_path))

        old_code = self.code #since load_collection will change self.code
        self.tb_collection.setCurrentCell(0,0)
        self.load_collection()
        self.generate_icon(code=old_code)

    def parse_code(self, filename):
        return filename.rpartition("-")[2].partition(".")[0]

    def load_collection(self,init=False):

        #if init:
            #self.show()
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

    def on_tb_collection_itemClicked(self):
        self.generate_icon(
                code=self.parse_code(str(self.tb_collection.currentItem().text())),
                hist=True)


    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_J:
            if self.history.cursor >= len(self.history.item_list) - 1:
                self.generate_icon()
            else:
                self.generate_icon_in_history_forward()
        if key == Qt.Key_K:
            self.generate_icon_in_history_backward()
        if key == Qt.Key_Q:
            self.close()
        if key == Qt.Key_E:
            self.export_file("eps")
        if key == Qt.Key_S:
            self.export_file("jpg")
        if key == Qt.Key_R:
            self.animation()

        if key == Qt.Key_Delete:
            if self.tb_collection.currentItem():
                self.generate_icon_in_history_backward()
                file_path = os.path.join(
                        os.getcwd(),
                        "jpg",
                        str(self.tb_collection.currentItem().text()))
                os.remove(file_path)
                self.load_collection()

        QMainWindow.keyPressEvent(self, event)

    def update_probar(self, val):
        if self.probar.isHidden():
            self.statusbar.showMessage("Loading collection...")
            self.probar.show()
        self.probar.setValue(val)

    def finish_probar(self):
        self.statusbar.clearMessage()
        self.probar.hide()

class Load_Collection(QThread):
    partDone = pyqtSignal(int)
    procDone = pyqtSignal(bool)

    def __init__(self,main_window, parent=None):
        super(Load_Collection, self).__init__(parent)
        self.stopped = False
        self.completed = False
        self.main_window = main_window

    def stop(self):
        self.stopped = False

    def run(self):
        self.process()
        self.stop()

    def process(self):

        collection_folder = "jpg"
        if not os.path.exists(collection_folder):
            os.mkdir(collection_folder)

        self.main_window.setEnabled(False)
        collection_path = os.path.join(os.getcwd(), collection_folder)
        file_list = sorted(os.listdir(collection_path),
                key=lambda f: os.path.getmtime(os.path.join(collection_path,f)),
                reverse=True)

        hash_list = []
        count = len(file_list)
        self.main_window.tb_collection.setRowCount(count)
        self.main_window.tb_collection.clear()
        for i,item in enumerate(file_list):
            self.partDone.emit(i*100/count)

            table_item = QTableWidgetItem(0)
            hash_code = self.main_window.parse_code(item)
            self.main_window.generate_icon(code=hash_code, ui=False)
            table_item.setIcon(QIcon(QPixmap(self.main_window.icon_path)))
            table_item.setText(item)
            self.main_window.tb_collection.setItem(i,0,table_item)

        self.procDone.emit(True)
        self.main_window.setEnabled(True)

class Pixmap(QObject):

    def __init__(self, pix):
        super(Pixmap, self).__init__()

        self.pixmap_item = QGraphicsPixmapItem(pix)
        self.pixmap_item.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

    def _set_pos(self, pos):
        self.pixmap_item.setPos(pos)

    pos = pyqtProperty(QPointF, fset=_set_pos)

class Play_Anim(QThread):

    def __init__(self,main_window, parent=None):
        super(Play_Anim, self).__init__(parent)
        self.stopped = False
        self.completed = False
        self.main_window = main_window

    def stop(self):
        self.stopped = False

    def run(self):
        self.process()
        self.stop()

    def process(self):
        self.main_window.anim.emit()

if __name__ == "__main__":

    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showFullScreen()
    sys.exit(app.exec_())
