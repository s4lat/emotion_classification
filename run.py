from main import MainWindow
from PyQt5.QtWidgets import QApplication, QStyleFactory
import sys, cfg

if __name__ == '__main__':
	app = QApplication(sys.argv)
	
	# Установка стиля если он есть
	if cfg.PREFFERED_THEME in QStyleFactory.keys():
		app.setStyle(cfg.PREFFERED_THEME)

	win = MainWindow()
	win.show()
	sys.exit(app.exec_())