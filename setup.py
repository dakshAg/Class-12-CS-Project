import pickle
import tkinter
from tkinter import Label, LEFT, Entry, BOTTOM, X

import mysql.connector
import pyperclip
from PIL import Image, ImageTk


class Setup:
    bg_color = "#1C2833"
    showing_err = False
    bg_color_light = "#273746"

    def __init__(self, frame, root, home_screen):
        self.frame = frame
        self.show_instructions()
        self.home_screen = home_screen
        root.mainloop()

    def show_instructions(self):
        def next_step(e):
            user = entry_user.get()
            passwd = entry_pass.get()
            dbname = entry_db.get()
            self.save_db(user, passwd, dbname)
            print("Next Clicked")

        def copy_text(e):
            pyperclip.copy('CREATE DATABASE <dbname>;')
            Label(self.frame, text="Command Copied", bg=self.bg_color, fg="white").place(relx=0.55, rely=0.25,
                                                                                         anchor="w")

        for widget in self.frame.winfo_children():
            widget.destroy()

        title = Label(self.frame, text="DigiLib Setup", bg=self.bg_color, fg="white", font=("Arial", 24))
        title.place(relx=0.5, rely=0.1, anchor="center")

        info_label = Label(self.frame, text="Please Create a Database by Using the Following Command on MySQL:",
                           wraplength=600, justify=LEFT, bg=self.bg_color, fg="white", font=("Arial", 16))
        info_label.place(relx=0.1, rely=0.2, anchor="w")

        code_label = Label(self.frame, text="CREATE DATABASE <dbname>;", bg=self.bg_color_light, fg="white",
                           font=("Courier", 16))
        code_label.place(relx=0.1, rely=0.25, anchor="w")

        img = Image.open("images/icon_copy.png")
        img = img.resize((25, 25), Image.ANTIALIAS)
        self.ic_copy = ImageTk.PhotoImage(img)

        btn_copy = Label(self.frame, image=self.ic_copy, borderwidth=0, bg=self.bg_color, highlightthickness=0, bd=0)
        btn_copy.place(relx=0.5, rely=0.25, anchor="w")
        btn_copy.bind("<Button-1>", copy_text)

        img = Image.open("images/btn_next.png")
        img = img.resize((140, 46), Image.ANTIALIAS)
        self.sub_img = ImageTk.PhotoImage(img)

        btn_next = Label(self.frame, image=self.sub_img, borderwidth=0, bg=self.bg_color,
                         highlightthickness=0, bd=0)
        btn_next.place(relx=0.8, rely=0.6, anchor="center")
        btn_next.bind("<Button-1>", next_step)

        info_label = Label(self.frame, text="Please Enter Database Details:", wraplength=450, justify=LEFT,
                           bg=self.bg_color, fg="white")
        info_label.config(font=("Arial", 16))
        info_label.place(relx=0.1, rely=0.35, anchor="w")

        Label(self.frame, text="Username:", bg=self.bg_color, fg="white").place(relx=0.1, rely=0.4, anchor="w")
        entry_user = Entry(self.frame, borderwidth=2, highlightthickness=2, insertbackground="white",
                           highlightbackground=self.bg_color_light, bg=self.bg_color_light, fg="white")
        entry_user.place(relx=0.3, rely=0.4, anchor="w")

        Label(self.frame, text="Password:", bg=self.bg_color, fg="white").place(relx=0.1, rely=0.45, anchor="w")
        entry_pass = Entry(self.frame, borderwidth=2, highlightthickness=2, insertbackground="white",
                           highlightbackground=self.bg_color_light, bg=self.bg_color_light, fg="white")
        entry_pass.place(relx=0.3, rely=0.45, anchor="w")

        Label(self.frame, text="Database:", bg=self.bg_color, fg="white").place(relx=0.1, rely=0.5, anchor="w")
        entry_db = Entry(self.frame, borderwidth=2, highlightthickness=2, insertbackground="white",
                         highlightbackground=self.bg_color_light, bg=self.bg_color_light, fg="white")
        entry_db.place(relx=0.3, rely=0.5, anchor="w")

    def save_db(self, user, passwd, dbname):
        try:
            mysql.connector.connect(host="localhost", user=user, passwd=passwd, database=dbname)
            print("Connection Successful")
            info = {"user": user, "passwd": passwd, "db": dbname}
            self.save_info(info)
            self.create_tables()
            print("Setup Successful")
            # input("Press Enter to Quit")
            self.display_success()
        except:
            print("Invalid Details\n")
            self.show_error("Invalid Details")

    def show_error(self, err):
        if not self.showing_err:
            Label(self.frame, text=err, borderwidth=0, highlightthickness=0, bd=0, fg="white", bg="#922B21"
                  ).pack(side=BOTTOM, expand=True, fill=X, anchor=tkinter.S)
            self.showing_err = True

    def display_success(self):
        def redirect_to_home(e):
            self.home_screen.refresh_db()
            self.home_screen.show_student_entry(frame=self.frame)

        for widget in self.frame.winfo_children():
            widget.destroy()

        Label(self.frame, text="Setup Successful", fg="white", bg=self.bg_color, font=("Arial", 24)
              ).place(relx=0.5, rely=0.2, anchor="center")
        img = Image.open("images/img_tick.png")
        img = img.resize((200, 200), Image.ANTIALIAS)
        self.img_tick = ImageTk.PhotoImage(img)

        Label(self.frame, image=self.img_tick, borderwidth=0, bg=self.bg_color, highlightthickness=0, bd=0).place(
            relx=0.5, rely=0.5, anchor="center")

        img = Image.open("images/btn_next.png")
        img = img.resize((140, 46), Image.ANTIALIAS)
        self.sub_img = ImageTk.PhotoImage(img)

        btn_next = Label(self.frame, image=self.sub_img, borderwidth=0, bg=self.bg_color,
                         highlightthickness=0, bd=0)
        btn_next.place(relx=0.8, rely=0.8, anchor="center")
        btn_next.bind("<Button-1>", redirect_to_home)

    @staticmethod
    def fetch_db_info():
        file_obj = open("database.dat", "rb")
        info = pickle.load(file_obj)
        return info

    @staticmethod
    def create_tables():
        queries = """
        CREATE TABLE Students (
        student_id INT AUTO_INCREMENT,
        roll_no INT,
        name VARCHAR(255),
        class_sect VARCHAR(255),
        status VARCHAR(255),
        PRIMARY KEY (student_id)
        );
        CREATE TABLE Books (
        book_id INT PRIMARY KEY AUTO_INCREMENT,
        book_name VARCHAR(255),
        author VARCHAR(255),
        qty VARCHAR(255),
        status VARCHAR(255),
        fixed_charge INT,
        per_day_charge INT
        );
        CREATE TABLE Borrows (
        borrow_id INT PRIMARY KEY AUTO_INCREMENT,
        student_id INT,
        book_id INT,
        borrow_date DATE,
        return_date DATE,
        status VARCHAR(255),
        cost INT
        );
        """

        db_info = Setup.fetch_db_info()
        con_obj = mysql.connector.connect(host="localhost", user=db_info["user"], passwd=db_info["passwd"],
                                          database=db_info["db"])
        cursor = con_obj.cursor()
        cursor.execute(queries)
        con_obj.close()
        print("Created Tables")

    @staticmethod
    def save_info(info):
        file_obj = open("database.dat", "wb")
        pickle.dump(info, file_obj)
        print("Information Saved")
