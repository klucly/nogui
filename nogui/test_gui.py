# import __init__ as nogui
import nogui
from nogui import Matrix, Vec2
import tkinter
from tkinter import filedialog
import threading
from math import sin, cos, tan, degrees, radians
import os
from time import sleep
import importlib
import shutil

class Thread(threading.Thread):
    def __init__(self, func) -> None:
        super().__init__()
        self.func = func

    def run(self) -> None: self.func()
        

class PropertiesWin:
    size = "200x600"
    win = None
    title = "properties"
    resizable = 1, 1
    objectlist_input_list = []

    def create_win(self, main) -> None:
        self.win = tkinter.Tk()
        self.win.title(self.title)
        self.win.resizable(self.resizable[0], self.resizable[1])
        self.win.geometry(self.size)

        self.menu = tkinter.Menu(self.win)
        self.menu.file = tkinter.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label = "File", menu = self.menu.file)

        self.menu.file.file = tkinter.Menu(self.menu.file, tearoff = 0)
        self.menu.file.add_cascade(label = "File", menu = self.menu.file.file)

        self.menu.file.file.add_command(label = "Open", command = main.open)
        self.menu.file.file.add_command(label = "Save", command = main.save)
        self.menu.file.file.add_command(label = "Save as", command = main.saveas)
        self.menu.file.file.add_checkbutton(label = "run", command = main.menu_start_stop, variable = tkinter.BooleanVar())
        self.menu.file.file.add_command(label = "Reload", command = main.reload_files)

        self.menu.file.files = tkinter.Menu(self.menu.file, tearoff = 0)
        self.menu.file.add_cascade(label = "Files", menu = self.menu.file.files)

        self.menu.file.files.add_command(label = "New", command = main.new_pyfile)
        
        self.menu.file.files.delete_file = tkinter.Menu(self.menu.file.files, tearoff = 0)
        self.menu.file.files.add_cascade(label = "Delete", menu = self.menu.file.files.delete_file)

        self.menu.create = tkinter.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label = "Create", menu = self.menu.create)

        self.menu.create.add_command(label = "Rectangle", command = lambda: main.create_object("Rectangle"))
        self.menu.create.add_command(label = "Circle", command = lambda: main.create_object("Circle"))
        self.menu.create.add_command(label = "Super-rectangle", command = lambda: main.create_object("SuperRectangle"))
        self.menu.create.add_command(label = "Polygon", command = lambda: main.create_object("Polygon"))

        self.menu.functions = tkinter.Menu(self.menu.file, tearoff = 0)
        self.menu.file.add_cascade(label = "build in funcs", menu = self.menu.functions)

        for str_func in main.__dir__():
            func = getattr(main, str_func)
            if str_func[0] != "_":
                if func.__class__ == self.create_win.__class__:
                    if func.__code__.co_argcount <= 1:
                        if "thread" in str_func or "Thread" in str_func:
                            self.menu.functions.add_command(label = func.__code__.co_name, command = func, background = "#700", activebackground = "#b00", foreground = "#ccc", activeforeground = "#000")
                        elif "update" in str_func:
                            self.menu.functions.add_command(label = func.__code__.co_name, command = func, background = "#070", activebackground = "#0b0", foreground = "#ccc", activeforeground = "#000")
                        elif "object" in str_func:
                            self.menu.functions.add_command(label = func.__code__.co_name, command = func, background = "#007", activebackground = "#00b", foreground = "#ccc", activeforeground = "#fff")
                        else:
                            self.menu.functions.add_command(label = func.__code__.co_name, command = func, background = "#444", activebackground = "#bbb", foreground = "#ccc", activeforeground = "#000")
        self.menu.functions.inactive = tkinter.Menu(self.menu.functions, tearoff = 0)
        self.menu.functions.add_cascade(label = "Inactive", menu = self.menu.functions.inactive)

        for str_func in main.__dir__():
            func = getattr(main, str_func)
            if str_func[0] != "_":
                if func.__class__ == self.create_win.__class__:
                    if func.__code__.co_argcount > 1:
                        self.menu.functions.inactive.add_command(label = func.__code__.co_name, command = func, background = "#444", activebackground = "#888", state = tkinter.DISABLED)


        self.win.config(menu = self.menu)

        self.properties_frame = tkinter.LabelFrame(self.win, text = "Properties")
        self.properties_frame.place(relheight=.5, relwidth=1)

        self.properties_widget = tkinter.Listbox(self.properties_frame)
        self.properties_widget.place(relwidth = 1, relheight = 1)
        
        self.objectlist_frame = tkinter.LabelFrame(self.win, text = "Objects")
        self.objectlist_frame.place(rely = .5, relheight=.5, relwidth=1)

        self.objectlist_widget = tkinter.Listbox(self.objectlist_frame)
        self.objectlist_widget.place(relwidth = 1, relheight = 1)
        self.objectlist_widget.bind("<Double-Button-1>", lambda event: main.select_object())
        self.objectlist_widget.bind("<Button-3>", main.obj_menu)

        self.objectlist_widget.menu = tkinter.Menu(self.win, tearoff = 0)
        
        self.objectlist_widget.menu.add_command(label = "Delete", command = main.delete_object)
        self.objectlist_widget.menu.add_command(label = "Move up", command = lambda: main.move_obj("up"))
        self.objectlist_widget.menu.add_command(label = "Move down", command = lambda: main.move_obj("down"))
        self.objectlist_widget.menu.add_command(label = "Update", command = main.update_objlist_widget)

        self.win.bind("<Button-1>", lambda coords: self.objectlist_widget.menu.unpost())
        self.win.bind("<Alt-r>", lambda something: main.reload_files())
        self.win.bind("<Alt-e>", lambda something: main.menu_start_stop())
        self.win.bind("<Control-s>", lambda something: main.save())
        self.win.bind("<Control-Shift-S>", lambda something: main.saveas())
        self.win.bind("<Control-o>", lambda something: main.open())

class Main:
    first_window = tkinter.Tk()
    first_window.size_text = tkinter.Label(first_window, text = "Console size: ", fg="#fff")
    first_window.size_input = tkinter.Entry(first_window, width = 7, insertwidth = 7)
    first_window.bg_symbol_text = tkinter.Label(first_window, text = "Bg symbol: ", fg="#fff")
    first_window.bg_symbol_input = tkinter.Entry(first_window, insertwidth = 1, width = 1)
    first_window.create_button = tkinter.Button(first_window, text = "Create")
    first_window.open_button = tkinter.Button(first_window, text = "Open")
    first_window.is_broken = False
    properties_win = PropertiesWin()
    curselected_index = None

    win_size = [40, 20]
    win_bg = "."

    objectlist = []
    attrList = []
    tick = 0
    error_count = 0
    run = False
    saved = False
    need_save = False
    need_open = False
    mainthread = None
    show_console_errors = True
    update_file_tread = False
    properties_thread_ = None
    canvasThread_ = None
    debugConsoleThread_ = None
    filesThread_ = None

    filedir = {"name":str(id(properties_win)), "files":{}}
    filelibs = []
    
    def first_window_update(self) -> None:
        str_size = self.first_window.size_input.get()
        str_bg_symbol = self.first_window.bg_symbol_input.get()

        if len(str_size) > 7:
            self.first_window.size_input.delete(0, tkinter.END)
            self.first_window.size_input.insert(0, str_size[:-1])
        
        if len(str_bg_symbol) > 1:
            self.first_window.bg_symbol_input.delete(0, tkinter.END)
            self.first_window.bg_symbol_input.insert(0, str_bg_symbol[:-1])


    def __init__(self) -> None:
        self.first_window.resizable(0, 0)
        self.first_window.title("New app")
        self.first_window.bg_symbol_input.insert(0, ".")
        self.first_window.size_input.insert(0, "40x20")
        self.first_window.bind("<KeyPress>", lambda key: self.first_window_update())
        self.first_window.size_text.grid(row = 1, column = 1)
        self.first_window.size_input.grid(row = 1, column = 2)
        self.first_window.bg_symbol_text.grid(row = 2, column = 1)
        self.first_window.bg_symbol_input.grid(row = 2, column = 2)
        self.first_window.create_button.grid(row = 3, column = 1)
        self.first_window.open_button.grid(row = 3, column = 2)
        self.first_window.create_button["command"] = self.start
        self.first_window.open_button["command"] = self.first_open
        if "files" in os.listdir("."): shutil.rmtree("files")
        os.mkdir("files")
        try:
            while not self.first_window.is_broken: self.first_window.update()
        except tkinter.TclError: print("Exiting...")


    def thread_init(self) -> None:
        self.properties_thread_ = Thread(self.properties_thread)
        self.properties_thread_.start()
        self.debugConsoleThread_ = Thread(self.debugConsoleThread)
        self.debugConsoleThread_.start()
        self.filesThread_ = Thread(self.filesThread)
        self.filesThread_.start()
        while 1: self.canvasThread()


    def start(self) -> None:
        self.win_bg = self.first_window.bg_symbol_input.get()
        self.win_size = self.first_window.size_input.get().split("x")
        self.win_size = int(self.win_size[0]), int(self.win_size[1])
        self.first_window.destroy()
        self.first_window.is_broken = True
        
        self.matrix = nogui.Matrix(self.win_size, self.win_bg, 30, 1)

        self.thread_init()


    def first_open(self) -> None:
        self.first_window.destroy()
        self.first_window.is_broken = True
        self.matrix = nogui.Matrix(self.win_size, self.win_bg, 30, 1)

        self.mainthread = lambda: self.open(filedialog.askopenfile())
        self.thread_init()
        

    def menu_start_stop(self) -> None: self.run = not self.run


    def create_object(self, obj) -> None:
        if obj == "Rectangle":
            self.objectlist.append(nogui.RectangleXYWH(self.matrix, Vec2(1, 1), Vec2(2, 2), "#"))
        elif obj == "Circle":
            self.objectlist.append(nogui.Circle(self.matrix, Vec2(10, 5), 5, "#"))
        elif obj == "SuperRectangle":
            self.objectlist.append(nogui.RectangleFULL(self.matrix, Vec2(1, 1), Vec2(5, 5), "#", 0))
        elif obj == "Polygon":
            self.objectlist.append(nogui.Polygon(self.matrix, [[2, 5], [10, 10], [4, 12]], "#"))
        self.objectlist[-1].attr = {}
        
        self.update_objlist_widget()


    def update_objlist_widget(self) -> None:
        self.properties_win.objectlist_widget.delete(0, tkinter.END)
        for i in range(len(self.objectlist)):

            if self.objectlist[i].__repr__()[0] != "<" or self.objectlist[i].__repr__()[-1] != ">":
                self.properties_win.objectlist_widget.insert(tkinter.END, f"{self.objectlist[i].__repr__()} {i}")
            else:
                self.properties_win.objectlist_widget.insert(tkinter.END, f"Undefined object {i}")


    def update_properties_widget(self, attrs) -> None:
        for obj in self.properties_win.objectlist_input_list:
            obj.destroy()
        self.properties_win.objectlist_input_list = []
        properties = []
        self.properties_win.properties_widget.delete(0, tkinter.END)
        for attr in attrs:
            self.properties_win.properties_widget.insert(tkinter.END, attr)
            self.properties_win.objectlist_input_list.append(tkinter.Entry(self.properties_win.properties_frame))
            properties.append(attrs[attr])

        for i in range(len(attrs)):
            self.properties_win.objectlist_input_list[i].delete(0, tkinter.END)
            self.properties_win.objectlist_input_list[i].insert(0, properties[i])
            self.properties_win.objectlist_input_list[i].place(x = 100, y = i*20.2, relwidth = 1, height = 20.2)


    def get_attrs_from_obj(self, selected_obj):
        attrs = {}
        self.attrList = []
        attrList = selected_obj.__dir__()
        blocked_attrs = ["matrix", "x_min", "x_max", "y_min", "y_max", "figure", "lines", "center", "max_x", "min_x", "min_y", "max_y", "attr"]

        for attr in attrList:
            if attr[0] != "_" and getattr(selected_obj, attr).__class__ != self.__init__.__class__ and attr not in blocked_attrs:
                # attrs[attr] = getattr(selected_obj, attr)
                try: attrs[attr] = selected_obj.attr[attr]
                except: attrs[attr] = getattr(selected_obj, attr)
                self.attrList.append(attr)

        return attrs, self.attrList


    def select_object(self) -> None:
        selected_i = self.properties_win.objectlist_widget.curselection()
        self.curselected_index = selected_i[0]
        selected_obj = self.objectlist[selected_i[0]]
        
        attrs = self.get_attrs_from_obj(selected_obj)[0]
        self.update_properties_widget(attrs)


    def obj_menu(self, coords) -> None:
        x, y = coords.x_root, coords.y_root
        self.properties_win.objectlist_widget.menu.post(x, y)


    def delete_object(self) -> None:
        if self.curselected_index != None:
            self.objectlist.pop(self.curselected_index)
            if self.curselected_index != 0:
                self.curselected_index -= 1
            else: self.curselected_index = None
            self.update_objlist_widget()
            self.update_properties_widget([])


    def move_obj(self, vector: str) -> None:
        obj = self.objectlist[self.curselected_index]
        index = self.curselected_index

        self.objectlist.pop(index)
        if vector == "up": self.objectlist.insert(index-1, obj)
        elif vector == "down": self.objectlist.insert(index+1, obj)

        self.update_objlist_widget()
        self.update_properties_widget([])


    def command(self, command: str) -> None:
        attrs = command.split(" ")[1:]
        command = command.split(" ")[0]
        
        if command == "add":
            obj = attrs[0]

            if obj == "rectangle" or obj == "rect":
                self.objectlist.append(nogui.RectangleXYWH(self.matrix, Vec2(int(attrs[1]), int(attrs[2])), Vec2(int(attrs[3]), int(attrs[4])), attrs[5]))
            elif obj == "circle":
                self.objectlist.append(nogui.Circle(self.matrix, Vec2(int(attrs[1]), int(attrs[2])), int(attrs[3]), attrs[4]))
            elif obj == "superrect":
                self.objectlist.append(nogui.RectangleFULL(self.matrix, Vec2(int(attrs[1]), int(attrs[2])), Vec2(int(attrs[3]), int(attrs[4])), attrs[5], int(attrs[6])))
            self.mainthread = self.update_objlist_widget

        elif command == "change" or command == "c":
            obj_i, attr = attrs[0].split(".")
            obj = self.objectlist[int(obj_i)]
            if self.curselected_index == int(obj_i):
                try:
                    self.mainthread = lambda: self.properties_win.objectlist_input_list[self.get_attrs_from_obj(obj)[1].index(attr)].delete(0, tkinter.END)
                    sleep(.01)
                    self.mainthread = lambda: self.properties_win.objectlist_input_list[self.get_attrs_from_obj(obj)[1].index(attr)].insert(0, attrs[1])
                except: pass
            try: obj.attr[attr] = eval(attrs[1])
            except:
                try: obj.attr[attr] = attrs[1]
                except: pass
            try: setattr(obj, attr, obj.attr[attr])
            except: pass


    def saveas(self) -> None: self.need_save = True


    def save(self, file = "None") -> None:
        if not self.saved:
            self.need_save = True
            return None
        output = {"objlist":{}}

        for obj in self.objectlist:
            if obj.__class__ == nogui.RectangleXYWH:
                obj_type = "Rectangle "+str(self.objectlist.index(obj))
            elif obj.__class__ == nogui.Circle:
                obj_type = "Circle "+str(self.objectlist.index(obj))
            elif obj.__class__ == nogui.RectangleFULL:
                obj_type = "RectangleFULL "+str(self.objectlist.index(obj))
            elif obj.__class__ == nogui.Polygon:
                obj_type = "Polygon "+str(self.objectlist.index(obj))
            else: obj_type = "Undefined "+str(self.objectlist.index(obj))

            output["objlist"][obj_type] = obj.attr

        output["files"] = self.filedir["files"]
        output["win_size"] = self.win_size
        output["win_bg"] = self.win_bg


        if file == None:
            self.saved = False
            
        elif file != "None":
            file.write(str(output))
            file.close()


    def open(self, file = "None") -> None:
        if file == "None":
            self.need_open = True
            return None
        elif file == None:
            return None

        self.curselected_index = None
        self.objectlist = []
        inp = file.read()
        file.close()
        inp = eval(inp)

        if "win_size" in inp: self.win_size = inp["win_size"]
        if "win_bg" in inp: self.win_bg = inp["win_bg"]

        self.matrix = Matrix(self.win_size, self.win_bg, 30, True)

        for filename in inp["files"]:
            fileinp = inp["files"][filename]
            self.new_pyfile(fileinp)


        for obj in inp["objlist"]:
            
            if obj.split(" ")[0] == "Rectangle":
                self.create_object("Rectangle")
            elif obj.split(" ")[0] == "Circle":
                self.create_object("Circle")
            elif obj.split(" ")[0] == "RectangleFULL":
                self.create_object("SuperRectangle")
            elif obj.split(" ")[0] == "Polygon":
                self.create_object("Polygon")
            elif obj.split(" ")[0] == "Undefined":
                ...

            for attr in inp["objlist"][obj]:
                try: self.objectlist[-1].attr[attr] = inp["objlist"][obj][attr]
                except: pass


    def new_pyfile(self, insert = "") -> None:

        if self.filelibs == []:
            self.properties_win.menu.file.files.add_separator()

        direct = self.filedir["name"]
        if direct not in os.listdir("files"):
            os.mkdir("files/"+direct)
        

        dirlist = os.listdir("files/"+direct)
        filelistlen = (len(dirlist)-1 if len(dirlist)-1 >= 0 else 0)

        filename = "file-"+str(filelistlen)

        with open(f"files/{direct}/{filename}.py", "w") as file:
            file.write(insert)

        self.properties_win.menu.file.files.add_command(label = filename, command = lambda: self.open_file(filename))
        self.properties_win.menu.file.files.delete_file.add_command(label = filename, command = lambda: self.delete_file(filename))
        self.filedir["files"][filename] = ""

        file = importlib.__import__(f"files.{self.filedir['name']}.{filename}")
        file = getattr(getattr(file, self.filedir['name']), filename)
        self.filelibs.append(file)


    def open_file(self, file) -> None:
        if os.name == "nt":
            os.system(f"files/{self.filedir['name']}/{file}.py")
        else:
            os.system(f"open files/{self.filedir['name']}/{file}.py")
            os.system(f"kde-open files/{self.filedir['name']}/{file}.py")
            os.system(f"xdg-open files/{self.filedir['name']}/{file}.py")
            os.system(f"gnome-open files/{self.filedir['name']}/{file}.py")
            nogui.clear_console()
        sleep(.5)
        print(">>>", end = "")


    def reboot_file_thread(self) -> None:
        self.filesThread_ = Thread(self.filesThread)
        self.filesThread_.start()


    def reload_files(self) -> None: self.tick = 0


    def delete_file(self, name):
        self.filelibs.pop(int(name.split("-")[1]))
        self.properties_win.menu.file.files.delete(name)
        self.properties_win.menu.file.files.delete_file.delete(name)
        os.remove(f"files/{self.filedir['name']}/{name}.py")
        self.filedir["files"].pop(name)
        if self.filelibs == []:
            self.properties_win.menu.file.files.delete(tkinter.END)
        

    def quit(self): ...





    def properties_thread(self) -> None:
        self.properties_win.create_win(self)
        while 1:
            if self.curselected_index == None: selected_obj = None
            else:
                if len(self.objectlist) > self.curselected_index:
                    selected_obj = self.objectlist[self.curselected_index]
        
                    for propertyinp in self.properties_win.objectlist_input_list:
                        property_str = propertyinp.get()
                        try: property = eval(propertyinp.get())
                        except: property = propertyinp.get()
                        index = self.properties_win.objectlist_input_list.index(propertyinp)
                        try:
                            setattr(selected_obj, self.get_attrs_from_obj(selected_obj)[1][index], property)
                            selected_obj.attr[self.attrList[index]] = property_str
                        except: ...

            for obj in self.objectlist:
                try:
                    attrs = self.get_attrs_from_obj(obj)[0]
                    for attr in attrs:
                        try: setattr(obj, attr, eval(attrs[attr]))
                        except: setattr(obj, attr, attrs[attr])
                except:
                    ...
            try:
                self.properties_win.win.update()
            except tkinter.TclError:
                self.quit()

            if self.need_save:
                file = filedialog.asksaveasfile(filetypes = (("Nogui project", "*.ngs"),("All files", "*.*")))
                self.need_save = False
                self.saved = True
                self.save(file)
            if self.need_open:
                file = filedialog.askopenfile()
                self.need_open = False
                self.open(file)
            if self.mainthread != None:
                try: self.mainthread()
                except: print("Mainthread error")
                self.mainthread = None
         

    def canvasThread(self) -> None:
        self.matrix.fill()

        if self.tick == 2:
            for filename in self.filedir["files"]:
                with open(f"files/{self.filedir['name']}/{filename}.py") as file:
                    fileinp = file.read()
                self.filedir["files"][filename] = fileinp

        if self.run:
            self.tick += 1
        else:
            self.tick = 0
        try:
            for obj in self.objectlist:
                if hasattr(obj, "draw"):
                    obj.draw()
                if not hasattr(obj, "attr"):
                    obj.attr = {}
            self.matrix.show()
        except: pass
        self.update_file_tread = True


    def debugConsoleThread(self) -> None:
        print("Debug console initializated")
        while 1:
            inp = input(">>>")
            if len(inp) > 1:
                if inp[0] == "$":
                    os.system(inp[1:])
                elif inp[0] == "/":
                    self.command(inp[1:])
                else:
                    if self.show_console_errors:
                        try: exec(inp)
                        except: print("You have an error somewhere...")
                    else:
                        exec(inp)


    def filesThread(self) -> None:
        while 1:
        
            if self.update_file_tread:
                
                if self.tick == 2:
                    for i in range(len(self.filelibs)):
                        self.filelibs[i] = importlib.reload(self.filelibs[i])
                        if hasattr(self.filelibs[i], "start"):
                            self.filelibs[i].start(self)

                if self.run:
                    for i in range(len(self.filelibs)):
                        if hasattr(self.filelibs[i], "loop"):
                            self.filelibs[i].loop(self)
            
                self.update_file_tread = False


if __name__ == "__main__":
    Main()