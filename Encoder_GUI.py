from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
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
    decrypted_message = message.get()
    output_file_name = output_file.get()
    encryption_key = alphabet_key.get()

    if len(decrypted_message) < 1:
        messagebox.showinfo("Alert", "Please enter a message to encrypt.")

    if len(input_file_name) < 1:
        messagebox.showinfo("Alert", "Please enter a file to use.")

    if len(output_file_name) < 1:
        input_ary = input_file_name.split("/")
        file_name = input_ary[len(input_ary) - 1].split(".")
        output_file_name = file_name[0] + "_ENCRYPTED.png"

    if len(encryption_key) < 26:
        encryption_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Check to make sure the input file name is valid
    # Check to make sure the output file name is valid
    # Check to make sure the key is valid

    return_items = encoder.encrypt(decrypted_message, input_file_name, output_file_name, encryption_key)

    messagebox.showinfo("Alert", "Plaintext Message: " + return_items[0] + "\nAlphabet Key used: " + return_items[1] +
                        "\nOutput File: " + return_items[2])


root = Tk()

Label(root, text="Message:").grid(row=0)

message = Entry(root)
message.grid(row=1)

Label(root, text="Input File:").grid(row=2)

input_button = Button(root, text="Select File")
input_button.bind("<Button-1>", get_input_file)
input_button.grid(row=3)

Label(root, text="Output File: (Optional)").grid(row=4)

output_file = Entry(root)
output_file.grid(row=5)

Label(root, text="Alphabet Key: (Optional)").grid(row=6)

alphabet_key = Entry(root)
alphabet_key.grid(row=7)

encrypt_button = Button(root, text="Encrypt Message")
encrypt_button.bind("<Button-1>", encrypt_message)
encrypt_button.grid(row=8)

root.mainloop()