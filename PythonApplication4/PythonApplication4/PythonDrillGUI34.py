from tkinter import *


def createPage(item):
       print("creating page")
       bodyText = item.get()
       print(bodyText)
       file = open("newfile.html", "w")
       file.write("<html>")
       file.write(bodyText)
       file.write("</body>")
       file.write("</html>")
       
       

    

win=Tk()

Label(win, text="Body Text").grid(row=0)

e1 = Entry(win)
b1 = Button(win,text="Create Page", command = lambda: createPage(e1))

e1.grid(row=0,column=1)
b1.grid(row=1,column=1)

win.mainloop()