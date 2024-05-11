import customtkinter
from tkinter import messagebox
import sqlite3
from ballot_window import BallotWindow


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # global variable
        users_entry = []

        self.title("Voting Ballot")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # Adding frames to see how it will mess with the button
        self.info_frame = customtkinter.CTkFrame(self)
        self.info_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nesw")

        # First Name
        self.label_1 = customtkinter.CTkLabel(self.info_frame, text="First Name", font=("", 22))
        self.label_1.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")

        self.entry_1 = customtkinter.CTkEntry(self.info_frame, width=200, height=30)
        self.entry_1.grid(row=0, column=1, padx=10, pady=(10,0), sticky="w")
        # Last Name
        self.label_2 = customtkinter.CTkLabel(self.info_frame, text="Last Name", font=("", 22))
        self.label_2.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_2 = customtkinter.CTkEntry(self.info_frame, width=200, height=30)
        self.entry_2.grid(row=1, column=1, padx=10, pady=(10,0), sticky="w")

        # NUID
        self.label_3 = customtkinter.CTkLabel(self.info_frame, text="NUID", font=("", 22))
        self.label_3.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.entry_3 = customtkinter.CTkEntry(self.info_frame, width=200, height=30)
        self.entry_3.grid(row=2, column=1, padx=10, pady=(10,0), sticky="w")

        # Next Button
        self.button = customtkinter.CTkButton(self, text="Next", command=self.button_next)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.toplevel_window = None

    def center_window(self):
        self.update_idletasks()
        width = 500
        height = 200
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def next_window(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = BallotWindow(self.entry_1, self.entry_2, self.entry_3, self)
            self.center_window()

    def button_next(self):
        nuid = customtkinter.CTkEntry.get(self.entry_3)

        if len(nuid) == 8:
           # print("VALID NUID")

            # Check if NUID already voted
            con = sqlite3.connect('Ballotdata.db')
            cur = con.cursor()

            # Check if the NUID already exists in the database
            cur.execute("SELECT COUNT(*) FROM ballot WHERE NUID = ?", (nuid,))
            result = cur.fetchone()
            # NUID already exists, meaning the user has already voted
            if result[0] > 0:
                messagebox.showerror("NUID Error", "NUID has already voted!")
            # NUID does not exist, proceed to the next window
            else:
                self.next_window()

            con.close()

        else:
            print("INVALID NUID")
            messagebox.showinfo("NUID ERROR", "NUID is invalid needs to be 8 digits.")
