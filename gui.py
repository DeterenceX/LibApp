import tkinter as ttk

window = ttk.Tk()
window.geometry("1000x1000")
window.title("MyLib")

photo = ttk.PhotoImage(file='book.png') #create a photoimage to use in widgets

label = ttk.Label(window,text="Hello World",
                  font=("Arial",40),
                  fg="white",
                  bg="black",
                  relief="raised",
                  bd=10,
                  padx=20,
                  pady=20,
                  image=photo,
                  compound='bottom'
                  )
label.pack() # or place, for exact placement x,y

icon = ttk.PhotoImage(file='ravenlogo.png')
window.iconphoto(True, icon)
window.config(background='dark gray')

button = ttk.Button(window,text="click me")

def click():
    print("hello")
button.config(command=click, #command takes a function, and runs it when button is pressed.
              font=("arial",50,"bold"),
              bg='#358263',
              fg='white',
              activebackground='black', # activebackground is the color when the button is pressed
              activeforeground='purple', # activeforeground is the color when the button is pressed
              relief='raised'
              )
button.config(state = "normal") # disable the button, it will not respond to clicks
button.pack()

entry = ttk.Entry(window, font=("Arial", 30), bg="black", fg="white", bd=10, relief="raised")
entry.insert(0, "Type here...")  # Insert a default text
entry.pack()






window.mainloop() #place window on screen, listening for events



