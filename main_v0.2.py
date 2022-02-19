import icon
import sys
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont, QIcon, QKeyEvent
from PyQt5.QtWidgets import QCheckBox, QMainWindow, QAction, QComboBox, QLabel, QRadioButton, \
    QTextEdit, QDesktopWidget, QMessageBox, QFileDialog, QApplication, \
    QDialog, QPushButton

keymap = ('{1}', '{#1}', '{2}', '{#2}', '{3}', '{4}', '{#4}', '{5}', '{#5}',
        '{6}', '{#6}', '{7}',
        '(1)', '(#1)', '(2)', '(#2)', '(3)', '(4)', '(#4)', '(5)', '(#5)',
        '(6)', '(#6)', '(7)',
        '1', '#1', '2', '#2', '3', '4', '#4', '5', '#5', '6', '#6', '7',
        '[1]', '[#1]', '[2]', '[#2]', '[3]', '[4]', '[#4]', '[5]', '[#5]',
        '[6]', '[#6]', '[7]',
        '<1>', '<#1>', '<2>', '<#2>', '<3>', '<4>', '<#4>', '<5>', '<#5>',
        '<6>', '<#6>', '<7>', '<#7>')


keys = ('1', '2', '3', '4', '5', '6', '7')
sig = ('{-2}', '(-1)', ' 0 ', '[+1]', '<+2>')
sharp = ('关', '开', '固定')
bordercolor = ("border:3px solid blue", "border:3px solid rgb(0,255,120)",    # 蓝 青
         "border:3px solid white", "border:3px solid rgb(255,60,255)",    # 白 粉
         "border:3px solid red")             # 红 
posi = [0, 0, 1]
flag = 0
sharpflag = 0
filename = ''


class TextEdit(QMainWindow):
    def __init__(self):
        super().__init__()
        font = QFont("Microsoft YaHei", 10)
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
        redo_act.setShortcut('Ctrl+Y')
        redo_act.triggered.connect(self.redo_function)

        up_act = QAction(QIcon(':icon/Up.png'), '升半度', self)
        up_act.setShortcut('Page Up')
        up_act.triggered.connect(self.up_function)

        down_act = QAction(QIcon(':icon/Down.png'), '降半度', self)
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

        font10 = QFont("Microsoft YaHei", 10)
        font11 = QFont("Microsoft YaHei", 11)
        font12 = QFont("Microsoft YaHei", 12)
        self.statusbar = self.statusBar()
        self.statusbar.setStyleSheet("background: white")

        self.oldCombo = QComboBox(self)
        self.oldCombo.addItems(['旧', '  C', '#C', '  D', '#D', '  E', '  F', '#F',
                                '  G', '#G', '  A', '#A', '  B'])
        self.oldCombo.setEditable(False)
        self.oldCombo.setFixedSize(44, 27)
        self.oldCombo.setFont(font10)

        self.newCombo = QComboBox(self)
        self.newCombo.addItems(['新', '  C', '#C', '  D', '#D', '  E', '  F', '#F',
                                '  G', '#G', '  A', '#A', '  B'])
        self.newCombo.setEditable(False)
        self.newCombo.setFixedSize(44, 27)
        self.newCombo.setFont(font10)
        
        self.modeLable = QLabel('   ', self)
        
        self.check1 = QCheckBox('1 ')
        self.check2 = QCheckBox('2 ')
        self.check3 = QCheckBox('3 ')
        self.check4 = QCheckBox('4 ')
        self.check5 = QCheckBox('5 ')
        self.check6 = QCheckBox('6 ')
        self.check7 = QCheckBox('7 ')
        checks = (self.check1, self.check2, self.check3, self.check4,
                  self.check5, self.check6, self.check7)
        for i in range(7):
            checks[i].setShortcut('ctrl+'+str(i+1))
            checks[i].toggled.connect(self.checks_toggled)
            checks[i].setFont(font11)

        self.modeRadio = QRadioButton('固定')
        self.modeRadio.setChecked = False
        self.modeRadio.setShortcut('ctrl+M')
        self.modeRadio.toggled.connect(self.radio_toggled)
        self.modeRadio.setFont(font11)

        self.confirmBtn = QPushButton(self)
        self.confirmBtn.setText("OK")
        self.confirmBtn.clicked.connect(self.cbtn_clicked)
        self.confirmBtn.setFixedSize(30, 24)
        self.confirmBtn.setFont(font10)

        # ***********建立编辑框***********
        self.text = QTextEdit(self)
        self.text.setFont(font12)
        self.setCentralWidget(self.text)
        self.setMinimumSize(250, 300)
        self.resize(524, 700)
        self.text.setStyleSheet("border:3px solid white")
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
        self.toolbar.setStyleSheet("background: white")
        self.toolbar.addAction(undo_act)
        self.toolbar.addAction(redo_act)
        #self.toolbar.insertWidget(undo_act, self.status_flag)
        self.toolbar.addWidget(self.oldCombo)
        self.toolbar.addWidget(self.newCombo)
        self.toolbar.addWidget(self.confirmBtn)
        #self.toolbar.insertWidget(undo_act, self.modeLable)
        self.toolbar.addWidget(self.modeLable)
        #self.toolbar.addWidget(self.modeCombo)
        self.toolbar.addWidget(self.check1)
        self.toolbar.addWidget(self.check2)
        self.toolbar.addWidget(self.check3)
        self.toolbar.addWidget(self.check4)
        self.toolbar.addWidget(self.check5)
        self.toolbar.addWidget(self.check6)
        self.toolbar.addWidget(self.check7)
        self.toolbar.addWidget(self.modeRadio)

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
            QMessageBox.warning(self, "提示：", "未选择合适的曲调 ",
                                QMessageBox.Cancel,
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
        self.change_tune(1)

    def down_function(self):
        self.change_tune(-1)

    def change_tune(self, n):  # 转调函数  n个半度
        global keymap
        changeable_flag = True
        piece = self.text.toPlainText()
        if n > 0:
            for limit_tune in keymap[-n:]:  # 判断是否含有转调后会超限的音符
                #print(limit_tune)
                if limit_tune in piece:
                    n -= 12
                    changeable_flag = True
                    break
            if n < 0:
                for limit_tune in keymap[:-n]:
                    if limit_tune in piece:
                        changeable_flag = False
                        break

        else:
            for limit_tune in keymap[:-n]:
                if limit_tune in piece:
                    n += 12
                    changeable_flag = True
                    break
            if n > 0:
                for limit_tune in keymap[-n:]:
                    if limit_tune in piece:
                        changeable_flag = False
                        break
        if not changeable_flag:
            QMessageBox.warning(self, "提示：", "转调结果超出表示范围！",
                                QMessageBox.Cancel,
                                QMessageBox.Cancel)
        else:
            tmp_text = ''
            i = 0
            while i < len(piece):
                # 获取音符
                if piece[i] in ('{', '(', '[', '<'):
                    if piece[i + 1] == '#':
                        tmp_char = piece[i:(i + 4)]
                        i = i + 4
                    else:
                        tmp_char = piece[i:(i + 3)]
                        i = i + 3
                elif piece[i] == '#':
                    tmp_char = piece[i:(i + 2)]
                    i = i + 2
                else:
                    tmp_char = piece[i]
                    i += 1
                # 替换#3、#7为4、1
                if ('#3' in tmp_char) or ('#7' in tmp_char):
                    tmp_char = tmp_char.replace('#', '')
                    tmp_char = keymap[keymap.index(tmp_char) + 1]
                # 转调
                try:
                    if tmp_char in keymap:
                        order = (keymap.index(tmp_char) + n)
                        if order < 0:
                            raise IndexError('IndexError')
                        else:
                            tmp_text += keymap[order]
                    else:
                        tmp_text += tmp_char
                except IndexError:
                    # QMessageBox.warning(self, "提示：", "转调结果超出表示范围！",
                    #                     QMessageBox.Cancel,
                    #                     QMessageBox.Cancel)
                    return 0
            self.text.selectAll()
            self.text.insertPlainText(tmp_text)

    def redo_function(self):
        self.text.redo()

    def undo_function(self):
        self.text.undo()

    def unsaved(self):
        destroy = self.text.document().isModified()
        #print(destroy)

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

    def add_brace(self, str0, num0):
        newstr = ''
        if num0 == -2:
            newstr = "{" + str0 + '}'
        elif num0 == -1:
            newstr = "(" + str0 + ')'
        elif num0 == 1:
            newstr = "[" + str0 + ']'
        elif num0 == 2:
            newstr = "<" + str0 + '>'
        else:
            newstr = str0
        return newstr

    def radio_toggled(self):
        global sharpflag 
        if self.modeRadio.isChecked():
            sharpflag = 2
            self.statusbar.setStyleSheet("background: rgb(255,180,105)")
            #self.statusbar.setStyleSheet("background: rgb(58,156,255)")
            self.text.setFocus()
        else:
            sharpflag = 0
            self.statusbar.setStyleSheet("background: rgb(255,255,255)")
            self.text.setFocus()

    def checks_toggled(self):
        self.text.setFocus()

    def set_output(self, key_text):
        """ 更改按键输出的音符 """
        global keys, sig, flag, posi, sharpflag
        checks = (self.check1.isChecked(), self.check2.isChecked(), self.check3.isChecked(), self.check4.isChecked(),
                  self.check5.isChecked(), self.check6.isChecked(), self.check7.isChecked())
        checktext = ['-1', '-1', '-1', '-1', '-1', '-1', '-1']
        for i in range(7):        # 检查哪些音符可能固定#号
            if checks[i]:
                checktext[i] = str(i+1)
            else:
                checktext[i] = '-1'
        if key_text == '+':       # 判断按键
            if flag < 2:
                flag += 1
        elif key_text == '-':
            if flag > -2:
                flag -= 1
        elif key_text == '0':
            flag = 0
        elif key_text == '8':
            self.text.insertPlainText(' ')
        elif key_text == '9':
            if self.modeRadio.isChecked():
                pass
            else:
                if sharpflag ==0:     #设置#
                    sharpflag = 1
                    self.statusbar.setStyleSheet("background: yellow")
                else:
                    sharpflag =0
                    self.statusbar.setStyleSheet("background: rgb(255,255,255)")
        elif key_text in ('.', '。'):
            back_key = QKeyEvent(QEvent.KeyPress, Qt.Key_Backspace,
                                 Qt.NoModifier)
            QApplication.sendEvent(self.text, back_key)
        elif key_text in keys:
            if (self.modeRadio.isChecked()) and (key_text in checktext):
                key = '#'+key_text
            else:
                if sharpflag == 1:
                    key = '#'+key_text
                else:
                    key = key_text
            try:
                final_key = self.add_brace(key, flag)
                self.text.insertPlainText(final_key)
            except Exception:
                QMessageBox.warning(self, "提示：", "输入超出范围！！",
                                        QMessageBox.Cancel, QMessageBox.Cancel)
        else:
            # self.text.insertPlainText(key_text)
            return False
        self.text.setStyleSheet(bordercolor[flag+2])
        # self.statusbar.showMessage('第%s行  第%s列   共%s行    当前输入模式：%s    # 输入：%s'     
        #                            % (posi[0], posi[1], posi[2], sig[flag + 2], sharp[sharpflag]))
        return True
        # if (len(key_text)==0) or (key_text==' '):
        #     return False
        # else:
        #     return True

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
        global posi, flag, sharpflag
        text_doc = self.text.document()
        text_cur = self.text.textCursor()
        posi[0] = (text_cur.blockNumber() + 1)
        posi[1] = (text_cur.positionInBlock())
        posi[2] = (text_doc.blockCount())
        self.statusbar.showMessage('第%s行  第%s列   共%s行    当前输入模式：%s    # 输入：%s'
                                   % (posi[0], posi[1], posi[2], sig[flag + 2], sharp[sharpflag]))
        if event.type() == QEvent.KeyPress:
            key_value = event.key()
            key_text = event.text()
            if key_value in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Backspace,
                             Qt.Key_Enter, Qt.Key_Return):
                return self.setmodify(key_value, text_cur)
            else:
                # print('按键内容： ' + '"' + key_text + '"' + '   内容长度： ' + str(len(key_text)))
                return self.set_output(key_text)
        # elif event.type() == QEvent.InputMethod:
        #     key_text = event.commitString()
        #     return self.set_output(key_text)
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
