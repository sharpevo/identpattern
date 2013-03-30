import time
import shutil
import os
import tempfile
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#from ui_main import Ui_MainWindow
from lib.identicon import identicon
from lib.commandstack.commandstack import CommandStack

MAX_HISTORY = 10
class MainWindow(QGraphicsView):#QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):

        QMainWindow.__init__(self, parent)
        #self.setupUi(self)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        desktop = QApplication.desktop()
        screen_size = desktop.availableGeometry()
        self.screen_height = screen_size.height()

        self.scene_canvas = QGraphicsScene(-screen_size.width()/2,
                -screen_size.height()/2,
                screen_size.width(),
                screen_size.height())
        self.setScene(self.scene_canvas)

        gradient = QRadialGradient(0,0, screen_size.width()/2, 0,0)
        gradient.setColorAt(0, QColor("#00aaaa"))
        gradient.setColorAt(1, QColor("#eeeeee"))
        self.setBackgroundBrush(QBrush(gradient))
        self.history = CommandStack(MAX_HISTORY)
        self.icon_path = os.path.join(tempfile.gettempdir(), "icon.png")
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
        self.pix = QPixmap(self.icon_path)
        self.animation()

    def animation(self):
        """
        OutElastic: Quick tiled;
        InOutElastic: centered then tiled;"""

        self.scene_canvas.clear()

        mode = self.screen_height//self.pix.height()+1


        #mode = 8
        count = mode * mode

        self.group = QParallelAnimationGroup()
        for i in range(count):
            item = Pixmap(self.pix)
            item.pixmap_item.setOffset(-self.pix.width() / 2, -self.pix.height() / 2)
            item.pixmap_item.setZValue(i)
            self.scene_canvas.addItem(item.pixmap_item)
            anim = QPropertyAnimation(item, "pos")
            anim.setStartValue(QPointF(-self.pix.width()/2, -self.pix.height()/2))
            anim.setEndValue(QPointF(((i%mode)-mode/2)*self.pix.width() + self.pix.width()/2,
                    ((i//mode)-mode/2)*self.pix.height() + self.pix.height()/2))
            #anim.setDuration(550+i*25)
            anim.setDuration(1800)
            anim.setEasingCurve(QEasingCurve.InOutElastic)
            self.group.addAnimation(anim)
        self.group.start()
        self.scene_canvas.items()[0].pixmap().save("test.jpg")

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

class Pixmap(QObject):

    def __init__(self, pix):
        super(Pixmap, self).__init__()

        self.pixmap_item = QGraphicsPixmapItem(pix)
        self.pixmap_item.setOpacity(0.7)
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
