import os
import sys
from PIL import Image
import webbrowser
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # colours
        self.bg_colour = "#151515"

        # standard font
        self.tier_font = "Helvecita"

        # basic setup
        self.title("Tier List")
        self.geometry("900x700")
        self.resizable(0, 0)

        # icon
        self.icon_ico = self.resource_path("logo.ico")
        self.iconbitmap(self.icon_ico)

        # settings
        self.image_width = 100 # standard resized width


        # frames (not necessary but allows for easy creation of multiple frames)
        container = tk.Frame(self)
        container.place(x=0, y=0, width=900, height=700)
        self.frames = {"MAIN" : MainPage(container, self),
                       "SETTINGS" : SettingsPage(container, self)}

        self.frames["MAIN"].tkraise()

    def initialise_frame(self, frame_object, image=None): # for all the basic setup stuff in frames
        frame_object.place(x=0, y=0, width=900, height=700)
        frame_object.configure(bg=self.bg_colour)

        if image != None: # for making it easier to initialise a frame with a background
            background_gif = tk.PhotoImage(file=self.resource_path(image))
            background = tk.Label(frame_object, image=background_gif, borderwidth=0, highlightthickness=0)
            background.image = background_gif # keep reference to image
            background.place(x=0, y=0)

    def resource_path(self, relative_path): # copied from stackoverflow, for making the program a .exe in future
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS # PyInstaller creates a temp folder and stores path in _MEIPASS
            
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        #intialise
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.initialise_frame(self, "background.gif") # use a image for the 'grid'

        # fonts
        self.text_font = (self.controller.tier_font, 14)
        self.title_font = (self.controller.tier_font, 32)
        self.button_font = (self.controller.tier_font, 40) # initial font for each tier

        # colours
        self.colours = ["#c95444", "#ff8000", "#ffff00", "#b5e61d", "#00a2e8"]
        self.standard_tiers = ["S", "A", "B", "C", "D"]

        # widgets
        self.title = tk.Label(self, text="My Tier List", font=self.title_font, fg="white", bg=self.controller.bg_colour, cursor="hand2")
        self.title.bind("<Button-1>", self.edit_title)
        self.title.place(x=5, y=5, width=890, height=92) # place the title perfectly inside the borderlines

        # load images
        self.load_button = tk.Button(self, text="LOAD", command=lambda: self.load_image(), font=self.title_font, fg="green", bg=self.controller.bg_colour, cursor="hand2")
        self.load_button.place(x=720, y=600)

        # settings
        self.settings_button = tk.Button(self, text="SETTINGS", command=lambda: self.controller.frames["SETTINGS"].tkraise(), font=self.title_font, fg="grey", bg=self.controller.bg_colour, cursor="hand2")
        self.settings_button.place(x=440, y=600)
    
        # youtube
        youtube_plug = tk.Button(self, text="youtube.com/alphascript", command=lambda: webbrowser.open_new("https://youtube.com/alphascript"), font=self.text_font, fg="red", bg=self.controller.bg_colour, cursor="pirate", relief="sunken", borderwidth=0, highlightthickness=0)
        youtube_plug.place(x=5, y=660)

        # create tier buttons, dims = 165x75
        self.buttons = []

        for i in range(len(self.colours)):
            button = tk.Label(self, text=self.standard_tiers[i], font=self.button_font, bg=self.colours[i], wraplength=192, cursor="hand2")
            button.bind("<Button-1>", lambda event, i=i: self.edit_tier(event, self.buttons[i]))

            button.place(x=6, y=(i*80)+104, width=192, height=72)
            self.buttons.append(button)

    def load_image(self): # load and format image for label
        image_dir = filedialog.askopenfilename(initialdir=os.getcwd(), title="Load Image", filetypes=(("GIF Images", ".gif"), )) # load gif directory

        if image_dir == "": # if filedialog was closed
            return

        resized_dir = image_dir[:-4] + "_resized.gif" # create new gif for resized image by removing .gif extension first
        
        if not image_dir[:-4].endswith("_resized"): # check if file is already resized
            resized = Image.open(image_dir).resize((self.controller.image_width, 73)) # slightly less than height to allow for error
            resized.save(resized_dir)

            image = tk.PhotoImage(file=resized_dir)

        else:
            image = tk.PhotoImage(file=image_dir)

        label = tk.Label(self, image=image, cursor="fleur", borderwidth=0, highlightthickness=0)
        label.image = image # keep reference of image
        label.place(x=400, y=565) # place in middle of grid at bottom

        self.make_draggable(label)

    # drag functions copied from stackoverflow 
    def make_draggable(self, widget): 
        widget.bind("<Button-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)

    def on_drag_start(self, event):
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def on_drag_motion(self, event):
        widget = event.widget
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y

        # fix positions between borders if place there, hardcoded because why not
        if 99 < y < 505 and 204 < x < 797:
            if y < 180:
                y = 102

            elif y < 260:
                y = 180

            elif y < 340:
                y = 260

            elif y < 420:
                y = 340

            else:
                y = 420

        widget.place(x=x, y=y)

    # create new instance of toplevel class to configure parts
    def edit_title(self, event):
        ConfigureTitle(self)

    def edit_tier(self, event, button):
        ConfigureTier(self, button)

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        # initialise
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.initialise_frame(self, "settings_background.gif")

        # fonts
        self.input_font = (self.controller.tier_font, 32)
        self.button_font = (self.controller.tier_font, 24)

        # widgets
        self.width_var = tk.StringVar()
        self.width_var.set(str(self.controller.image_width))
        width = tk.Entry(self, textvariable=self.width_var, width=10, font=self.input_font)
        width.place(x=325, y=400)

        apply_button = tk.Button(self, text="Apply", command=lambda: self.save(), font=self.button_font, fg="green", bg=self.controller.bg_colour, cursor="hand2")
        apply_button.place(x=600, y=600)

        cancel_button = tk.Button(self, text="Cancel", command=lambda: self.controller.frames["MAIN"].tkraise(), font=self.button_font, fg="red", bg=self.controller.bg_colour, cursor="hand2")
        cancel_button.place(x=165, y=600)

    def save(self):
        width = self.width_var.get()
        if width.isdigit():
            self.controller.image_width = int(width)
            self.controller.frames["MAIN"].tkraise()

        else:
            messagebox.showerror(title="Settings Update Failure", message="The width you entered was of an invalid data type. Please only enter positive integers.")

class ConfigureTitle(tk.Toplevel):
    def __init__(self, controller):
        # initialise toplevel
        tk.Toplevel.__init__(self)
        self.controller = controller

        # fonts
        self.title_font = (self.controller.controller.tier_font, 28)
        self.button_font = (self.controller.controller.tier_font, 18)
        self.input_font = (self.controller.controller.tier_font, 10)

        # basic setup
        self.title("Configuring Title")
        self.geometry("400x300")
        self.configure(bg=self.controller.controller.bg_colour)
        self.resizable(0, 0)
        
        # widgets
        title = tk.Label(self, text="Title:", bg=self.controller.controller.bg_colour, fg="white", font=self.title_font)
        title.place(x=160, y=15)

        self.name_entry = tk.Text(self, width=30, height=4, font=self.input_font)
        self.name_entry.insert(1.0, self.controller.title["text"])
        self.name_entry.place(x=90, y=75)

        apply_button = tk.Button(self, text="Apply", font=self.button_font, fg="green", bg=self.controller.controller.bg_colour, command=lambda: self.save())
        apply_button.place(x=65, y=200)

        cancel_button = tk.Button(self, text="Cancel", font=self.button_font, fg="red", bg=self.controller.controller.bg_colour, command=lambda: self.destroy())
        cancel_button.place(x=250, y=200)

    def save(self):
        new_title = self.name_entry.get(1.0, "end-1c")
        size = len(new_title)

        if size < 48:
            self.controller.title.configure(text=new_title)
            self.destroy()

        else:
            messagebox.showerror(title="Title Configuration Error", message="The given title was too large, limit=48 chars.")


class ConfigureTier(tk.Toplevel): # pretty much replica of configuretitle
    def __init__(self, controller, button):
        # initialise toplevel
        tk.Toplevel.__init__(self)
        self.controller = controller
        self.button = button

        # font
        self.title_font = (self.controller.controller.tier_font, 28)
        self.button_font = (self.controller.controller.tier_font, 18)
        self.input_font = (self.controller.controller.tier_font, 10)

        # basic setup
        self.title("Configuring Tier")
        self.geometry("400x300")
        self.configure(bg=self.controller.controller.bg_colour)
        self.resizable(0, 0)
        
        # widgets
        title = tk.Label(self, text="Tier Name:", fg="white", bg=self.controller.controller.bg_colour, font=self.title_font)
        title.place(x=105, y=15)

        self.name_entry = tk.Text(self, width=30, height=4, font=self.input_font)
        self.name_entry.insert(1.0, self.button["text"])
        self.name_entry.place(x=90, y=75)

        apply_button = tk.Button(self, text="Apply", font=self.button_font, fg="green", bg=self.controller.controller.bg_colour, command=lambda: self.save())
        apply_button.place(x=50, y=200)

        cancel_button = tk.Button(self, text="Cancel", font=self.button_font, fg="red", bg=self.controller.controller.bg_colour, command=lambda: self.destroy())
        cancel_button.place(x=250, y=200)

    def save(self):
        tier_name = self.name_entry.get(1.0, "end-1c")
        size = len(tier_name)
        if size < 121:
            if size < 16:
                font_size = (5 - (size//4)) * 8 # calculate varying font size for less than 16 chars

            else:
                font_size = 10
            
            self.button.configure(text=tier_name, font=(self.controller.controller.tier_font, font_size))
            self.destroy()


        else:
            messagebox.showerror(title="Tier Configuration Error", message="The given tier name was too large, limit=120 chars.")

# run the program
gui = GUI()
gui.mainloop()

