import tkinter as tk
from tkinter import font as tkfont


class ImageApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # self.title_font = tkfont.Font(family='Helvetica', size=12, weight="bold", slant="italic")
        self.title('IMAGE CR - All image cutter and resizer')
        self.configure(background='#595959')
        self.geometry("400x200")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("PageOne")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#e6e6e6')
        self.controller = controller
        button1 = tk.Button(self, text="CUTTER", border = 0, bg = '#e6e6e6',
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="RESIZER", border = 0,
                            command=lambda: controller.show_frame("PageTwo"))
        button1.place(relx=0, rely=0, relwidth=0.5, relheight=0.1)
        button2.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.1)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f6f6ee')
        self.controller = controller
        button1 = tk.Button(self, text="CUTTER", border=0, bg='#e6e6e6',
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="RESIZER", border=0, bg='#f6f6ee',
                            command=lambda: controller.show_frame("PageTwo"))
        button1.place(relx=0, rely=0, relwidth=0.5, relheight=0.1)
        button2.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.1)


if __name__ == "__main__":
    app = ImageApp()
    app.mainloop()