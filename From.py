import sys
import pandas as pd
from PySide6.QtCore import QSortFilterProxyModel,QItemSelection
from PySide6.QtGui import QGuiApplication, QStandardItemModel, QStandardItem, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, \
    QTableWidgetItem, QFileDialog, QTableView, QToolBar, QDialog, QSizePolicy,QHeaderView

from edit_dise import LinkedComboBoxDelegate


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
        window_width = screen_geometry.width() * 0.8
        window_height = screen_geometry.height() * 0.8
        # 设置窗口大小
        self.setGeometry(window_width * 0.1, window_height * 0.1, window_width, window_height)

        # 创建表格
        self.table_info = QTableView()
        # 设置选择行为 单行选中
        self.table_info.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_info.setSortingEnabled(True)
        self.table_quantity = QTableView()


        self.table_disease = QTableView()
        # 设置选择行为 单行选中
        self.table_disease.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        # 设置自动缩放表头
        # self.table_disease.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # 设置排序
        self.table_disease.setSortingEnabled(True)
        # 创建表格模型
        self.table_info_model = QStandardItemModel()
        # 其他模型
        self.table_quantity_model = QStandardItemModel()
        self.table_disease_model = QStandardItemModel()

        # 过滤显示模型
        self.show_table_quantity_model = QStandardItemModel()
        self.show_table_disease_model = QStandardItemModel()

        # 将表格模型设置为表格的模型
        self.table_info.setModel(self.table_info_model)
        # 下面的两个是显示模型
        # self.table_disease.setModel(self.show_table_disease_model)
        # self.table_quantity.setModel(self.show_table_quantity_model)

        # 设置委托
        delegate = LinkedComboBoxDelegate()
        # 委托有1-7
        for col_1 in range(1, 7):
            self.table_disease.setItemDelegateForColumn(col_1, delegate)

        self.toolBar = QToolBar('工具栏')
        self.Toolbar_init()
        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.toolBar)
        # 将表格添加到布局
        layout.addWidget(self.table_info)
        # 创建数量表对话框
        self.table_quantity.setFixedHeight(70)
        self.table_quantity.setFixedWidth(self.width() - 20)
        self.table_quantity_QDialog = QDialog(self)
        self.table_quantity_QDialog.setWindowTitle("数量表")
        layout_table = QVBoxLayout()
        layout_table.addWidget(self.table_quantity)
        self.table_quantity_QDialog.setLayout(layout_table)

        # 创建病害表对话框
        # self.table_disease.setFixedHeight(self.height())
        self.table_disease.setFixedWidth(self.width() - 20)

        self.table_disease_QDialog = QDialog(self)
        self.table_disease_QDialog.setWindowTitle("病害表")

        layout_table_d = QVBoxLayout()
        toolBar_d = QToolBar('工具栏')
        toolBar_d.addAction('添加', self.add_disease)
        # toolBar_d.addAction('复制', self.copy_selected_disease)
        toolBar_d.addAction('删除', self.delete_disease)


        layout_table_d.addWidget(toolBar_d)
        layout_table_d.addWidget(self.table_disease)
        self.table_disease_QDialog.setLayout(layout_table_d)
        self.table_quantity.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.table_quantity.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        # 信号连接初始化
        self.connect_init()

        self.show()
        sys.exit(app.exec_())

    # 信号连接初始化
    def connect_init(self):
        # 连接信号 表格发生选中变化时候
        self.table_info.selectionModel().currentChanged.connect(self.on_info_table_selection_changed)
        # pass

    # 表格选中变化
    def on_info_table_selection_changed(self, current, previous):
        # 获取选中行的ID
        index = current.sibling(current.row(), 0)  # ID在第0列
        selected_id = self.table_info_model.data(index)

        print('info _table 选择发生变化', selected_id)

        self.show_table_quantity_model = self.create_filter_model(self.table_quantity_model, selected_id)
        self.show_table_disease_model = self.create_filter_model(self.table_disease_model, selected_id)
        self.table_quantity.setModel(self.show_table_quantity_model)

        self.table_disease.setModel(self.show_table_disease_model)
        self.show_table_disease_model.invalidateFilter()
        self.show_table_quantity_model.invalidateFilter()

    def create_filter_model(self, source_model, filter_id):
        """
        根据给定的模型和桥梁ID创建并返回一个新的过滤模型。

        参数:
        source_model -- 原始的QStandardItemModel对象
        filter_id -- 用于过滤的桥梁ID

        返回:
        QSortFilterProxyModel -- 过滤后的代理模型
        """
        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(source_model)

        # 自定义过滤逻辑
        def filter_accepts_row(row_source, parent):
            index = source_model.index(row_source, 0, parent)  # 假设ID在第0列
            id_value = source_model.data(index, Qt.ItemDataRole.DisplayRole)
            return id_value == str(filter_id)  # 比较ID值

        proxy_model.filterAcceptsRow = filter_accepts_row  # 覆盖默认的过滤接受行方法
        return proxy_model

    def add_disease(self):
        # 获取当前选中行的ID
        index = self.table_info.selectionModel().currentIndex()
        if not index.isValid():
            print("请先在桥梁信息表中选择一个项目。")
            return
        selected_id = self.table_info_model.data(index.sibling(index.row(), 0))

        # 计算列数
        column_count = self.table_disease_model.columnCount()

        # 创建新行数据，这里以示例填充数据，实际应用中应根据需求调整
        new_disease_row = [''] * column_count
        new_disease_row[0] = selected_id  # 假设第一列是ID，这里设置为选中桥梁的ID

        # 在模型末尾添加新行
        self.table_disease_model.appendRow([QStandardItem(item) for item in new_disease_row])

        # 如果有筛选模型，则需要刷新筛选模型以显示新增数据
        if isinstance(self.table_disease.model(), QSortFilterProxyModel):
            self.table_disease.model().invalidateFilter()

    def delete_disease(self):
        # 获取当前选中的索引
        indexes = self.table_disease.selectedIndexes()
        if not indexes:
            print("请先在病害表中选择要删除的行。")
            return

        # 通常只选择了一行，但这里处理多行选择的情况
        for index in indexes:
            if index.isValid():
                self.show_table_disease_model.removeRow(index.row())

        # 如果有筛选模型，则需要刷新筛选模型以反映删除操作
        if isinstance(self.table_disease.model(), QSortFilterProxyModel):
            self.table_disease.model().invalidateFilter()


    def Toolbar_init(self):
        self.toolBar.addAction('打开文件', self.open_file)
        self.toolBar.addAction('保存文件', self.save_file)
        self.toolBar.addAction('添加桥梁', self.add_item_to_table_info)
        self.toolBar.addAction('删除桥梁', self.delete_selected_rows)
        self.toolBar.addAction('显示数量表', self.show_qunantity)
        self.toolBar.addAction('显示病害表', self.show_disease)
        self.toolBar.addAction('开始计算', self.show_disease)
        self.toolBar.addAction('导出word', self.show_disease)
        self.toolBar.addAction('登录', self.show_disease)


    def show_qunantity(self):
        # self.table_quantity.show()
        self.table_quantity_QDialog.move(self.x(), self.y() + self.height() - 100)
        # self.table_quantity_QDialog.setWindowFlag(Qt.FramelessWindowHint)
        self.table_quantity_QDialog.show()

    def show_disease(self):
        self.table_disease_QDialog.move(self.x(), self.y() + 200)

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

    # info 删除桥梁
    # 添加方法
    def add_item_to_table_info(self):
        # 获取当前table_info的最大ID
        max_id = 0
        for row in range(self.table_info_model.rowCount()):
            id_item = self.table_info_model.item(row, 0)  # 假设ID在第一列
            if id_item is not None and id_item.text().isdigit():
                max_id = max(max_id, int(id_item.text()))
        new_id = max_id + 1

        # 添加新行到table_info_model
        new_items = [QStandardItem(str(new_id))]  # ID
        # ... 根据需要添加其他列的项
        self.table_info_model.appendRow(new_items)

        # 同步添加到table_quantity_model
        new_quantity_items = [QStandardItem(str(new_id))]  # 假设也使用ID作为第一列
        # ... 其他列的项
        self.table_quantity_model.appendRow(new_quantity_items)

    # 删除方法的完善
    def delete_selected_rows(self, linked_model=None):
        indexes = self.table_info.selectedIndexes()

        if not indexes:
            print("请先在病害表中选择要删除的行。")
            return
        # 通常只选择了一行，但这里处理多行选择的情况
        for index in indexes:
            id = index.sibling(index.row(), 0).data()
            self.delete_disease_table(self.table_disease_model,id)

            self.delete_disease_table(self.show_table_disease_model, id)

            if index.isValid():
                self.table_info_model.removeRow(index.row())



    # 修改delete_disease方法以使用新的删除逻辑
    #  删除病害指定ID
    def delete_disease_table(self, model,id):

        rows = []
        for row in range(model.rowCount()):
            index = model.index(row, 0)
            if model.data(index) == id:
                rows.append(row)
        for row_del in reversed(rows):
            model.removeRow(row_del)


if __name__ == "__main__":
    QtMainWindow()
