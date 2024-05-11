import sqlite3
import customtkinter
from tkinter import messagebox
from app import App
from database import create_table

app = App()
app.center_window()
create_table()
app.mainloop()
