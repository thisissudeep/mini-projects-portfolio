from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
from src.coding.decode import decode


class Frame2Decode:
    def __init__(self, root, previous_frame, stegno):
        self.root = root
        self.stegno = stegno
        previous_frame.destroy()
        self.create_frame()

    def create_frame(self):
        d_f2 = Frame(self.root)
        label_art = Label(d_f2, text="٩(^‿^)۶")
        label_art.config(font=("courier", 90))
        label_art.grid(row=1, pady=50)

        l1 = Label(d_f2, text="Select Image with Hidden text:")
        l1.config(font=("courier", 18))
        l1.grid()

        bws_button = Button(
            d_f2, text="Select", command=lambda: self.frame2_decode(d_f2)
        )
        bws_button.config(font=("courier", 18))
        bws_button.grid()

        back_button = Button(
            d_f2, text="Cancel", command=lambda: self.stegno.home(d_f2)
        )
        back_button.config(font=("courier", 18))
        back_button.grid(pady=15)
        d_f2.grid()

    def frame2_decode(self, d_f2):
        d_f3 = Frame(self.root)
        myfile = filedialog.askopenfilename(
            filetypes=(
                [
                    ("png", "*.png"),
                    ("jpeg", "*.jpeg"),
                    ("jpg", "*.jpg"),
                    ("All Files", "*.*"),
                ]
            )
        )

        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
            return

        myimg = Image.open(myfile, "r")
        myimage = myimg.resize((300, 200))
        img = ImageTk.PhotoImage(myimage)

        l4 = Label(d_f3, text="Selected Image :")
        l4.config(font=("courier", 18))
        l4.grid()

        panel = Label(d_f3, image=img)
        panel.image = img
        panel.grid()

        hidden_data = decode(myimg)
        l2 = Label(d_f3, text="Hidden data is :")
        l2.config(font=("courier", 18))
        l2.grid(pady=10)

        text_area = Text(d_f3, width=50, height=10)
        text_area.insert(INSERT, hidden_data)
        text_area.configure(state="disabled")
        text_area.grid()

        back_button = Button(
            d_f3, text="Cancel", command=lambda: self.stegno.home(d_f3)
        )
        back_button.config(font=("courier", 11))
        back_button.grid(pady=15)
        d_f3.grid(row=1)
        d_f2.destroy()
