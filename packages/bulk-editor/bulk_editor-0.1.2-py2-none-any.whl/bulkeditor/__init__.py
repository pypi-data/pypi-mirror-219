from PIL import Image as ImageEdit
from PIL import ImageFont, ImageDraw 
from PIL import ImageTk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.colorchooser import askcolor
import pkg_resources

import cv2

'''
todo: 
4. Code architecture and code clean
5. Make it as a Compiler package
'''

class GetImageAxisAndCreateImage:
	
	def createImage(self,path,x,y, fontColor):
		directory_to_save = filedialog.askdirectory()
		fontFilePath = pkg_resources.resource_filename(__name__, 'Roboto-Bold.ttf')
		certificateFont= ImageFont.truetype(fontFilePath, 42)
		textFile = pkg_resources.resource_filename(__name__, 'Certificate.txt')
		nameList=[]
		certificateName = []
		file = open(textFile, "r")
		nameList = file.readlines()
		file.close
		for i in nameList:
			certificateName.append(i.replace("\n","").strip())
		for i in certificateName:
			certificateImage = ImageEdit.open(path) 
			editableImage = ImageDraw.Draw(certificateImage)    
			editableImage.text((x,y-30),i,fontColor,font=certificateFont)
			certificateImage.save(directory_to_save +"/"+ i.strip()+".png")
		messagebox.showinfo("Information", "File created succesfully")
		cv2.destroyAllWindows()
	
	def select_color(self, path, x, y):
		global fontColor
		fontColor = askcolor(title="Choose color for the text")
		print(fontColor) 

		if messagebox.askquestion("Form", "Confirm color and proceed") == "yes":
			self.createImage(path,x,y, fontColor[0])


	def Submit(self,path,x,y):
		if messagebox.askquestion("Form", "Confirm position") == "yes":
			self.select_color(path=path,x=x, y=y)


	def click_event(self, event, x, y, flags, params):
		# checking for left mouse clicks
		if event == cv2.EVENT_LBUTTONDOWN:

			# displaying the coordinates
			# on the Shell
			print(x, ' ', y)
			img = cv2.imread(params, 1)

			# displaying the coordinates
			# on the image window
			font = cv2.FONT_HERSHEY_COMPLEX
			cv2.putText(img,"Your text will lie here", (x,y), font,
					1, (255, 0, 0), 2)
			
			cv2.imshow('DoSmartie - Bulk Image Editor', img)
			self.Submit(params,x,y)

		# checking for right mouse clicks	
		if event==cv2.EVENT_RBUTTONDOWN:

			# displaying the coordinates
			# on the Shell
			print(x, ' ', y)
			self.Submit(params,x,y)
		
	def __init__(self, path) -> None:
		cv2.namedWindow("DoSmartie - Bulk Image Editor", cv2.WINDOW_NORMAL)
		img = cv2.imread(path, 1)
		cv2.imshow('DoSmartie - Bulk Image Editor', img)
		cv2.setMouseCallback('DoSmartie - Bulk Image Editor', self.click_event, path)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

class BulkEditor:

	def select_image(self):
		global windowA, windowB
		textFile = pkg_resources.resource_filename(__name__, 'Certificate.txt')
		self.text = self.textField.get("1.0", "end-1c")
		with open(textFile, 'w') as file:
			file.write(self.text)
		path = filedialog.askopenfilename()
		if len(path) > 0:
			image = GetImageAxisAndCreateImage(path)

	def __init__(self):
		root = Tk()
		root.title("DoSmartie - Bulk edit images")
		logoFilePath = pkg_resources.resource_filename(__name__, 'logo.png')
		ico =  ImageEdit.open(logoFilePath)
		photo = ImageTk.PhotoImage(ico)
		root.wm_iconphoto(False, photo)
		root.geometry("360x360")  
		heading = Label(text="Enter the data to be added")
		label = Label(text="Each image will be created from a single line of text.")
		self.textField = Text(root, height = 24, width = 52)
		panelA = None
		panelB = None
		btn = Button(root, text="Select an image", command=self.select_image)
		btn.pack(side="bottom", fill="both", expand="no", padx="10", pady="10")
		heading.pack()
		label.pack()
		self.textField.pack()
		root.mainloop()
