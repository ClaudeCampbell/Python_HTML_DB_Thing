
def createPage():
       print("creating page")
       file = open("newfile.html", "w")
       file.write("<html>")
       file.write("<body>")
       file.write("Stay tuned for our amazing summer sale! ")
       file.write("</body>")
       file.write("</html>")

createPage()