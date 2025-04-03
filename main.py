import sys
import os
from PyQt5 import QtWidgets, uic


class RenderSubmissionTool(QtWidgets.QMainWindow):
    def __init__(self):
        super(RenderSubmissionTool, self).__init__()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(base_dir, "ui/submitRender_ui.ui")
        # Load the UI
        uic.loadUi(ui_file, self)
        self.setWindowTitle("Render Submission Tool")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = RenderSubmissionTool()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
