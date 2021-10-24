from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QAbstractItemView, QApplication, QTreeView
from task import Task

class TaskList(QTreeView):
    def __init__(self, parent=None):
        super(TaskList, self).__init__(parent=parent)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['TaskList'])
        self.setModel(model)
        self.setUniformRowHeights(True)

        for i in range(3):
            parent = self.addTask({
                "title":"Task "+str(i),
                "info":"Task "+str(i),
                "command":"print('task 1')"
            })
            for j in range(3):
                sub = self.addSubTask({
                    "title":"Task "+str(j),
                    "command":"print('task 1')"
                }, parentTask=parent)

    def addTask(self, task):
        if isinstance(task, dict):
            task = Task(**task)

        if isinstance(task, Task):
            item = QStandardItem()
            self.model().appendRow(item)
            self.setIndexWidget(item.index(), task)
            task.item = item
            return task

    def addGroupTask(self, title="", tasks=[] ):
        tasksObject = []
        for task in tasks:
            if isinstance(task, dict):
                task = Task(**task)
            
            if isinstance(task, Task):
                tasksObject.append(task)

        # if isinstance(task, Task):
        #     item = QStandardItem()
        #     parentTask.item.appendRow(item)
        #     self.setIndexWidget(item.index(), task)
        #     task.item = item
        #     return task
        
if __name__ == "__main__":
    apps = QApplication()
    task = TaskList()
    task.show()
    apps.exec_()
