import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random




class Cube:
	def __init__(self,center,size,colors): #[x,y,z],size of cube, 6 colors
		size/=2
		self.nodes=[[center[0]+size,center[1]-size,center[2]-size],[center[0]+size,center[1]+size,center[2]-size],[center[0]-size,center[1]+size,center[2]-size],[center[0]-size,center[1]-size,center[2]-size],[center[0]+size,center[1]-size,center[2]+size],[center[0]+size,center[1]+size,center[2]+size],[center[0]-size,center[1]-size,center[2]+size],[center[0]-size,center[1]+size,center[2]+size]]
		self.color=colors
		self.walls=((0,1,2,3),(3,2,7,6),(6,7,5,4),(4,5,1,0),(1,5,7,2),(4,0,3,6))
		self.lines=((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7))
	def draw(self):
		
		for i in range(6):
			glBegin(GL_QUADS)
			glColor3fv(self.color[i])
			for j in range(4):
				glVertex3fv(self.nodes[self.walls[i][j]])
			glEnd()
		
		glColor3fv((0,0,0))
		for i in range(12):
			glBegin(GL_LINES)
			for j in range(2):
				glVertex3fv(self.nodes[self.lines[i][j]])
			glEnd()
	def rotate(self,direction,angle):
		if(direction=='x'):
			for i in range(8):
				newx=self.nodes[i][2]
				newy=self.nodes[i][1]
				self.nodes[i][2]=newx*math.cos(math.radians(angle))-newy*math.sin(math.radians(angle))
				self.nodes[i][1]=newx*math.sin(math.radians(angle))+newy*math.cos(math.radians(angle))
		elif(direction=='y'):
			for i in range(8):
				newx=self.nodes[i][2]
				newy=self.nodes[i][0]
				self.nodes[i][2]=newx*math.cos(math.radians(angle))-newy*math.sin(math.radians(angle))
				self.nodes[i][0]=newx*math.sin(math.radians(angle))+newy*math.cos(math.radians(angle))
		else:
			for i in range(8):
				newx=self.nodes[i][0]
				newy=self.nodes[i][1]
				self.nodes[i][0]=newx*math.cos(math.radians(angle))-newy*math.sin(math.radians(angle))
				self.nodes[i][1]=newx*math.sin(math.radians(angle))+newy*math.cos(math.radians(angle))

class Rubik:
	def __init__(self):
		self.reset()
	def reset(self):
		self.tab=[[[],[],[]],[[],[],[]],[[],[],[]]]
		for i in range(3):
			for j in range(3):
				for k in range(3):
					self.tab[i][j].append(Cube([-2+i*2,-2+j*2,-2+k*2],2,((255/255,255/255,255/255),(183/255,18/255,52/255),(255/255,213/255,0/255),(255/255,88/255,0/255),(0/255,70/255,173/255),(0/255,155/255,72/255),(0/255,70/255,173/255))))
	def shuffle(self,number):
		for i in range(number):
			temp=random.randint(0,2)
			if temp==0:
				temp=random.randint(0,2)
				self.rotate('x',temp,90)
				self.changePosition('x',temp,True)
			elif temp==1:
				temp=random.randint(0,2)
				self.rotate('y',temp,90)
				self.changePosition('y',temp,True)
			else:
				temp=random.randint(0,2)
				self.rotate('z',temp,90)
				self.changePosition('z',temp,True)
	def rotate(self,direction,number,angle):
		if(direction=='x'):
			for i in range(3):
				for j in range(3):
					self.tab[number][i][j].rotate('x',angle)
		elif(direction=='y'):
			for i in range(3):
				for j in range(3):
					self.tab[i][number][j].rotate('y',angle)
		else:
			for i in range(3):
				for j in range(3):
					self.tab[i][j][number].rotate('z',angle)
	def changePosition(self,direction,number,side):
		if(direction=='x'):
			temp=self.tab[number][0][1]
			self.tab[number][0][1]=self.tab[number][1][0]
			self.tab[number][1][0]=self.tab[number][2][1]
			self.tab[number][2][1]=self.tab[number][1][2]
			self.tab[number][1][2]=temp
			
			temp=self.tab[number][0][0]
			self.tab[number][0][0]=self.tab[number][2][0]
			self.tab[number][2][0]=self.tab[number][2][2]
			self.tab[number][2][2]=self.tab[number][0][2]
			self.tab[number][0][2]=temp
		elif(direction=='y'):
			temp=self.tab[0][number][1]
			self.tab[0][number][1]=self.tab[1][number][0]
			self.tab[1][number][0]=self.tab[2][number][1]
			self.tab[2][number][1]=self.tab[1][number][2]
			self.tab[1][number][2]=temp
			
			temp=self.tab[0][number][0]
			self.tab[0][number][0]=self.tab[2][number][0]
			self.tab[2][number][0]=self.tab[2][number][2]
			self.tab[2][number][2]=self.tab[0][number][2]
			self.tab[0][number][2]=temp
		else:
			temp=self.tab[1][0][number]
			self.tab[1][0][number]=self.tab[0][1][number]
			self.tab[0][1][number]=self.tab[1][2][number]
			self.tab[1][2][number]=self.tab[2][1][number]
			self.tab[2][1][number]=temp
			
			temp=self.tab[0][0][number]
			self.tab[0][0][number]=self.tab[0][2][number]
			self.tab[0][2][number]=self.tab[2][2][number]
			self.tab[2][2][number]=self.tab[2][0][number]
			self.tab[2][0][number]=temp
		
		if not side:
			self.changePosition(direction,number,True)
			self.changePosition(direction,number,True)
	def draw(self):
		for i in self.tab:
			for j in i:
				for k in j:
					k.draw()
		
	
class Game:
	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode((600, 600),DOUBLEBUF|OPENGL)
		pygame.display.set_caption(('Rubik\'s cube'))
		gluPerspective(45, 1.0, 0.1, 50.0)
		glTranslatef(0.0,0.0, -15)
		glRotatef(45, 1, -2, -1)
		self.clock = pygame.time.Clock()
		glEnable(GL_DEPTH_TEST)
		glLineWidth(2)
		self.queue=[]
		
		self.rubik=Rubik()
		#self.rubik.shuffle(50)
	def show(self):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glClearColor(0.5294117647058824,0.807843137254902,0.9215686274509803,1)
		self.rubik.draw()
		
		pygame.display.flip()
		self.clock.tick(60)
	def loop(self):
		while True:
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_KP1:
						if pygame.key.get_pressed()[pygame.K_KP0]:
							for i in range(30): self.queue.append(['x',0,-3])
							self.queue.append(['x',0,-4])
						else:
							for i in range(30): self.queue.append(['x',0,3])
							self.queue.append(['x',0,4])
					if event.key == pygame.K_KP2:
						if pygame.key.get_pressed()[pygame.K_KP0]:
							for i in range(30): self.queue.append(['x',1,-3])
							self.queue.append(['x',1,-4])
						else:
							for i in range(30): self.queue.append(['x',1,3])
							self.queue.append(['x',1,4])
					if event.key == pygame.K_KP3:
						if pygame.key.get_pressed()[pygame.K_KP0]:
							for i in range(30): self.queue.append(['x',2,-3])
							self.queue.append(['x',2,-4])
						else:
							for i in range(30): self.queue.append(['x',2,3])
							self.queue.append(['x',2,4])
					if event.key == pygame.K_KP4:
						if pygame.key.get_pressed()[pygame.K_KP0]:
							for i in range(30): self.queue.append(['y',0,-3])
							self.queue.append(['y',0,-4])
						else:
							for i in range(30): self.queue.append(['y',0,3])
							self.queue.append(['y',0,4])
					if event.key == pygame.K_KP5:
						if pygame.key.get_pressed()[pygame.K_KP0]:
							for i in range(30): self.queue.append(['y',1,-3])
							self.queue.append(['y',1,-4])
						else:
							for i in range(30): self.queue.append(['y',1,3])
							self.queue.append(['y',1,4])
					if event.key == pygame.K_KP6:
						if pygame.key.get_pressed()[pygame.K_KP0]:
							for i in range(30): self.queue.append(['y',2,-3])
							self.queue.append(['y',2,-4])
						else:
							for i in range(30): self.queue.append(['y',2,3])
							self.queue.append(['y',2,4])
					if event.key == pygame.K_KP7:
						if pygame.key.get_pressed()[pygame.K_KP0]:
							for i in range(30): self.queue.append(['z',0,-3])
							self.queue.append(['z',0,-4])
						else:
							for i in range(30): self.queue.append(['z',0,3])
							self.queue.append(['z',0,4])
					if event.key == pygame.K_KP8:
						if pygame.key.get_pressed()[pygame.K_KP0]:
							for i in range(30): self.queue.append(['z',1,-3])
							self.queue.append(['z',1,-4])
						else:
							for i in range(30): self.queue.append(['z',1,3])
							self.queue.append(['z',1,4])
					if event.key == pygame.K_KP9:
						if pygame.key.get_pressed()[pygame.K_KP0]:
							for i in range(30): self.queue.append(['z',2,-3])
							self.queue.append(['z',2,-4])
						else:
							for i in range(30): self.queue.append(['z',2,3])
							self.queue.append(['z',2,4])
						
			
			
			if pygame.key.get_pressed()[pygame.K_q]:
				glRotatef(1, 1, 0, 0)
			if pygame.key.get_pressed()[pygame.K_a]:
				glRotatef(-1, 1, 0, 0)
			if pygame.key.get_pressed()[pygame.K_w]:
				glRotatef(1, 0, 1, 0)
			if pygame.key.get_pressed()[pygame.K_s]:
				glRotatef(-1, 0, 1, 0)
			if pygame.key.get_pressed()[pygame.K_e]:
				glRotatef(1, 0, 0, 1)
			if pygame.key.get_pressed()[pygame.K_d]:
				glRotatef(-1, 0, 0, 1)
			
			if self.queue!=[]:
				if self.queue[0][2]==-4:
					self.rubik.changePosition(self.queue[0][0],self.queue[0][1],False)
				elif self.queue[0][2]==4:
					self.rubik.changePosition(self.queue[0][0],self.queue[0][1],True)
				else:
					self.rubik.rotate(self.queue[0][0],self.queue[0][1],self.queue[0][2])
				self.queue.pop(0)
			self.show()
			
game=Game()
game.loop()