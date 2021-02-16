import tkinter
import tkinter.filedialog
import datetime
import json
import sys
import os

def centerWindow(parent:tkinter.Tk, width:int, height:int) -> str:
    screenWidth:int     = parent.winfo_screenwidth()
    screenHeight:int    = parent.winfo_screenheight()
    topCornerX:int      = int((screenWidth / 2) - (width / 2))
    topCornerY:int      = int((screenHeight / 2) - (height / 2))

    return f"{width}x{height}+{topCornerX}+{topCornerY}"

class ConfigurationFileNotFound(Exception) : pass

class Task(object):
    def __init__(self, name:str, due:datetime.date = None, created = None, completed = None) -> None:
        self.Name:str               = name
        self.DueDate:datetime.date  = due

        self.Created:datetime.date  = datetime.datetime.utcnow() if created is None else created
        self.Completed:bool         = tkinter.BooleanVar() if completed is None else completed


class TaskWidget(object):
    def __init__(self, parent:tkinter.Tk, callback, task:Task) -> None:
        self.BoundTask  = task
        self.Frame      = tkinter.Frame(parent, bg = "#f9f9f9", highlightthickness = 0)
        self.Title      = tkinter.Label(self.Frame, text = task.Name, anchor = "w", padx = 10, bg = "#f9f9f9")
        self.Check      = tkinter.Checkbutton(self.Frame, highlightthickness = 0, variable = self.BoundTask.Completed, command = lambda : callback(), onvalue = True, offvalue = False, bg = "#f9f9f9")
        
        if self.BoundTask.Completed == True : self.Check.select()

        self.Frame.grid(sticky = "w")
        self.Title.pack(side = "right", expand = 1, fill = "both")
        self.Check.pack(side = "left",  expand = 0, anchor = "e")

        return


class TaskList(object):
    def __init__(self, parent, _OnNewTask = None) -> None:
        self.Parent:tkinter.Tk              = parent
        self.NewTaskCallback                = _OnNewTask

        self.ScrollingCanvas:tkinter.Canvas = tkinter.Canvas(parent,                width = parent.winfo_width(), highlightthickness = 0)
        self.Scrollregion:tkinter.Frame     = tkinter.Frame(self.ScrollingCanvas,   width = parent.winfo_width())
        self.Frame:tkinter.Frame            = tkinter.Frame(parent,                 highlightthickness = 0)
        self.CompletedLabel:tkinter.Label   = tkinter.Label(self.Scrollregion,      text = "completed", anchor = "w", fg = "#000000", justify = "center")

        self.Tasks:list                     = list()
        self.TaskData:dict                  = dict()

        self.Content:tkinter.StringVar      = tkinter.StringVar()

        self.Scrollregion.bind("<Configure>", lambda event : self.ScrollingCanvas.configure(scrollregion = self.ScrollingCanvas.bbox("all")))
        self.ScrollingCanvas.create_window((0,0), window = self.Scrollregion, anchor = "nw")
        self.ScrollingCanvas.bind_all("<MouseWheel>", lambda event : self.ScrollCanvas(event))

        self.InitTaskCreator()

        self.ScrollingCanvas.pack(fill = "both", expand = 1)
        self.Frame.pack(fill = "both")
        self.Parent.pack_propagate(0)

        return


    def InitTaskCreator(self) -> None:
        self.Wrapper = tkinter.Frame(self.Parent, bg = "#84bd59")
        self.Entry = tkinter.Entry(self.Wrapper, textvariable = self.Content, highlightthickness = 0, relief = "flat")
    
        self.Parent.bind("<Return>", lambda event : self.CreateTask())

        self.Wrapper.pack(fill = "x")
        self.Entry.pack(pady = 10)

        self.Entry.focus()

        return


    def OrderList(self) -> None:
        try:
            # for task in self.Tasks : task.Frame.pack_forget()
            for task in self.Tasks : task.Frame.pack_forget()
            self.CompletedLabel.grid_forget()

        except Exception : pass

        newTaskOrder:list       = list()
        uncompleted:list        = list()
        completed:list          = list()

        for task in self.Tasks:
            if task.BoundTask.Completed.get() == False:
                uncompleted.append(task)
            else:
                completed.append(task)
            
            continue

        uncompletedCount:int    = len(uncompleted)

        for index, task in enumerate(uncompleted): 
            background = "#EEEEEE" if (index % 2 == 0 or index == 0) else "#FFFFFF"

            newTaskOrder.append(task)

            task.Title.configure(fg = "#000000")
            task.Frame.configure(bg = background)
            task.Title.configure(bg = background)
            task.Check.configure(bg = background)

            self.Parent.update()

            task.Title.configure(width = self.Parent.winfo_width())
            task.Frame.grid(row = index, sticky = "w")
            print(index)

            continue

        if len(completed) != 0 : self.CompletedLabel.grid(pady = 15, padx = 37, row = uncompletedCount, sticky = "w")

        for index, task in enumerate(completed):
            print(index + uncompletedCount)
            background = "#EEEEEE" if (index % 2 == 0 or index == 0) else "#FFFFFF"

            newTaskOrder.append(task)

            task.Title.configure(fg = "#999999")
            task.Frame.configure(bg = background)
            task.Title.configure(bg = background)
            task.Check.configure(bg = background)

            self.Parent.update()
            task.Title.configure(width = self.Parent.winfo_width())
            task.Frame.grid(row = index + uncompletedCount + 1, sticky = "w")

            continue 

        self.Tasks = newTaskOrder

        return


    def AddTask(self, task:Task) -> None:
        self.Tasks.append(TaskWidget(self.Scrollregion, self.OrderList, task))
        self.OrderList()

        self.NewTaskCallback()

        return
    

    def CreateTask(self) -> None:
        if len(self.Content.get()) > 1:
            self.AddTask(Task(self.Content.get()))
            self.Entry.delete(0, "end")

        elif len(self.Content.get()) != 0:
            self.Wrapper.configure(bg = "#FF0000")
            self.Parent.after(25, lambda : self.Wrapper.configure(bg = "#84bd59"))

        return

    def ScrollCanvas(self, event) -> None:
        if (self.Scrollregion.winfo_height() < self.Parent.winfo_height() - self.Wrapper.winfo_height()) : return

        if sys.platform == "darwin":
            self.ScrollingCanvas.yview_scroll(int(event.delta / 4), "units")
        else:
            self.ScrollingCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        return


class Marrow(object):
    def __init__(self) -> None:

        if os.path.exists("config.json"):
            with open("config.json") as configFile : self.Configuration = json.load(configFile)

        else:
            raise ConfigurationFileNotFound("Unable to build Marrow")
        
        self.Root:tkinter.Tk        = tkinter.Tk()
        self.ArrowKeys:tuple        = ("<Up>", "<Down>")
        self.StoredTasks:dict       = dict()
        self.Width:int              = 400
        self.Height:int             = 600 
        self.cursorIndex            = -1 #(the entry box)

        self.Root.geometry(centerWindow(self.Root, self.Width, self.Height))
        self.Root.title(f"Marrow {self.Configuration['version']}")
        self.Root.protocol("WM_DELETE_WINDOW", self.QuitMarrow)

        self.Root.bind("<space>", lambda event : self.selectTask(self.cursorIndex) if self.cursorIndex != -1 else False)
        for key in self.ArrowKeys : self.Root.bind(key, lambda event : self.MoveCursor(str(event.keysym)))

        self.TasksWidget:TaskList   = TaskList(self.Root, _OnNewTask = self.SaveTasks)

        if self.Configuration["TaskDataFilepath"] == "": 
            self.MarrowSetup()

        else:
            with open(self.Configuration["TaskDataFilepath"], "r") as file : 
                self.StoredTasks = json.load(file)
                self.LoadStoredTasks()
            
        self.Root.attributes("-topmost", True)

        self.Root.mainloop()

        return
    

    def writeConfig(self) -> None:
        with open("config.json", "w", encoding = "utf-8") as configFile: 
            json.dump(self.Configuration, configFile, ensure_ascii = False, indent = 4)

        return


    def MarrowSetup(self) -> None:
        filepath:str = str()
        while not filepath : filepath = tkinter.filedialog.askdirectory() + "/MarrowTasks.json"
        self.Configuration["TaskDataFilepath"] = filepath

        with open(filepath, "w+") as taskFile : json.dump({"tasks" : []}, taskFile, ensure_ascii = False, indent = 4)

        self.writeConfig()

        return


    def LoadStoredTasks(self) -> None:
        for data in self.StoredTasks["tasks"]:
            name:str                        = data['name']
            create                          = datetime.datetime.strptime(data['created'],   r"%Y-%m-%d %H:%M:%S.%f")
            completed:tkinter.BooleanVar    = tkinter.BooleanVar(value = data['completed'])

            try:
                due = datetime.datetime.strptime(data['due'],       r"%Y-%m-%d %H:%M:%S.%f")

            except ValueError : due = None

            self.TasksWidget.AddTask(Task(name, due, created = create, completed = completed))

        return


    def SaveTasks(self) -> None:
        print("tasks saved!")
        self.StoredTasks = {
            "tasks" : []
        }

        for task in self.TasksWidget.Tasks:
            self.StoredTasks["tasks"].append({
                "name"      : task.BoundTask.Name,
                "created"   : str(task.BoundTask.Created),
                "due"       : str(task.BoundTask.DueDate),
                "completed" : task.BoundTask.Completed.get(),
            })

            continue

        with open(self.Configuration["TaskDataFilepath"], "w+") as file : json.dump(self.StoredTasks, file, ensure_ascii = False, indent = 4)

        return


    def QuitMarrow(self) -> None:
        self.SaveTasks()
        self.Root.quit()

        return


    def MoveCursor(self, direction) -> None:
        taskCount = len(self.TasksWidget.Tasks)
        if taskCount < 1 : return

        self.TasksWidget.OrderList()
        self.cursorIndex += -1 if (direction == "Up") else 1

        if self.cursorIndex > taskCount - 1:
            self.cursorIndex = -1
            self.TasksWidget.Entry.focus()

            return

        elif self.cursorIndex <= -1:
            self.cursorIndex = taskCount - 1

        self.selectTask(self.cursorIndex)

        return
    

    def selectTask(self, index) -> None:
        selectedWidget:TaskWidget = self.TasksWidget.Tasks[self.cursorIndex]
        selectedWidget.Title.configure(bg = "#699c43", fg = "#FFFFFF")
        selectedWidget.Check.configure(bg = "#699c43")
        selectedWidget.Frame.configure(bg = "#699c43")
        selectedWidget.Check.focus_set()

        return

if __name__ == "__main__" : program:Marrow = Marrow()