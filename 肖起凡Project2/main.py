import warnings
import math
import argparse

import matplotlib.image as PngImage
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--texture', default = 'y', help = 'choice of texture')
parser.add_argument('-o', '--object', default = 'Vase', help = 'type of object')
ARGS = parser.parse_args()


def vaseFunc(x):
	alpha = 0.25
	beta = 0.5
	return alpha * math.sin(x) + beta

			
class RSG:
	def __init__(self, normalTexture = True):
		self.initLight()
		self.initTexture(normalTexture)
		self.initSetting()
		return
		
	
	def initLight(self):
		position = []
		if ARGS.object == 'Ball':
			position = [0.0, 0.0, 0.0, 1.0]
		elif ARGS.object == 'Vase':
			position = [0.75, -0.75, -0.5, 1.0]
		else:
			print("Unrecognized object!")
			exit(0)
		strength = [1.0, 1.0, 1.0, 1.0]
		glLightfv(GL_LIGHT0, GL_POSITION, position)
		glLightfv(GL_LIGHT0, GL_DIFFUSE, strength)
		glEnable(GL_LIGHTING)
		glEnable(GL_LIGHT0)
		
	
	def initTexture(self, normalTexture):
		self.drawTexture = not normalTexture
		if normalTexture:
			glEnable(GL_TEXTURE_GEN_S)
			glEnable(GL_TEXTURE_GEN_T)
			return
		
		img = PngImage.imread('texture.png')
		img = np.asarray(img * 255, dtype = np.uint8)
		color = GL_RGBA
		
		self.texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, self.texture)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP | GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP | GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexImage2D(GL_TEXTURE_2D, 0, color, img.shape[0], img.shape[1], 0, color, GL_UNSIGNED_BYTE, img)
		glEnable(GL_TEXTURE_2D)
	
	
	def initSetting(self):
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_POLYGON_SMOOTH)
		#glEnable(GL_COLOR_MATERIAL)
	
	
	def drawBegin(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glPushMatrix()
		glMatrixMode(GL_MODELVIEW)
		if ARGS.object == 'Ball':
			glRotatef(45.0, 0.0, -1.0, 0.0)
			glRotatef(15.0, 1.0, 0.0, 0.0)
			glRotatef(15.0, 0.0, 0.0, -1.0)
		elif ARGS.object == 'Vase':
			glRotatef(77.76, 1.0, 0.0, 0.0)
		else:
			print("Unrecognized object!")
			exit(0)
	
	
	def drawEnd(self):
		glPopMatrix()
		glFlush()
	
	
	def drawCircle(self, z, r, tex = True):
		if not tex:
			glDisable(GL_TEXTURE_2D)

		glBegin(GL_POLYGON)
		glNormal3f(0.0,0.0,1.0)
		for a in range(0, 360, 4):
			theta = a * math.pi / 180
			x = math.sin(theta)
			y = math.cos(theta)
			if tex:
				glTexCoord2fv([x, y])
			glVertex3fv([x * r, y * r, z])
		glEnd()
		
		if not tex:
			glEnable(GL_TEXTURE_2D)
	
	
	def drawingBall(self):
		eps = 1 / 512
		R = 0.75
		z = -R
		while z <= R:
			r = math.sqrt(R * R - z * z)
			self.drawCircle(z = z, r = r)
			z += eps
			
		
	def drawingVase(self):
		eps = 1 / 512
		R = 0.75
		z = -R
		base = (5 / 8) * 2 * math.pi
		while z <= -R + 4 * eps:
			l = (z + R) / (R + R) * 2 * math.pi
			r = vaseFunc(l + base)
			self.drawCircle(z = z, r = r, tex = False)
			z += eps
		while z <= R:
			l = (z + R) / (R + R) * 2 * math.pi
			r = vaseFunc(l + base)
			self.drawCircle(z = z, r = r)
			z += eps
	
	
	def output3D(self):
		self.drawBegin()
		if ARGS.object == 'Ball':
			self.drawingBall()
		elif ARGS.object == 'Vase':
			self.drawingVase()
		else:
			print("Unrecognized object!")
			exit(0)
		#self.showCoordinate()
		self.drawEnd()
		
		
	def showCoordinate(self):
		glBegin(GL_LINES)
		o = [0.0, 0.0, 0.0]		
		for i in range(3):
			p = [0.0, 0.0, 0.0]
			p[i] = 3.0
			glVertex3fv(o)
			glVertex3fv(p)
		glEnd()

	
if __name__ == "__main__":
	warnings.simplefilter("ignore", DeprecationWarning)
	glutInit()
	glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
	glutInitWindowSize(512, 512)
	glutCreateWindow(ARGS.object)
	normalTexture = (ARGS.texture == 'n')
	obj = RSG(normalTexture = normalTexture)
	glutDisplayFunc(obj.output3D)
	glutMainLoop()