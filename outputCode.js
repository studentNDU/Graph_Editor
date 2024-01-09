const { dialog } = require('electron').remote;
const { BrowserWindow } = require('electron').remote;
const { app } = require('electron').remote;
const { Menu } = require('electron').remote;
const { MenuItem } = require('electron').remote;
const { ipcMain } = require('electron');
const { ipcRenderer } = require('electron');
const { shell } = require('electron');
const { clipboard } = require('electron');
const { nativeImage } = require('electron');
const { screen } = require('electron');
const { shell } = require('electron');
const { webFrame } = require('electron');
const { remote } = require('electron');
const { globalShortcut } = require('electron');
const { powerMonitor } = require('electron');
const { powerSaveBlocker } = require('electron');
const { protocol } = require('electron');
const { webContents } = require('electron');
const { BrowserView } = require('electron');
const { Notification } = require('electron');
const { Tray } = require('electron');
const { nativeTheme } = require('electron');
const { systemPreferences } = require('electron');
const { TouchBar } = require('electron');

class GraphicsEditor {
    constructor(master) {
        this.master = master;
        this.master.title = "Графічний редактор";
        this.master.geometry = "800x600";
        this.image = null;
        this.canvas = document.createElement('canvas');
        this.canvas.width = 800;
        this.canvas.height = 600;
        this.canvas.style.backgroundColor = "white";
        this.master.appendChild(this.canvas);
        const menubar = document.createElement('menu');
        const filemenu = document.createElement('menu');
        filemenu.label = "Файл";
        const openCommand = document.createElement('menuitem');
        openCommand.label = "Відкрити";
        openCommand.onclick = this.open_image.bind(this);
        filemenu.appendChild(openCommand);
        const saveCommand = document.createElement('menuitem');
        saveCommand.label = "Зберегти";
        saveCommand.onclick = this.save_image.bind(this);
        filemenu.appendChild(saveCommand);
        filemenu.appendChild(document.createElement('hr'));
        const exitCommand = document.createElement('menuitem');
        exitCommand.label = "Вихід";
        exitCommand.onclick = this.master.close.bind(this.master);
        filemenu.appendChild(exitCommand);
        menubar.appendChild(filemenu);
        const toolmenu = document.createElement('menu');
        toolmenu.label = "Інструменти";
        const lineCommand = document.createElement('menuitem');
        lineCommand.label = "Лінія";
        lineCommand.onclick = this.set_tool_line.bind(this);
        toolmenu.appendChild(lineCommand);
        const circleCommand = document.createElement('menuitem');
        circleCommand.label = "Коло";
        circleCommand.onclick = this.set_tool_circle.bind(this);
        toolmenu.appendChild(circleCommand);
        const rectangleCommand = document.createElement('menuitem');
        rectangleCommand.label = "Прямокутник";
        rectangleCommand.onclick = this.set_tool_rectangle.bind(this);
        toolmenu.appendChild(rectangleCommand);
        toolmenu.appendChild(document.createElement('hr'));
        const eraserCommand = document.createElement('menuitem');
        eraserCommand.label = "Ластик";
        eraserCommand.onclick = this.set_tool_eraser.bind(this);
        toolmenu.appendChild(eraserCommand);
        menubar.appendChild(toolmenu);
        const colormenu = document.createElement('menu');
        colormenu.label = "Колір";
        const chooseColorCommand = document.createElement('menuitem');
        chooseColorCommand.label = "Вибрати колір";
        chooseColorCommand.onclick = this.choose_color.bind(this);
        colormenu.appendChild(chooseColorCommand);
        menubar.appendChild(colormenu);
        this.master.appendChild(menubar);
        this.tool = "line";
        this.current_shape = null;
        this.color = "black";
        this.canvas.addEventListener("mousedown", this.start_draw.bind(this));
        this.canvas.addEventListener("mousemove", this.draw.bind(this));
        this.canvas.addEventListener("mouseup", this.end_draw.bind(this));
    }
    open_image() {
        const file_path = dialog.showOpenDialogSync();
        if (file_path) {
            this.image = new Image();
            this.image.src = file_path[0];
            this.image.onload = () => {
                const ctx = this.canvas.getContext('2d');
                ctx.drawImage(this.image, 0, 0, 800, 600);
            }
        }
    }
    save_image() {
        const file_path = dialog.showSaveDialogSync({ defaultPath: ".png" });
        if (file_path) {
            const ctx = this.canvas.getContext('2d');
            const dataURL = this.canvas.toDataURL();
            const link = document.createElement('a');
            link.href = dataURL;
            link.download = file_path;
            link.click();
        }
    }
    set_tool_line() {
        this.tool = "line";
    }
    set_tool_circle() {
        this.tool = "circle";
    }
    set_tool_rectangle() {
        this.tool = "rectangle";
    }
    set_tool_eraser() {
        this.tool = "eraser";
    }
    choose_color() {
        const color = dialog.showColorPickerSync();
        if (color) {
            this.color = color;
        }
    }
    start_draw(event) {
        this.last_x = event.clientX;
        this.last_y = event.clientY;
        if (this.tool === "circle") {
            this.current_shape = new Path2D();
            this.current_shape.ellipse(this.last_x, this.last_y, 0, 0, 0, 0, 2 * Math.PI);
        } else if (this.tool === "rectangle") {
            this.current_shape = new Path2D();
            this.current_shape.rect(this.last_x, this.last_y, 0, 0);
        } else if (this.tool === "eraser") {
            this.current_shape = new Path2D();
            this.current_shape.ellipse(this.last_x, this.last_y, 5, 5, 0, 0, 2 * Math.PI);
        }
    }
    draw(event) {
        const ctx = this.canvas.getContext('2d');
        if (this.tool === "line") {
            ctx.beginPath();
            ctx.moveTo(this.last_x, this.last_y);
            ctx.lineTo(event.clientX, event.clientY);
            ctx.lineWidth = 5;
            ctx.strokeStyle = this.color;
            ctx.stroke();
            this.last_x = event.clientX;
            this.last_y = event.clientY;
        } else if (this.tool === "circle") {
            const width = event.clientX - this.last_x;
            const height = event.clientY - this.last_y;
            ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            ctx.drawImage(this.image, 0, 0, 800, 600);
            ctx.beginPath();
            ctx.ellipse(this.last_x, this.last_y, Math.abs(width), Math.abs(height), 0, 0, 2 * Math.PI);
            ctx.lineWidth = 2;
            ctx.strokeStyle = this.color;
            ctx.stroke();
        } else if (this.tool === "rectangle") {
            const width = event.clientX - this.last_x;
            const height = event.clientY - this.last_y;
            ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            ctx.drawImage(this.image, 0, 0, 800, 600);
            ctx.beginPath();
            ctx.rect(this.last_x, this.last_y, width, height);
            ctx.lineWidth = 2;
            ctx.strokeStyle = this.color;
            ctx.stroke();
        } else if (this.tool === "eraser") {
            const x = event.clientX - 5;
            const y = event.clientY - 5;
            ctx.clearRect(x, y, 10, 10);
        }
    }
    end_draw(event) {
        // Do nothing
    }
}

const root = document.createElement('div');
document.body.appendChild(root);
const app = new GraphicsEditor(root);


