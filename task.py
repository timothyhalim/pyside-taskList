import traceback
from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QAction, QApplication, QHBoxLayout, QLabel, QMenu, QWidget

from enum import Enum

class Status(Enum):
    DISABLED = 0
    ENABLED = 1
    RUNNING = 2
    DONE = 3
    ERROR = 4

class StatusIcon(QLabel):
    def __init__(self, parent=None):
        super(StatusIcon, self).__init__(parent=parent)
        self.setFixedHeight(20)
        self.setFixedWidth(20)
        self.setStatus("ENABLED")

    def __repr__(self):
        return self.status

    def __str__(self):
        return self.status

    def setStatus(self, status):
        self.status = status
        if status == "ENABLED":
            self.setStyleSheet("background-color:Gray;")
        elif status == "DISABLED":
            self.setStyleSheet("background-color:Black;")
        elif status == "RUNNING":
            self.setStyleSheet("background-color:Orange;")
        elif status == "DONE":
            self.setStyleSheet("background-color:Green;")
        elif status == "ERROR":
            self.setStyleSheet("background-color:Red;")

class Command(QObject):
    stateChanged = Signal(str)
    onError = Signal(str)

    def __init__(self, command, parent=None):
        super(Command, self).__init__(parent=parent)
        self.command = command
        self.errorMsg = ""
        self.setState("ENABLED")

    def setState(self, state):
        self.state = state
        self.stateChanged.emit(self.state)

    def disable(self):
        self.setState("DISABLED")

    def run(self):
        if not self.state == "DISABLED":
            self.setState("RUNNING")
            QApplication.processEvents() 
            try:
                if isinstance(self.command, str):
                    exec(self.command)
                else:
                    self.command()
                self.setState("DONE")
            except:
                self.setState("ERROR")
                self.errorMsg = traceback.format_exc()
                self.onError.emit(self.errorMsg)
                print(self.errorMsg)

class BaseTask(QWidget):
    def __init__(self, title="", info="", parent=None, **kwargs):
        super(BaseTask, self).__init__(parent=parent)
        
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(1,1,1,1)
        self.status = StatusIcon()
        self.title = QLabel()

        for w in (self.status, self.title):
            self.mainLayout.addWidget(w)
            
        self.setTitle(title)
        self.setInfo(info)

    def setTitle(self, title):
        self.title.setText(title)

    def setInfo(self, info):
        self.info = info
        self.setToolTip(info)

class SingleTask(BaseTask):
    def __init__(self, title="", command="", info="", parent=None, **kwargs):
        super(SingleTask, self).__init__(title=title, info=info, parent=parent, **kwargs)
        
        if command:
            self.setCommand(command)

    def setCommand(self, command):
        self.command = Command(command)
        self.command.stateChanged.connect(self.status.setStatus)
        self.command.onError.connect(self.onError)
        self.status.update()

    def onError(self, errorMsg):
        self.setToolTip(
            self.info + "\n" + "Error:" + "\n" + errorMsg
        )
        
    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        enable = QAction("Enable")
        disable = QAction("Disable")
        run = QAction("Run")
        copyError = QAction("Copy Error Message")
        if self.command.state == "DISABLED":
            contextMenu.addAction(enable)
        else:
            contextMenu.addAction(disable)
            contextMenu.addAction(run)
        
        if self.command.state == "ERROR":
            contextMenu.addAction(copyError)

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == enable:
            self.command.setState("ENABLED")
        elif action == disable:
            self.command.setState("DISABLED")
        elif action == run:
            self.run()
        elif action == copyError:
            print("COPY")

    def run(self):
        self.setToolTip(self.info)
        self.command.run()

class GroupTask(BaseTask):
    def __init__(self, title="", info="", parent=None, **kwargs):
        super(GroupTask, self).__init__(title=title, info=info, parent=parent, **kwargs)

        self.tasks = []

    def addTask(self, task):
        if isinstance(task, dict):
            task = SingleTask(**task)

        if isinstance(task, SingleTask):
            task.command.stateChanged.connect(self.checkStatus)
            self.tasks.append(task)
            return task

    def getTask(self):
        return self.tasks

    def checkStatus(self, status=None):
        for task in self.tasks:
            ...

    def run(self):
        self.setToolTip(self.info)
        self.command.run()


if __name__ == "__main__":
    apps = QApplication()
    task = SingleTask(**{
                    "title":"Task",
                    "info":"Task Tooltip"
                })
    task.setCommand("""
import time

for i in range(5):
    print(i)
    time.sleep(1)
    if i == 4:
        raise Exception
    """)
    task.show()
    apps.exec_()
