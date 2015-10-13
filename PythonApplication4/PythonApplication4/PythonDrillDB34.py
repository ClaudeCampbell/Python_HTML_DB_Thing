import sqlite3 as lite
import sys
from tkinter import *
from tkinter import filedialog

def createPage(item, item2): #Gathers input from the text box and writes it into a new html file
       print("creating page")
       bodyText = item.get()
       name = item2.get()
       print(bodyText)
       file = filedialog.asksaveasfile(mode='w',defaultextension='.html', initialfile = name) #creating the new file
       file.write("<html>")
       file.write("<body>")
       file.write(bodyText)
       file.write("</body>")
       file.write("</html>")

def createPageFromTemplate(item, item2): #Gathers input from a template and writes it into a new html file
       print("creating page")
       file = filedialog.asksaveasfile(mode='w',defaultextension='.html', initialfile = item2) #creating the new file
       file.write("<html>")
       file.write("<body>")
       file.write(item)
       file.write("</body>")
       file.write("</html>")

def saveTemplate(item, item2): #saves the template to the database
    bodyText = item.get()
    name = item2.get()
    con = lite.connect('test.db')

    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO bodyoptions VALUES('"+name+"','"+bodyText+"')")
    fetchAll()


def createNewWindow(): #creates the window that allows for creating pages and saving templates.
    newWin=Tk()

    Label(newWin, text="Name").grid(row=0)
    Label(newWin, text="Body Text").grid(row=1)

    e1 = Entry(newWin)
    e2 = Entry(newWin)
    b1 = Button(newWin,text="Create Page", command = lambda: createPage(e2,e1)) #lambda is used so that arguments can be passed into a button command
    b2 = Button(newWin, text="Save Template", command = lambda: saveTemplate(e2,e1))

    e1.grid(row=0,column=1)
    e2.grid(row=1,column=1)
    b1.grid(row=2,column=1)
    b2.grid(row=3,column=1)

def createAvailableWindow(): #creates the window that allows for a template selection from a database
    con = lite.connect('test.db')

    chooseWin=Tk()

    def onClick(event):
        lb1.focus_set()
        print ("clicked at", event.x, event.y)
        index = lb1.nearest(event.y)
        print(lb1.get(index))
        option = lb1.get(index) #stores the option so body can be retrieved from sql
        with con:
            cur = con.cursor()
            cur.execute("SELECT body FROM bodyOptions WHERE option='"+option+"'")

            rows = cur.fetchall()
            text.delete("1.0", END)
            text.insert(INSERT, str(rows).translate({ord(i):None for i in '\'()",[]'})) #inserting the row as a text string and removing extraneous characters.

    def onDoubleClick(event):
        lb1.focus_set()
        print ("clicked at", event.x, event.y)
        index = lb1.nearest(event.y)
        print(lb1.get(index))
        option = lb1.get(index) #stores the option so body can be retrieved from sql and to be used in page generation
        with con:
            cur = con.cursor()
            cur.execute("SELECT body FROM bodyOptions WHERE option='"+option+"'")

            rows = cur.fetchall()
            text.delete("1.0", END)
            bodyText = str(rows).translate({ord(i):None for i in '\'()",[]'}) #body is stored as a variable in this case so it can be placed into the page
            text.insert(INSERT, bodyText) # doing this again in case a user double clicks a new option
            createPageFromTemplate(bodyText,option) #creating the page from the selected template


    lb1 = Listbox(chooseWin)
    with con:
        cur = con.cursor()
        cur.execute("SELECT option FROM bodyOptions")

        rows = cur.fetchall()
        
        for row in rows:
            print(row)
            lb1.insert(0, str(row).translate({ord(i):None for i in '\'()",'})) #inserting the row as a text string and removing extraneous characters.
            
    text = Text(chooseWin)

    lb1.bind("<Button-1>", onClick)
    lb1.bind("<Double-1>", onDoubleClick)
    lb1.pack()
    text.pack()
    
        
      
def initializeDB(): #this function is for testing only. Creates a database on the local machine with examples of input
        con = lite.connect('test.db')
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE bodyOptions(option TEXT, body TEXT)")
            cur.execute("INSERT INTO bodyoptions VALUES('Sample Text', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur sed augue eget lectus imperdiet lacinia sit amet scelerisque felis. Suspendisse iaculis sapien nec auctor vulputate. Etiam vel purus a ipsum convallis tincidunt. Duis sem libero, tincidunt vel augue ut, eleifend ullamcorper arcu. Morbi euismod odio condimentum felis congue mollis. Morbi condimentum sodales lectus, vitae porttitor augue facilisis id. Nunc nec maximus nunc, vel ullamcorper felis. Pellentesque nec ex ac neque viverra mollis vitae posuere leo. Nunc tristique, urna eu mattis pretium, nisl libero ultricies justo, commodo tristique neque nunc ut dui. Nunc fermentum ipsum sit amet fermentum fermentum. Nulla sit amet arcu et nulla tempus consectetur. Morbi ac urna vel sapien eleifend mollis.')")
            cur.execute("INSERT INTO bodyoptions VALUES('Hello World!', 'Hello world, this is computer')")
            cur.execute("INSERT INTO bodyoptions VALUES('Test','Test page, please ignore')")

def fetchAll(): #this function is for testing only. Returns all values in the database and prints them to the console.
    con = lite.connect('test.db')
    
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM bodyOptions")

        rows = cur.fetchall()

        for row in rows:
            print(row)
#initializeDB()
fetchAll()


mainWin=Tk()

b1 = Button(mainWin, text = "Create new body text", command = createNewWindow)
b2 = Button(mainWin, text = "Choose from available body text", command = createAvailableWindow)

b1.pack()
b2.pack()

mainWin.mainloop()

