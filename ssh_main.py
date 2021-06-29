import sys
from PyQt5.QtWidgets import (QWidget, QListWidget, QVBoxLayout, QApplication, QPushButton, QMessageBox)
from ssh_pexpect import reboot_TO, slovar_to

LISTS = slovar_to().keys()


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Перезагрузка ТО разработана Кириченко А. В.')
        self.l = QListWidget()
        self.l.addItems(LISTS)
        self.l.itemClicked.connect(self.example)
        vbox = QVBoxLayout()
        vbox.addWidget(self.l)
        self.setLayout(vbox)

    def selectionChanged(self, item):
        for i in slovar_to()[item.text()]:
            ip = i
        reboot_TO(ip)
        print("Вы завершили процес: {}".format(ip))

        self.update_1()
        # ...
    def update_1(self):
        self.l.clear()
        self.l.addItems(LISTS)

    def example(self, item):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        # msg.setIconPixmap(pixmap)  # Своя картинка
        msg.setWindowTitle("Информация")
        msg.setText(f'Вы действительно хатите перезагрузить терминал {item.text()}')
        okButton = msg.addButton('Да', QMessageBox.AcceptRole)
        msg.addButton('Нет', QMessageBox.RejectRole)
        msg.exec()
        if msg.clickedButton() == okButton:
            self.selectionChanged(item)
        else:
            print("No")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())