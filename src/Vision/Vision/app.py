import tkinter as tk
from Vision.main_window import TurretWindow

class TurretApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Turret Control")
        self.geometry('2560x1440')
        # Load main UI window
        self.main_window = TurretWindow(self)
       
        self.main_window.pack()

    def run(self, img):
        self.mainloop()
        self.main_window.update_image(img)

if __name__ == "__main__":
    app = TurretApp()
    app.run()