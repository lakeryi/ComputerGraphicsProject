from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import messagebox

import os
import wave
import warnings
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pyaudio as pa
import numpy as np
import pygame as pg
from pygame.locals import *


class MusicVisualization:
	def __init__(self, master):
		self.file_name = 'None'
		self.file_exist = False
	
		master.protocol('WM_DELETE_WINDOW', self.closeButton)
		
		global tk_img_1
		tk_img_1 = PhotoImage(file = "Cover.png")
		self.photo_1 = Label(master, image = tk_img_1)
		self.photo_1.grid(row = 1, columnspan = 7)
		
		self.button_1 = Button(master, text = '选择音频', width = 20, height = 2, command = self.choose, font = 64)
		self.button_1.grid(row = 2, column = 1, sticky = W)
		
		self.button_2 = Button(master, text = '可视化', width = 20, height = 2, command = self.visualize, font = 64)
		self.button_2.grid(row = 2, column = 3)
		
		self.button_3 = Button(master, text = '退出程序', width = 20, height = 2, command = self.shutdown, font = 64)
		self.button_3.grid(row = 2, column = 5, sticky = E)


	def visulizeBegin(self):
		self.player = pa.PyAudio()
		self.stream = self.player.open(format = self.player.get_format_from_width(self.file.getsampwidth()), channels = self.file.getnchannels(), rate = self.file.getframerate(), output = True)		
		pg.init()
		pg.display.set_caption(self.file_name)
		self.window = pg.display.set_mode((1024 + 64, 512 + 256))
		
	
	def visulizeEnd(self):
		pg.quit()
		self.stream.stop_stream()
		self.stream.close()
		self.player.terminate()
		self.file = wave.open(self.file_name, "rb")
		
		
	def visulizing(self):
		batch = 1024
		while True:
			data = self.file.readframes(batch)
			if data == b'':
				break
			#print(data)
			self.stream.write(data)
			fft_data = np.real(np.fft.fft(np.fromstring(data, dtype = np.int16)))
			self.window.fill((0, 0, 0))
			
			break_flag = False
			for event in pg.event.get():
				if event.type == pg.QUIT:
					break_flag = True
					break
			if break_flag or fft_data.size <= 0:
				break
				
			r_num = 0
			g_num = 85
			b_num = 171
			interval = fft_data.size // 128
			#print(fft_data.size)
			
			for i in range(0, 32, 8):
				pg.draw.rect(self.window, (r_num, g_num, b_num), Rect((i, 256 + 128 - 0), (8, 0)))
				r_num = (r_num + 3) % 256
				g_num = (g_num + 5) % 256
				b_num = (b_num + 3) % 256
			
			for i in range(0, fft_data.size, interval):
				#sum = 0
				#for j in range(min(interval, fft_data.size - i)):
					#sum += fft_data[i + j]
				#h = abs(int(sum / interval / 4096))
				#print(h)
				h = fft_data[i] / 4096
				pg.draw.rect(self.window, (r_num, g_num, b_num), Rect((32 + 8 * i / interval, 256 + 128 - h), (8, 2 * h)))
				r_num = (r_num + 3) % 256
				g_num = (g_num + 5) % 256
				b_num = (b_num + 3) % 256
			
			for i in range(0, 32, 8):
				pg.draw.rect(self.window, (r_num, g_num, b_num), Rect((1024 + 32 + i, 256 + 128 - 0), (8, 0)))
				r_num = (r_num + 3) % 256
				g_num = (g_num + 5) % 256
				b_num = (b_num + 3) % 256
			pg.display.update()
		

	def visualize(self):
		if not self.file_exist:
			messagebox.showwarning(title = '警告', message = '请先选择音频文件！')
			return
		self.visulizeBegin()
		self.visulizing()
		self.visulizeEnd()
		
	
	def choose(self):
		self.file_name = filedialog.askopenfilename(title = '选择音频文件', filetypes = [('WAV', '*.wav')], initialdir = (os.path.expanduser('.')))
		self.file = wave.open(self.file_name, "rb")
		self.file_exist = True

	
	def shutdown(self):
		sys.exit(0)

	
	def closeButton(self):
		result = messagebox.askyesno(title = '警告', message = '确认强制关闭程序？')
		if result:
			self.shutdown()
		else:
			return

			
if __name__ == "__main__":
	warnings.simplefilter("ignore", DeprecationWarning)
	GUI = Tk()
	GUI.title('音频可视化')
	MusicVisualization(GUI)
	GUI.mainloop()