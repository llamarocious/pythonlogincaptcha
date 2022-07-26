from stdiomask import getpass
import os, sys, hashlib, random, string
from captcha.image import ImageCaptcha
from PIL import Image, ImageTk
from tkinter import Tk, Label

userInfo = {}

imageInfo = ImageCaptcha(width=200, height=60)
captchaText = 'Captcha'
randomString = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
imageGenerated = imageInfo.generate(randomString)

# declaration of the main function 
# user is greeted by the main page
def main():
    print("1. Register \n2. Login \n3. Exit")
    userChoice = input("Please enter the number: ")
    if userChoice == '1':
        os.system('cls')
        register()
    elif userChoice == '2':
        login()
    elif userChoice == '3':
        exit()
    else:
        os.system('cls')
        print("Not part of the choices!")
        main()

# declaration of register function
def register():
    print("Enter username. It has to be more than 3 characters.")


    while True:
        username = input("Username: ")
        if username != '':
            break

    # checks if username already exists
    if username in userInfo:
        displayUserAlreadyExistMessage

    else:
        while True:
            # checks the number of characters using the len() function 
            if len(username) <= 3:
                print("Username has to be more than characters.")
                register()
            else:
                break
   
        while True:
            print("Enter password. It has to be more than 5 characters.")
            password = getpass("Password: ")
            confirm = getpass("Confirm Password: ")
            if len(password) < 6:
                os.system('cls')
                print("Password has to be atleast 3 characters.")
                register()
                break

            if confirm == password:
                break
            else:
                os.system('cls')
                print("Passwords don't match.")
                register()

            if password != '':
                break
            

        # calls userAlreadyExist to prevent duplication of accounts
        if userAlreadyExist(username, password):
            while True:
                os.system('cls')
                error = input("You Are Already Registered.\n\n1. Try Again \n2. Go to Main Menu \nPlease enter the number: ")
                if error == '1':
                    register()
                    
                elif error == '2':
                    os.system('cls')
                    main()
                else:
                    break

        addUserInfo([username, hash_password(password)])
        print("You've successfully registered!")
        os.system('pause')
        os.system('cls')
        main()

# the function that writes username and password data stored in text file
def addUserInfo(userInfo: list):
    with open(os.path.join(sys.path[0], "userInfo.txt"), "a") as file:
        for info in userInfo:
            file.write(info)
            file.write(' ')
        file.write('\n')


def userAlreadyExist(username, password=None):
    if password == None:
        with open(os.path.join(sys.path[0], "userInfo.txt"), "r") as file:
            for line in file:
                line = line.split()
                if line[0] == username:
                    return True
        return False

    else:
        password = hash_password(password)
        usersInfo = {}
        with open(os.path.join(sys.path[0], "userInfo.txt"), "r") as file:
            for line in file:
                line = line.split()
                if line[0] == username and line[1] == password:
                    usersInfo.update({line[0]: line[1]})
        if usersInfo == {}:
            return False
        return usersInfo[username] == password

# declaration of login function
def login():
    os.system('cls')
    with open(os.path.join(sys.path[0], "userInfo.txt"), "r") as file:
        for line in file:
            line = line.split()
            userInfo.update({line[0]: line[1]})

    while True:
        username = input("Username: ")

        if username in userInfo:
            break
        elif username not in userInfo:
            print("Username does not exist.")
            os.system('pause')
            os.system('cls')
            login()
    
    while True:
        password = getpass("Password: ")
        if not check_password_hash(password, userInfo[username]):
            print("Incorrect Password.")
            os.system('pause')
            os.system('cls')
            login()
        else:
            break
    
    capt()

# captcha function 
def capt():
    # function that transforms the generates captcha into an image
    def createImage():
        global imageInfo, randomString, imageGenerated, imageDisplay, imageLabel


        imageInfo = ImageCaptcha(width=300, height=100)
        randomString = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        imageGenerated = imageInfo.generate(randomString)
        imageDisplay = ImageTk.PhotoImage(Image.open(imageGenerated))

        imageLabel = Label(root, image=imageDisplay)
        imageLabel.grid(row=1, column=0, columnspan=2, padx=10)

    def loginFailed():
        print("Login failed. Re-enter captcha.")
        createImage()
        check()

    def loginSuccess():
        print("You have successfully logged in!")
        exit()

    def check():
        x = randomString
        y = input("Enter captcha: ")
        if x == y:
            loginSuccess()
        else:
            loginFailed()

    root = Tk()
    root.title('Captcha Authentication')
    createImage()
    check()
    

def displayUserAlreadyExistMessage():
    while True:
        print()
        error = input("You Are Already Registered.\n\n1. Try Again \n2. Go to Main Menu \nPlease enter the number: ")
        if error == '1':
            register()
            
        elif error == '2':
            os.system('cls')
            main()         
    
# encodes the password using the hash algorithm 
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_password_hash(password, hash):
    return hash_password(password) == hash

# start
# clearing the terminal and calling the main function
os.system('cls')
main()
