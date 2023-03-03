from PyQt5 import QtCore, QtGui, QtWidgets


class Widget(QtWidgets.QWidget):
    red_meat = {"name" : "red meat", "choices": ["t-bone", "filet mignon", "ribeye"]}
    poultry = {"name": "poultry", "choices": ["chicken thighs", "chicken tenders", "chicken breasts"]}
    fish = {"name":"fish", "choices": ["salmon", "tuna", "trout"]}

    categories = [red_meat, poultry, fish]


    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        lay = QtWidgets.QVBoxLayout(self)
        tree = QtWidgets.QTreeWidget()
        tree.setColumnCount(1)
        lay.addWidget(tree)

        for i in self.categories:
            parent_it = QtWidgets.QTreeWidgetItem("{}".format(i))
            tree.addTopLevelItem(parent_it)
            for j in range(5):
                it = QtWidgets.QTreeWidgetItem(["{}-{}-{}".format(i, j, l) for l in range(2)])
                parent_it.addChild(it)
        tree.expandAll()

        tree.itemClicked.connect(self.onItemClicked)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, it, col):
        print(it.text(col))


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
