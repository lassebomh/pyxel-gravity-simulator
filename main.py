import pyxel as px
import numpy as np
from math import sqrt, pi, cos, sin
from random import choice

class MouseCreate:
	def __init__(self):
		self.name = "Create planet"
		self.radius = 4
		self.color = 4

	def middle_click(self):
		self.color = choice([4, 8, 12, 5, 9, 13, 2, 6, 10, 14, 3, 11])
		
	def left_click(self):
		global objs
		objs = np.append(objs, [Mass(
			x=px.mouse_x+camera_x,
			y=px.mouse_y+camera_y,
			x_vec=0,
			y_vec=0,
			mass=rtom(self.radius),
			color=self.color)])

	def left_start_dragging(self):
		global time_enabled
		time_enabled = False

	def left_stop_dragging(self):
		global objs, time_enabled
		time_enabled = True
		objs = np.append(objs, [Mass(
			x=left_drag_x+camera_x,
			y=left_drag_y+camera_y,
			x_vec=(px.mouse_x-left_drag_x)/25,
			y_vec=(px.mouse_y-left_drag_y)/25,
			mass=rtom(self.radius),
			color=self.color)])

	def render(self):
		global right_dragging, right_drag_x, right_drag_y
		if right_dragging:
			self.radius = sqrt((px.mouse_x-right_drag_x)**2+(px.mouse_y-right_drag_y)**2)
			px.circ(right_drag_x, right_drag_y, self.radius, self.color)
		elif left_dragging:
			px.circ(left_drag_x, left_drag_y, self.radius, self.color)
			_objs = np.array([Mass(obj.x, obj.y, obj.x_vec, obj.y_vec, obj.mass, "circle", 1) for obj in objs]+[Mass(
				x=left_drag_x+camera_x,
				y=left_drag_y+camera_y,
				x_vec=(px.mouse_x-left_drag_x)/25,
				y_vec=(px.mouse_y-left_drag_y)/25,
				mass=rtom(self.radius),
				color=8)])
			for tick in range(500):
				for self_obj in _objs:
					for other_obj in _objs:
						if other_obj == self_obj:
							continue
						try:
							self_obj.x_vec += -(4*other_obj.mass*(self_obj.x-other_obj.x))/(((self_obj.x-other_obj.x)**2+(self_obj.y-other_obj.y)**2)**(3/2))
						except ZeroDivisionError: pass
						try:
							self_obj.y_vec += -(4*other_obj.mass*(self_obj.y-other_obj.y))/(((self_obj.x-other_obj.x)**2+(self_obj.y-other_obj.y)**2)**(3/2))
						except ZeroDivisionError: pass

				for obj in _objs:
					obj.x += obj.x_vec
					obj.y += obj.y_vec

				for self_obj in _objs:
					for other_obj in _objs:
						if other_obj == self_obj:
							continue
						if sqrt((self_obj.x-other_obj.x)**2+(self_obj.y-other_obj.y)**2) < mtor(self_obj.mass)+mtor(other_obj.mass):
							#px.circb(self_obj.x-camera_x, self_obj.y-camera_y, mtor(self_obj.mass), self_obj.color)
							#px.circb(other_obj.x-camera_x, other_obj.y-camera_y, mtor(other_obj.mass), other_obj.color)
							other_obj.x_vec = other_obj.mass/(other_obj.mass+self_obj.mass) * other_obj.x_vec + self_obj.mass/(other_obj.mass+self_obj.mass) * self_obj.x_vec	
							other_obj.y_vec = other_obj.mass/(other_obj.mass+self_obj.mass) * other_obj.y_vec + self_obj.mass/(other_obj.mass+self_obj.mass) * self_obj.y_vec	
							other_obj.x = other_obj.mass/(other_obj.mass+self_obj.mass) * other_obj.x + self_obj.mass/(other_obj.mass+self_obj.mass) * self_obj.x	
							other_obj.y = other_obj.mass/(other_obj.mass+self_obj.mass) * other_obj.y + self_obj.mass/(other_obj.mass+self_obj.mass) * self_obj.y	
							other_obj.mass += self_obj.mass
							px.circb(other_obj.x-camera_x, other_obj.y-camera_y, mtor(other_obj.mass), other_obj.color)
							_objs = np.delete(_objs, np.where(_objs == self_obj), 0)
				for obj in _objs:
					px.pix(obj.x-camera_x, obj.y-camera_y, obj.color)
		else:
			px.circb(px.mouse_x, px.mouse_y, self.radius, self.color)

class MouseBlackHole:
	def __init__(self):
		self.name = "Black hole"
		self.circle_list = []
		self.radius = 10
		self.accel = 0

	def right_dragging(self):
		self.radius = sqrt((px.mouse_x-right_drag_x)**2+(px.mouse_y-right_drag_y)**2)
		a = int(2*self.radius*pi)//3
		for d in range(a):
			angle = (d/a)*2*pi
			px.pix(cos(angle)*self.radius+40, sin(angle)*self.radius+40, 7)

class Mass:
	def __init__(self, x, y, x_vec, y_vec, mass, visual_type="circle", color=10):
		self.color = color
		self.mass = mass
		self.x = x
		self.y = y
		self.x_vec = x_vec
		self.y_vec = y_vec
		if visual_type == "circle":
			self.render = lambda: px.circ(self.x-camera_x, self.y-camera_y, mtor(self.mass), self.color)

def mtor(mass):
	return sqrt(mass/pi)

def rtom(radius):
	return pi*radius**2

px.init(255, 255)
px.mouse(True)

objs = np.array([])
mouse = MouseCreate()
left_held = None
right_held = None
left_dragging = False
right_dragging = False
left_drag_x, left_drag_y = None, None
right_drag_x, right_drag_y = None, None
time_enabled = True
camera_x = 0
camera_y = 0

held_time = 4
camera_speed = 3

#objs = np.append(objs, [Mass(x=80, y=127, x_vec=0, y_vec=-2, mass=50)])
#objs = np.append(objs, [Mass(x=160, y=127, x_vec=0, y_vec=3, mass=20)])
#objs = np.append(objs, [Mass(x=127, y=167, x_vec=1, y_vec=0, mass=90)])

def update():
	global objs, right_held, left_held, camera_x, camera_y, camera_speed, mouse, left_drag_x, left_drag_y, right_drag_x, right_drag_y, left_dragging, right_dragging, time_enabled

	if px.btnp(px.KEY_Q):
		px.quit()
	if px.btnp(px.KEY_1):
		mouse = MouseCreate()
	if px.btnp(px.KEY_2):
		mouse = MouseBlackHole()
	if px.btnp(px.KEY_SPACE):
		time_enabled = not time_enabled

	if px.btn(px.KEY_W):
		camera_y -= camera_speed
	if px.btn(px.KEY_S):
		camera_y += camera_speed
	if px.btn(px.KEY_D):
		camera_x += camera_speed
	if px.btn(px.KEY_A):
		camera_x -= camera_speed

	if px.btnp(px.MOUSE_MIDDLE_BUTTON):
		if "middle_click" in dir(mouse): mouse.middle_click()

	if px.btn(px.MOUSE_LEFT_BUTTON):
		if left_held == None:
			left_held = 0
		else:
			left_held += 1

		if left_held == held_time:
			left_drag_x, left_drag_y = px.mouse_x, px.mouse_y
			if "left_start_dragging" in dir(mouse):
				mouse.left_start_dragging()
			left_dragging = True
		elif left_held > held_time:
			if "left_dragging" in dir(mouse): mouse.left_dragging()
	else:
		if not left_held == None:
			if left_held <= held_time:
				if "left_click" in dir(mouse): mouse.left_click()
				left_held = None
			else:
				left_dragging = False
				if "left_stop_dragging" in dir(mouse):
					mouse.left_stop_dragging()
					left_drag_x, left_drag_y = None, None
				left_held = None

	if px.btn(px.MOUSE_RIGHT_BUTTON):
		if right_held == None:
			right_held = 0
		else:
			right_held += 1

		if right_held == held_time:
			right_drag_x, right_drag_y = px.mouse_x, px.mouse_y
			if "right_start_dragging" in dir(mouse):
				mouse.right_start_dragging()
			right_dragging = True
		elif right_held > held_time:
			if "right_dragging" in dir(mouse): mouse.right_dragging()
	else:
		if not right_held == None:
			if right_held <= held_time:
				if "right_click" in dir(mouse): mouse.right_click()
				right_held = None
			else:
				if "right_stop_dragging" in dir(mouse):
					mouse.right_stop_dragging()
					right_drag_x, right_drag_y = None, None
				right_dragging = False
				right_held = None

	if time_enabled:
		for self_obj in objs:
			for other_obj in objs:
				if other_obj == self_obj:
					continue
				self_obj.x_vec += -(4*other_obj.mass*(self_obj.x-other_obj.x))/(((self_obj.x-other_obj.x)**2+(self_obj.y-other_obj.y)**2)**(3/2))
				self_obj.y_vec += -(4*other_obj.mass*(self_obj.y-other_obj.y))/(((self_obj.x-other_obj.x)**2+(self_obj.y-other_obj.y)**2)**(3/2))



		for obj in objs:
			obj.x += obj.x_vec
			obj.y += obj.y_vec

		for self_obj in objs:
			for other_obj in objs:
				if other_obj == self_obj:
					continue
				if sqrt((self_obj.x-other_obj.x)**2+(self_obj.y-other_obj.y)**2) < mtor(self_obj.mass)+mtor(other_obj.mass):
					other_obj.x_vec = other_obj.mass/(other_obj.mass+self_obj.mass) * other_obj.x_vec + self_obj.mass/(other_obj.mass+self_obj.mass) * self_obj.x_vec	
					other_obj.y_vec = other_obj.mass/(other_obj.mass+self_obj.mass) * other_obj.y_vec + self_obj.mass/(other_obj.mass+self_obj.mass) * self_obj.y_vec	
					other_obj.x = other_obj.mass/(other_obj.mass+self_obj.mass) * other_obj.x + self_obj.mass/(other_obj.mass+self_obj.mass) * self_obj.x	
					other_obj.y = other_obj.mass/(other_obj.mass+self_obj.mass) * other_obj.y + self_obj.mass/(other_obj.mass+self_obj.mass) * self_obj.y	
					other_obj.mass += self_obj.mass
					objs = np.delete(objs, np.where(objs == self_obj), 0)

def draw():
	px.cls(0)
	for obj in objs:
		obj.render()
	px.text(5, 255-10, mouse.name, 6)
	if "render" in dir(mouse): mouse.render()
	if not time_enabled: px.text(5, 255-20, "PAUSED", 6)

px.run(update, draw)