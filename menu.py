from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.Qt import Qt
import sys

class Menu():
    def __init__(self): 
        red_meat = {"name" : "red meat", "choices": ["t-bone", "filet mignon", "ribeye"]}
        poultry = {"name": "poultry", "choices": ["chicken thighs", "chicken tenders", "chicken breasts"]}
        fish = {"name":"fish", "choices": ["salmon", "tuna", "trout"]}

        categories = [red_meat, poultry, fish]


        app     = QtWidgets.QApplication(sys.argv)
        tree    = QtWidgets.QTreeWidget()
        headerItem  = QtWidgets.QTreeWidgetItem()
        item    = QtWidgets.QTreeWidgetItem()

        for i in categories:
            parent = QtWidgets.QTreeWidgetItem(tree)
            parent.setText(0, "{}".format(i['name']))
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            for x in i['choices']:
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, "{}".format(x))
                child.setCheckState(0, Qt.Unchecked)
        tree.show() 


        sys.exit(app.exec_())
        


if __name__ == '__main__':
    menu = Menu()

