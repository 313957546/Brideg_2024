from PySide6.QtWidgets import QComboBox, QApplication, QWidget, QVBoxLayout, QTableView, QMainWindow, QTableWidgetItem, \
    QItemDelegate
from PySide6.QtCore import Qt

# 示例数据结构简化版
data_structure = {
    "河南": {
        "安阳": {
            "北关区": ["某某街道", "其他街道"]
        },
        # ...其他城市和区县
    },
    # ...其他省份
}


class CustomDelegate(QItemDelegate):
    def __init__(self, parent=None, options=None):
        super().__init__(parent)
        self.options = options or {}

    def createEditor(self, parent, option, index):
        if index.column() == 0:  # 假设联动发生在第一列
            editor = QComboBox(parent)
            current_level = index.row() // 4  # 简单假设每四级为一级
            current_key = next((k for k in reversed(list(self.options.keys())) if current_level >= len(k.split('/'))),
                               None)
            if current_key:
                editor.addItems(self.options[current_key])
            editor.currentIndexChanged.connect(lambda idx: self.commitData.emit(editor))
            return editor
        return super().createEditor(parent, option, index)


class QtMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table_disease = QTableView()
        self.delegate = CustomDelegate(options=data_structure)
        self.table_disease.setItemDelegate(self.delegate)
        # ...其他初始化代码

        # 假设数据已填充到模型中
        # 注意：实际应用中，您需要根据联动逻辑动态调整数据模型中的内容，这里未展开具体实现


if __name__ == "__main__":
    app = QApplication([])
    window = QtMainWindow()
    window.show()
    app.exec()
