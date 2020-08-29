import tkinter as tk
import os
import sys

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
        self.button_font = (self.tier_font, 10)

        # colours
        self.b1_colour = "#c95444" # tier colours NEED TO CHECK COLOURS
        self.b2_colour = "#ff8000" # only store here temporarily
        self.b3_colour = "#ffff00"
        self.b4_colour = "#b5e61d"
        self.b5_colour = "#00a2e8"

        self.colours = ["#c95444", "#ff8000", "#ffff00", "#b5e61d", "#00a2e8"]

        # create side buttons, dims = 165x75
        self.buttons = []

        for i in range(len(self.colours)):
            button = tk.Button(self, text="", font=self.button_font, bg=self.colours[i], command=lambda i=i: self.edit_tier(self.buttons[i]), relief="flat", wraplength=192)
            button.place(x=6, y=(i*80)+104, width=192, height=72) # button is 75 pixels high and title portion is 100 deep + line width of 2 pixels for each line.
            self.buttons.append(button)
 
    def edit_tier(self, button):
        ConfigureTier(self, button) # raise the class to configure the title of the box
     
class ConfigureTier(tk.Toplevel):
    def __init__(self, controller, button):
        #initialise toplevel
        tk.Toplevel.__init__(self) 
        self.controller = controller
        self.button = button
            
        # font
        self.title_font = (self.controller.tier_font, 18)
        self.button_font = (self.controller.tier_font, 14)
        self.input_font = (self.controller.tier_font, 12)

        # basic setup
        self.title("Configuring Box")
        self.geometry("400x300") 
        self.configure(bg=self.controller.controller.bg_colour)
        self.resizable(0, 0)

        # widgets
        title = tk.Label(self, text="What would you like\nto rename the tier?", bg=self.controller.controller.bg_colour, fg="white", font=self.title_font)
        title.place(x=45, y=15)

        self.name_var = tk.StringVar()
        name_entry = tk.Entry(self, textvariable=self.name_var, font=self.input_font)
        name_entry.place(x=25, y=100)
        
        apply_button = tk.Button(self, text="Apply", font=self.button_font, fg="green", bg=self.controller.controller.bg_colour, command=lambda: self.save())
        apply_button.place(x=50, y=200)
        
    def save(self):
        tier_name = self.name_var.get()
        size = len(tier_name)

        if size < 121:
            if size < 16:
                font_size = (5 - (size//4)) * 8

            else:
                font_size = 10 

        else:
            tier_name = "The given tier name was too large, limit=120 chars."

        self.button.configure(text=tier_name, font=(self.controller.tier_font, font_size))
        self.destroy()

gui = GUI()
gui.mainloop()
