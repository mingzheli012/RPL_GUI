from gui_sub import *

''' GUI initialization '''
root = tk.Tk()
background = "pics/RPL.PNG"
img = ImageTk.PhotoImage(Image.open(background))
root.geometry("%dx%d"%(img.width(),img.height()))
root.title("RPL")
canvas = tk.Canvas(root, width=img.width(), height=img.height())
canvas.pack()
canvas.create_image(math.ceil(img.width()/2),
                    math.ceil(img.height()/2),
                    image=img)
window = GUI_Windows(root,canvas)

''' Insert Button to Canvas '''
next_button_image = ImageTk.PhotoImage(Image.open('pics/green_button.png'))
next_button = Button(canvas,text="Connect",
                     color="blue",command=lambda: window.connecting_window(),
                     image=next_button_image, h=136, w=371)
next_button.button['font'] = tkFont.Font(size=50)
next_button.button.config(bg='#12101f', borderwidth=0)
next_button.draw(750,700)



'''main loop'''
root.mainloop()
