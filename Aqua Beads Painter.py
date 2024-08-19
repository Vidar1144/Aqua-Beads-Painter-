#!/usr/bin/env python3

import tkinter as tk
from tkinter import colorchooser, filedialog
from tkinter.colorchooser import askcolor
from PIL import Image, ImageDraw

class AquaBeadPainter:
	def __init__(self, root):
		self.root = root
		self.root.title("Aqua Bead Painter")
		
		self.canvas_size = 500  # Size of the canvas
		self.grid_size = 25  # 25x25 grid
		self.dot_size = self.canvas_size // self.grid_size
		self.selected_color = "#FFFFFF"  # Start with white color
		
		self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="black")
		self.canvas.pack()
		
		self.canvas.bind("<Button-1>", self.paint_dot)
		self.canvas.bind("<Double-1>", self.erase_dot)  # Bind double-click to erase
		
		self.create_grid()
		self.create_color_selection()
		self.create_buttons()
		
		self.history = []  # To store the history of actions
		
	def create_grid(self):
		self.dots = []
		for i in range(self.grid_size):
			row = []
			for j in range(self.grid_size):
				x0 = i * self.dot_size
				y0 = j * self.dot_size
				x1 = x0 + self.dot_size
				y1 = y0 + self.dot_size
				dot = self.canvas.create_oval(x0, y0, x1, y1, outline="white", fill="black", tags=f"dot_{i}_{j}")
				row.append(dot)
			self.dots.append(row)
			
	def create_color_selection(self):
		self.color_label = tk.Label(self.root, text="Current Color", bg=self.selected_color, width=20)
		self.color_label.pack(pady=10, side="left")
		
		color_wheel_button = tk.Button(self.root, text="Select Color", command=self.choose_color)
		color_wheel_button.pack(pady=10, side="left")
		
	def choose_color(self):
		color_code = askcolor(title="Choose color")[1]
		if color_code:
			self.selected_color = color_code
			self.color_label.config(bg=self.selected_color)
			
	def create_buttons(self):
		button_frame = tk.Frame(self.root)
		button_frame.pack(side="bottom", pady=10)
		
		save_button = tk.Button(button_frame, text="Save Design", command=self.save_design)
		save_button.pack(side="left", padx=10)
		
		undo_button = tk.Button(button_frame, text="Undo", command=self.undo)
		undo_button.pack(side="left", padx=10)
		
	def paint_dot(self, event):
		x = event.x // self.dot_size
		y = event.y // self.dot_size
		
		current_color = self.canvas.itemcget(self.dots[x][y], "fill")
		self.history.append((x, y, current_color))
		
		self.canvas.itemconfig(self.dots[x][y], fill=self.selected_color)
		
	def erase_dot(self, event):
		x = event.x // self.dot_size
		y = event.y // self.dot_size
		
		current_color = self.canvas.itemcget(self.dots[x][y], "fill")
		self.history.append((x, y, current_color))
		
		# Set the dot color back to black (erased)
		self.canvas.itemconfig(self.dots[x][y], fill="black")
		
	def undo(self):
		if self.history:
			x, y, color = self.history.pop()
			self.canvas.itemconfig(self.dots[x][y], fill=color)
			
	def save_design(self):
		file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
		if not file_path:
			return
		
		image = Image.new("RGB", (self.canvas_size, self.canvas_size), "black")
		draw = ImageDraw.Draw(image)
		
		for i in range(self.grid_size):
			for j in range(self.grid_size):
				x0 = i * self.dot_size
				y0 = j * self.dot_size
				x1 = x0 + self.dot_size
				y1 = y0 + self.dot_size
				
				color = self.canvas.itemcget(self.dots[i][j], "fill")
				if color == "black":
					color = "black"
					
				draw.ellipse([x0, y0, x1, y1], fill=color, outline="white")
				
		image.save(file_path, "JPEG")
		print(f"Design saved as {file_path}")
		
if __name__ == "__main__":
	root = tk.Tk()
	app = AquaBeadPainter(root)
	root.mainloop()
	