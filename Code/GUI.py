from tkinter.ttk import *
from tkinter import *
from tkinter import font as tkFont
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class GUI:

    def __init__(self, window):
        self.window = window
        self.label = None
        self.plot = None
        self.figure = None
        self.canvas = None
        self.toolbar = None

    def set_plot(self, plot):
        self.plot = plot

    def set_figure(self, figure):
        self.figure = figure

    def set_canvas(self, canvas):
        self.canvas = canvas

    def set_toolbar(self, toolbar):
        self.toolbar = toolbar

    def center_window(self):
        self.window.geometry("%dx%d" % (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        #self.window.withdraw()
        #self.window.update_idletasks()
        #x = (self.window.winfo_screenwidth() - self.window.winfo_reqwidth()) / 30
        #y = (self.window.winfo_screenheight() - self.window.winfo_reqheight()) / 5
        #self.window.geometry("+%d+%d" % (x, y))
        #self.window.deiconify()

    def set_title(self, title_name):
        self.window.title(title_name)

    def set_background(self, background_color):
        self.window.configure(background=background_color)

    def create_label_frame(self, parent, label_text):
        return LabelFrame(master=parent, text=label_text)

    def set_object_grid_parameter(self, object, grid_row, grid_column, column_span=1, row_span=1, x_padding=5, y_padding=5, sticky=E+W+N+S):
        object.grid(row=grid_row, column=grid_column, columnspan=column_span, rowspan=row_span, padx=x_padding, pady=y_padding, sticky=sticky)

    def create_text_label(self, parent, width, height, fg='Red', text='', font=('Helvetica', 20)):
        return Label(master=parent, width=width, height=height, text=text, fg=fg, font=font)

    def create_label(self, parent, width=10, height=10):
        lbl = Label(master=parent, width=width, height=height)
        self.label = lbl
        self.set_blank_image()
        return lbl

    def set_blank_image(self):
        img = PhotoImage()
        self.label.configure(image=img)
        self.label.image = img

    def remove_blank_image(self):
        self.label.configure(image=None)
        self.label.image = None

    def create_button(self, parent, label_text, button_width=22, button_height=2, background="white", foreground="red", function=None):
        return Button(master=parent, text=label_text, width=button_width, height=button_height, highlightbackground=background, fg=foreground, command=function)

    def create_font(self):
        return tkFont.Font(family='Helvetica', size=20, weight='bold')

    def create_figure_canvas(self, fig, parent):
        return FigureCanvasTkAgg(fig, master=parent)

    def create_nav_toolbar(self, canvas, parent):
        return NavigationToolbar2Tk(canvas, parent)
