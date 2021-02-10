import tkinter
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
    def __init__(self, name:str, due :datetime.date = None) -> None:
        self.Name:str               = name
        self.Created:datetime.date  = datetime.datetime.utcnow()
        self.DueDate:datetime.date  = due
        self.Completed:bool         = tkinter.BooleanVar()


class TaskWidget(object):
    def __init__(self, parent:tkinter.Tk, callback, task:Task) -> None:
        self.BoundTask  = task
        self.Frame      = tkinter.Frame(parent, bg = "#f9f9f9")
        self.Title      = tkinter.Label(self.Frame, text = task.Name, anchor = "w", padx = 10, bg = "#f9f9f9")
        self.Check      = tkinter.Checkbutton(self.Frame, variable = self.BoundTask.Completed, command = lambda : callback(), onvalue = True, offvalue = False, bg = "#f9f9f9")
        
        if self.BoundTask.Completed == True : self.Check.select()

        self.Frame.pack(expand = 1, fill = "both")
        self.Title.pack(side = "right", expand = 1, fill = "both")
        self.Check.pack(side = "left",  expand = 0, anchor = "e")

        return


class TaskList(object):
    def __init__(self, parent) -> None:
        self.Parent:tkinter.Tk              = parent

        self.ScrollingCanvas:tkinter.Canvas = tkinter.Canvas(parent,                width = parent.winfo_width())
        self.Scrollregion:tkinter.Frame     = tkinter.Frame(self.ScrollingCanvas,   width = parent.winfo_width())
        self.Frame:tkinter.Frame            = tkinter.Frame(parent)
        self.CompletedLabel:tkinter.Label   = tkinter.Label(self.Scrollregion,      text = "completed", anchor = "w", fg = "#000000", justify = "center")

        self.Tasks:dict                     = dict()
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
            for task in self.Tasks.values() : task.Frame.pack_forget()
            self.CompletedLabel.pack_forget()

        except Exception : pass

        uncompleted:list    = list()
        completed:list      = list()
        
        for task in self.Tasks.values():
            if task.BoundTask.Completed.get() == False:
                uncompleted.append(task)
            else:
                completed.append(task)
            
            continue

        for index, task in enumerate(uncompleted): 
            background = "#EEEEEE" if (index % 2 == 0 or index == 0) else "#FFFFFF"

            task.Title.configure(fg = "#000000")
            task.Frame.configure(bg = background)
            task.Title.configure(bg = background)
            task.Check.configure(bg = background)

            self.Parent.update_idletasks()

            task.Title.configure(width = self.Parent.winfo_width())
            task.Frame.pack(expand = 1, fill = "both")

            continue

        for index, task in enumerate(completed):
            background = "#EEEEEE" if (index % 2 == 0 or index == 0) else "#FFFFFF"

            task.Title.configure(fg = "#999999")
            task.Frame.configure(bg = background)
            task.Title.configure(bg = background)
            task.Check.configure(bg = background)

            self.Parent.update_idletasks()
            self.CompletedLabel.pack(fill = "x", pady = 15, padx = 37)
            task.Title.configure(width = self.Parent.winfo_width())
            task.Frame.pack(expand = 1, fill = "both")

            continue 

        return


    def AddTask(self, task:Task) -> None:
        self.Tasks[task.Created] = TaskWidget(self.Scrollregion, self.OrderList, task)
        self.OrderList()

        return
    

    def CreateTask(self) -> None:
        if len(self.Content.get()) > 1:
            self.AddTask(Task(self.Content.get()))
            self.Entry.delete(0, "end")

        else:
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
        
        if self.Configuration["TaskDataFilepath"] == "" : self.MarrowSetup()

        self.Root:tkinter.Tk        = tkinter.Tk()
        self.Width:int              = 400
        self.Height:int             = 600 

        self.Root.geometry(centerWindow(self.Root, self.Width, self.Height))
        self.Root.attributes("-topmost", True)
        self.Root.title("Marrow (beta)")

        self.Tasks:TaskList         = TaskList(self.Root)

        self.Root.mainloop()

        return
    
    def MarrowSetup(self) -> None:

        return

if __name__ == "__main__" : program:Marrow = Marrow()