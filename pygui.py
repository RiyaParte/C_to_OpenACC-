import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QGroupBox, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QGridLayout, QPlainTextEdit, QFileDialog, QLabel, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot 
import openacc
import dependency_test  
class App(QWidget): 
	def __init__(self):
		super().__init__()
		self.title = 'C to openacc converter'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480

		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.showMaximized()
		# self.setGeometry(self.left, self.top, self.width, self.height) 

		self.layout = QGridLayout()
		self.setLayout(self.layout)
		# layout.setColumnStretch(1, 4)
		# layout.setColumnStretch(2, 4)
		verticalLayout1 = QVBoxLayout() 
		verticalLayout2 = QVBoxLayout()  
		# verticalLayout3 = QVBoxLayout() 
		# horizontalLayout = QHBoxLayout()


		btn_file_upload = QPushButton('Upload File', self)
		btn_file_upload.setToolTip('Upload a File from your computer') 
		btn_file_upload.clicked.connect(self.function_file_upload) 

		btn_dependency_test = QPushButton('Test Dependency', self)
		btn_dependency_test.setToolTip('Test Dependency in for loop for Parallelization') 
		btn_dependency_test.clicked.connect(self.function_dependency_test) 

		btn_convert = QPushButton('Convert', self)
		btn_convert.setToolTip('Convert your code into Cuda')
		btn_convert.clicked.connect(self.function_convert)

		btn_save = QPushButton('Save File', self)
		btn_save.setToolTip('Convert your code into Cuda') 
		btn_save.clicked.connect(self.function_save) 

		self.input_box = QPlainTextEdit(self)
		self.output_box = QPlainTextEdit(self)

		input_name= QLabel(self)
		output_name = QLabel(self)
		self.file_name = QLabel(self)
		input_name.setText("Input")
		output_name.setText("Output")
 
		verticalLayout1.addWidget(input_name) 
		verticalLayout1.addWidget(self.input_box)  
		verticalLayout2.addWidget(output_name) 
		verticalLayout2.addWidget(self.output_box)  


		self.layout.addWidget(btn_file_upload,0,0)
		self.layout.addWidget(btn_dependency_test,1,0)
		self.layout.addWidget(btn_convert,2,0)
		self.layout.addWidget(btn_save,3,0) 

		self.layout.setRowStretch(1,4)
		self.layout.addLayout(verticalLayout1,0,1,4,1)
		self.layout.addLayout(verticalLayout2,0,2,4,1)
		# self.setLayout(horizontalLayout)
		self.show()  


	@pyqtSlot()
	def function_file_upload(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","C Files (*.c);;C++ Files (*.cpp);;Text Files (*.txt);;All Files (*)", options=options)
		if fileName:
			file = open(fileName,'r') 
			with file:
				self.input_box.setPlainText(file.read())  

		print('PyQt5 button click')

	def function_dependency_test(self):
		file_input = open("input.c",'w')
		text = self.input_box.toPlainText()
		file_input.write(text)
		file_input.close()
		dependency_test.dependency('input.c')
		file_output = open("dependency.txt",'r')
		with file_output:
			self.output_box.setPlainText(file_output.read())  
		file_output.close()

		print('PyQt5 button click')

	def function_convert(self):

		file_input = open("input.c",'w')
		text = self.input_box.toPlainText()
		file_input.write(text)
		file_input.close()
		# execfile(new.py)
		# import new
		openacc.convert('input.c')
		file_output = open("final.c",'r')
		with file_output:
			self.output_box.setPlainText(file_output.read())  
		file_output.close()

		
		# print('PyQt5 button click')

	def function_save(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","Cuda Files (*.cu);;All Files (*)", options=options)
		if fileName: 
			file = open(fileName,'w')
			text = self.output_box.toPlainText()
			file.write(text)

		# print('PyQt5 button click')
 

 
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
