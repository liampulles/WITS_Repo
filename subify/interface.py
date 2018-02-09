from PyQt5 import QtCore, QtGui, QtWidgets, uic
from helper import sub_file
from ocr import liam_ocr
import cv2
import numpy as np
import pickle

form_class, base_class = uic.loadUiType('intro.ui')

class SelectWindow(QtWidgets.QMainWindow):
    segments = []
    cap = None
    filename = None
    current_frame = 0
    current_segment = None
    total_frames = 0
    main_window = None
    segment_define = False
    new_seg_start = 0

    def __init__(self, parent = None):
        select_form, select_base = uic.loadUiType('select.ui')
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = select_form()
        self.ui.setupUi(self)

    def load(self, filename_in, main_window_in):
        self.filename = filename_in
        self.cap = cv2.VideoCapture(filename_in)
        ret, frame = self.cap.read()
        self.load_image(frame)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.ui.lblFrameTotal.setText("/ {}".format(self.total_frames))
        self.main_window = main_window_in

        self.ui.btnFinish.clicked.connect(self.finish)
        self.ui.btnRestart.clicked.connect(self.restart)
        self.ui.btnClose.clicked.connect(self.cancel)

        self.ui.slFrame.setMaximum(self.total_frames)
        self.ui.sbxFrameCurrent.setMaximum(self.total_frames)
        self.ui.slFrame.valueChanged.connect(self.sliderChange)
        self.ui.sbxFrameCurrent.valueChanged.connect(self.sbxChange)
        self.frameChange(0)

        self.ui.btnSegmentStartEnd.clicked.connect(self.segStartEnd)
        self.ui.btnCancel.clicked.connect(self.cancelSegment)
        self.ui.btnDeleteSegment.clicked.connect(self.deleteSegment)

        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Right"), self, self.goRight)
        self.shortcut1 = QtWidgets.QShortcut(QtGui.QKeySequence("Left"), self, self.goLeft)
        self.shortcut2 = QtWidgets.QShortcut(QtGui.QKeySequence("Shift+Right"), self, self.goRightFast)
        self.shortcut3 = QtWidgets.QShortcut(QtGui.QKeySequence("Shift+Left"), self, self.goLeftFast)

    def goRight(self):
        self.ui.sbxFrameCurrent.setValue(min(self.current_frame+1,self.total_frames))

    def goLeft(self):
        self.ui.sbxFrameCurrent.setValue(max(self.current_frame-1,0))

    def goRightFast(self):
        self.ui.sbxFrameCurrent.setValue(min(self.current_frame+10,self.total_frames))

    def goLeftFast(self):
        self.ui.sbxFrameCurrent.setValue(max(self.current_frame-10,0))

    def cancelSegment(self):
        self.ui.btnCancel.setEnabled(False)
        self.ui.btnSegmentStartEnd.setText("Segment Start")
        self.segment_define = False

    def deleteSegment(self):
        del self.segments[self.current_segment]
        self.current_segment = None
        self.frameChange(self.current_frame)

    def segStartEnd(self):
        #Are we already defining a segment?
        if self.segment_define:
            #Are we in another segment?
            if self.current_segment != None:
                msg = "You are attempting place the end of the new segment in another segment. \
                       Segments may not overlap. \
                       Please choose another frame, or cancel the current new segment and \
                       delete the conlifcting segment at this position."
                reply = QtWidgets.QMessageBox.question(self, 'Invalid Placement.',
                         msg, QtWidgets.QMessageBox.Ok)

                return
            else:
                #Is the segment ending before the segment beginning?
                if self.new_seg_start > self.current_frame:
                    msg = "You cannot place the segment ending before the segment beginning. \
                           Please select a frame after frame {}, or cancel the new segment \
                           and start again.".format(self.new_seg_start)
                    reply = QtWidgets.QMessageBox.question(self, 'Invalid Placement.',
                             msg, QtWidgets.QMessageBox.Ok)

                    return
                else:
                    #Does the new segment contain other segments?
                    contained = self.containedSegments(self.new_seg_start,self.current_frame)
                    if len(contained) > 0:
                        msg = "The new segment contains several other segments. \
                               Press Ok to consume the contained segments, or Cancel."
                        reply = QtWidgets.QMessageBox.question(self, 'Invalid Placement.',
                                 msg, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel)

                        if reply == QtWidgets.QMessageBox.Cancel:
                            return
                        else:
                            for i in contained:
                                del self.segments[i]
                    #Good to go.
                    new_segment = (self.new_seg_start,self.current_frame)
                    self.segments += [new_segment]
                    self.ui.btnCancel.setEnabled(False)
                    self.ui.btnSegmentStartEnd.setText("Segment Start")
                    self.segment_define = False
                    self.frameChange(self.current_frame)
        #New segment
        else:
            #Are we in another segment?
            if self.current_segment != None:
                msg = "You are attempting place the beginning a new segment in another segment. \
                       Segments may not overlap. \
                       Please choose another frame, or cancel the current new segment and \
                       delete the conlifcting segment at this position."
                reply = QtWidgets.QMessageBox.question(self, 'Invalid Placement.',
                         msg, QtWidgets.QMessageBox.Ok)

                return
            else:
                #Good to go.
                self.new_seg_start = self.current_frame
                self.ui.btnCancel.setEnabled(True)
                self.ui.btnSegmentStartEnd.setText("Segment End")
                self.segment_define = True

    def containedSegments(self,start,end):
        contained = []
        for i in range(len(self.segments)):
            segment = self.segments[i]
            if (start <= segment[0]) & (end >= segment[1]):
                contained += [i]
        return contained

    def sliderChange(self):
        frame_no = self.ui.slFrame.value()
        self.ui.sbxFrameCurrent.setValue(frame_no)
        self.frameChange(frame_no)

    def sbxChange(self):
        frame_no = self.ui.sbxFrameCurrent.value()
        self.ui.slFrame.setValue(frame_no)
        self.frameChange(frame_no)

    def getSegment(self,frame_no):
        for i in range(len(self.segments)):
            segment = self.segments[i]
            if (frame_no >= segment[0]) & (frame_no <= segment[1]):
                return i, True
        return None, False

    def frameChange(self,frame_no):
        frame_no = frame_no % self.total_frames
        segment, status = self.getSegment(frame_no)

        if status:
            self.ui.lblInfo.setText("In segment (Frames {} - {}).".format(self.segments[segment][0],self.segments[segment][1]))
            self.current_segment = segment
            self.ui.btnDeleteSegment.setEnabled(True)
        else:
            self.current_segment = None
            self.ui.lblInfo.setText("No segment on this frame.")
            self.ui.btnDeleteSegment.setEnabled(False)

        if self.current_frame != (frame_no - 1):
            self.cap.set(1,frame_no)
        if (self.current_frame != frame_no):
            ret, frame = self.cap.read()
            self.load_image(frame)

        self.current_frame = frame_no

    def load_image(self,frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.ui.lblImage.setPixmap(pix)

    def finish(self):
        if len(self.segments) == 0:
            msg = "No segments have been selected. Press 'Ok' to return to \
                   the start screen, or 'Cancel' to go back to segment selection."
            reply = QtWidgets.QMessageBox.question(self, 'No Segments',
                     msg, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel)

            if reply == QtWidgets.QMessageBox.Ok:
                self.cap.release()
                self.main_window.show()
                self.close()
            else:
                return

        #Move on.
        self.capapp = CaptureWindow()
        self.capapp.load(self.cap,self.segments)
        self.capapp.show()
        self.hide()
        #self.segapp = SegmentWindow()
        #self.segapp.load(self.cap,self.segments)
        #self.segapp.show()
        #self.hide()

    def restart(self):
        msg = "Really Restart?"
        reply = QtWidgets.QMessageBox.question(self, 'Restart?',
                 msg, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel)

        if reply == QtWidgets.QMessageBox.Ok:
            self.segments = []
            self.current_segment = None
        else:
            return

    def cancel(self):
        msg = "Return to start screen?"
        reply = QtWidgets.QMessageBox.question(self, 'Cancel?',
                 msg, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel)

        if reply == QtWidgets.QMessageBox.Ok:
            self.cap.release()
            self.main_window.show()
            self.close()
        else:
            return

class SegmentWindow(QtWidgets.QMainWindow):
    current_segment = 0
    start_frame = 0
    end_frame = 0
    segment = []
    final_segs = None
    img_final = None
    current_frame = 0
    cap = None
    cyrillics = []
    translated = []

    def __init__(self, parent = None):
        main_form, main_base = uic.loadUiType('main.ui')
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = main_form()
        self.ui.setupUi(self)

    def load(self, cap_in,segments_in):
        self.cap = cap_in
        self.segments = segments_in
        self.current_segment = 0
        self.cyrillics = [""]*len(self.segments)
        self.translated = [""]*len(self.segments)

        self.segmentChanger(self.current_segment)
        self.cap.set(1,self.current_frame)
        ret, frame = self.cap.read()
        self.load_image(frame)
        self.ui.lblFrames.setText("/ {}".format(self.end_frame-self.start_frame))

        self.ui.btnNext.clicked.connect(self.nextSegment)
        self.ui.btnPrev.clicked.connect(self.prevSegment)
        self.ui.sbxSegments.valueChanged.connect(self.sbxSegments)

        self.ui.slFrame.valueChanged.connect(self.sliderChange)
        self.ui.sbxFrameCurrent.valueChanged.connect(self.sbxChange)

        self.ui.btnOcr.clicked.connect(self.Ocr)
        self.frameChange(self.current_frame)

    def Ocr(self):
        for line in self.final_segs:
            liam_ocr.wordSeperation(line)

    def sbxSegments(self):
        new_segment = self.ui.sbxFrameCurrent.value()
        self.segmentChanger(new_segment)

    def prevSegment(self):
        self.ui.sbxFrameCurrent.setValue(self.current_segment-1)
        self.segmentChanger(self.current_segment-1)

    def nextSegment(self):
        if self.current_segment < len(self.segments) - 1:
            self.ui.sbxFrameCurrent.setValue(self.current_segment+1)
            self.segmentChanger(self.current_segment+1)
        else:
            self.finish()

    def finish(self):
        print("finish")
        return

    def segmentChanger(self,segment_no):
        segment_no %= len(self.segments)

        self.ui.btnPrev.setEnabled(True)
        self.ui.btnNext.setText("Next Segment")
        if segment_no == 0:
            self.ui.btnPrev.setEnabled(False)
        if segment_no == len(self.segments)-1:
            self.ui.btnNext.setText("Finish")

        print(len(self.cyrillics))

        self.cyrillics[self.current_segment] = self.ui.texCyrillic.toPlainText()
        self.translated[self.current_segment] = self.ui.texEnglish.toPlainText()

        self.current_segment = segment_no

        self.ui.texCyrillic.setPlainText(self.cyrillics[self.current_segment])
        self.ui.texEnglish.setPlainText(self.translated[self.current_segment])

        self.start_frame = self.segments[segment_no][0]
        self.end_frame = self.segments[segment_no][1]
        self.current_frame = int((self.start_frame+self.end_frame)/2.0)

        self.ui.slFrame.setMaximum(self.end_frame-self.start_frame)
        self.ui.sbxFrameCurrent.setMaximum(self.end_frame-self.start_frame)
        self.ui.lblFrames.setText("/ {}".format(self.end_frame-self.start_frame))
        self.frameChange(self.current_frame)

    def sliderChange(self):
        frame_no = self.ui.slFrame.value()
        self.ui.sbxFrameCurrent.setValue(frame_no)
        self.frameChange(frame_no + self.start_frame)

    def sbxChange(self):
        frame_no = self.ui.sbxFrameCurrent.value()
        self.ui.slFrame.setValue(frame_no)
        self.frameChange(frame_no + self.start_frame)

    def frameChange(self,frame_no):
        frame_no = frame_no % self.end_frame

        if self.current_frame != (frame_no - 1):
            self.cap.set(1,frame_no)
        if (self.current_frame != frame_no):
            ret, frame = self.cap.read()
            self.load_image(frame)

        self.current_frame = frame_no

    def load_image(self,frame):
        frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(frame2, frame2.shape[1], frame2.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.ui.lblFrame.setPixmap(pix)

        self.img_final = liam_ocr.binarize(frame)
        self.final_segs = liam_ocr.characterSegmentation(self.img_final)
        #print(max(markers.flatten()))

        red = np.zeros((frame.shape[0],frame.shape[1]), np.uint8)
        red[:,:] = 127
        for line in self.final_segs:
            for char in line:
                y1 = char['vert'][0]
                y2 = char['vert'][1]
                x1 = char['hor'][0]
                x2 = char['hor'][1]
                red[y1:y2,x1:x2] = char['subpic']

        col = cv2.cvtColor(red, cv2.COLOR_GRAY2RGB)
        img = QtGui.QImage(col, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.ui.lblGray.setPixmap(pix)

class MessageWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        message_form, message_base = uic.loadUiType('message.ui')
        self.ui = message_form()
        self.ui.setupUi(self)

class CaptureWindow(QtWidgets.QMainWindow):
    current_segment = 0
    start_frame = 0
    end_frame = 0
    segments = []
    final_segs = None
    img_final = None
    current_frame = 0
    cap = None
    captured = []

    def __init__(self, parent = None):
        capture_form, capture_base = uic.loadUiType('capture.ui')
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = capture_form()
        self.ui.setupUi(self)

    def load(self, cap_in,segments_in):
        self.cap = cap_in
        self.segments = segments_in
        self.current_segment = 0

        self.segmentChanger(self.current_segment)
        self.cap.set(1,self.current_frame)
        ret, frame = self.cap.read()
        self.load_image(frame)
        self.ui.lblFrames.setText("/ {}".format(self.end_frame-self.start_frame))
        self.ui.lblRemaining.setText("Remaining: {}".format(len(self.segments)-self.current_segment))

        self.ui.slFrame.valueChanged.connect(self.sliderChange)
        self.ui.sbxFrameCurrent.valueChanged.connect(self.sbxChange)

        self.frameChange(self.current_frame)
        self.ui.btnCapture.clicked.connect(self.capture)


    def capture(self):
        capture = {'final_segs':self.final_segs,'frame_no':self.current_frame}
        self.captured += [capture]
        if self.current_segment + 1 == len(self.segments):
            self.mesapp = MessageWindow()
            self.mesapp.ui.lblMessage.setText("Now resizing subimages...")
            self.mesapp.show()
            self.hide()
            print("Dump captured")
            with open('data.pickle', 'wb') as f:
                # Pickle the 'data' dictionary using the highest protocol available.
                pickle.dump(self.captured, f, pickle.HIGHEST_PROTOCOL)
            with open('data.pickle', 'rb') as f:
                #            The protocol version used is detected automatically, so we do not
                # have to specify it.
                self.captured = pickle.load(f)
            raws = liam_ocr.resCaptures(self.captured)
            self.mesapp.hide()
            self.mesapp.ui.lblMessage.setText("Now clustering subimages...")
            self.mesapp.show()
            liam_ocr.characterCluster(raws)
            print("done!")
        else:
            self.segmentChanger(self.current_segment+1)
            self.ui.lblRemaining.setText("Remaining: {}".format(len(self.segments)-self.current_segment))

    def segmentChanger(self,segment_no):
        segment_no %= len(self.segments)

        self.current_segment = segment_no

        self.start_frame = self.segments[segment_no][0]
        self.end_frame = self.segments[segment_no][1]
        self.current_frame = int((self.start_frame+self.end_frame)/2.0)

        self.ui.slFrame.setMaximum(self.end_frame-self.start_frame)
        self.ui.sbxFrameCurrent.setMaximum(self.end_frame-self.start_frame)
        self.ui.slFrame.setValue(self.current_frame)
        self.ui.sbxFrameCurrent.setValue(self.current_frame)
        self.ui.lblFrames.setText("/ {}".format(self.end_frame-self.start_frame))
        self.frameChange(self.current_frame)

    def sliderChange(self):
        frame_no = self.ui.slFrame.value()
        self.ui.sbxFrameCurrent.setValue(frame_no)
        self.frameChange(frame_no + self.start_frame)

    def sbxChange(self):
        frame_no = self.ui.sbxFrameCurrent.value()
        self.ui.slFrame.setValue(frame_no)
        self.frameChange(frame_no + self.start_frame)

    def frameChange(self,frame_no):
        frame_no = frame_no % self.end_frame

        if self.current_frame != (frame_no - 1):
            self.cap.set(1,frame_no)
        if (self.current_frame != frame_no):
            ret, frame = self.cap.read()
            self.load_image(frame)

        self.current_frame = frame_no

    def load_image(self,frame):
        frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(frame2, frame2.shape[1], frame2.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.ui.lblFrame.setPixmap(pix)

        self.img_final = liam_ocr.binarize(frame)
        self.final_segs = liam_ocr.characterSegmentation(self.img_final)
        #print(max(markers.flatten()))

        red = np.zeros((frame.shape[0],frame.shape[1]), np.uint8)
        red[:,:] = 127
        for line in self.final_segs:
            for char in line:
                y1 = char['vert'][0]
                y2 = char['vert'][1]
                x1 = char['hor'][0]
                x2 = char['hor'][1]
                red[y1:y2,x1:x2] = char['subpic']

        col = cv2.cvtColor(red, cv2.COLOR_GRAY2RGB)
        img = QtGui.QImage(col, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.ui.lblGray.setPixmap(pix)

class MainWindow(QtWidgets.QMainWindow):
    MESSAGE = "Hello!"
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = form_class()
        self.ui.setupUi(self)
        self.ui.btnNewProject.clicked.connect(self.openMovie)

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
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())
