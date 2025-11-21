"""
协同表格视图 - 使用.ui文件的版本
直接加载collaborative_table.ui文件，不再手动创建UI组件
"""

import os
from PyQt5.QtWidgets import (
    QWidget, QTableWidgetItem, QHeaderView, QCheckBox, QPushButton, 
    QMenu, QAction, QAbstractItemView, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5 import uic

from src.common.base import BaseWidget
from src.common.utils import ResourceUtils


class CollaborativeTableView(BaseWidget):
    """协同表格视图类 - 使用.ui文件版本"""
    
    # 定义信号
    item_selected = pyqtSignal(list)  # 选中项变化
    item_action_triggered = pyqtSignal(str, int, str)  # 操作触发 (action, row, item_id)
    search_triggered = pyqtSignal(str)  # 搜索触发
    filter_changed = pyqtSignal(str)  # 过滤器变化
    page_changed = pyqtSignal(int)  # 页面变化
    batch_action_triggered = pyqtSignal(str, list)  # 批量操作触发
    
    def __init__(self, parent=None):
        # 初始化属性（在super().__init__之前）
        self.current_page = 1
        self.total_pages = 1
        self.page_size = 20
        self.table_data = []
        self.selected_rows = []
        
        super().__init__(parent)
        
    def init_ui(self):
        """设置UI界面 - 直接加载.ui文件"""
        # 直接加载.ui文件
        self.load_ui()
        
        # 设置表格属性
        self.setup_table()
        
        # 设置信号连接
        self.setup_connections()
        
        # 设置更多操作菜单
        self.setup_more_menu()
        
        # 初始化示例数据
        self.load_sample_data()
        
    def apply_styles(self):
        """应用样式 - 重写BaseWidget的方法"""
        super().apply_styles()  # 调用父类的样式方法
        
        # 添加自定义样式
        self.setStyleSheet(self.get_custom_styles())
    
    def load_ui(self):
        """直接加载.ui文件"""
        # 获取.ui文件路径
        ui_file_path = ResourceUtils.get_ui_path(__file__, 'collaborative_table.ui')
        
        if not os.path.exists(ui_file_path):
            raise FileNotFoundError(f"UI文件不存在: {ui_file_path}")
        
        # 使用uic.loadUi直接加载UI文件
        uic.loadUi(ui_file_path, self)
        
        print(f"✅ 成功加载UI文件: {ui_file_path}")
    
    def setup_table(self):
        """设置表格属性"""
        # 直接使用UI文件中定义的控件名称
        table = self.dataTableWidget
        
        # 设置列宽
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # 复选框列
        header.resizeSection(0, 50)
        
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # ID列
        header.resizeSection(1, 80)
        
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # 名称列
        
        header.setSectionResizeMode(3, QHeaderView.Fixed)  # 类型列
        header.resizeSection(3, 100)
        
        header.setSectionResizeMode(4, QHeaderView.Fixed)  # 错误拥有者列
        header.resizeSection(4, 120)
        
        header.setSectionResizeMode(5, QHeaderView.Fixed)  # 修改时间列
        header.resizeSection(5, 150)
        
        header.setSectionResizeMode(6, QHeaderView.Fixed)  # 操作列
        header.resizeSection(6, 200)
        
        # UI文件已设置基本行高属性，这里可以进行额外的自定义设置
        self.setup_additional_table_properties()
    
    def setup_additional_table_properties(self):
        """设置额外的表格属性（UI文件已设置基本行高）"""
        table = self.dataTableWidget
        
        # UI文件中已经设置了：
        # - verticalHeaderDefaultSectionSize: 45px (默认行高)
        # - verticalHeaderMinimumSectionSize: 30px (最小行高)
        # - verticalHeaderVisible: false (隐藏行号)
        
        # 禁用选中变色效果
        table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 按行选择
        table.setSelectionMode(QAbstractItemView.NoSelection)     # 禁用选择
        
        # 这里可以根据需要进行额外的自定义
        print(f"✅ 表格行高设置: 默认45px (来自UI文件), 最小30px")
        print(f"✅ 已禁用表格选中变色效果")
        
        # 可选：根据内容自动调整行高
        # table.resizeRowsToContents()
    
    def setup_connections(self):
        """设置信号连接"""
        # 搜索框
        self.searchLineEdit.returnPressed.connect(
            lambda: self.search_triggered.emit(self.searchLineEdit.text())
        )
        
        # 过滤下拉框（原来的typeComboBox改名为filterComboBox）
        self.filterComboBox.currentTextChanged.connect(self.filter_changed.emit)
        
        # 新增按钮
        self.submitButton.clicked.connect(self.handle_submit)
        self.refreshButton.clicked.connect(self.handle_refresh)
        
        # 分页按钮
        self.prevButton.clicked.connect(self.prev_page)
        self.nextButton.clicked.connect(self.next_page)
        
        # 表格选择变化
        self.dataTableWidget.itemSelectionChanged.connect(self.on_selection_changed)
    
    def setup_more_menu(self):
        """设置更多操作菜单"""
        menu = QMenu(self)
        
        delete_action = QAction("删除", menu)
        delete_action.triggered.connect(lambda: self.handle_batch_action("delete"))
        menu.addAction(delete_action)
        
        lock_action = QAction("锁定", menu)
        lock_action.triggered.connect(lambda: self.handle_batch_action("lock"))
        menu.addAction(lock_action)
        
        copy_action = QAction("复制", menu)
        copy_action.triggered.connect(lambda: self.handle_batch_action("copy"))
        menu.addAction(copy_action)
        
        export_action = QAction("导出", menu)
        export_action.triggered.connect(lambda: self.handle_batch_action("export"))
        menu.addAction(export_action)
        
        # 使用新的控件名称
        self.moreButton.setMenu(menu)
        self.moreButton.setPopupMode(self.moreButton.InstantPopup)
    
    def load_sample_data(self):
        """加载示例数据"""
        sample_data = [
            {
                "id": "001", 
                "name": "AK47突击步枪", 
                "type": "武器", 
                "owner": "张三", 
                "modified": "2025-11-13 14:30",
                "status": "normal"
            },
            {
                "id": "002", 
                "name": "装甲车", 
                "type": "载具", 
                "owner": "李四", 
                "modified": "2025-11-13 13:20",
                "status": "locked"
            },
            {
                "id": "003", 
                "name": "医疗包", 
                "type": "道具", 
                "owner": "王五", 
                "modified": "2025-11-13 12:15",
                "status": "error"
            },
            {
                "id": "004", 
                "name": "钢铁材料", 
                "type": "材料", 
                "owner": "赵六", 
                "modified": "2025-11-13 11:45",
                "status": "normal"
            },
            {
                "id": "005", 
                "name": "手榴弹", 
                "type": "武器", 
                "owner": "孙七", 
                "modified": "2025-11-13 10:30",
                "status": "normal"
            }
        ]
        
        # 初始化过滤下拉框
        self.filterComboBox.addItems(["全部", "载具", "武器", "道具", "材料"])
        
        self.update_table_data(sample_data)
        
        # 更新搜索结果显示
        self.update_search_result_info(len(sample_data))
        
        # 更新排队信息
        self.update_queue_info(3, "allen")
    
    def update_table_data(self, data):
        """更新表格数据"""
        self.table_data = data
        table = self.dataTableWidget
        
        # 清空现有数据
        table.setRowCount(0)
        
        # 添加数据行
        for row_idx, item in enumerate(data):
            table.insertRow(row_idx)
            
            # 复选框列 - 创建居中的复选框
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(self.on_checkbox_changed)
            
            # 设置复选框大小
            checkbox.setFixedSize(18, 18)
            
            # 创建容器widget来实现水平和垂直居中
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignCenter)  # 水平和垂直居中
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            
            table.setCellWidget(row_idx, 0, checkbox_widget)
            
            # 数据列
            table.setItem(row_idx, 1, QTableWidgetItem(item["id"]))
            table.setItem(row_idx, 2, QTableWidgetItem(item["name"]))
            table.setItem(row_idx, 3, QTableWidgetItem(item["type"]))
            table.setItem(row_idx, 4, QTableWidgetItem(item["owner"]))
            table.setItem(row_idx, 5, QTableWidgetItem(item.get("modified", item.get("modified_time", ""))))
            
            # 操作按钮列
            self.create_action_buttons(row_idx, item)
            
            # 设置行颜色
            self.set_row_color(row_idx, item["status"])
    
    def create_action_buttons(self, row, item):
        """创建操作按钮"""
        button_widget = QWidget()
        layout = QHBoxLayout(button_widget)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        # 编辑按钮
        edit_btn = QPushButton("编辑")
        edit_btn.setFixedSize(50, 25)
        edit_btn.clicked.connect(lambda: self.item_action_triggered.emit("edit", row, item["id"]))
        layout.addWidget(edit_btn)
        
        # 删除按钮
        delete_btn = QPushButton("删除")
        delete_btn.setFixedSize(50, 25)
        delete_btn.clicked.connect(lambda: self.item_action_triggered.emit("delete", row, item["id"]))
        layout.addWidget(delete_btn)
        
        # 锁定/解锁按钮
        lock_text = "解锁" if item["status"] == "locked" else "锁定"
        lock_btn = QPushButton(lock_text)
        lock_btn.setFixedSize(50, 25)
        lock_btn.clicked.connect(lambda: self.item_action_triggered.emit("lock", row, item["id"]))
        layout.addWidget(lock_btn)
        
        # 复制按钮
        copy_btn = QPushButton("复制")
        copy_btn.setFixedSize(50, 25)
        copy_btn.clicked.connect(lambda: self.item_action_triggered.emit("copy", row, item["id"]))
        layout.addWidget(copy_btn)
        
        self.dataTableWidget.setCellWidget(row, 6, button_widget)
    
    def set_row_color(self, row, status):
        """设置行颜色"""
        colors = {
            "normal": QColor(255, 255, 255),      # 白色
            "locked": QColor(255, 248, 220),      # 浅黄色
            "error": QColor(255, 235, 238),       # 浅红色
        }
        
        color = colors.get(status, colors["normal"])
        
        for col in range(self.dataTableWidget.columnCount()):
            item = self.dataTableWidget.item(row, col)
            if item:
                item.setBackground(color)
    
    def on_checkbox_changed(self, state):
        """复选框状态变化"""
        self.update_selected_rows()
        
    def update_selected_rows(self):
        """更新选中行列表"""
        self.selected_rows = []
        for row in range(self.dataTableWidget.rowCount()):
            checkbox_widget = self.dataTableWidget.cellWidget(row, 0)
            if checkbox_widget:
                # 从容器widget中获取checkbox
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    self.selected_rows.append(row)
        
        self.item_selected.emit(self.selected_rows)
    
    def on_selection_changed(self):
        """表格选择变化"""
        self.update_selected_rows()
    
    def handle_batch_action(self, action):
        """处理批量操作"""
        if not self.selected_rows:
            QMessageBox.warning(self, "警告", "请先选择要操作的项目")
            return
        
        selected_ids = []
        for row in self.selected_rows:
            item_id = self.dataTableWidget.item(row, 1).text()
            selected_ids.append(item_id)
        
        self.batch_action_triggered.emit(action, selected_ids)
        
        # 显示操作结果
        QMessageBox.information(
            self, "操作完成", 
            f"已对 {len(selected_ids)} 个项目执行 {action} 操作"
        )
    
    def prev_page(self):
        """上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination()
            self.page_changed.emit(self.current_page)
    
    def next_page(self):
        """下一页"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_pagination()
            self.page_changed.emit(self.current_page)
    
    def update_pagination(self):
        """更新分页信息"""
        self.tabLabel.setText(f"{self.current_page}/{self.total_pages}")
        self.prevButton.setEnabled(self.current_page > 1)
        self.nextButton.setEnabled(self.current_page < self.total_pages)
    
    def handle_submit(self):
        """处理提交操作"""
        selected_ids = []
        for row in self.selected_rows:
            if row < self.dataTableWidget.rowCount():
                item_id = self.dataTableWidget.item(row, 1).text()
                selected_ids.append(item_id)
        
        if selected_ids:
            self.batch_action_triggered.emit("submit", selected_ids)
            QMessageBox.information(self, "提交", f"已提交 {len(selected_ids)} 个项目")
        else:
            QMessageBox.warning(self, "警告", "请先选择要提交的项目")
    
    def handle_refresh(self):
        """处理刷新操作"""
        # 重新加载数据
        self.load_sample_data()
        QMessageBox.information(self, "刷新", "数据已刷新")
    
    def update_search_result_info(self, count):
        """更新搜索结果信息"""
        self.searchResNumLabel.setText(str(count))
    
    def update_queue_info(self, queue_count, current_user):
        """更新排队信息"""
        self.LineUpNumLabel.setText(str(queue_count))
        self.handleUserLabel.setText(current_user)
    
    def clear_table(self):
        """清空表格"""
        self.dataTableWidget.setRowCount(0)
        
    def update_data(self, data):
        """更新表格数据 - 兼容接口"""
        self.update_table_data(data)
        
    def update_status_info(self, total_count, last_update):
        """更新状态信息"""
        # 更新搜索结果显示
        self.update_search_result_info(total_count)
        
    def set_total_pages(self, total_pages):
        """设置总页数"""
        self.total_pages = max(1, total_pages)
        self.update_pagination()
    
    def get_custom_styles(self):
        """获取自定义样式"""
        return """
            /* 数据表格框架 */
            QFrame#dataTableFrame {
                background-color: white;
            }
            
            /* 分页框架 */
            QFrame#paginationFrame {
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
            }
            
            /* 下拉框 */
            QComboBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px 10px;
                background-color: white;
                min-height: 20px;
            }
            
            QComboBox:hover {
                border-color: #007bff;
            }
            
            /* 搜索框 */
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px 10px;
                min-height: 20px;
            }
            
            QLineEdit:focus {
                border-color: #007bff;
                outline: none;
            }
            
            /* 按钮 */
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
                min-height: 20px;
            }
            
            QPushButton:hover {
                background-color: #0056b3;
            }
            
            QPushButton:disabled {
                background-color: #6c757d;
            }
            
            /* 提交按钮特殊样式 */
            QPushButton#submitButton {
                background-color: #28a745;
            }
            
            QPushButton#submitButton:hover {
                background-color: #218838;
            }
            
            /* 更新按钮特殊样式 */
            QPushButton#refreshButton {
                background-color: #17a2b8;
            }
            
            QPushButton#refreshButton:hover {
                background-color: #138496;
            }
            
            /* 更多操作按钮 */
            QToolButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                padding: 5px 10px;
            }
            
            QToolButton:hover {
                background-color: #545b62;
            }
            
            /* 数据表格 */
            QTableWidget {
                gridline-color: #dee2e6;
                background-color: white;
                selection-background-color: transparent;
                border: none;
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            
            QTableWidget::item:selected {
                background-color: transparent;
                color: inherit;
            }
            
            /* 表格头部 */
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
                color: #495057;
            }
            
            /* 标签样式 */
            QLabel {
                color: #495057;
            }
            
            /* 搜索结果数字标签 */
            QLabel#searchResNumLabel {
                color: #007bff;
                font-weight: bold;
            }
            
            /* 排队数字标签 */
            QLabel#LineUpNumLabel {
                color: #dc3545;
                font-weight: bold;
            }
            
            /* 当前处理用户标签 */
            QLabel#handleUserLabel {
                color: #28a745;
                font-weight: bold;
            }
            
            /* 分页标签 */
            QLabel#tabLabel {
                color: #495057;
                font-weight: bold;
                padding: 0 10px;
            }
            
            /* 复选框样式 */
            QCheckBox {
                spacing: 0px;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #ced4da;
                background-color: white;
            }
            
            QCheckBox::indicator:hover {
                border-color: #007bff;
                background-color: #f8f9fa;
            }
            
            QCheckBox::indicator:checked {
                border-color: #007bff;
                background-color: #007bff;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEzLjg1NCA0LjE0NkwxNC4xNDYgNC44NTRMMTMuODU0IDQuMTQ2Wk02IDEyTDUuNjQ2IDExLjY0NkM1LjU1MSAxMS43NDEgNS41NTEgMTEuODk5IDUuNjQ2IDExLjk5NEw2IDEyWk0yLjE0NiA4Ljg1NEwxLjg1NCA4LjE0NkwyLjE0NiA4Ljg1NFpNNS42NDYgMTEuNjQ2TDEuODU0IDcuODU0TDIuMTQ2IDguMTQ2TDUuOTM4IDExLjkzOEw1LjY0NiAxMS42NDZaTTYuMzU0IDExLjY0NkwxMy44NTQgNC4xNDZMMTQuMTQ2IDQuODU0TDYuNjQ2IDEyLjM1NEw2LjM1NCAxMS42NDZaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K);
            }
            
            QCheckBox::indicator:checked:hover {
                background-color: #0056b3;
            }
        """