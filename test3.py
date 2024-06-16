import json
import sys
import pandas as pd
from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtGui import QGuiApplication, QStandardItemModel, QStandardItem, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, \
    QTableWidgetItem, QFileDialog, QTableView, QToolBar, QDialog, QSizePolicy,QComboBox
from edit_dise import LinkedComboBoxDelegate
#
# data = {}
# with open('./res/result.json', 'r') as f:
#     data = json.load(f)
#
#
# def find_in_nested_dict(nested_dict, key_path) -> dict:
#     """
#     在多层嵌套的字典中根据键路径查找值。
#
#     :param nested_dict: 多层嵌套的字典
#     :param key_path: 一系列的键，组成路径来指向目标值，例如 ['key1', 'key2', 'key3']
#     :return: 查找到的值，如果路径不存在则返回None
#     """
#     if not key_path:  # 如果路径为空，说明已经到达最底层但未找到匹配的键
#         return None
#     current_key = key_path[0]
#     if current_key in nested_dict:
#         if len(key_path) == 1:  # 如果这是路径中的最后一个键
#             return nested_dict[current_key]
#         else:  # 否则，继续在下一层字典中搜索
#             return find_in_nested_dict(nested_dict[current_key], key_path[1:])
#     else:
#         return None  # 当前键不在字典中，直接返回None


# 示例
app = QApplication(sys.argv)
MainWindow = QMainWindow()
MainWindow.setWindowTitle('test')
MainWindow.resize(800, 600)
combobox_1 = QComboBox()
combobox_2 = QComboBox()
combobox_3 = QComboBox()
combobox_4 = QComboBox()
layout = QVBoxLayout()
layout.addWidget(combobox_1)
layout.addWidget(combobox_2)
layout.addWidget(combobox_3)
layout.addWidget(combobox_4)

combobox_1.addItems(data.keys())
print((find_in_nested_dict(data,[combobox_1.currentText()])).keys())
combobox_2.addItems((find_in_nested_dict(data,[combobox_1.currentText()])).keys())
cen = QWidget()
cen.setLayout(layout)
MainWindow.setCentralWidget(cen)
MainWindow.show()
sys.exit(app.exec_())


# 查找目标值
key_path = ['圬工拱桥', '桥面', '水泥混凝土桥面铺装', '坑洞']
value = find_in_nested_dict(data, key_path)
print(type(value))  # 输出应为 'target_value'
print(value.keys())
