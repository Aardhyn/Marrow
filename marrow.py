import tkinter
import datetime
import sys
import os

class Task(object):
    def __init__(self, name:str, created:datetime.date = datetime.date.today(), due :datetime.date = None):
        self.Name:str               = name
        self.DueDate:datetime.date  = due
        self.Completed:bool         = tkinter.BooleanVar()


class TaskWidget(object):
    def __init__(self, parent, callback, task:Task) -> None:
        self.BoundTask = task
        self.Frame = tkinter.Frame(parent, bg = "#EFEFEF" )
        self.Title = tkinter.Label(self.Frame, text = task.Name, anchor = "w", padx = 20, bg = "#EFEFEF")
        self.Check = tkinter.Checkbutton(self.Frame, variable = self.BoundTask.Completed, command = lambda : callback(), onvalue = True, padx = 7, offvalue = False, bg = "#EFEFEF")
        
        if self.BoundTask.Completed == True : self.Check.select()

        self.Frame.pack(expand = 1, fill = "both")
        self.Title.pack(side = "right", expand = 1, fill = "x")
        self.Check.pack(side = "left", expand = 0)


class TaskList(object):
    def __init__(self, parent) -> None:
        self.Parent                         = parent
        self.Frame                          = tkinter.Frame(parent)
        self.CompleatedLabel:tkinter.Label  = tkinter.Label(self.Frame, text = "completed")
        self.Tasks:dict                     = dict()
        self.Content:tkinter.StringVar      = tkinter.StringVar()

        self.InitTaskCreator()
        self.Frame.pack(fill = "x", side = "top")
        self.Parent.pack_propagate(0)

        return


    def InitTaskCreator(self) -> None:
        self.Wrapper = tkinter.Frame(self.Parent, bg = "#DDDDDD")
        self.Entry = tkinter.Entry(self.Wrapper, textvariable = self.Content)
    
        self.Parent.bind("<Return>", lambda event : self.CreateTask())

        self.Wrapper.pack(fill = "x")
        self.Entry.pack()

        return


    def orderList(self) -> None:
        try:
            for task in self.Tasks.values() : task.Frame.pack_forget()
            self.CompleatedLabel.pack_forget()

        except Exception : pass

        for task in self.Tasks.values(): 
            if task.BoundTask.Completed.get() == False: 
                task.Frame.pack(expand = 1, fill = "both")

        self.CompleatedLabel.pack(fill = "x")

        for task in self.Tasks.values():
            if task.BoundTask.Completed.get() == True: 
                task.Frame.pack(expand = 1, fill = "both")


        return


    def addTask(self, task:Task) -> None:
        self.Tasks[task.Name] = TaskWidget(self.Frame, self.orderList, task)
        self.orderList()

        return
    

    def CreateTask(self) -> None:
        self.addTask(Task(self.Content.get()))
        self.Entry.delete(0, "end")

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

        self.Root.mainloop()

        return


if __name__ == "__main__" : program:Marrow = Marrow()