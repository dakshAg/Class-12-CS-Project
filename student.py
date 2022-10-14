from datetime import date
from tkinter import Label, Entry, Frame

import mysql.connector
from PIL import Image, ImageTk

from setup import Setup


class Student:
    bg_color = "#1C2833"
    bg_color_light = "#273746"

    def __init__(self, data, frame, root, homescreen):
        self.data = data
        self.frame = frame

        img = Image.open("images/btn_return_book.png")
        img = img.resize((70, 23), Image.ANTIALIAS)
        self.img_return = ImageTk.PhotoImage(img)

        self.init_db()
        self.student_home()
        self.homescreen = homescreen
        root.mainloop()

    def init_db(self):
        db_info = Setup.fetch_db_info()
        self.con_obj = mysql.connector.connect(host="localhost", user=db_info["user"], passwd=db_info["passwd"],
                                               database=db_info["db"])
        self.my_cursor = self.con_obj.cursor(dictionary=True)

    def student_home(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        def borrow(e):
            self.borrow_book()

        def back(e):
            self.homescreen.refresh_db()
            self.homescreen.show_student_entry(frame=self.frame)

        Label(self.frame, text="Welcome {}".format(self.data["name"]), font=("Arial", 20), bg=self.bg_color,
              fg="white").place(relx=0.1, rely=0.2, anchor="w")
        Label(self.frame, text="Class: {}\tRoll No: {}".format(self.data["class_sect"], self.data["roll_no"]),
              bg=self.bg_color, fg="white").place(relx=0.1, rely=0.25, anchor="w")

        title_label = Label(self.frame, text="Borrowing History", bg=self.bg_color, fg="white")
        title_label.config(font=("Arial", 18))
        title_label.place(relx=0.1, rely=0.32, anchor="w")

        img = Image.open("images/btn_back.png")
        img = img.resize((98, 32), Image.ANTIALIAS)
        self.img_back = ImageTk.PhotoImage(img)
        btn_back = Label(self.frame, image=self.img_back, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                         bd=0)
        btn_back.place(relx=0.1, rely=0.1, anchor="w")
        btn_back.bind("<Button-1>", back)

        img = Image.open("images/btn_borrow_book.png")
        img = img.resize((194, 45), Image.ANTIALIAS)
        self.img_borrow = ImageTk.PhotoImage(img)
        btn_borrow = Label(self.frame, image=self.img_borrow, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                           bd=0)
        btn_borrow.place(relx=0.9, rely=0.1, anchor="e")
        btn_borrow.bind("<Button-1>", borrow)

        self.print_borrow_history()

    def borrow_book(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        def back(e):
            self.student_home()

        img = Image.open("images/btn_back.png")
        img = img.resize((98, 32), Image.ANTIALIAS)
        self.img_back = ImageTk.PhotoImage(img)
        btn_back = Label(self.frame, image=self.img_back, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                         bd=0)
        btn_back.place(relx=0.1, rely=0.1, anchor="w")
        btn_back.bind("<Button-1>", back)

        Label(self.frame, text="Enter Book ID to Borrow", font=("Arial", 20), bg=self.bg_color, fg="white").place(
            relx=0.1, rely=0.2)
        ent_bid = Entry(self.frame, bg=self.bg_color_light, fg="white",
                        borderwidth=2, highlightthickness=2, insertbackground="white",
                        highlightbackground=self.bg_color_light)
        ent_bid.place(relx=0.1, rely=0.25)

        def save_borrow(e):
            if self.book_id_valid(ent_bid.get()) == 0:
                self.show_error("Invalid Book ID")
                return

            borrow_date = date.today().strftime("%Y/%m/%d")
            query = """
            INSERT INTO Borrows
            (student_id, book_id, borrow_date, status)
            VALUES
            ('{}','{}','{}','{}');
            """.format(self.data["student_id"], ent_bid.get(), borrow_date, "BORROWED")

            self.my_cursor.execute(query)
            self.con_obj.commit()
            print("Book Borrowed")
            self.show_book_borrowed_success(ent_bid.get())

        img = Image.open("images/btn_borrow_book.png")
        img = img.resize((194, 45), Image.ANTIALIAS)
        self.img_borrow = ImageTk.PhotoImage(img)
        btn_borrow = Label(self.frame, image=self.img_borrow, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                           bd=0)
        btn_borrow.place(relx=0.9, rely=0.35, anchor="e")
        btn_borrow.bind("<Button-1>", save_borrow)

    def show_book_borrowed_success(self, bid):
        def okay(e):
            self.student_home()

        for widget in self.frame.winfo_children():
            widget.destroy()
        Label(self.frame, text="Book Borrowed Successfully", font=("Arial", 20), bg=self.bg_color, fg="white").place(
            relx=0.5, rely=0.1, anchor="center")
        book_details = self.book_details(bid)

        book_frame = Frame(self.frame, bg=self.bg_color)
        book_frame.place(relx=0.1, rely=0.2, anchor="nw")

        fon = ("Arial", 20)
        Label(book_frame, bg=self.bg_color, fg="white", font=fon,
              text="Book Name: {}".format(book_details["book_name"])).grid(row=0, sticky="w")
        Label(book_frame, bg=self.bg_color, fg="white", font=fon,
              text="Author: {}".format(book_details["author"])).grid(row=1, sticky="w")
        Label(book_frame, bg=self.bg_color, fg="white", font=fon,
              text="Fixed Charge: {}".format(book_details["fixed_charge"])).grid(row=2, sticky="w")
        Label(book_frame, bg=self.bg_color, fg="white", font=fon,
              text="Per Day Charge: {}".format(book_details["per_day_charge"])).grid(row=3, sticky="w")

        img = Image.open("images/btn_ok.png")
        img = img.resize((94, 45), Image.ANTIALIAS)
        self.img_ok = ImageTk.PhotoImage(img)
        btn_ok = Label(self.frame, image=self.img_ok, borderwidth=0, bg=self.bg_color, highlightthickness=0, bd=0)
        btn_ok.place(relx=0.9, rely=0.4, anchor="e")
        btn_ok.bind("<Button-1>", okay)

    def show_error(self, err):
        Label(self.frame, text=err, borderwidth=0, highlightthickness=0, bd=0, fg="white", bg="#922B21",
              width=int(self.frame.winfo_width()), justify="center").place(relx=0.5, rely=0.6, anchor="center")

    def print_borrow_history(self):
        frame_bors = Frame(self.frame, bg=self.bg_color)
        frame_bors.place(relx=0.1, rely=0.35, anchor="nw")
        query = "SELECT * FROM Borrows WHERE student_id = {};".format(self.data["student_id"])
        self.my_cursor.execute(query)
        self.print_history_row(
            {"borrow_id": "Borrow ID", "student_id": "Student ID", "book_id": "Book ID", "borrow_date": "Borrow Date",
             "return_date": "Return Date", "status": "Status", "cost": "Cost"}, frame_bors, 0)

        bdata = self.my_cursor.fetchall()
        for row in range(len(bdata)):
            self.print_history_row(bdata[row], frame_bors, row + 1)

    def print_history_row(self, row, frame, n):
        def ret_book(e):
            self.return_book(row)

        Label(frame, text=row["borrow_id"], bg=self.bg_color, fg="white").grid(column=0, row=n)
        Label(frame, text=row["student_id"], bg=self.bg_color, fg="white").grid(column=1, row=n)
        Label(frame, text=row["book_id"], bg=self.bg_color, fg="white").grid(column=2, row=n)
        Label(frame, text=row["borrow_date"], bg=self.bg_color, fg="white").grid(column=3, row=n)
        Label(frame, text=row["return_date"], bg=self.bg_color, fg="white").grid(column=4, row=n)
        Label(frame, text=row["status"], bg=self.bg_color, fg="white").grid(column=5, row=n)
        Label(frame, text=row["cost"], bg=self.bg_color, fg="white").grid(column=6, row=n)

        if row["status"] == "BORROWED":
            btn_submit = Label(frame, image=self.img_return, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                               bd=0)
            btn_submit.grid(column=7, row=n)
            btn_submit.bind("<Button-1>", ret_book)

    def return_book(self, brow):
        b_date = brow["borrow_date"]
        r_date = date.today()
        delta = r_date - b_date
        print(delta.days)

        book = self.book_details(brow["book_id"])
        cost = book["fixed_charge"] + book["per_day_charge"] * delta.days
        print("Cost", cost)

        query = "UPDATE Borrows SET return_date = '{}', status = 'RETURNED', cost={} WHERE borrow_id={}".format(
            r_date.strftime("%Y/%m/%d"), cost, brow["borrow_id"])
        self.my_cursor.execute(query)
        self.con_obj.commit()
        self.student_home()

    def book_id_valid(self, bid):
        query = "SELECT * FROM Books WHERE book_id = {};".format(bid)
        self.my_cursor.execute(query)
        data = self.my_cursor.fetchall()
        print(data)
        return len(data)

    def book_details(self, bid):
        query = "SELECT * FROM Books WHERE book_id = {};".format(bid)
        self.my_cursor.execute(query)
        return self.my_cursor.fetchone()
