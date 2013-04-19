import time
import shutil
import os
import tempfile
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#from ui_main import Ui_MainWindow
from lib.identicon_python import identicon
from lib.random_avatar import Visicon
from lib.commandstack.commandstack import CommandStack

MAX_HISTORY = 10
class MainWindow(QGraphicsView):#QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):

        QMainWindow.__init__(self, parent)
        #self.setupUi(self)
        #self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.DragMode(QGraphicsView.ScrollHandDrag)
        self.setAcceptDrops(True)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        desktop = QApplication.desktop()
        screen_size = desktop.availableGeometry()
        self.screen_height = screen_size.height()

        self.scene_canvas = QGraphicsScene()#-640, -400, 1280, 800)
        #self.scene_canvas = QGraphicsScene(-screen_size.width()/2,
                #-screen_size.height()/2,
                #screen_size.width(),
                #screen_size.height())
        #self.scene_canvas = QGraphicsScene(-self.screen_height/2,
                #-self.screen_height/2,
                #self.screen_height,
                #self.screen_height)
        self.animation_group = QParallelAnimationGroup()
        self.setScene(self.scene_canvas)

        gradient = QRadialGradient(0,0, screen_size.width()/2, 0,0)
        gradient.setColorAt(0, QColor("#00aaaa"))
        gradient.setColorAt(1, QColor("#eeeeee"))
        self.setBackgroundBrush(QBrush(gradient))
        self.history = CommandStack(MAX_HISTORY)
        self.icon_path = os.path.join(tempfile.gettempdir(), "icon.png")
        self.generate_icon()

        self.load_scene()

        self.setGeometry(QRect(0, 0, screen_size.width(), screen_size.height()))
        self.setSceneRect(-screen_size.width()/2+self.pix.width(),
                -screen_size.height()/2+self.pix.height(),
                screen_size.width(),
                screen_size.height())


        self.animator=QTimer()
        self.animator.timeout.connect(self.generate_icon)

    def generate_icon(self, code=0, hist=False, ui=True):

        hash_code = code
        if not hash_code:
            import random
            hash_code = "%032x" % random.getrandbits(128)
            self.code = int(hash_code[2:], 16)
        else:
            self.code = hash_code

        ICON_PATH = os.path.join(tempfile.gettempdir(), "icon.png")
        visicon = Visicon(str(self.code), "", 72)
        img = visicon.draw_image()
        img.save(ICON_PATH)

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

        self.animation_group.clear()

        mode = self.screen_height//self.pix.height()

        count = mode * mode
        self.item_number = count

        remove = False
        if len(self.scene_canvas.items()) >= count:
            remove = True
        items = self.scene_canvas.items()[-count:]
        for i in range(count):
            item = Pixmap(self.pix)
            if remove:
                self.scene_canvas.removeItem(items[count-1-i])
            item.pixmap_item.setZValue(i)
            item.pixmap_item.set_movable(True)
            item.pixmap_item.set_code(self.code)
            self.scene_canvas.addItem(item.pixmap_item)
            anim = QPropertyAnimation(item, "pos")
            anim.setStartValue(QPointF(-self.pix.width()/2, -self.pix.height()/2))
            anim.setEndValue(QPointF(((i%mode)-mode/2)*self.pix.width() + self.pix.width()/2,
                    ((i//mode)-mode/2)*self.pix.height() + self.pix.height()/2))
            anim.setDuration(350+i*25)
            #anim.setDuration(1500)
            anim.setEasingCurve(QEasingCurve.OutBack)
            self.animation_group.addAnimation(anim)
        self.animation_group.start()
        #self.scene_canvas.items()[0].pixmap().save("test.jpg")

    def play(self):
        if self.animator.isActive():
            self.animator.stop()
        else:
            self.animator.start(3000)
        self.generate_icon()

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

    def export_icon(self):
        file_type = "jpg"
        if not os.path.exists(file_type):
            os.mkdir(file_type)

        item = self.scene_canvas.items()[self.item_number]
        timestamp = time.strftime("%Y_%m_%d")
        dst_name = "%s-%s.%s" % (timestamp, item.code(), file_type)
        dst_path = os.path.join(file_type, dst_name)
        item.pixmap().save(dst_path)
        cwd = os.path.join(os.getcwd(), file_type)
        text = QGraphicsTextItem("File '%s' has been saved in '%s'" % (dst_path, cwd))
        #text.setPos(-100, -100)
        #self.scene_canvas.addItem(text)

    def load_scene(self):
        with open("test.txt", "r") as f:
            for line in f.readlines():
                code, x, y = line.split(":")
                self.generate_icon(code, ui=False)
                pixmap = QPixmap(self.icon_path)
                item = GraphicsPixmapItem(pixmap)
                item.moveBy(float(x), float(y))
                item.setZValue(len(self.scene_canvas.items())+1)
                item.set_code(code)
                self.scene_canvas.addItem(item)


    def save_scene(self):
        count = self.item_number
        items = self.scene_canvas.items()[:-count]
        with open("test.txt","w+") as f:
            f.writelines(["%s:%s:%s%s" % (item.code(),
                                        item.pos().x(),
                                        item.pos().y(),
                                        os.linesep)
                                        for item in items])

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
            self.save_scene()
            self.close()
        if key == Qt.Key_G:
            self.export_icon()
        if key == Qt.Key_P:
            self.play()


        QMainWindow.keyPressEvent(self, event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/icondata"):
            if event.source() == self:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.ignore()

    dragMoveEvent = dragEnterEvent

    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/icondata'):
            itemData = event.mimeData().data('application/icondata')
            dataStream = QDataStream(itemData, QIODevice.ReadOnly)

            pixmap = QPixmap()
            offset = QPoint()
            dataStream >> pixmap >> offset

            new_item = Pixmap(pixmap)
            scene_pos = self.mapToScene(event.pos())
            new_item.pixmap_item.moveBy(scene_pos.x()-self.offset.x(), scene_pos.y()-self.offset.y())
            new_item.pixmap_item.get_original_pixmap()
            new_item.pixmap_item.setZValue(len(self.scene_canvas.items())+1)
            new_item.pixmap_item.set_code(event.mimeData().text())
            self.scene_canvas.addItem(new_item.pixmap_item)


            if event.source() == self:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if not item:
            return

        if event.button() == Qt.RightButton:
            if not item.movable:
                self.scene_canvas.removeItem(item)
            return

        #if event.button() != Qt.LeftButton:
            #event.ignore()
            #return


        item.get_original_pixmap()
        pixmap = QPixmap(item.pixmap())

        itemData = QByteArray()
        dataStream = QDataStream(itemData, QIODevice.WriteOnly)
        dataStream << pixmap << (event.pos() - item.pos()).toPoint()

        mimeData = QMimeData()
        mimeData.setData('application/icondata', itemData)
        mimeData.setText(item.code())

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        self.offset = event.pos() - self.mapFromScene(item.pos())
        drag.setHotSpot(self.offset)

        if drag.exec_(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction) == Qt.MoveAction:
            if not item.movable:
                self.scene_canvas.removeItem(item)
            item.show()
        else:
            item.show()
            item.setPixmap(pixmap)

    def mouseReleaseEvent(self, event):
        if event.button() != Qt.LeftButton:
            event.ignore()
            return
        else:
            #self.show_favor_icon(item)
            pass

    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.pos())
        if not item:
            return
        self.show_favor_icon(item)

    def show_favor_icon(self,item):
        self.pix = QPixmap(item.original_pixmap)
        self.code = item.code()
        self.animation()


class Pixmap(QObject):

    def __init__(self, pix):
        super(Pixmap, self).__init__()
        self.pixmap_item = GraphicsPixmapItem(pix)

    def _set_pos(self, pos):
        self.pixmap_item.setPos(pos)

    pos = pyqtProperty(QPointF, fset=_set_pos)

class GraphicsPixmapItem(QGraphicsPixmapItem):

    def __init__(self, pixmap):
        super(GraphicsPixmapItem, self).__init__()
        self.setOpacity(0.7)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setAcceptsHoverEvents(True)

        self.original_pixmap = pixmap
        self.setPixmap(pixmap)
        self.setCursor(Qt.OpenHandCursor)
        self.movable=False

    def get_movable(self):
        return self.movable

    def set_movable(self, movable):
        self.movable = movable

    def hoverEnterEvent(self, event):
        tempPixmap = QPixmap(self.pixmap())
        painter = QPainter()
        painter.begin(tempPixmap)
        painter.fillRect(self.pixmap().rect(), QColor(127, 127, 127, 127))
        painter.end()

        self.setPixmap(tempPixmap)

    def hoverLeaveEvent(self, event):
        self.get_original_pixmap()

    def get_original_pixmap(self):
        self.setPixmap(self.original_pixmap)

    def set_code(self, code):
        self._code = code

    def code(self):
        return str(self._code)

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            event.ignore()
            return
        self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)


if __name__ == "__main__":

    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    #main_window.showFullScreen()
    main_window.show()
    sys.exit(app.exec_())
