from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QSound
import sys
from enum import Enum
from pathlib import Path
from collections.abc import Sequence

_HAS_BLUR_LIB = False
try:
    from BlurWindow.blurWindow import GlobalBlur
    _HAS_BLUR_LIB = True
except ImportError or ModuleNotFoundError:
    pass

class ImageCrop(Enum):
    DEFAULT = 1
    CIRCLE = 2

class CurveType:
    LINEAR = QtCore.QEasingCurve.Linear
    IN_QUAD = QtCore.QEasingCurve.InQuad
    OUT_QUAD = QtCore.QEasingCurve.OutQuad
    IN_OUT_QUAD = QtCore.QEasingCurve.InOutQuad
    OUT_IN_QUAD = QtCore.QEasingCurve.OutInQuad
    IN_CUBIC = QtCore.QEasingCurve.InCubic
    OUT_CUBIC = QtCore.QEasingCurve.OutCubic
    IN_OUT_CUBIC = QtCore.QEasingCurve.InOutCubic
    OUT_IN_CUBIC = QtCore.QEasingCurve.OutInCubic
    IN_QUART = QtCore.QEasingCurve.InQuart
    OUT_QUART = QtCore.QEasingCurve.OutQuart
    IN_OUT_QUART = QtCore.QEasingCurve.InOutQuart
    OUT_IN_QUART = QtCore.QEasingCurve.OutInQuart
    IN_QUINT = QtCore.QEasingCurve.InQuint
    OUT_QUINT = QtCore.QEasingCurve.OutQuint
    IN_OUT_QUINT = QtCore.QEasingCurve.InOutQuint
    OUT_IN_QUINT = QtCore.QEasingCurve.OutInQuint
    IN_SINE = QtCore.QEasingCurve.InSine
    OUT_SINE = QtCore.QEasingCurve.OutSine
    IN_OUT_SINE = QtCore.QEasingCurve.InOutSine
    OUT_IN_SINE = QtCore.QEasingCurve.OutInSine
    IN_EXPO = QtCore.QEasingCurve.InExpo
    OUT_EXPO = QtCore.QEasingCurve.OutExpo
    IN_OUT_EXPO = QtCore.QEasingCurve.InOutExpo
    OUT_IN_EXPO = QtCore.QEasingCurve.OutInExpo
    IN_CIRC = QtCore.QEasingCurve.InCirc
    OUT_CIRC = QtCore.QEasingCurve.OutCirc
    IN_OUT_CIRC = QtCore.QEasingCurve.InOutCirc
    OUT_IN_CIRC = QtCore.QEasingCurve.OutInCirc
    IN_ELASTIC = QtCore.QEasingCurve.InElastic
    OUT_ELASTIC = QtCore.QEasingCurve.OutElastic
    IN_OUT_ELASTIC = QtCore.QEasingCurve.InOutElastic
    OUT_IN_ELASTIC = QtCore.QEasingCurve.OutInElastic
    IN_BACK = QtCore.QEasingCurve.InBack
    OUT_BACK = QtCore.QEasingCurve.OutBack
    IN_OUT_BACK = QtCore.QEasingCurve.InOutBack
    OUT_IN_BACK = QtCore.QEasingCurve.OutInBack
    IN_BOUNCE = QtCore.QEasingCurve.InBounce
    OUT_BOUNCE = QtCore.QEasingCurve.OutBounce
    IN_OUT_BOUNCE = QtCore.QEasingCurve.InOutBounce
    OUT_IN_BOUNCE = QtCore.QEasingCurve.OutInBounce
    IN_CURVE = QtCore.QEasingCurve.InCurve
    OUT_CURVE = QtCore.QEasingCurve.OutCurve
    SINE_CURVE = QtCore.QEasingCurve.SineCurve
    COSINE_CURVE = QtCore.QEasingCurve.CosineCurve
    BEZIER_SPLINE = QtCore.QEasingCurve.BezierSpline
    TCB_SPLINE = QtCore.QEasingCurve.TCBSpline

class ImageAlign(Enum):
    LEFT = 1
    RIGHT = 2

class TextAlign(Enum):
    LEFT = 1
    RIGHT = 2
    CENTER = 3

class ActionType(Enum):
    TEXT = 1
    SELECT = 2

class ShowPosType(Enum):
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4

class Vec2:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

class Color:
    def __init__(self, r: int = 255, g: int = 255, b: int = 255, a: int = 255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

class Action:
    def __init__(self, type: ActionType, help: str = "", options: Sequence[str] = [], callback = None, style: str = ""):
        self.type = type
        self.style = style
        self.help = help
        self.options = options
        self.callback = callback

class Button:
    def __init__(self, text: str = "", icon: str|None = None,  callback = None, style: str = ""):
        self.style = style
        self.text = text
        self.icon = icon
        self.callback = callback

class Config:
    def __init__(self):
        self.MIN_SIZE = Vec2(300, 100)
        self.DURATION = 5000

        self.ANIM_SHOW_HIDE_TIME = 500
        
        self.USE_ANIM_FADE = True
        self.ANIM_FADE_CURVE = CurveType.LINEAR

        self.POS_OFFSET = Vec2(10, 10)
        self.ANIM_POS_OFFSET = Vec2(0, 0)
        self.ANIM_POS_CURVE = CurveType.LINEAR

        self.SHOW_POS = ShowPosType.BOTTOM_RIGHT

        self.CONTENT_SPACE = 20

        self.BG_COLOR = Color(79, 79, 79, 255)
        self.FG_COLOR = Color(242, 242, 242)
        self.IMAGE_SIZE = Vec2(100, 100)
        self.IMAGE_ALIGN = ImageAlign.LEFT
        self.TEXT_ALIGN = TextAlign.LEFT
        self.DRAG_SUPPORT = False
        self.IMAGE = ""
        self.IMAGE_CROP = ImageCrop.CIRCLE
        self.SOUND = ""
        self.TITLE = ""
        self.MESSAGE = ""
        self.APP_NAME = ""

        self.TITLE_FONT_SIZE = 14
        self.TITLE_STYLE = ""
        self.MESSAGE_FONT_SIZE = 12
        self.MESSAGE_STYLE = ""
        self.APP_NAME_FONT_SIZE = 10
        self.APP_NAME_STYLE = ""

        self.USE_BLUR_BG = False
        self.USE_ACRILIC = False
        self.IS_BLUR_DARK = True

        self.ACTIONS = dict()
        self.BUTTONS = dict()

class Toast(QtWidgets.QWidget):
    popuphidden = QtCore.pyqtSignal()

    def __init__(self, title: str="", message: str="", image: str="", sound: str="", duration: int=5000, config: Config|None=None):
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
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMinimumSize(QtCore.QSize(self.config.MIN_SIZE.x, self.config.MIN_SIZE.y))

        self._animation = QtCore.QPropertyAnimation(self, b"windowOpacity", self)
        self._animation.finished.connect(self._hide)
        self._animation.setEasingCurve(self.config.ANIM_FADE_CURVE)

        self._animationPos = QtCore.QPropertyAnimation(self, b"pos", self)
        self._animationPos.setEasingCurve(self.config.ANIM_POS_CURVE)

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._hideAnimation)

    #------PRIVATES------

    def _maskImage(self, imgdata, imgtype: str ='png', size: int = 100):
        # Load image
        image = QtGui.QImage.fromData(imgdata, imgtype)
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
        out_img = QtGui.QImage(imgsize, imgsize, QtGui.QImage.Format_ARGB32)
        out_img.fill(QtCore.Qt.transparent)
        brush = QtGui.QBrush(image)

        # Paint the output image
        painter = QtGui.QPainter(out_img)
        painter.setBrush(brush)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawEllipse(0, 0, imgsize, imgsize)
        painter.end()

        # Convert the image to a pixmap and rescale it.
        pr = QtGui.QWindow().devicePixelRatio()
        pm = QtGui.QPixmap.fromImage(out_img)
        pm.setDevicePixelRatio(pr)
        size *= pr
        pm = pm.scaled(int(size), int(size), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        return pm

    def _setupUi(self):
        self._mainLayout = QtWidgets.QVBoxLayout(self)
        self._buttonsLayout = QtWidgets.QHBoxLayout()
        self._textLayout = QtWidgets.QVBoxLayout()
        self._hLayout = QtWidgets.QHBoxLayout()

        self._mainLayout.addLayout(self._hLayout)

        self._mainLayout.setSpacing(1)
        self._hLayout.setSpacing(self.config.CONTENT_SPACE)
        self._labelTitle = QtWidgets.QLabel(self)
        self._labelMessage = QtWidgets.QLabel(self)
        self._labelAppName = QtWidgets.QLabel(self)
        #self._labelTitle.setStyleSheet("border: 1px solid black;")
        #self._labelMessage.setStyleSheet("border: 1px solid black;")
        #self._labelAppName.setStyleSheet("border: 1px solid black;")
        
        fontTitle = QtGui.QFont()
        fontTitle.setPointSize(self.config.TITLE_FONT_SIZE)
        fontMessage = QtGui.QFont()
        fontMessage.setPointSize(self.config.MESSAGE_FONT_SIZE)
        fontAppName = QtGui.QFont()
        fontAppName.setPointSize(self.config.APP_NAME_FONT_SIZE)
        self._labelTitle.setFont(fontTitle)
        self._labelMessage.setFont(fontMessage)
        self._labelAppName.setFont(fontAppName)

        self._labelTitle.setFixedHeight(self._labelTitle.height())
        if self.config.APP_NAME != "":
            self._labelMessage.setFixedHeight(self._labelTitle.height())

        pal = self._labelTitle.palette()
        pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor(self.config.FG_COLOR.r,self.config.FG_COLOR.g,self.config.FG_COLOR.b))
        self._labelTitle.setPalette(pal)

        pal = self._labelMessage.palette()
        pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor(self.config.FG_COLOR.r,self.config.FG_COLOR.g,self.config.FG_COLOR.b))
        self._labelMessage.setPalette(pal)

        pal = self._labelAppName.palette()
        pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor(self.config.FG_COLOR.r,self.config.FG_COLOR.g,self.config.FG_COLOR.b))
        self._labelAppName.setPalette(pal)

        if self.config.TITLE_STYLE != "":
            self._labelTitle.setStyleSheet(self.config.TITLE_STYLE)
        if self.config.MESSAGE_STYLE != "":
            self._labelMessage.setStyleSheet(self.config.MESSAGE_STYLE)
        if self.config.APP_NAME_STYLE != "":
            self._labelAppName.setStyleSheet(self.config.APP_NAME_STYLE)

        if self.config.TEXT_ALIGN == TextAlign.CENTER:
            self._labelTitle.setAlignment(QtCore.Qt.AlignCenter)
            self._labelMessage.setAlignment(QtCore.Qt.AlignCenter)
            self._labelAppName.setAlignment(QtCore.Qt.AlignCenter)
        elif self.config.TEXT_ALIGN == TextAlign.RIGHT:
            self._labelTitle.setAlignment(QtCore.Qt.AlignRight)
            self._labelMessage.setAlignment(QtCore.Qt.AlignRight)
            self._labelAppName.setAlignment(QtCore.Qt.AlignRight)
        elif self.config.TEXT_ALIGN == TextAlign.LEFT:
            self._labelTitle.setAlignment(QtCore.Qt.AlignLeft)
            self._labelMessage.setAlignment(QtCore.Qt.AlignLeft)
            self._labelAppName.setAlignment(QtCore.Qt.AlignLeft)

        self._textLayout.addWidget(self._labelTitle)
        if self.config.MESSAGE != "":
            self._textLayout.addWidget(self._labelMessage)
        if self.config.APP_NAME != "":
            self._textLayout.addWidget(self._labelAppName)
        self._textLayout.setSpacing(0)

        if (self.config.IMAGE != "" and self.config.IMAGE_ALIGN == ImageAlign.RIGHT) or self.config.IMAGE == "":
            self._hLayout.addLayout(self._textLayout)
        appearance = self.palette()
        appearance.setColor(QtGui.QPalette.All, QtGui.QPalette.Window,
                     QtGui.QColor(self.config.BG_COLOR.r,self.config.BG_COLOR.g,self.config.BG_COLOR.b,self.config.BG_COLOR.a))
        self.setPalette(appearance)
        
        if self.config.IMAGE != "":
            self._limage = QtWidgets.QLabel(self)
            #self._limage.setStyleSheet("border: 1px solid black;")
            if self.config.IMAGE_CROP == ImageCrop.CIRCLE:
                imgdata = open(self.config.IMAGE, 'rb').read() 
                pixmap = self._maskImage(imgdata, Path(self.config.IMAGE).suffix, self.config.IMAGE_SIZE.x)
            else:
                pixmap = QtGui.QPixmap(self.config.IMAGE)
                pixmap = pixmap.scaled(self.config.IMAGE_SIZE.x, self.config.IMAGE_SIZE.y)
            self._limage.setPixmap(pixmap)
            self._limage.resize(self.config.IMAGE_SIZE.x, self.config.IMAGE_SIZE.y)
            self._hLayout.addWidget(self._limage)

        if (self.config.IMAGE != "" and self.config.IMAGE_ALIGN == ImageAlign.LEFT):
            self._hLayout.addLayout(self._textLayout)

        self._limage.setFixedSize(self.config.IMAGE_SIZE.x, self.config.IMAGE_SIZE.y)

        if self.config.SOUND != "":
            self._sound = QSound(self.config.SOUND)
            self._sound.play()

        width = self._limage.geometry().width() + max(self._labelTitle.geometry().width(), self._labelMessage.geometry().width(), self._labelAppName.geometry().width()) + self.config.CONTENT_SPACE
        height = max(self._limage.geometry().height(), self._labelTitle.geometry().height() + self._labelMessage.geometry().height() + self._labelAppName.geometry().height()) + self.config.CONTENT_SPACE

        self._actions = dict()
        for key, action in self.config.ACTIONS.items():
            if action.type == ActionType.TEXT:
                w = QtWidgets.QLineEdit(self)
                w.setToolTip(action.help)
                if action.style != "":
                    w.setStyleSheet(action.style)
                if action.callback is not None:
                    w.textChanged.connect(action.callback)
                self._actions[key] = w
                self._mainLayout.addWidget(w)
                width += w.width()
            else:
                w = QtWidgets.QComboBox(self)
                w.setToolTip(action.help)
                if action.style != "":
                    w.setStyleSheet(action.style)
                if action.callback is not None:
                    w.currentTextChanged.connect(action.callback)
                for item in action.options:
                    w.addItem(item)
                self._actions[key] = w
                self._mainLayout.addWidget(w)
                height += w.height() + self._hLayout.spacing()

        if len(self.config.BUTTONS) > 0:
            height += self.config.CONTENT_SPACE
        if len(self.config.ACTIONS) > 0:
            height += self.config.CONTENT_SPACE

        self._buttons = dict()
        bntHeight = 0
        for key, button in self.config.BUTTONS.items():
            w = QtWidgets.QPushButton(button.text, self)
            if button.style != "":
                w.setStyleSheet(button.style)
            if button.callback is not None:
                w.clicked.connect(button.callback)
            if button.icon != "":
                w.setIcon(QtGui.QIcon(button.icon))
            self._buttons[key] = w
            self._buttonsLayout.addWidget(w)
            bntHeight = w.height()
        height += bntHeight
        if len(self.config.BUTTONS) > 0:
            self._mainLayout.addLayout(self._buttonsLayout)

        self.setGeometry(QtCore.QRect(self._hLayout.geometry().x(), self._hLayout.geometry().y(), width, height))

        if _HAS_BLUR_LIB == True and self.config.USE_BLUR_BG == True:
            GlobalBlur(self.winId(), Acrylic=self.config.USE_ACRILIC, Dark=self.config.IS_BLUR_DARK, QWidget=self)
            self.config.BG_COLOR.a = 0

    def _setPopupText(self):
        self._labelTitle.setText(self.config.TITLE)
        self._labelTitle.adjustSize()
        if self.config.MESSAGE != "":
            self._labelMessage.setText(self.config.MESSAGE)
            self._labelMessage.adjustSize()
        if self.config.APP_NAME != "":
            self._labelAppName.setText(self.config.APP_NAME)
            self._labelAppName.adjustSize()


    def _hideAnimation(self):
        if self.__isHide:
            return
        self.__isHide = True
        self._timer.stop()
        
        self._animation.setDuration(self.config.ANIM_SHOW_HIDE_TIME)
        self._animation.setStartValue(1.0)
        self._animation.setEndValue(0.0 if self.config.USE_ANIM_FADE else 1.0)
        self._animation.start()

        self._animationPos.setDuration(self.config.ANIM_SHOW_HIDE_TIME)
        self._animationPos.setEndValue(QtCore.QPoint(self._x, self._y) + QtCore.QPoint(self.config.ANIM_POS_OFFSET.x, self.config.ANIM_POS_OFFSET.y))
        self._animationPos.setStartValue(QtCore.QPoint(self._x, self._y))
        self._animationPos.start()

    def _hide(self, force: bool=False):
        if (force or self.windowOpacity() == 0) and not self.__isClosed:
            self.__isClosed = True
            QtWidgets.QWidget.hide(self)
            self.popuphidden.emit()
            if __name__ == '__main__':
                sys.exit()

    def _moveToast(self):
        try:
            screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
            screen_size = (screen_geometry.width(), screen_geometry.height())
            win_size = (self.width(), self.height())
            self._x, self._y = 0, 0
            if self.config.SHOW_POS == ShowPosType.BOTTOM_RIGHT:
                self._x = screen_size[0] - win_size[0] - self.config.POS_OFFSET.x
                self._y = screen_size[1] - win_size[1] - self.config.POS_OFFSET.y
            elif self.config.SHOW_POS == ShowPosType.BOTTOM_LEFT:
                self._x = self.config.POS_OFFSET.x
                self._y = screen_size[1] - win_size[1] - self.config.POS_OFFSET.y
            elif self.config.SHOW_POS == ShowPosType.TOP_RIGHT:
                self._x = screen_size[0] - win_size[0] - self.config.POS_OFFSET.x
                self._y = self.config.POS_OFFSET.y
            elif self.config.SHOW_POS == ShowPosType.TOP_LEFT:
                self._x = self.config.POS_OFFSET.x
                self._y = self.config.POS_OFFSET.y
            self.setGeometry(self._x, self._y, self.width(), self.height())
        except Exception as e:
            print(e)

    #------PUBLIC------

    def show(self):
        self._setupUi()
        self._setPopupText()

        self._moveToast()

        if self.config.USE_ANIM_FADE:
            self.setWindowOpacity(0.0)
        self._animation.setDuration(self.config.ANIM_SHOW_HIDE_TIME)
        self._animation.setStartValue(0.0 if self.config.USE_ANIM_FADE else 1.0)
        self._animation.setEndValue(1.0)

        self._animationPos.setDuration(self.config.ANIM_SHOW_HIDE_TIME)
        self._animationPos.setStartValue(QtCore.QPoint(self._x, self._y) + QtCore.QPoint(self.config.ANIM_POS_OFFSET.x, self.config.ANIM_POS_OFFSET.y))
        self._animationPos.setEndValue(QtCore.QPoint(self._x, self._y))
        self._moveToast()
        QtWidgets.QWidget.show(self)
        self._animation.start()
        self._animationPos.start()
        if (self.config.DURATION > 0):
            self._timer.start(self.config.DURATION)

    #------EVENTS------

    def paintEvent(self, event):
        backgroundColor = self.palette().light().color()
        backgroundColor.setRed(self.config.BG_COLOR.r)
        backgroundColor.setGreen(self.config.BG_COLOR.g)
        backgroundColor.setBlue(self.config.BG_COLOR.b)
        backgroundColor.setAlpha(self.config.BG_COLOR.a)
        customPainter = QtGui.QPainter(self)
        customPainter.fillRect(self.rect(), backgroundColor)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

        if event.buttons() == QtCore.Qt.MidButton:
            self._hideAnimation()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.config.DRAG_SUPPORT:
            self.move(event.globalPos() - self._dragPosition)
            event.accept()

    #------SETTERS------

    def setConfig(self, config: Config):
        self.config = config

    def setTitle(self, data: str, fontSize: int = 14, style: str = ""):
        self.config.TITLE = data
        self.config.TITLE_FONT_SIZE = fontSize
        self.config.TITLE_STYLE = style

    def setMessage(self, data: str, fontSize: int = 12, style: str = ""):
        self.config.MESSAGE = data
        self.config.MESSAGE_FONT_SIZE = fontSize
        self.config.MESSAGE_STYLE = style

    def setAppName(self, data: str, fontSize: int = 10, style: str = ""):
        self.config.APP_NAME = data
        self.config.APP_NAME_FONT_SIZE = fontSize
        self.config.APP_NAME_STYLE = style

    def setTextAlign(self, data: TextAlign):
        self.config.TEXT_ALIGN = data

    def setSound(self, data: str):
        self.config.SOUND = data

    def setDragToast(self, data: bool):
        self.config.DRAG_SUPPORT = data

    def setImage(self, data: str):
        self.config.IMAGE = data

    def setImageSize(self, data: int) :
        self.config.IMAGE_SIZE = Vec2(data, data)

    def setImageSize(self, data1: int, data2: int):
        self.config.IMAGE_SIZE = Vec2(data1, data2)

    def setImageAlign(self, data: ImageAlign):
        self.config.IMAGE_ALIGN = data

    def setImageCrop(self, data: ImageCrop):
        self.config.IMAGE_CROP = data

    def setDuration(self, data: int):
        self.config.DURATION = data

    def setAnimTime(self, data: int):
        self.config.ANIM_SHOW_HIDE_TIME = data

    def setAnimUseFade(self, data: bool):
        self.config.USE_ANIM_FADE = data

    def setAnimFadeCurve(self, data: CurveType):
        self.config.ANIM_FADE_CURVE = data

    def setAnimPosOffset(self, x: int, y: int):
        self.config.ANIM_POS_OFFSET = Vec2(x, y)

    def setAnimPosCurve(self, data: CurveType):
        self.config.ANIM_POS_CURVE = data

    def setPosOffset(self, x: int, y: int):
        self.config.POS_OFFSET = Vec2(x, y)

    def setShowPos(self, data: ShowPosType):
        self.config.SHOW_POS = data

    def setSpaceTextImage(self, data: int):
        self.config.CONTENT_SPACE = data

    def setBgColor(self, data: Color):
        self.config.BG_COLOR = data

    def setFgColor(self, data: Color):
        self.config.FG_COLOR = data

    def addButton(self, name: str, data: Button):
        self.config.BUTTONS[name] = data

    def clearButtons(self):
        self.config.BUTTONS = dict()

    def addAction(self, name: str, data: Action):
        self.config.ACTIONS[name] = data

    def clearActions(self):
        self.config.ACTIONS = dict()
    
    def setUseBlurBg(self, data: bool):
        self.config.USE_BLUR_BG = data

    def setUseBlurAcrilicBg(self, data: bool):
        self.config.USE_ACRILIC = data

    def setIsBlurDark(self, data: bool):
        self.config.IS_BLUR_DARK = data


if __name__ == '__main__':
    from qt_material import apply_stylesheet
    app = QtWidgets.QApplication(sys.argv)
    
    toast = Toast()
    toast.setTitle("Some Title")
    toast.setMessage("This is notification for you")
    #toast.setImage("images.png")
    toast.setTextAlign(TextAlign.LEFT)
    toast.setUseBlurBg(True)
    toast.setAnimPosOffset(30, 0)
    toast.setAnimPosCurve(CurveType.IN_CUBIC)
    toast.setAnimFadeCurve(CurveType.IN_CUBIC)
    toast.config.BUTTONS["btn1"] = Button("Play")
    #toast.setSound("sound.wav")

    apply_stylesheet(app, theme='dark_teal.xml')
    toast.show()
    sys.exit(app.exec_())
