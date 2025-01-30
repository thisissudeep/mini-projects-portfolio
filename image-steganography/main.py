from tkinter import *
from src.gui.frame1_encode import Frame1Encode
from src.gui.frame2_decode import Frame2Decode
from tkinter import ttk


class Stegno:
    art = """¯\_(ツ)_/¯"""
    art2 = '''
@(\/)
(\/)-{}-)@
@(={}=)/\)(\/)
(\/(/\)@| (-{}-)
(={}=)@(\/)@(/\)@
(/\)\(={}=)/(\/)
@(\/)\(/\)/(={}=)
(-{}-)""""@/(/\)
|:   |
/::'   \\
/:::     \\
|::'       |
|::        |
\::.       /
':______.'
`""""""`'''

    def main(self, root):
        root.title("ImageSteganography")
        root.geometry("500x600")
        root.resizable(width=False, height=False)
        f = Frame(root)

        title = Label(f, text="Image Steganography")
        title.config(font=("courier", 33))
        title.grid(pady=10)

        b_encode = Button(
            f, text="Encode", command=lambda: Frame1Encode(root, f, self), padx=14
        )
        b_encode.config(font=("courier", 14))
        b_decode = Button(
            f, text="Decode", padx=14, command=lambda: Frame2Decode(root, f, self)
        )
        b_decode.config(font=("courier", 14))
        b_decode.grid(pady=12)

        ascii_art = Label(f, text=self.art)
        ascii_art.config(font=("courier", 60))

        ascii_art2 = Label(f, text=self.art2)
        ascii_art2.config(font=("courier", 12, "bold"))

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        f.grid()
        title.grid(row=1)
        b_encode.grid(row=2)
        b_decode.grid(row=3)
        ascii_art.grid(row=4, pady=10)
        ascii_art2.grid(row=5, pady=5)

    def home(self, frame):
        frame.destroy()
        self.main(root)


if __name__ == "__main__":
    root = Tk()
    stegno = Stegno()
    stegno.main(root)
    root.mainloop()
