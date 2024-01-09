import tkinter as tk

class GraphicsEditor:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.current_tool = None
        self.start_x = None
        self.start_y = None

        self.tools = {
            'line': self.use_line,
            'rectangle': self.use_rectangle,
            'circle': self.use_circle,
            'eraser': self.use_eraser
        }

        self.colors = {
            'black': 'black',
            'red': 'red',
            'green': 'green',
            'blue': 'blue'
        }

        self.selected_color = 'black'

        self.create_toolbox()
        self.create_color_palette()

        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.continue_drawing)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drawing)

    def create_toolbox(self):
        toolbox_frame = tk.Frame(self.root)
        toolbox_frame.pack(side='top', fill='x')

        for tool in self.tools:
            button = tk.Button(toolbox_frame, text=tool.capitalize(), command=self.tools[tool])
            button.pack(side='left', padx=5, pady=5)

    def create_color_palette(self):
        palette_frame = tk.Frame(self.root)
        palette_frame.pack(side='left', fill='y')

        for color in self.colors:
            button = tk.Button(palette_frame, bg=color, width=3, command=lambda c=color: self.select_color(c))
            button.pack(side='left', padx=5, pady=5)

    def select_color(self, color):
        self.selected_color = self.colors[color]

    def use_line(self):
        self.current_tool = 'line'

    def use_rectangle(self):
        self.current_tool = 'rectangle'

    def use_circle(self):
        self.current_tool = 'circle'

    def use_eraser(self):
        self.current_tool = 'eraser'

    def start_drawing(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def continue_drawing(self, event):
        if self.current_tool == 'line':
            self.canvas.delete('temp_shape')
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.selected_color, width=2, tags='temp_shape')
        elif self.current_tool == 'rectangle':
            self.canvas.delete('temp_shape')
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.selected_color, width=2, tags='temp_shape')
        elif self.current_tool == 'circle':
            self.canvas.delete('temp_shape')
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.selected_color, width=2, tags='temp_shape')
        elif self.current_tool == 'eraser':
            self.canvas.create_rectangle(event.x - 10, event.y - 10, event.x + 10, event.y + 10, fill='white', outline='white')

    def stop_drawing(self, event):
        if self.current_tool != 'pen' and self.start_x is not None and self.start_y is not None:
            if self.current_tool == 'line':
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.selected_color, width=2)
            elif self.current_tool == 'rectangle':
                self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.selected_color, width=2)
            elif self.current_tool == 'circle':
                self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.selected_color, width=2)

        self.start_x = None
        self.start_y = None

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Graphics Editor')
    editor = GraphicsEditor(root)
    root.mainloop()
