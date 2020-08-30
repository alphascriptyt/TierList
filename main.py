import tkinter as tk
from tkinter import filedialog
import os
import sys
from PIL import Image

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # colours
        self.bg_colour = "#151515"

        # basic setup
        self.title("Tier List")
        self.geometry("900x700") 
        self.configure(bg=self.bg_colour)
        self.resizable(0, 0)

        # frames (not necessary but allows for multiple frames)
        container = tk.Frame(self)
        container.place(x=0, y=0, width=900, height=700)
        self.frames = {"MAIN" : MainPage(container, self)}

        self.frames["MAIN"].tkraise()

    def initialise_frame(self, frame_object, image=None): # for all the basic setup stuff in frames
        frame_object.place(x=0, y=0, width=900, height=700) # set the frame in position
        frame_object.configure(bg=self.bg_colour) # set the background to black

        if image != None: #for making it easier to initialise a frame and set the background
            background_gif = tk.PhotoImage(file=self.resource_path(image))
            background = tk.Label(frame_object, image=background_gif, borderwidth=0, highlightthickness=0)
            background.image = background_gif
            background.place(x=0, y=0)

    def resource_path(self, relative_path): # copied from stackoverflow xD 
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS

        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        #initialise 
        tk.Frame.__init__(self, parent) 
        self.controller = controller
        self.controller.initialise_frame(self, "background_colours.gif")

        # fonts
        self.tier_font = "Helvecita"
        self.title_font = (self.tier_font, 32)
        self.button_font = (self.tier_font, 40) # standard font for the tiers

        # colours
        self.b1_colour = "#c95444" # tier colours NEED TO CHECK COLOURS
        self.b2_colour = "#ff8000" # only store here temporarily
        self.b3_colour = "#ffff00"
        self.b4_colour = "#b5e61d"
        self.b5_colour = "#00a2e8"

        self.colours = ["#c95444", "#ff8000", "#ffff00", "#b5e61d", "#00a2e8"]
        self.standard_tiers = ["S", "A", "B", "C", "D"]

        # widgets
        self.title = tk.Label(self, text="My Tier List", font=self.title_font, bg=self.controller.bg_colour, fg="white", cursor="hand2")
        self.title.bind("<Button-1>", self.edit_title)
        self.title.place(x=5, y=5, width=890, height=92)

        # load images
        self.loaded_images = []

        self.load_button = tk.Button(self, text="LOAD", command=lambda: self.load_image(), font=self.title_font, fg="green", bg=self.controller.bg_colour, cursor="hand2")
        self.load_button.place(x=700, y=600)

        # create side buttons, dims = 165x75
        self.buttons = []

        for i in range(len(self.colours)):
            button = tk.Label(self, text=self.standard_tiers[i], font=self.button_font, bg=self.colours[i], wraplength=192, cursor="hand2")
            button.bind("<Button-1>", lambda event, i=i: self.edit_tier(event, self.buttons[i]))

            button.place(x=6, y=(i*80)+104, width=192, height=72) # button is 75 pixels high and title portion is 100 deep + line width of 2 pixels for each line.
            self.buttons.append(button)
    
    def load_image(self): # load and format image for label
        image_dir = filedialog.askopenfilename(initialdir=os.getcwd(), title="Load Image", filetypes=(("GIF Images", ".gif"),)) # load .gif
        resized_dir = image_dir[:-4] + "_resized.gif" 

        resized = Image.open(image_dir).resize((100, 75))
        resized.save(resized_dir)
        
        image = tk.PhotoImage(file=resized_dir)
        label = tk.Label(self, image=image, borderwidth=0, highlightthickness=0)
        label.image = image

        self.make_draggable(label)
        self.loaded_images.append(label)

        label.place(x=500, y=500) # calculate position
        
    # drag functions copied from stackoverflow, change to tkinter dnd?
    def make_draggable(self, widget): # make into class???? 
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
        widget.place(x=x, y=y)

    def edit_title(self, event):
        ConfigureTitle(self)

    def edit_tier(self, event, button):
        ConfigureTier(self, button) # raise the class to configure the title of the box
 
class ConfigureTitle(tk.Toplevel):
    def __init__(self, controller):
        #initialise toplevel
        tk.Toplevel.__init__(self) 
        self.controller = controller
            
        # font
        self.title_font = (self.controller.tier_font, 28)
        self.button_font = (self.controller.tier_font, 18)
        self.input_font = (self.controller.tier_font, 10)

        # basic setup
        self.title("Configuring Title")
        self.geometry("400x300") 
        self.configure(bg=self.controller.controller.bg_colour)
        self.resizable(0, 0)

        # widgets
        title = tk.Label(self, text="Title:", bg=self.controller.controller.bg_colour, fg="white", font=self.title_font)
        title.place(x=105, y=15) 
        
        self.name_entry = tk.Text(self, width=30, height=4, font=self.input_font)
        self.name_entry.insert(1.0, self.controller.title["text"])
        self.name_entry.place(x=90, y=75)

        apply_button = tk.Button(self, text="Apply", font=self.button_font, fg="green", bg=self.controller.controller.bg_colour, command=lambda: self.save())
        apply_button.place(x=50, y=200)
    
        cancel_button = tk.Button(self, text="Cancel", font=self.button_font, fg="red", bg=self.controller.controller.bg_colour, command=lambda: self.destroy())
        cancel_button.place(x=250, y=200)
        
    def save(self):
        new_title = self.name_entry.get(1.0, "end-1c")
        size = len(new_title)

        if size < 48:
            self.controller.title.configure(text=new_title)
            self.destroy()

        else:
            new_title = "The given tier name was too large,\nlimit=48 chars." 

            self.name_entry.delete(1.0, "end")
            self.name_entry.insert(1.0, new_title)
            
class ConfigureTier(tk.Toplevel):
    def __init__(self, controller, button):
        #initialise toplevel
        tk.Toplevel.__init__(self) 
        self.controller = controller
        self.button = button
            
        # font
        self.title_font = (self.controller.tier_font, 28)
        self.button_font = (self.controller.tier_font, 18)
        self.input_font = (self.controller.tier_font, 10)

        # basic setup
        self.title("Configuring Tier")
        self.geometry("400x300") 
        self.configure(bg=self.controller.controller.bg_colour)
        self.resizable(0, 0)

        # widgets
        title = tk.Label(self, text="Tier Name:", bg=self.controller.controller.bg_colour, fg="white", font=self.title_font)
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
                font_size = (5 - (size//4)) * 8

            else:
                font_size = 10 
            
            self.button.configure(text=tier_name, font=(self.controller.tier_font, font_size))
            self.destroy()

        else:
            tier_name = "The given tier name was too large,\nlimit=120 chars."
            self.name_entry.delete(1.0, "end")
            self.name_entry.insert(1.0, tier_name)
            
gui = GUI()
gui.mainloop()
