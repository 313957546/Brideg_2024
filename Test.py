from PySide6.QtCore import Qt, QModelIndex, QSortFilterProxyModel
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QApplication, QComboBox, QStyledItemDelegate, QTableView, QWidget
from collections import defaultdict

# 定义联动数据
data = {
    "河南": {
        "安阳": {
            "北关区": ["某某街道", "其他街道"],
            "其他区": ["某街道"]
        },
        "其他城市": {
            "某区": ["某街道"]
        }
    },
    "其他省份": {
        # ...其他数据
    }
}


# 自定义委托实现联动逻辑
class LinkedComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, data_linkage, parent=None):
        super().__init__(parent)
        self.data_linkage = data_linkage
        self.parent_model = None
        self.prev_indexes = defaultdict(int)  # 用于记录每一级前一个选择的索引

    def setParentModel(self, model):
        self.parent_model = model

    def createEditor(self, parent, option, index):
        combobox = QComboBox(parent)
        current_level = index.column()
        current_data = self.data_linkage
        for i in range(current_level):  # 根据当前级别回溯获取上级选择
            prev_index = self.prev_indexes[index.row(), i]
            current_data = current_data[list(current_data.keys())[prev_index]]

        combobox.addItems(list(current_data.keys()))
        combobox.currentIndexChanged.connect(lambda idx: self.updatePrevIndexes(index, idx))
        return combobox

    def updatePrevIndexes(self, index, new_index):
        self.prev_indexes[index.row(), index.column()] = new_index
        # 更新当前行后续列的模型数据，使其清空或根据新的选择重新设置
        for col in range(index.column() + 1, 4):  # 假设只有四列
            self.parent_model.setData(self.parent_model.index(index.row(), col), "", Qt.ItemDataRole.EditRole)
        self.commitData.emit(self.sender())

    def setEditorData(self, editor, index):
        # 这里简化处理，实际应用中可能需要更复杂的逻辑来处理初始值
        pass

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), Qt.ItemDataRole.EditRole)


# 主程序
app = QApplication([])

# 创建数据模型
model = QStandardItemModel(0, 4)  # 假设有4列
proxy_model = QSortFilterProxyModel()
proxy_model.setSourceModel(model)
table_view = QTableView()
table_view.setModel(proxy_model)

# 初始化行数
for _ in range(5):  # 假设初始化5行
    model.insertRow(model.rowCount())

# 设置委托
delegate = LinkedComboBoxDelegate(data)
delegate.setParentModel(model)
for col in range(4):
    table_view.setItemDelegateForColumn(col, delegate)

table_view.show()
app.exec()
