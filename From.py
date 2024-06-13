import sys
import pandas as pd
from PySide6.QtGui import QGuiApplication, QStandardItemModel, QStandardItem, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, \
    QTableWidgetItem, QFileDialog, QTableView, QToolBar, QDialog


class QtMainWindow(QMainWindow):
    def __init__(self):
        app = QApplication(sys.argv)
        # 初始化窗口
        super().__init__()
        # 设置窗口标题
        self.setWindowTitle("桥梁技术状况评定系统")
        # 获取主屏幕的几何信息
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        # 计算窗口尺寸为屏幕宽高的1/2
        window_width = screen_geometry.width() // 2
        window_height = screen_geometry.height() // 2
        # 设置窗口大小
        self.setGeometry(window_width // 2, window_height // 2, window_width, window_height)

        # 创建表格
        self.table_info = QTableView()
        self.table_quantity = QTableView()
        self.table_disease = QTableView()
        # 创建表格模型
        self.table_info_model = QStandardItemModel()
        self.table_quantity_model = QStandardItemModel()
        self.table_disease_model = QStandardItemModel()

        # 将表格模型设置为表格的模型
        self.table_info.setModel(self.table_info_model)
        # self.table_quantity.setModel(self.table_quantity_model)
        # self.table_disease.setModel(self.table_disease_model)

        self.toolBar = QToolBar('工具栏')
        self.Toolbar_init()
        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.toolBar)
        # 将表格添加到布局
        layout.addWidget(self.table_info)
        # 创建数量表对话框
        self.table_quantity.setFixedHeight(70)
        self.table_quantity.setFixedWidth(self.width())
        self.table_quantity_QDialog = QDialog(self)
        self.table_quantity_QDialog.setWindowTitle("数量表")
        layout_table = QVBoxLayout()
        layout_table.addWidget(self.table_quantity)
        self.table_quantity_QDialog.setLayout(layout_table)

        # 创建病害表对话框
        self.table_disease.setFixedHeight(self.height())
        self.table_disease.setFixedWidth(self.width())
        self.table_disease_QDialog = QDialog(self)
        self.table_disease_QDialog.setWindowTitle("病害表")
        layout_table_d = QVBoxLayout()
        toolBar_d = QToolBar('工具栏')
        toolBar_d.addAction('添加', self.add_disease)
        toolBar_d.addAction('删除', self.delete_disease)
        layout_table_d.addWidget(toolBar_d)
        layout_table_d.addWidget(self.table_disease)
        self.table_disease_QDialog.setLayout(layout_table_d)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.show()
        sys.exit(app.exec_())

    def add_disease(self):
        pass

    def delete_disease(self):
        pass

    def Toolbar_init(self):
        self.toolBar.addAction('打开文件', self.open_file)
        self.toolBar.addAction('保存文件', self.save_file)
        self.toolBar.addAction('show数量表', self.show_qunantity)
        self.toolBar.addAction('show病害表', self.show_disease)

    def show_qunantity(self):
        # self.table_quantity.show()
        self.table_quantity_QDialog.move(self.x(), self.y() + self.height() + 20)
        self.table_quantity_QDialog.show()

    def show_disease(self):
        self.table_disease_QDialog.move(self.x(), self.y())
        self.table_disease_QDialog.show()

    # 打开文件
    def open_file(self):
        file_dialog = QFileDialog()  # 创建文件对话框
        file_path, _ = file_dialog.getOpenFileName(self, "打开文件", "", "Excel 文件 (*.xlsx *.xls)")  # 获取选择的文件路径
        if file_path:  # 如果有选择文件
            try:
                # 读取 Excel 文件
                self.file_path = file_path
                excel_data = pd.read_excel(file_path, sheet_name=None)
                # 提取桥梁信息、数量表和病害表
                self.bridge_sheet = excel_data.get("桥梁信息表")
                self.quantity_sheet = excel_data.get("数量表")
                self.disease_sheet = excel_data.get("病害表")
                # 将数据连接到表格model
                self.pd_to_model(self.bridge_sheet, self.table_info_model)
                self.pd_to_model(self.quantity_sheet, self.table_quantity_model)
                self.pd_to_model(self.disease_sheet, self.table_disease_model)

                # 根据桥梁ID的关联性来填充表格数据


            except Exception as e:
                print("加载文件出错:", e)

    # pandas DataFrame 转换为QStandardItemModel
    def pd_to_model(self, pd_data: pd.DataFrame, table_model: QStandardItemModel):
        # 清空表格
        table_model.clear()
        table_model.setHorizontalHeaderLabels(pd_data.columns.tolist())
        for row_index, row_data in pd_data.iterrows():
            item_list = []
            for col_index, value in row_data.items():
                item = QStandardItem(str(value))  # 转换为字符串，因为QStandardItem需要字符串
                item_list.append(item)
            table_model.insertRow(row_index, item_list)

    # 保存文件
    def save_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "保存文件", "", "Excel 文件 (*.xlsx *.xls)")
        if file_path:
            try:
                with pd.ExcelWriter(file_path) as writer:
                    # model转换为DataFrame 再写出文件
                    self.model_to_pd_dataframe(self.table_info_model).to_excel(writer, sheet_name="桥梁信息表",
                                                                               index=False)
                    self.model_to_pd_dataframe(self.table_quantity_model).to_excel(writer, sheet_name="数量表",
                                                                                   index=False)
                    self.model_to_pd_dataframe(self.table_disease_model).to_excel(writer, sheet_name="病害表",
                                                                                  index=False)
                print("保存成功")
            except Exception as e:
                print("保存文件出错:", e)
            except Exception as e:
                print("保存文件出错:", e)

    # 将QStandardItemModel转换为Pandas DataFrame
    def model_to_pd_dataframe(self, model):
        """
        将QStandardItemModel转换为Pandas DataFrame。

        参数:
        model -- QStandardItemModel实例

        返回:
        DataFrame -- 包含模型数据的Pandas DataFrame
        """
        column_count = model.columnCount()
        row_count = model.rowCount()

        # 获取表头
        headers = [model.headerData(column, Qt.Horizontal) for column in range(column_count)]

        # 初始化数据列表
        data = []
        for row in range(row_count):
            row_data = []
            for column in range(column_count):
                index = model.index(row, column)
                item = model.data(index, Qt.DisplayRole)
                row_data.append(item)
            data.append(row_data)

        # 创建DataFrame
        df = pd.DataFrame(data, columns=headers)
        return df


if __name__ == "__main__":
    QtMainWindow()
