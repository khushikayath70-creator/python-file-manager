#import Pathlib Library hum kuch bhi create krte hai na to hume ek Path ki need hoti hai esiliye hum Path library install karege....
# from pathlib import Path
# &
# import os = os bhi import krwana pdega q ki jb hum koi file delete krege to hume usko apne operating systm me se delete hoga esiliye 
# import os

from pathlib import Path
import os 

def createfile():
    try:
        name = input("Enter your file name:- ")
        path = Path(name)
        if not path.exists() :
            with open(path, "w") as fs:
                data = input("what you want to write:- ")
                fs.write(data)
            print("file created successfully")
        else:
            print("file name already exists")

    except Exception as err:
        print(f"an error occured as {err}")

def readfile():
    try:
        name = input("Enter your File name to read :- ")
        path = Path(name)
        if path.exists():
            with open(path, "r") as fs:
                content = fs.read()
                print(f"this is your content: \n {content}")
        else:
            print("error path is not exists.") 
    except Exception as err:
        print(f"An error occured as {err}")

def updatefile():
    try:
        name = input("Enter your File name to read :- ")
        path = Path(name)
        if path.exists():
            print("Operations: ")
            print("1. Renaming the file.")
            print("2. appending the content.")
            print("3. overwriting the file")

            choice = int(input("Enter your Option:- "))

            if choice == 1:
                newFile = input("Tell your new file name:- ")
                new_path = Path(newFile)

                if not new_path.exists():
                    path.rename(new_path)
                    print("renamed successfull!")
                else:
                    print("File Already exists")
            elif choice == 2:
                with open(path, "a") as fs:
                    data = input("what do you want to append:- ")
                    fs.write("\n"+data)
                print("successfully appended")
            elif choice == 3:
                with open(path, "w") as fs:
                    data = input("what do you want to overwrite:- ")
                    fs.write("\n"+data)
                print("successfully overWrite")
    except Exception as err:
        print(f"an error is occured {err}")

def deletefile():
    try:
        name = input("tell your file name:- ")
        path = Path(name)
        if path.exists():
            path.unlink()
            print("File deleted successfully! ")
        else:
            print("Error such as file no exists.")
    except Exception as err:
        print(f"An error is occured as {err}")


print("Press 1 to create a file.")
print("Press 2 to reading a file.")
print("Press 3 to update a file.")
print("Press 4 to delete a file.")

a = int(input("\n Type your response :- "))

if a == 1:
    createfile()
if a == 2:
    readfile()
if a == 3:
    updatefile()
if a == 4:
    deletefile()