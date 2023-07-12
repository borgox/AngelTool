import tkinter as tk
from PIL import Image, ImageTk
from nuke import AngelNuker
import requests
import time
import random


def convert_to_icon(image_path, icon_path):
    # Open the image
    image = Image.open(image_path)

    # Resize the image if needed
    # image = image.resize((32, 32))  # Adjust the size as desired

    # Save the image as an .ico file
    image.save(icon_path, format="ICO")


def set_favicon(window, icon_path):
    window.iconbitmap(icon_path)


def MainWindow():
    # Create the Tkinter window
    window = tk.Tk()
    window.title("Angel Tool | By borgo")
    path = "logo.png"
    icon_path = "logo.ico"
    convert_to_icon(path, icon_path)
    set_favicon(window, icon_path)

    # Set the background color to bright cyan
    window.configure(bg="cyan")

    # Open the image with transparency
    image_path = "logo.png"  # Replace with the actual path to your image
    image = Image.open(image_path)

    # Create a solid background image with the same size as the original image
    background = Image.new("RGBA", image.size, (0, 255, 255, 255))  # Cyan background (R=0, G=255, B=255, A=255)

    # Composite the image onto the solid background
    image = Image.alpha_composite(background, image)

    # Create an instance of the PhotoImage class
    image_tk = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = tk.Label(window, image=image_tk, bg="cyan")
    image_label.pack(anchor="nw")  # Place the image at the top left

    # Add Rainbow Text (not animated) below the image
    text_label = tk.Label(window, text="1. Nuke", font=("Arial", 18, "bold"), fg="red", bg="cyan")
    text_label.pack(pady=20)

    # Add a medium-sized "Choose Option" text
    choose_option_label = tk.Label(window, text="Choose Option", font=("Arial", 24, "bold"), bg="cyan")
    choose_option_label.pack(pady=20)

    # Entry widget for selecting the option
    entry_var = tk.StringVar()
    entry = tk.Entry(window, textvariable=entry_var, font=("Arial", 18))
    entry.pack(pady=10)

    # Function to handle submitting the form
    def submit_form():
        option = entry_var.get()
        print("Selected option:", option)

        if option == "1":
            window.withdraw()  # Hide the main window

            # Create a new window for entering the token
            token_window = tk.Toplevel()
            token_window.title("Enter Token")
            set_favicon(token_window, icon_path)
            token_window.configure(bg="cyan")

            # Create an image label in the new window
            image_label = tk.Label(token_window, image=image_tk, bg="cyan")
            image_label.pack(anchor="nw")

            # Add a label for entering the token
            token_label = tk.Label(token_window, text="Enter Token", font=("Arial", 18, "bold"), fg="red", bg="cyan")
            token_label.pack(pady=20)

            # Entry widget for the token
            token_var = tk.StringVar()
            token_entry = tk.Entry(token_window, textvariable=token_var, font=("Arial", 18))
            token_entry.pack(pady=10)

            # Function to handle submitting the token form
            def submit_token_form():
                token = token_var.get()
                print("Entered token:", token)
                name = name_entry.get()
                guild_id = int(guild_id_entry.get())
                bot = bool(bot_entry_var.get())
                print("Entered Name", name)
                print("Entered guild ID: ", guild_id)
                print("ENtered bot: ", bot)
                # Call the validate_token_function to validate the token
                is_valid = validate_token_function(token)

                if is_valid:
                    token_window.destroy()  # Close the token window
                    window.deiconify()  # Show the main window again

                    # Create an instance of the AngelNuker class
                    

                    angel_nuker = AngelNuker(name, token, guild_id, bot)
                    angel_nuker.nuke()
                    # Use the `angel_nuker` instance as needed

            # Submit button for the token form
            

            # Add labels and entry fields for the init function parameters
            name_label = tk.Label(token_window, text="Name:", font=("Arial", 14, "bold"), fg="red", bg="cyan")
            name_label.pack(pady=10)

            name_entry = tk.Entry(token_window, font=("Arial", 14))
            name_entry.pack(pady=5)

            guild_id_label = tk.Label(token_window, text="Guild ID:", font=("Arial", 14, "bold"), fg="red", bg="cyan")
            guild_id_label.pack(pady=10)

            guild_id_entry = tk.Entry(token_window, font=("Arial", 14))
            guild_id_entry.pack(pady=5)

            bot_label = tk.Label(token_window, text="Is Bot:", font=("Arial", 14, "bold"), fg="red", bg="cyan")
            bot_label.pack(pady=10)

            bot_entry_var = tk.BooleanVar()
            bot_checkbutton = tk.Checkbutton(token_window, variable=bot_entry_var, font=("Arial", 14),
                                             bg="cyan", )
            bot_checkbutton.pack(pady=20)
            submit_button = tk.Button(token_window, text="Submit", font=("Arial", 14, "bold"), fg="red",
                                      command=submit_token_form)
            submit_button.pack(pady=10)

        else:
            # Show glitched screen with error messages
            window.withdraw()

            glitched_window = tk.Toplevel()
            glitched_window.title("Error")
            
            glitched_window.configure(bg="black")

            error_message = "Error: Invalid option selected"
            error_label = tk.Label(glitched_window, text=error_message, font=("Arial", 30, "bold"), fg="red",
                                   bg="black")
            error_label.pack(pady=50)

            glitched_label = tk.Label(glitched_window, text="...", font=("Arial", 300), fg="green", bg="black")
            glitched_label.pack()

            # Function to rerun the main window after a delay
            def rerun_main_window():
                glitched_window.destroy()
                window.deiconify()

            # After 3 seconds, rerun the main window
            glitched_window.after(3000, rerun_main_window)

    # Submit button for the main form
    submit_button = tk.Button(window, text="Submit", font=("Arial", 14, "bold"), fg="red", command=submit_form)
    submit_button.pack(pady=10)

    # Bind the Enter key press event to the submit_form function
    window.bind("<Return>", lambda event: submit_form())

    # Start the Tkinter event loop
    window.mainloop()


def validate_token_function(token):
    headers = {
        "Authorization": f"Bot {token}"
    }

    try:
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        response.raise_for_status()
        user_data = response.json()
        if "id" in user_data:
            print("Token is valid. User ID:", user_data["id"])
            return True
        else:
            print("Invalid token.")
            return False
    except requests.exceptions.HTTPError as e:
        print("Error validating token:", e.response.text)
        return False
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
        return False


MainWindow()
