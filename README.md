# pyqt5notification

Tini script for notification in pyqt5


![Imgur](https://github.com/J-CITY/pyqt5notification/blob/master/scr/scr.png)

```python
app = QtWidgets.QApplication(sys.argv)
toast = Toast("SIMPLE TITLE", "SIMPLE MESSAGE", "image.png")
toast.config.IMAGE_ALIGN = IMAGE_ALIGN_RIGHT
toast.config.TEXT_ALIGN = TEXT_ALIGN_RIGHT
toast.show()
sys.exit(app.exec_())
```
