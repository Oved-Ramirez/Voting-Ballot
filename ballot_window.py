import customtkinter
from tkinter import messagebox
import sqlite3


class BallotWindow(customtkinter.CTkToplevel):
    def __init__(self, entry_1, entry_2, entry_3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry_1 = entry_1
        self.entry_2 = entry_2
        self.entry_3 = entry_3

        self.geometry("500x200")
        self.title("Voting Ballot")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.vote_frame = customtkinter.CTkFrame(self)
        self.vote_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nesw")

        self.label_title = customtkinter.CTkLabel(self, text="Candidates", font=("", 22))
        self.label_title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="new")

        # 1st Candidate
        self.cand_var = customtkinter.IntVar(value=0)

        self.radio_button = customtkinter.CTkRadioButton(self.vote_frame, text="John", font=("", 22),
                                                         variable=self.cand_var, value=1)
        self.radio_button.grid(row=0, column=1, padx=200, pady=(50,0), sticky="ew")
        # 2nd Candidate
        self.radio_button_2 = customtkinter.CTkRadioButton(self.vote_frame, text="Jane", font=("", 22),
                                                           variable=self.cand_var, value=2)
        self.radio_button_2.grid(row=1, column=1, padx=200, pady=10, sticky="ew")
        # Submit Button
        self.button_submit = customtkinter.CTkButton(self, text="Submit",
                                                     command=lambda: self.submit_vote(entry_1, entry_2, entry_3))
        self.button_submit.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def submit_vote(self, entry_1, entry_2, entry_3):
        # Get the first name, last name, and NUID from the entries
        first_name = entry_1.get()
        last_name = entry_2.get()
        nuid = entry_3.get()
        cand_var = self.cand_var.get()

        if cand_var == 1:
            cand_var = "John"
            messagebox.showinfo("Candidate Votes", "You have Voted for John")
        elif cand_var == 2:
            cand_var = "Jane"
            messagebox.showinfo("Candidate Votes", "You have Voted for Jane")
        else:
            messagebox.showwarning("Candidate Error", "Must Select Candidate")

        # Connecting to database
        con = sqlite3.connect('Ballotdata.db')
        cur = con.cursor()

        # check if table has data
        cur.execute("SELECT COUNT(*) FROM ballot WHERE NUID = ?", (nuid,))
        result = cur.fetchone()

        # NUID doesn't exist, insert a new record
        if result[0] == 0:
            cur.execute("INSERT INTO ballot (First_name, Last_name, NUID, Vote) VALUES (?, ?, ?, ?)",
                        (first_name, last_name, nuid, cand_var))
        # NUID exists, update the existing record
        else:
            cur.execute("UPDATE ballot SET Vote = ? WHERE NUID = ?", (cand_var, nuid))

        # Commit Changes
        con.commit()
        # Close connection
        con.close()
        # Close Window
        close_window(self)


def close_window(self):
    self.destroy()
    self.entry_1.delete(0, 'end')
    self.entry_2.delete(0, 'end')
    self.entry_3.delete(0, 'end')

