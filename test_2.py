from faker import Faker
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableView, QHeaderView
from PySide6.QtGui import QStandardItemModel, QStandardItem


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.fake = Faker(locale='zh_cn')
        self.data = [[self.fake.name(), self.fake.phone_number(), self.fake.address()] for _ in range(100)]


        # 创建模型
        self.model = QStandardItemModel()
        for indexRow ,row in enumerate(self.data):
            for indexColumn, column in enumerate(row):
                # 创建输入需要行索引 列索引
                self.model.setItem(indexRow,indexColumn,QStandardItem(column))


        # print(self.model)
        self.table= QTableView()
        self.table.setModel(self.model)

        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

        # self.table_2 = QTableView()
        # self.table_2.setModel(self.model)



        self.mianlayout = QVBoxLayout()
        self.mianlayout.addWidget(self.table)
        # self.mianlayout.addWidget(self.table_2)
        self.setLayout(self.mianlayout)
if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()