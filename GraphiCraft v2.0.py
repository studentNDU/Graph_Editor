from tkinter import *
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk

class GraphicsEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Графічний редактор")
        self.master.geometry("800x600")

        self.image = None
        self.canvas = Canvas(self.master, width=800, height=600, bg="white")
        self.canvas.pack()

        menubar = Menu(self.master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Відкрити", command=self.open_image)
        filemenu.add_command(label="Зберегти", command=self.save_image)
        filemenu.add_separator()
        filemenu.add_command(label="Вихід", command=self.master.quit)
        menubar.add_cascade(label="Файл", menu=filemenu)

        toolmenu = Menu(menubar, tearoff=0)
        toolmenu.add_command(label="Лінія", command=self.set_tool_line)
        toolmenu.add_command(label="Коло", command=self.set_tool_circle)
        toolmenu.add_command(label="Прямокутник", command=self.set_tool_rectangle)
        toolmenu.add_separator()
        toolmenu.add_command(label="Ластик", command=self.set_tool_eraser)
        menubar.add_cascade(label="Інструменти", menu=toolmenu)

        colormenu = Menu(menubar, tearoff=0)
        colormenu.add_command(label="Вибрати колір", command=self.choose_color)
        menubar.add_cascade(label="Колір", menu=colormenu)

        self.master.config(menu=menubar)

        self.tool = "line"
        self.current_shape = None
        self.color = "black"

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.image = self.image.resize((800, 600), Image.ANTIALIAS)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            self.canvas.postscript(file=file_path + ".eps")
            img = Image.open(file_path + ".eps")
            img.save(file_path)

    def set_tool_line(self):
        self.tool = "line"

    def set_tool_circle(self):
        self.tool = "circle"

    def set_tool_rectangle(self):
        self.tool = "rectangle"

    def set_tool_eraser(self):
        self.tool = "eraser"

    def choose_color(self):
        self.color = colorchooser.askcolor()[1]

    def start_draw(self, event):
        self.last_x, self.last_y = event.x, event.y
        if self.tool == "circle":
            self.current_shape = self.canvas.create_oval(self.last_x, self.last_y, self.last_x, self.last_y, outline=self.color, width=2)
        elif self.tool == "rectangle":
            self.current_shape = self.canvas.create_rectangle(self.last_x, self.last_y, self.last_x, self.last_y, outline=self.color, width=2)
        elif self.tool == "eraser":
            self.current_shape = self.canvas.create_oval(self.last_x, self.last_y, self.last_x, self.last_y, outline="white", fill="white", width=10)

    def draw(self, event):
        if self.tool == "line":
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, width=5, fill=self.color)
            self.last_x, self.last_y = event.x, event.y
        elif self.tool == "circle":
            self.canvas.coords(self.current_shape, self.last_x, self.last_y, event.x, event.y)
        elif self.tool == "rectangle":
            self.canvas.coords(self.current_shape, self.last_x, self.last_y, event.x, event.y)
        elif self.tool == "eraser":
            self.canvas.coords(self.current_shape, event.x-5, event.y-5, event.x+5, event.y+5)

    def end_draw(self, event):
        pass

if __name__ == "__main__":
    root = Tk()
    app = GraphicsEditor(root)
    root.mainloop()
