from tkinter import *

root = Tk()
img = PhotoImage(file="recursos/padrino.png")
label_imagen = Label(root, image=img)
label_imagen.pack()
print(img)

root.mainloop()
