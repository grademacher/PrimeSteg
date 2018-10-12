from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import string
import encoder

input_file_name = ""
decrypted_message = ""
output_file_name = ""
encryption_key = ""


def get_input_file(event):
    Tk().withdraw()
    global input_file_name
    input_file_name = askopenfilename()
    return


def encrypt_message(event):
    global decrypted_message
    global output_file_name
    global encryption_key
    # Get the information from the entry boxes
    decrypted_message = message.get("1.0", END)
    output_file_name = output_file.get()
    encryption_key = alphabet_key.get()

    # Check to make sure a message was provided to encrypt
    if len(decrypted_message) < 1:
        messagebox.showinfo("Alert", "Please enter a message to encrypt.")
        return

    # Check to make sure an input file name was provided
    if len(input_file_name) < 1:
        messagebox.showinfo("Alert", "Please enter a file to use.")
        return

    # Check to make sure the input file name is valid
    input_name_ary = input_file_name.split(".")
    file_extension = input_name_ary[1]
    if file_extension != "png" and file_extension != "jpg":
        messagebox.showinfo("Alert", "Please select a png or jpg image to encrypt with.")
        return

    # If an output file name was not provided, create one
    # Else, check the output name for the correct format
    if len(output_file_name) < 1:
        input_ary = input_file_name.split("/")
        file_name = input_ary[len(input_ary) - 1].split(".")
        output_file_name = file_name[0] + "_ENCRYPTED.png"
    else:
        output_ary = output_file_name.split(".")
        if len(output_ary) < 2:
            messagebox.showinfo("Alert", "Please enter a valid file extension for the output file.")
            return
        if output_ary[1] != "png":
            messagebox.showinfo("Alert", "The output format must be a .png file.")
            return

    # Check to make sure the encryption key is valid
    if len(encryption_key) < 1:
        encryption_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    else:
        if len(encryption_key) != 26:
            messagebox.showinfo("Alert", "The encryption key should only contain 26 characters.")
            return
        for c in encryption_key:
            if not c.isalpha():
                messagebox.showinfo("Alert", "The encryption key must contain only alpha characters.")
                return
        alphabet = set(string.ascii_lowercase)
        if not set(encryption_key.lower()) >= alphabet:
            messagebox.showinfo("Alert", "The encryption key must contain all letters of the alphabet")
            return
        encryption_key = encryption_key.upper()

    # Call the encryption function and hold onto the results
    return_items = encoder.encrypt(decrypted_message, input_file_name, output_file_name, encryption_key)

    # Display the results of the encryption process
    messagebox.showinfo("Alert", "Plaintext Message: " + return_items[0] + "\nAlphabet Key used: " + return_items[1] +
                        "\nOutput File: " + return_items[2])


root = Tk()

Label(root, text="Message:").grid(row=0)

message = Text(root)
message.grid(row=1, sticky=N+S+E+W, padx=5, pady=5)

Label(root, text="Input File:").grid(row=2)

input_button = Button(root, text="Select File")
input_button.bind("<Button-1>", get_input_file)
input_button.grid(row=3, sticky=N+S+E+W, padx=5, pady=5)

Label(root, text="Output File: (Optional)").grid(row=4)

output_file = Entry(root)
output_file.grid(row=5, sticky=N+S+E+W, padx=5, pady=5)

Label(root, text="Alphabet Key: (Optional)").grid(row=6)

alphabet_key = Entry(root)
alphabet_key.grid(row=7, sticky=E+W, padx=5, pady=5)

encrypt_button = Button(root, text="Encrypt Message")
encrypt_button.bind("<Button-1>", encrypt_message)
encrypt_button.grid(row=8)

for i in range(9):
    Grid.rowconfigure(root, i, weight=1)
Grid.columnconfigure(root, 0, weight=1)

root.mainloop()
