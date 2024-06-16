from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QComboBox, QStyledItemDelegate, QTableView
import json
import Disease

data = {}

with open('./res/病害数据.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


class LinkedComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_linkage = data
        self.prev_indexes = {}

    def createEditor(self, parent, option, index):
        """
        创建用于编辑的控件，即一个联动的下拉列表框。
        ...
        """
        col = index.column()
        row = index.row()

        # 确保当前行在prev_indexes中有记录，如果没有则初始化一个空字典
        # self.prev_indexes.setdefault(row, {})
        # 根据当前列来确定需要安装那一个 下拉列表
        print('col= ', col, '  row=', row)
        if col == 1:
            # 如果双击的时第一列（就是第2）
            combobox = QComboBox(parent)
            combobox.addItems(self.data_linkage.keys())
            # 需要绑定更新 传递当前行和列的索引
            combobox.currentIndexChanged.connect(
                lambda idx, index=index: self.updatePrevIndexes(row, col, index,combobox.currentText()))
            return combobox
        elif col == 2:
            combobox = QComboBox(parent)
            model = index.model()
            # 获得前一行的文本内容
            prve_col_data = model.data(model.index(row, col - 1))
            if prve_col_data == None:
                return combobox
            # 创建地址list
            find_list = []
            find_list.append(prve_col_data)
            add_list = self.find_in_nested_dict(self.data_linkage, find_list)
            combobox.addItems(add_list)
            # combobox.blockSignals(False)
            combobox.currentIndexChanged.connect(
                lambda idx, index=index: self.updatePrevIndexes(row, col, index,combobox.currentText()))
            return combobox

        elif col == 3:
            combobox = QComboBox(parent)
            model = index.model()
            # 获得前一行的文本内容
            prve_col_data_1 = model.data(model.index(row, col - 1))
            prve_col_data_2 = model.data(model.index(row, col - 2))
            if prve_col_data_1 == None:
                return combobox
            # 创建地址list
            find_list = []
            find_list.append(prve_col_data_2)
            find_list.append(prve_col_data_1)
            # print(find_list)
            add_list = self.find_in_nested_dict(self.data_linkage, find_list)
            combobox.addItems(add_list)

            combobox.currentIndexChanged.connect(
                lambda idx, index=index: self.updatePrevIndexes(row, col, index,combobox.currentText()))
            return combobox
        elif col == 4:
            combobox = QComboBox(parent)
            model = index.model()
            # 获得前一行的文本内容
            prve_col_data_1 = model.data(model.index(row, col - 1))
            prve_col_data_2 = model.data(model.index(row, col - 2))
            prve_col_data_3 = model.data(model.index(row, col - 3))
            if prve_col_data_1 == None:
                return combobox
            # 创建地址list
            find_list = []
            find_list.append(prve_col_data_3)
            find_list.append(prve_col_data_2)
            find_list.append(prve_col_data_1)
            # print(find_list)
            add_list = self.find_in_nested_dict(self.data_linkage, find_list)
            combobox.addItem('-请选择-')
            combobox.addItems(add_list)

            combobox.currentIndexChanged.connect(
                lambda idx, index=index: self.updatePrevIndexes(row, col, index,combobox.currentText()))
            return combobox
        else:
            pass


    def find_in_nested_dict(self, nested_dict, key_path) -> dict:
        """
        病害查询


        在多层嵌套的字典中根据键路径查找值。

        :param nested_dict: 多层嵌套的字典
        :param key_path: 一系列的键，组成路径来指向目标值，例如 ['key1', 'key2', 'key3']
        :return: 查找到的值，如果路径不存在则返回None
        """
        if '-请选择-' in key_path:
            return []
        if not key_path:  # 如果路径为空，说明已经到达最底层但未找到匹配的键
            return None
        current_key = key_path[0]
        if current_key in nested_dict:
            if len(key_path) == 1:  # 如果这是路径中的最后一个键
                return nested_dict[current_key]
            else:  # 否则，继续在下一层字典中搜索
                return self.find_in_nested_dict(nested_dict[current_key], key_path[1:])
        else:
            return None  # 当前键不在字典中，直接返回None

    def updatePrevIndexes(self, row, col, index,current_text):
        print('col发生变换', col)
        model = index.model()  # 使用index获取模型引用
        if col > 0 and col < 4:
            for clear_col in range(col + 1, 7):
                cell_index = model.index(row, clear_col)  # 使用model获取新的cell_index
                model.setData(cell_index, "-请选择-", Qt.EditRole)

        elif col == 4:
            print('更新填写max,构件id ')
            find_list = []
            for col_2 in range(1, 4):
                find_list.append(model.data(model.index(row, col_2)))

            find_list.append(current_text)
            dict = self.find_in_nested_dict(self.data_linkage, find_list)
            model.setData(model.index(row, 5), dict['构件ID'])
            model.setData(model.index(row, 6), dict['最大标度'])
        elif col == 7:

            pass
    def clearLaterIndexes(self, row, start_col):
        """清除指定行从start_col开始的所有后续层级的索引"""
        for col in range(start_col, len(self.prev_indexes[row])):
            if col in self.prev_indexes[row]:
                del self.prev_indexes[row][col]

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText())
