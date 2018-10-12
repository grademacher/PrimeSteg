from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import string
import decoder

input_file_name = ""
decrypted_message = ""
output_file_name = ""
decryption_key = ""
brute_force_iterations = 100


def get_input_file(event):
    Tk().withdraw()
    global input_file_name
    input_file_name = askopenfilename()
    return


def decrypt_message(event):
    global decrypted_message
    global output_file_name
    global decryption_key
    global brute_force_iterations
    # Get the information from the entry boxes
    # decrypted_message = message.get()
    output_file_name = output_file.get()
    decryption_key = alphabet_key.get()

    # Check to make sure an input file name was provided
    if len(input_file_name) < 1:
        messagebox.showinfo("Alert", "Please enter a file to use.")
        return

    # Check to make sure the input file is an image
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
        output_file_name = file_name[0] + "_DECRYPTED.txt"
    else:
        output_ary = output_file_name.split(".")
        if len(output_ary) < 2:
            messagebox.showinfo("Alert", "Please enter a valid file extension for the output file.")
            return
        if output_ary[1] != "txt":
            messagebox.showinfo("Alert", "The output format must be a .txt file.")
            return

    # Check to make sure the decryption key is valid
    if len(decryption_key) < 1:
        decryption_key = ""
    else:
        if len(decryption_key) != 26:
            messagebox.showinfo("Alert", "The decryption key should only contain 26 characters.")
            return
        for c in decryption_key:
            if not c.isalpha():
                messagebox.showinfo("Alert", "The decryption key must contain only alpha characters.")
                return
        alphabet = set(string.ascii_lowercase)
        if not set(decryption_key.lower()) >= alphabet:
            messagebox.showinfo("Alert", "The decryption key must contain all letters of the alphabet")
            return
        decryption_key = decryption_key.upper()

    # Check to make sure the input file name is valid
    input_name_ary = input_file_name.split(".")
    file_extension = input_name_ary[1]
    if file_extension != "png" and file_extension != "jpg":
        messagebox.showinfo("Alert", "Please select a png or jpg image to encrypt with.")
        return

    # Check for a specified number of iterations for the brute force attack
    if iteration_count.get() == "":
        brute_force_iterations = 100
    else:
        brute_force_iterations = int(iteration_count.get())

    # Call the decryption function and hold onto the results
    if len(decryption_key) == 0:
        return_ary = decoder.brute_force(input_file_name, output_file_name, brute_force_iterations)
        add_solution(return_ary[0], return_ary[1], return_ary[2], return_ary[3])

    else:
        return_ary = decoder.decrypt_key(input_file_name, output_file_name, decryption_key)
        messagebox.showinfo("Alert",
                            "Plaintext Message: " + return_ary[0] + "\nAlphabet Key used: " + return_ary[1] +
                            "\nOutput File: " + return_ary[2])


def add_solution(score, key, text, iteration):
    message.config(state=NORMAL)
    message.insert(END, ('\nbest score so far: ' + str(score) + ' on iteration ' + str(iteration)))
    message.insert(END, ('\n    best key: ' + ''.join(key)))
    message.insert(END, ('\n    plaintext: ' + text))
    message.config(state=DISABLED)
    return


root = Tk()

Label(root, text="Message:").grid(row=0)

message = Text(root)
message.grid(row=1, sticky=N+S+E+W, padx=5, pady=5)
message.config(state=DISABLED)

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

Label(root, text="Number of Iterations (Brute Force Only): (Optional) ").grid(row=8)

iteration_count = Entry(root)
iteration_count.grid(row=9, sticky=E+W, padx=5, pady=5)

decrypt_button = Button(root, text="Decrypt Message")
decrypt_button.bind("<Button-1>", decrypt_message)
decrypt_button.grid(row=10)

for i in range(11):
    Grid.rowconfigure(root, i, weight=1)
Grid.columnconfigure(root, 0, weight=1)

root.mainloop()