import tkinter
import datetime
import sys
import os

class Task(object):
    def __init__(self, name:str, created:datetime.date = datetime.date.today(), due :datetime.date = None):
        self.Name:str               = name
        self.DueDate:datetime.date  = due
        self.Compleated:bool        = False
    
    def compleate(self) -> None:
        self.Compleated = True
        return


class TaskWidget(object):
    def __init__(self, parent, task:Task) -> None:
        self.Frame = tkinter.Frame(parent)
        self.Title = tkinter.Label(self.Frame, text = task.Name, bg = "#FF0000")
        self.Check = tkinter.Checkbutton(self.Frame, variable = task.Compleated)

        self.Frame.pack(expand = 1, fill = "both")
        self.Title.pack(side = "left", expand = 1, fill = "x")
        self.Check.pack(side = "right", expand = 0)


class TaskList(object):
    def __init__(self, parent) -> None:
        self.frame      = tkinter.Frame(parent)
        self.tasks:dict = dict()
        return

    def addTask(self, task:Task) -> None:
        self.tasks[task.Name] = TaskWidget(self.frame, task)
        return

    def orderList(self) -> None:
        return


class Marrow(object):
    def __init__(self) -> None:
        # properties 
        self.Root:tkinter.Tk    = tkinter.Tk()
        self.Width:int          = 400
        self.Height:int         = 600       

        screenWidth:int         = self.Root.winfo_screenwidth()
        screenHeight:int        = self.Root.winfo_screenheight()
        topCornerX:int          = (screenWidth / 2) - (self.Width / 2)
        topCornerY:int          = (screenHeight / 2) - (self.Height / 2)

        self.Root.geometry(f"{self.Width}x{self.Height}+{int(topCornerX)}+{int(topCornerY)}")
        self.Root.attributes("-topmost", True)
        self.Root.title("Marrow (V0.0.1)")

        self.TaskList   = TaskList(self.Root)
        do:Task         = Task("ring Carron")
        self.TaskList.addTask(do)
        self.TaskList.addTask(do)
        self.TaskList.addTask(do)
        self.TaskList.addTask(do)
        self.TaskList.addTask(do)
        self.TaskList.addTask(do)
        self.TaskList.addTask(do)

        self.TaskList.frame.pack(fill = "x")

        self.Root.mainloop()

        return


if __name__ == "__main__" : Marrow()