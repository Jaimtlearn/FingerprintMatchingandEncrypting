from dotenv import load_dotenv
from Crypto import Random
from Crypto.Cipher import AES
import os
import time
import getpass
load_dotenv()

class Encryption:
    # Initializing Key
    def __init__(self,key):
        self.key = key

    # Adds padding to the Image
    def padding(self,txt):
        return txt + b"\0" * (AES.block_size - len(txt) % AES.block_size)
    
    # Encrypt Function
    def encrypt(self,message,key,key_size=256):
        message = self.padding(message)
        IV = Random.new().read(AES.block_size)
        Cipher_text = AES.new(key,AES.MODE_CBC, IV)
        return IV + Cipher_text.encrypt(message)
    
    def encrypt_file(self,filename):
        with open(filename,'rb') as f:
            text = f.read()
        enc = self.encrypt(text,self.key)
        with open(filename + ".enc",'wb') as f:
            f.write(enc)
        os.remove(filename)
    # Decrypt Function
    def decrypt(self,text,key):
        IV = text[:AES.block_size]
        cipher = AES.new(key,AES.MODE_CBC,IV)
        plaintext = cipher.decrypt(text[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self,filename):
        with open(filename,'rb') as f:
            text = f.read()
        dec = self.decrypt(text,self.key)
        with open(filename[:-4],'wb') as f:
            f.write(dec)
        os.remove(filename)

    #get all files code
    def encrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)
    

obj = Encryption(bytes.fromhex(os.getenv('KEY'))) # Fetching Key from envrionment
clear = lambda: os.system('cls') # Function for clearing cli screen

if os.path.isfile('data.txt.enc'): # If secured password file is created
    while True:
        password = getpass.getpass("Enter Password :")
        obj.decrypt_file("data.txt.enc")
        p = ''
        with open("data.txt",'r') as f:
            p = f.readlines()
        if p[0] == password:
            obj.encrypt_file("data.txt")
            break
    while True: # taking input
        clear()
        choice = int(input(
            "1. Press '1' to encrypt file.\n2. Press '2' to decrypt file.\n3. Press '3' to Encrypt all files in the directory.\n4. Press '4' to decrypt all files in the directory.\n5. Press '5' to exit.\n"))
        clear()
        if choice == 1:
            obj.encrypt_file(input("Enter name of file to encrypt: "))
        elif choice == 2:
            obj.decrypt_file(input("Enter name of file to decrypt: "))
        elif choice == 3:
            obj.encrypt_all_files()
        elif choice == 4:
            obj.decrypt_all_files()
        elif choice == 5:
            exit()
        else:
            print("Please select a valid option!")
else: # If there is no data.txt.enc file
    while True:
        clear()
        password = getpass.getpass("Setting up stuff. Enter a password that will be used for decryption: ") # Takes password
        repassword = getpass.getpass("Confirm password: ") # Confirmation for previous input
        if password == repassword:
            break
        else:
            print("Passwords Mismatched!")
            
    with open("data.txt",'w+') as f:
        f.write(password)

    obj.encrypt_file("data.txt")
    print("Please restart the program to complete the setup")
    time.sleep(15)
