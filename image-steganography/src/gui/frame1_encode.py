from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
from src.coding.encode import Encoder
import os
from io import BytesIO


class Frame1Encode:
    def __init__(self, root, previous_frame, stegno):
        self.root = root
        self.stegno = stegno
        previous_frame.destroy()
        # Get the project root directory (image-stegnography folder)
        self.project_root = self.get_project_root()
        self.create_frame()

    def get_project_root(self):
        # Get the directory where main.py is located (project root)
        current_file = os.path.abspath(__file__)  # Get path of current file
        src_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(current_file))
        )  # Go up 3 levels
        return src_dir

    def create_frame(self):
        f2 = Frame(self.root)
        label_art = Label(f2, text="'\(°Ω°)/'")
        label_art.config(font=("courier", 70))
        label_art.grid(row=1, pady=50)

        l1 = Label(f2, text="Select the Image in which \nyou want to hide text :")
        l1.config(font=("courier", 18))
        l1.grid()

        bws_button = Button(f2, text="Select", command=lambda: self.frame2_encode(f2))
        bws_button.config(font=("courier", 18))
        bws_button.grid()

        back_button = Button(f2, text="Cancel", command=lambda: self.stegno.home(f2))
        back_button.config(font=("courier", 18))
        back_button.grid(pady=15)
        f2.grid()

    def frame2_encode(self, f2):
        ep = Frame(self.root)
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

        myimg = Image.open(myfile)
        myimage = myimg.resize((300, 200))
        img = ImageTk.PhotoImage(myimage)

        l3 = Label(ep, text="Selected Image")
        l3.config(font=("courier", 18))
        l3.grid()

        panel = Label(ep, image=img)
        panel.image = img
        panel.grid()

        l2 = Label(ep, text="Enter the message")
        l2.config(font=("courier", 18))
        l2.grid(pady=15)

        text_area = Text(ep, width=50, height=10)
        text_area.grid()

        encoder = Encoder()
        encoder.output_image_size = os.stat(myfile).st_size
        encoder.o_image_w, encoder.o_image_h = myimg.size

        encode_button = Button(ep, text="Cancel", command=lambda: self.stegno.home(ep))
        encode_button.config(font=("courier", 11))

        back_button = Button(
            ep,
            text="Encode",
            command=lambda: self.enc_fun(text_area, myimg, encoder, ep),
        )
        back_button.config(font=("courier", 11))
        back_button.grid(pady=15)
        encode_button.grid()
        ep.grid(row=1)
        f2.destroy()

    def enc_fun(self, text_area, myimg, encoder, frame):
        data = text_area.get("1.0", "end-1c")
        if len(data) == 0:
            messagebox.showinfo("Alert", "Kindly enter text in TextBox")
            return

        newimg = myimg.copy()
        encoder.encode_enc(newimg, data)

        # Create encoded directory if it doesn't exist using absolute path from project root
        encoded_dir = os.path.join(self.project_root, "data", "encoded")
        os.makedirs(encoded_dir, exist_ok=True)

        # Generate filename based on original image
        temp = os.path.splitext(os.path.basename(myimg.filename))[0]
        encoded_filename = f"{temp}_encoded.png"
        encoded_path = os.path.join(encoded_dir, encoded_filename)

        # Save in data/encoded directory
        newimg.save(encoded_path)

        # Also allow user to choose custom save location
        custom_save_path = filedialog.asksaveasfilename(
            initialfile=temp,
            initialdir=encoded_dir,  # Start in the encoded directory
            filetypes=([("png", "*.png")]),
            defaultextension=".png",
        )

        if custom_save_path:  # If user didn't cancel the save dialog
            newimg.save(custom_save_path)

        messagebox.showinfo(
            "Success",
            f"Encoding Successful!\n\nFile is saved as:\n1. {encoded_path}\n2. {custom_save_path if custom_save_path else 'No custom location selected'}",
        )
        self.stegno.home(frame)
