import icon
import sys
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont, QIcon, QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QAction, QComboBox, QLabel, \
    QTextEdit, QDesktopWidget, QMessageBox, QFileDialog, QApplication, \
    QDialog, QPushButton

keys = ('{1}', '{#1}', '{2}', '{#2}', '{3}', '{4}', '{#4}', '{5}', '{#5}',
        '{6}', '{#6}', '{7}',
        '(1)', '(#1)', '(2)', '(#2)', '(3)', '(4)', '(#4)', '(5)', '(#5)',
        '(6)', '(#6)', '(7)',
        '1', '#1', '2', '#2', '3', '4', '#4', '5', '#5', '6', '#6', '7',
        '[1]', '[#1]', '[2]', '[#2]', '[3]', '[4]', '[#4]', '[5]', '[#5]',
        '[6]', '[#6]', '[7]',
        '<1>', '<#1>', '<2>', '<#2>', '<3>', '<4>', '<#4>', '<5>', '<#5>',
        '<6>', '<#6>', '<7>')
sig = ('{-2}', '(-1)', ' 0 ', '[+1]', '<+2>')
posi = [0, 0, 1]
flag = 0
filename = ''


class TextEdit(QMainWindow):
    def __init__(self):
        super().__init__()
        font = QFont("Consolas", 12)
        self.setFont(font)
        self.ui()
        self.setWindowIcon(QIcon(":icon/icon.png"))
        self.text.installEventFilter(self)

    def ui(self):
        # ***********设置按钮、快捷键，连接到函数***********
        new_file = QAction(QIcon(':icon/New.png'), '新建', self)
        new_file.setShortcut('ctrl+N')
        new_file.triggered.connect(self.new_file)

        open_file = QAction(QIcon(':icon/Open.png'), '打开', self)
        open_file.setShortcut('ctrl+O')
        open_file.triggered.connect(self.open_file)

        save_file = QAction(QIcon(':icon/Save.png'), '保存', self)
        save_file.setShortcut('ctrl+S')
        save_file.triggered.connect(self.save_file)

        quit_app = QAction(QIcon(':icon/Exit.png'), '退出', self)
        quit_app.setShortcut('Ctrl+Q')
        quit_app.triggered.connect(self.close)

        undo_act = QAction(QIcon(':icon/Undo.png'), '撤销', self)
        undo_act.setShortcut('Ctrl+Z')
        undo_act.triggered.connect(self.undo_function)

        redo_act = QAction(QIcon(':icon/Redo.png'), '重做', self)
        redo_act.setShortcut('Ctrl+Alt+Z')
        redo_act.triggered.connect(self.redo_function)

        up_act = QAction(QIcon(':icon/Up.png'), '升调', self)
        up_act.setShortcut('Page Up')
        up_act.triggered.connect(self.up_function)

        down_act = QAction(QIcon(':icon/Down.png'), '降调', self)
        down_act.setShortcut('Page Down')
        down_act.triggered.connect(self.down_function)

        change_act = QAction(QIcon(':icon/Change.png'), '转调', self)
        change_act.setShortcut('Ctrl+L')
        change_act.triggered.connect(self.change_fun)

        tb_sta = QAction('工具栏', self)
        tb_sta.setShortcut('Ctrl+T')
        tb_sta.setCheckable(True)
        tb_sta.setChecked(True)
        tb_sta.triggered.connect(self.tbs_function)

        sb_sta = QAction('状态栏', self)
        sb_sta.setShortcut('Ctrl+P')
        sb_sta.setCheckable(True)
        sb_sta.setChecked(True)
        sb_sta.triggered.connect(self.sbs_function)

        self.statusbar = self.statusBar()
        self.status_flag = QLabel(self)
        self.status_flag.setFixedWidth(46)
        self.status_flag.setFixedHeight(24)
        self.status_flag.setAlignment(Qt.AlignCenter)
        self.status_flag.setStyleSheet("QLabel{color:rgb(255,0,240,250);"
                                       "font-size:20px;font-weight:bold;"
                                       "font-family:幼圆;}")
        self.status_flag.setText(' 0 ')

        self.oldCombo = QComboBox(self)
        self.oldCombo.addItems(['旧', ' C', '#C', ' D', '#D', ' E', ' F', '#F',
                                ' G', '#G', ' A', '#A', ' B'])
        self.oldCombo.setEditable(False)

        self.newCombo = QComboBox(self)
        self.newCombo.addItems(['新', ' C', '#C', ' D', '#D', ' E', ' F', '#F',
                                ' G', '#G', ' A', '#A', ' B'])
        self.newCombo.setEditable(False)

        self.confirmBtn = QPushButton(self)
        self.confirmBtn.setText("OK")
        self.confirmBtn.clicked.connect(self.cbtn_clicked)
        self.confirmBtn.setFixedSize(30, 25)

        # ***********建立编辑框***********
        self.text = QTextEdit(self)
        self.setCentralWidget(self.text)
        self.setMinimumSize(250, 260)
        self.resize(500, 600)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('口琴谱编辑器')

        # ***********设置菜单栏***********
        self.menubar = self.menuBar()
        menu_file = self.menubar.addMenu('&文&件')
        menu_file.addAction(new_file)
        menu_file.addAction(open_file)
        menu_file.addAction(save_file)
        menu_file.addAction(quit_app)
        menu_edit = self.menubar.addMenu('&编&辑')
        menu_edit.addAction(undo_act)
        menu_edit.addAction(redo_act)
        menu_edit.addAction(up_act)
        menu_edit.addAction(down_act)
        menu_edit.addAction(change_act)
        menu_view = self.menubar.addMenu('&视&图')
        menu_view.addAction(tb_sta)
        menu_view.addAction(sb_sta)

        # ***********设置工具栏***********
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addAction(undo_act)
        self.toolbar.addAction(redo_act)
        self.toolbar.insertWidget(undo_act, self.status_flag)
        self.toolbar.addWidget(self.oldCombo)
        self.toolbar.addWidget(self.newCombo)
        self.toolbar.addWidget(self.confirmBtn)

    def change_fun(self):
        small.show()

    def cbtn_clicked(self):
        old = self.oldCombo.currentIndex()
        # print(str(old))
        new = self.newCombo.currentIndex()
        # print(str(new))
        if old != 0 and new != 0:
            n = old - new
            editor.change_tune(n)
        else:
            QMessageBox.warning(self, "提示：", "未选择合适的曲调 ", QMessageBox.Cancel,
                                QMessageBox.Cancel)

    def tbs_function(self, state):
        if state:
            self.toolbar.show()
        else:
            self.toolbar.hide()

    def sbs_function(self, state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

    def up_function(self):
        self.change_tune(-1)

    def down_function(self):
        self.change_tune(1)

    def change_tune(self, n):  # 转调函数  n个半度
        global keys
        peice = self.text.toPlainText()
        if n > 0:
            limit_tune = keys[-n]
            if limit_tune in peice:
                n -= 12
        else:
            limit_tune = keys[-n - 1]
            if limit_tune in peice:
                n += 12
        tmp_text = ''
        i = 0
        while i < len(peice):
            # 获取音符
            if peice[i] in ('{', '(', '[', '<'):
                if peice[i + 1] == '#':
                    tmp_char = peice[i:(i + 4)]
                    i = i + 4
                else:
                    tmp_char = peice[i:(i + 3)]
                    i = i + 3
            elif peice[i] == '#':
                tmp_char = peice[i:(i + 2)]
                i = i + 2
            else:
                tmp_char = peice[i]
                i += 1
            # 替换#3、#7为4、1
            if ('#3' in tmp_char) or ('#7' in tmp_char):
                tmp_char = tmp_char.replace('#', '')
                tmp_char = keys[keys.index(tmp_char) + 1]
            # 转调
            if tmp_char in keys:
                order = keys.index(tmp_char)
                tmp_text += keys[order + n]
            else:
                tmp_text += tmp_char
        self.text.selectAll()
        self.text.insertPlainText(tmp_text)

    def redo_function(self):
        self.text.redo()

    def undo_function(self):
        self.text.undo()

    def unsaved(self):
        destroy = self.text.document().isModified()
        print(destroy)

        if destroy is False:
            return False
        else:
            detour = QMessageBox.question(self, '提示：', '文件有未保存更改，是否保存',
                                          QMessageBox.Yes | QMessageBox.No |
                                          QMessageBox.Cancel,
                                          QMessageBox.Cancel)
            if detour == QMessageBox.Cancel:
                return True
            elif detour == QMessageBox.No:
                return False
            elif detour == QMessageBox.Yes:
                return self.save_file()

    def save_file(self):
        global filename
        if filename == '':
            filename, file_type = QFileDialog.getSaveFileName(self, '保存文件',
                                                              'untitled.txt',
                                                              '文本 (*.txt)')
        try:
            f = filename
            with open(f, "w") as CurrentFile:
                CurrentFile.write(self.text.toPlainText())
            CurrentFile.close()
            self.text.document().setModified(False)
            return False
        except Exception as e:
            print(e)
            print("save file failed")
            return True

    def new_file(self):
        global filename
        if not self.unsaved():
            filename = ''
            self.text.clear()

    def open_file(self):
        global filename
        if not self.unsaved():
            self.text.clear()
            filename, file_type = QFileDialog.getOpenFileName(self, '打开文件', '',
                                                              '文本 (*.txt)')
            try:
                self.text.setText(open(filename).read())
            except Exception:
                print("open file failed")

    def closeEvent(self, event):
        if self.unsaved():
            event.ignore()

    def set_output(self, key_text):
        """ 更改按键输出的音符 """
        global keys, sig, flag, posi
        if key_text == '+':
            if flag < 2:
                flag += 1
                self.status_flag.setText(sig[flag + 2])
                self.statusbar.showMessage('第%s行  第%s列   共%s行    当前输入模式'
                                           '：%s' % (posi[0], posi[1], posi[2],
                                                    sig[flag + 2]))
            return True
        elif key_text == '-':
            if flag > -2:
                flag -= 1
                self.status_flag.setText(sig[flag + 2])
                self.statusbar.showMessage('第%s行  第%s列   共%s行    当前输入模式'
                                           '：%s' % (posi[0], posi[1], posi[2],
                                                    sig[flag + 2]))
            return True
        elif key_text == '0':
            flag = 0
            self.status_flag.setText(' 0 ')
            self.statusbar.showMessage('第%s行  第%s列   共%s行    当前输入模式：%s'
                                       % (posi[0], posi[1], posi[2],
                                          sig[flag + 2]))
            return True
        elif key_text == '8':
            self.text.insertPlainText(' ')
            return True
        elif key_text == '9':
            self.text.insertPlainText('#')
            return True
        elif key_text in ('.', '。'):
            back_key = QKeyEvent(QEvent.KeyPress, Qt.Key_Backspace,
                                 Qt.NoModifier)
            QApplication.sendEvent(self.text, back_key)
            return True
        elif key_text in keys:
            p = keys.index(key_text)
            cursor = self.text.textCursor()
            cursor.movePosition(cursor.Left, cursor.KeepAnchor, 1)
            if cursor.selectedText() == '#':
                cursor.deleteChar()
                try:
                    self.text.insertPlainText(keys[p + 12 * flag + 1])  # 输入
                except Exception:
                    QMessageBox.warning(self, "提示：", "输入超出范围！！",
                                        QMessageBox.Cancel, QMessageBox.Cancel)
            else:
                self.text.insertPlainText(keys[p + 12 * flag])
            return True
        else:
            return False

    def setmodify(self, key_value, cursor):  # 更改按键移动字符数
        left_char = '0'
        right_char = '0'
        # 获取鼠标位置左右字符
        if cursor.block().length() != 1:
            if cursor.atBlockStart():
                cursor.movePosition(cursor.Right, cursor.KeepAnchor, 1)
                right_char = cursor.selectedText()
                cursor.movePosition(cursor.Left, cursor.KeepAnchor, 1)
                self.text.setTextCursor(cursor)
            elif cursor.atBlockEnd():
                cursor.movePosition(cursor.Left, cursor.KeepAnchor, 1)
                left_char = cursor.selectedText()
                cursor.movePosition(cursor.Right, cursor.KeepAnchor, 1)
                self.text.setTextCursor(cursor)
            else:
                cursor.movePosition(cursor.Left, cursor.KeepAnchor, 1)
                left_char = cursor.selectedText()
                cursor.movePosition(cursor.Right, cursor.KeepAnchor, 2)
                right_char = cursor.selectedText()
                cursor.movePosition(cursor.Left, cursor.KeepAnchor, 1)
                self.text.setTextCursor(cursor)
        else:
            return False

        if key_value == Qt.Key_Backspace:
            if left_char in ('}', ')', ']', '>'):
                cursor.movePosition(cursor.Left, cursor.KeepAnchor, 3)
                if '#' in cursor.selectedText():
                    cursor.movePosition(cursor.Left, cursor.KeepAnchor, 1)
                self.text.setTextCursor(cursor)
            elif right_char in ('}', ')', ']', '>'):
                cursor.movePosition(cursor.Right, cursor.MoveAnchor, 1)
                cursor.movePosition(cursor.Left, cursor.KeepAnchor, 3)
                if '#' in cursor.selectedText():
                    cursor.movePosition(cursor.Left, cursor.KeepAnchor, 1)
                self.text.setTextCursor(cursor)
            elif left_char in ('{', '(', '[', '<'):
                cursor.movePosition(cursor.Left, cursor.MoveAnchor, 1)
                cursor.movePosition(cursor.Right, cursor.KeepAnchor, 3)
                if '#' in cursor.selectedText():
                    cursor.movePosition(cursor.Right, cursor.KeepAnchor, 1)
                self.text.setTextCursor(cursor)
            else:
                self.text.setTextCursor(cursor)

        elif key_value == Qt.Key_Left:
            if left_char in ('}', ')', ']', '>'):
                cursor.movePosition(cursor.Left, cursor.KeepAnchor, 3)
                if '#' in cursor.selectedText():
                    cursor.movePosition(cursor.Left, cursor.MoveAnchor, 1)
                self.text.setTextCursor(cursor)
            elif right_char in ('}', ')', ']', '>'):
                cursor.movePosition(cursor.Left, cursor.KeepAnchor, 2)
                if '#' in cursor.selectedText():
                    cursor.movePosition(cursor.Left, cursor.MoveAnchor, 1)
                self.text.setTextCursor(cursor)
            else:
                self.text.setTextCursor(cursor)

        elif key_value == Qt.Key_Right:
            if left_char in ('{', '(', '[', '<'):
                if right_char == '#':
                    cursor.movePosition(cursor.Right, cursor.MoveAnchor, 2)
                else:
                    cursor.movePosition(cursor.Right, cursor.MoveAnchor, 1)
                self.text.setTextCursor(cursor)
            elif right_char in ('{', '(', '[', '<'):
                cursor.movePosition(cursor.Right, cursor.KeepAnchor, 2)
                if '#' in cursor.selectedText():
                    cursor.movePosition(cursor.Right, cursor.KeepAnchor, 2)
                else:
                    cursor.movePosition(cursor.Right, cursor.KeepAnchor, 1)
                self.text.setTextCursor(cursor)
            else:
                self.text.setTextCursor(cursor)

        elif key_value in (Qt.Key_Enter, Qt.Key_Return):
            if left_char in ('{', '(', '[', '<'):
                cursor.movePosition(cursor.Left, cursor.MoveAnchor, 1)
                self.text.setTextCursor(cursor)
            elif right_char in ('}', ')', ']', '>'):
                cursor.movePosition(cursor.Right, cursor.MoveAnchor, 1)
                self.text.setTextCursor(cursor)
            elif left_char == '#':
                cursor.movePosition(cursor.Left, cursor.MoveAnchor, 1)
                cursor.movePosition(cursor.Left, cursor.KeepAnchor, 1)
                if cursor.selectedText() in ('{', '(', '[', '<'):
                    cursor.movePosition(cursor.Left, cursor.MoveAnchor, 1)
                    self.text.setTextCursor(cursor)
                else:
                    self.text.setTextCursor(cursor)
            else:
                self.text.setTextCursor(cursor)
        return False

    def eventFilter(self, widget, event):  # 捕获按键事件；刷新状态栏显示
        text_doc = self.text.document()
        text_cur = self.text.textCursor()
        global posi, flag
        posi[0] = (text_cur.blockNumber() + 1)
        posi[1] = (text_cur.positionInBlock())
        posi[2] = (text_doc.blockCount())
        self.statusbar.showMessage('第%s行  第%s列   共%s行    当前输入模式：%s'
                                   % (posi[0], posi[1], posi[2], sig[flag + 2]))
        if event.type() == QEvent.KeyPress:
            key_value = event.key()
            key_text = event.text()
            if key_value in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Backspace,
                             Qt.Key_Enter, Qt.Key_Return):
                return self.setmodify(key_value, text_cur)
            else:
                return self.set_output(key_text)

        elif event.type() == QEvent.InputMethod:
            key_text = event.commitString()
            return self.set_output(key_text)
        else:
            return False


class SmallWindow(QDialog):
    """弹出转调窗口"""

    def __init__(self):
        super().__init__()
        self.setFixedSize(240, 170)
        font = QFont("Consolas", 12)
        self.setFont(font)
        self.setWindowTitle('转调')
        self.setup_ui()

    def setup_ui(self):
        self.confirm_button = QPushButton(self)
        self.confirm_button.setGeometry(90, 110, 61, 31)
        self.confirm_button.setText("确认")
        self.confirm_button.clicked.connect(self.cb_clicked)

        self.oldbox = QComboBox(self)
        self.oldbox.setGeometry(30, 50, 61, 31)
        self.oldbox.addItems(
            ['原调', ' C', '#C', ' D', '#D', ' E', ' F', '#F', ' G', '#G',
             ' A', '#A', ' B'])

        self.newbox = QComboBox(self)
        self.newbox.setGeometry(150, 50, 61, 31)
        self.newbox.addItems(
            ['新调', ' C', '#C', ' D', '#D', ' E', ' F', '#F', ' G', '#G',
             ' A', '#A', ' B'])

    def cb_clicked(self):
        old = self.oldbox.currentIndex()
        # print(str(old))
        new = self.newbox.currentIndex()
        # print(str(new))
        if old != 0 and new != 0:
            n = old - new
            editor.change_tune(n)
        else:
            QMessageBox.warning(self, "提示：", "未选择合适的曲调 ",
                                QMessageBox.Cancel, QMessageBox.Cancel)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEdit()
    small = SmallWindow()
    editor.show()
    sys.exit(app.exec_())
