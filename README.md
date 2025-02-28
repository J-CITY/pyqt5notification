# Pyqt5 Notification

Tiny script for cross platform notification with pyqt5

It could use [BlurWindow](https://github.com/Peticali/PythonBlurBehind) if you want blur background

## Dependencies

PyQt5
```
python -m pip install PyQt5
```

If you want blur background
```
python -m pip install BlurWindow
```

## Examples:

![Imgur](https://github.com/J-CITY/pyqt5notification/blob/master/screens/scr1.png)

```python
# use for material ui widgets style
from qt_material import apply_stylesheet

app = QtWidgets.QApplication(sys.argv)

toast = Toast("SIMPLE TITLE", "SIMPLE MESSAGE", "images.png")

# init material ui style
apply_stylesheet(app, theme='dark_teal.xml')

toast.show()

sys.exit(app.exec_())
```

![Imgur](https://github.com/J-CITY/pyqt5notification/blob/master/screens/scr2.gif)

```python
from qt_material import apply_stylesheet

app = QtWidgets.QApplication(sys.argv)

toast = Toast()
toast.setTitle("Some Title")
toast.setMessage("This is notification for you")
toast.setImage("images.png")
toast.setTextAlign(TextAlign.LEFT)
toast.setUseBlurBg(True)
toast.setAnimPosOffset(30, 0)
toast.setAnimPosCurve(CurveType.IN_CUBIC)
toast.setAnimFadeCurve(CurveType.IN_CUBIC)
toast.config.BUTTONS["btn1"] = Button("Play")
toast.setSound("sound.wav")

apply_stylesheet(app, theme='dark_teal.xml')

toast.show()
sys.exit(app.exec_())
```
