from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QSound
import sys
from enum import Enum
from pathlib import Path

class ImageCrop(Enum):
    DEFAULT = 1
    CIRCLE = 2

IMAGE_ALIGN_LEFT = "left"
IMAGE_ALIGN_RIGHT = "right"

TEXT_ALIGN_LEFT = "left"
TEXT_ALIGN_RIGHT = "right"
TEXT_ALIGN_CENTER = "center"
class Config:
    def __init__(self):
        self.DURATION = 5000
        self.ANIM_SHOW_HIDE_TIME = 500
        self.BG_COLOR = (79, 79, 79)
        self.FG_COLOR = (242, 242, 242)
        self.IMAGE_SIZE = (100, 100)
        self.IMAGE_ALIGN = IMAGE_ALIGN_LEFT
        self.TEXT_ALIGN = TEXT_ALIGN_LEFT
        self.DRAG_SUPPORT = False
        self.IMAGE = ""
        self.IMAGE_CROP = ImageCrop.CIRCLE
        self.SOUND = ""
        self.TITLE = ""
        self.MESSAGE = ""

class Toast(QtWidgets.QWidget):
    popuphidden = QtCore.pyqtSignal()

    def __init__(self, title="", message="", image="", sound="", duration=5000, config=None):
        if config is not None:
            self.config = config
        else:
            self.config = Config()
            self.config.IMAGE = image
            self.config.SOUND = sound
            self.config.DURATION = duration
            self.config.TITLE = title
            self.config.MESSAGE = message

        self.__isHide = False
        self.__isClosed = False
        
        super(Toast, self).__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.setMinimumSize(QtCore.QSize(300, 100))
        self.animation = QtCore.QPropertyAnimation(self, b"windowOpacity", self)
        self.animation.finished.connect(self.hide)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.hideAnimation)

    def _maskImage(self, imgdata, imgtype ='png', size = 100): 
        # Load image 
        image = QtGui.QImage.fromData(imgdata, imgtype) 

        # convert image to 32-bit ARGB (adds an alpha 
        # channel ie transparency factor): 
        image.convertToFormat(QtGui.QImage.Format_ARGB32) 

        # Crop image to a square: 
        imgsize = min(image.width(), image.height()) 
        rect = QtCore.QRect( 
            int((image.width() - imgsize) / 2), 
            int((image.height() - imgsize) / 2), 
            imgsize, 
            imgsize, 
         ) 

        image = image.copy(rect) 

        # Create the output image with the same dimensions  
        # and an alpha channel and make it completely transparent: 
        out_img = QtGui.QImage(imgsize, imgsize, QtGui.QImage.Format_ARGB32) 
        out_img.fill(QtCore.Qt.transparent) 

        # Create a texture brush and paint a circle  
        # with the original image onto the output image: 
        brush = QtGui.QBrush(image) 

        # Paint the output image 
        painter = QtGui.QPainter(out_img) 
        painter.setBrush(brush) 

        # Don't draw an outline 
        painter.setPen(QtCore.Qt.NoPen) 

        # drawing circle 
        painter.drawEllipse(0, 0, imgsize, imgsize) 
    
        # closing painter event 
        painter.end() 

        # Convert the image to a pixmap and rescale it.  
        pr = QtGui.QWindow().devicePixelRatio() 
        pm = QtGui.QPixmap.fromImage(out_img) 
        pm.setDevicePixelRatio(pr) 
        size *= pr 
        pm = pm.scaled(int(size), int(size), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        # return back the pixmap data 
        return pm 

    def setupUi(self):
        self.hLayout = QtWidgets.QHBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        if self.config.TEXT_ALIGN == TEXT_ALIGN_CENTER:
            self.label.setAlignment(QtCore.Qt.AlignCenter)
        elif self.config.TEXT_ALIGN == TEXT_ALIGN_RIGHT:
            self.label.setAlignment(QtCore.Qt.AlignRight)
        elif self.config.TEXT_ALIGN == TEXT_ALIGN_LEFT:
            self.label.setAlignment(QtCore.Qt.AlignLeft)
        if (self.config.IMAGE != "" and self.config.IMAGE_ALIGN == IMAGE_ALIGN_RIGHT) or self.config.IMAGE == "":
            self.hLayout.addWidget(self.label)
        appearance = self.palette()
        appearance.setColor(QtGui.QPalette.All, QtGui.QPalette.Window,
                     QtGui.QColor(self.config.BG_COLOR[0],self.config.BG_COLOR[1],self.config.BG_COLOR[2]))
        self.setPalette(appearance)
        
        pal = self.label.palette()
        pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor(self.config.FG_COLOR[0],self.config.FG_COLOR[1],self.config.FG_COLOR[2]))
        self.label.setPalette(pal)
        
        if self.config.IMAGE != "":
            self.limage = QtWidgets.QLabel(self)
            self.limage.setStyleSheet("border: 1px solid black;") 
            if self.config.IMAGE_CROP == ImageCrop.CIRCLE:
                imgdata = open(self.config.IMAGE, 'rb').read() 
                pixmap = self._maskImage(imgdata, Path(self.config.IMAGE).suffix, self.config.IMAGE_SIZE[0])
            else:
                pixmap = QtGui.QPixmap(self.config.IMAGE)
                pixmap = pixmap.scaled(self.config.IMAGE_SIZE[0], self.config.IMAGE_SIZE[1])
            self.limage.setPixmap(pixmap)
            self.limage.resize(self.config.IMAGE_SIZE[0], self.config.IMAGE_SIZE[1])
            self.hLayout.addWidget(self.limage)
            
        if (self.config.IMAGE != "" and self.config.IMAGE_ALIGN == IMAGE_ALIGN_LEFT):
            self.hLayout.addWidget(self.label)

        if self.config.SOUND != "":
            self._sound = QSound(self.config.SOUND)
            self._sound.play()

    def setPopupText(self, text):
        self.label.setText(text)
        self.label.adjustSize()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

        if event.buttons() == QtCore.Qt.MidButton:
            self.hideAnimation()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.config.DRAG_SUPPORT:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def show(self):
        self.setupUi()
        self.setPopupText(self.config.TITLE + '\n' + self.config.MESSAGE)
        
        self.setWindowOpacity(0.0)
        self.animation.setDuration(self.config.ANIM_SHOW_HIDE_TIME)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        QtWidgets.QWidget.show(self)
        self.animation.start()
        if (self.config.DURATION > 0):
            self.timer.start(self.config.DURATION)
        self.moveToast()

    def hideAnimation(self):
        if self.__isHide:
            return
        self.__isHide = True
        self.timer.stop()
        self.animation.setDuration(self.config.ANIM_SHOW_HIDE_TIME)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.start()

    def hide(self, force=False):
        if (force or self.windowOpacity() == 0) and not self.__isClosed:
            self.__isClosed = True
            QtWidgets.QWidget.hide(self)
            self.popuphidden.emit()
            if __name__ == '__main__':
                sys.exit()

    def moveToast(self):
        try:
            screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
            screen_size = (screen_geometry.width(), screen_geometry.height())
            win_size = (self.width(), self.height())
            x = screen_size[0] - win_size[0] - 10
            y = screen_size[1] - win_size[1] - 10
            self.setGeometry(x, y, self.width(), self.height())
        except Exception as e:
            print (e)

    def setConfig(self, config):
        self.config = config

    def setTitle(self, data):
        self.config.TITLE = data

    def setMessage(self, data):
        self.config.MESSAGE = data

    def setTextAlign(self, data):
        self.config.TEXT_ALIGN = data

    def setSound(self, data):
        self.config.SOUND = data

    def setDragToast(self, data):
        self.config.DRAG_SUPPORT = data

    def setImage(self, data):
        self.config.IMAGE = data

    def setImageSize(self, data):
        self.config.IMAGE_SIZE = (data, data)

    def setImageSize(self, data1, data2):
        self.config.IMAGE_SIZE = (data1, data2)

    def setImageAlign(self, data):
        self.config.IMAGE_ALIGN = data

    def setImageCrop(self, data):
        self.config.IMAGE_CROP = data

    def setDuration(self, data):
        self.config.DURATION = data

    def setAnimTime(self, data):
        self.config.ANIM_SHOW_HIDE_TIME = data

    def setBgColor(self, data):
        self.config.BG_COLOR = data

    def setFgColor(self, data):
        self.config.FG_COLOR = data


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    toast = Toast("SIMPLE TITLE", "SIMPLE MESSAGE", "image.png", "", -1)
    toast.config.IMAGE_ALIGN = IMAGE_ALIGN_RIGHT
    toast.config.TEXT_ALIGN = TEXT_ALIGN_RIGHT
    #toast.config.SOUND = "sound.wav"
    toast.show()
    sys.exit(app.exec_())
