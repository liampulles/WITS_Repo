import cv2
import argparse
import detect
import re
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import numpy as np

form_class, base_class = uic.loadUiType('main.ui')

#From https://stackoverflow.com/questions/4623446/how-do-you-sort-files-numerically
def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]
#--------------

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = form_class()
        self.ui.setupUi(self)
        self.ui.btnNext.clicked.connect(self.nextImage)
        self.ui.btnPrev.clicked.connect(self.prevImage)

    def nextImage(self):
        #Are we on the second last image?
        if self.current == len(self.input) - 2:
            self.ui.btnNext.setEnabled(False)

        #Are we on the first image?
        if self.current == 0:
            self.ui.btnPrev.setEnabled(True)

        self.current += 1
        self.loadImage()

    def prevImage(self):
        #Are we on the second image?
        if self.current == 1:
            self.ui.btnPrev.setEnabled(False)

        #Are we on the last image
        if self.current == len(self.input) - 1:
            self.ui.btnNext.setEnabled(True)

        self.current -= 1
        self.loadImage()

    def loadImage(self):
        print("Loading image",self.input[self.current])
        frame, value, circles, argmax, orig = detect.image_process(self.input[self.current])
        frame = cv2.resize(frame, (640,480))
        orig = cv2.resize(cv2.cvtColor(orig,cv2.COLOR_RGB2BGR), (640,480))
        out = np.hstack((orig,frame))
        img = QtGui.QImage(out, out.shape[1], out.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.ui.lblImage.setPixmap(pix)
        self.ui.lblValue.setText("Total Value: R{0:.2f}".format(value))
        self.ui.lblName.setText(self.input[self.current])

    def load(self,files):
        self.input = sorted(files,key=alphanum_key)
        self.current = 0
        self.loadImage()
        self.ui.btnPrev.setEnabled(False)
        if len(self.input) == 1:
            self.ui.btnNext.setEnabled(False)

    def openMovie(self):
        filename, filters = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', filter="Movies (*.avi *.mp4 *.mkv *.mov *.ogg *.VOB)")
        marked = self.getSegments(filename)
        #marked = sub_file.segment_find(filename)
        #self.parseSegments(marked, filename)

    def getSegments(self, filename):
        self.selapp = SelectWindow()
        self.selapp.load(filename, self)
        self.selapp.show()
        self.hide()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    parser = argparse.ArgumentParser(description='Module and application to detect coins in an image.')
    parser.add_argument('--input','-i',help='Input image paths',nargs='+',required=True)
    args = parser.parse_args()
    if len(args.input) == 0:
        sys.exit(app.exec_())

    myapp = MainWindow()
    myapp.load(args.input)
    myapp.show()
    sys.exit(app.exec_())
