import csv
import textwrap
from tkinter import Label, Entry, Frame, filedialog, FLAT, StringVar

import mysql.connector
from PIL import Image, ImageTk

import extra_widgets as ew
from setup import Setup


class Admin:
    bg_color = "#1C2833"
    bg_color_light = "#273746"

    def __init__(self, frame, root, homescreen):
        self.frame = frame
        self.init_db()
        self.pass_window()
        self.homescreen = homescreen
        root.mainloop()

    def init_db(self):
        db_info = Setup.fetch_db_info()
        self.con_obj = mysql.connector.connect(host="localhost", user=db_info["user"], passwd=db_info["passwd"],
                                               database=db_info["db"])
        self.my_cursor = self.con_obj.cursor(dictionary=True)

    def pass_window(self):
        self.pass_visi = False

        def back(e):
            self.homescreen.refresh_db()
            self.homescreen.show_student_entry(frame=self.frame)

        def check_pass(e):
            if entry_pass.get() == "admin123":
                self.show_home()
            else:
                self.show_error("Wrong Password")

        def pass_ic_click(e):
            if self.pass_visi:
                ic_visi.configure(image=self.icon_visible)
                entry_pass.configure(show="•")
                self.pass_visi = False
            else:
                ic_visi.configure(image=self.icon_invisible)
                entry_pass.configure(show="")
                self.pass_visi = True

        for widget in self.frame.winfo_children():
            widget.destroy()
        title = Label(self.frame, text="DigiLib", bg=self.bg_color, fg="white", font=("Arial", 24))
        title.place(relx=0.5, rely=0.2, anchor="center")

        Label(self.frame, text="Password:", bg=self.bg_color, fg="white").place(relx=0.1, rely=0.3, anchor="w")
        entry_pass = Entry(self.frame, show="•", bg=self.bg_color_light, fg="white",
                           borderwidth=2, highlightthickness=2, insertbackground="white",
                           highlightbackground=self.bg_color_light)
        entry_pass.place(relx=0.2, rely=0.3, anchor="w")

        img = Image.open("images/icon_visible.png")
        img = img.resize((30, 30), Image.ANTIALIAS)
        self.icon_visible = ImageTk.PhotoImage(img)

        img = Image.open("images/icon_not_visible.png")
        img = img.resize((30, 30), Image.ANTIALIAS)
        self.icon_invisible = ImageTk.PhotoImage(img)

        ic_visi = Label(self.frame, image=self.icon_visible, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                        bd=0)
        ic_visi.place(relx=0.5, rely=0.3, anchor="center")
        ic_visi.bind("<Button-1>", pass_ic_click)

        img = Image.open("images/btn_next.png")
        img = img.resize((140, 46), Image.ANTIALIAS)
        self.img_next = ImageTk.PhotoImage(img)
        btn_submit = Label(self.frame, image=self.img_next, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                           bd=0)
        btn_submit.place(relx=0.8, rely=0.4, anchor="center")
        btn_submit.bind("<Button-1>", check_pass)

        img = Image.open("images/btn_back.png")
        img = img.resize((98, 32), Image.ANTIALIAS)
        self.img_back = ImageTk.PhotoImage(img)
        btn_back = Label(self.frame, image=self.img_back, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                         bd=0)
        btn_back.place(relx=0.1, rely=0.1, anchor="w")
        btn_back.bind("<Button-1>", back)

    def show_error(self, err):
        Label(self.frame, text=err, borderwidth=0, highlightthickness=0, bd=0, fg="white", bg="#922B21",
              width=int(self.frame.winfo_width()), justify="center").place(relx=0.5, rely=0.6, anchor="center")

    def show_home(self):
        def show_books(e):
            self.books_page()

        def show_students(e):
            self.students_page()

        def borrowing_hist(e):
            self.borrowing_history()

        def back(e):
            self.homescreen.refresh_db()
            self.homescreen.show_student_entry(frame=self.frame)

        for widget in self.frame.winfo_children():
            widget.destroy()

        img = Image.open("images/btn_back.png")
        img = img.resize((98, 32), Image.ANTIALIAS)
        self.img_back = ImageTk.PhotoImage(img)
        btn_back = Label(self.frame, image=self.img_back, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                         bd=0)
        btn_back.place(relx=0.1, rely=0.1, anchor="w")
        btn_back.bind("<Button-1>", back)

        img = Image.open("images/card_books.png")
        img = img.resize((200, 200), Image.ANTIALIAS)
        self.books_img = ImageTk.PhotoImage(img)

        btn_books = Label(self.frame, image=self.books_img, borderwidth=0, bg=self.bg_color, highlightthickness=0, bd=0)
        btn_books.place(relx=0.3, rely=0.4, anchor="center")
        btn_books.bind("<Button-1>", show_books)

        img = Image.open("images/card_students.png")
        img = img.resize((200, 200), Image.ANTIALIAS)
        self.students_img = ImageTk.PhotoImage(img)

        btn_students = Label(self.frame, image=self.students_img, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                             bd=0)
        btn_students.place(relx=0.7, rely=0.4, anchor="center")
        btn_students.bind("<Button-1>", show_students)

        img = Image.open("images/card_bor_hist.png")
        img = img.resize((200, 200), Image.ANTIALIAS)
        self.borrow_img = ImageTk.PhotoImage(img)

        btn_borrows = Label(self.frame, image=self.borrow_img, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                            bd=0)
        btn_borrows.place(relx=0.5, rely=0.8, anchor="center")
        btn_borrows.bind("<Button-1>", borrowing_hist)

    def books_page(self):
        def search_ic_press(e):
            print("Pressed Search Icon. No Action")

        def export_data(e):
            save_as_file = filedialog.asksaveasfile(mode="w", defaultextension='.csv')
            csv_writer = csv.writer(save_as_file)
            csv_writer.writerow(["Book ID", "Name", "Author", "Qty", "Status", "Fixed Charge", "Per Day Charge"])
            for row in data:
                vals = row.values()
                print(vals)
                csv_writer.writerow(vals)
            save_as_file.close()

        def show_home(e):
            self.show_home()

        def add_book(e):
            self.add_book()

        def search_callback(sv):
            self.display_searched_books(sv.get(), books_frame)

        for widget in self.frame.winfo_children():
            widget.destroy()

        img = Image.open("images/btn_back.png")
        img = img.resize((98, 32), Image.ANTIALIAS)
        self.img_back = ImageTk.PhotoImage(img)
        btn_back = Label(self.frame, image=self.img_back, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                         bd=0)
        btn_back.place(relx=0.1, rely=0.1, anchor="w")
        btn_back.bind("<Button-1>", show_home)

        img = Image.open("images/btn_add_book.png")
        img = img.resize((156, 45), Image.ANTIALIAS)
        self.img_ab = ImageTk.PhotoImage(img)
        btn_ab = Label(self.frame, image=self.img_ab, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                       bd=0)
        btn_ab.place(relx=0.9, rely=0.1, anchor="e")
        btn_ab.bind("<Button-1>", add_book)

        title = Label(self.frame, text="Books", bg=self.bg_color, fg="white", font=("Arial", 24))
        title.place(relx=0.1, rely=0.2, anchor="w")

        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: search_callback(sv))
        ent_search = Entry(self.frame, bg=self.bg_color_light, fg="white", borderwidth=5, highlightthickness=0,
                           insertbackground="white", highlightbackground=self.bg_color_light, relief=FLAT,
                           textvariable=sv)
        ent_search.place(relx=0.9, rely=0.2, anchor="e")

        img = Image.open("images/icon_search.png")
        img.mode = 'RGBA'
        img = img.resize((30, 30), Image.ANTIALIAS)
        self.img_search = ImageTk.PhotoImage(img)
        ic_search = Label(self.frame, image=self.img_search, borderwidth=0, background=self.bg_color,
                          highlightthickness=0)
        ic_search.place(relx=0.60, rely=0.2, anchor="e")
        ic_search.bind("<Button-1>", search_ic_press)

        books_frame = Frame(self.frame, bg=self.bg_color)
        books_frame.place(relx=0.1, rely=0.3, anchor="nw")

        query = "SELECT * FROM Books;"
        self.my_cursor.execute(query)
        self.book_row(b_frame=books_frame, nrow=0, font='Helvetica 18 bold',
                      data={"book_id": "Book ID", "book_name": "Name", "author": "Author", "qty": "Qty",
                            "status": "Status"}, editable=False, bg=self.bg_color)
        data = self.my_cursor.fetchall()

        img = Image.open("images/icon_delete.png")
        img = img.resize((30, 30), Image.ANTIALIAS)
        self.img_del = ImageTk.PhotoImage(img)

        img = Image.open("images/icon_edit.png")
        img = img.resize((30, 30), Image.ANTIALIAS)
        self.img_edit = ImageTk.PhotoImage(img)

        for i in range(len(data)):
            self.book_row(books_frame, i + 1, font='Helvetica 14', data=data[i])
        if not len(data):
            title = Label(self.frame, text="No Data Available", bg=self.bg_color, fg="white", font=("Arial", 14))
            title.place(relx=0.5, rely=0.4, anchor="center")

        img = Image.open("images/btn_export.png")
        img = img.resize((183, 45), Image.ANTIALIAS)
        self.img_export = ImageTk.PhotoImage(img)
        btn_export = Label(self.frame, image=self.img_export, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                           bd=0)
        btn_export.place(relx=0.9, rely=0.9, anchor="e")
        btn_export.bind("<Button-1>", export_data)

    def display_searched_books(self, keyword, bframe):
        for widget in bframe.winfo_children():
            widget.destroy()

        query = "SELECT * FROM Books WHERE book_name LIKE '%{}%' OR author LIKE '%{}%' OR book_id LIKE '%{}%'".format(
            keyword, keyword, keyword)

        self.my_cursor.execute(query)
        self.book_row(b_frame=bframe, nrow=0, font='Helvetica 18 bold',
                      data={"book_id": "Book ID", "book_name": "Name", "author": "Author", "qty": "Qty",
                            "status": "Status"}, editable=False, bg=self.bg_color)
        data = self.my_cursor.fetchall()

        img = Image.open("images/icon_delete.png")
        img = img.resize((30, 30), Image.ANTIALIAS)
        self.img_del = ImageTk.PhotoImage(img)

        img = Image.open("images/icon_edit.png")
        img = img.resize((30, 30), Image.ANTIALIAS)
        self.img_edit = ImageTk.PhotoImage(img)

        for i in range(len(data)):
            self.book_row(bframe, i + 1, font='Helvetica 14', data=data[i])
        if not len(data):
            title = Label(bframe, text="No Data Available", bg=self.bg_color, fg="white", font=("Arial", 14))
            title.grid(column=0, row=1)

    def book_row(self, b_frame, nrow, font, data, editable=True, bg=bg_color):
        def del_book(e):
            self.delete_book(data["book_id"])

        def ed_book(e):
            self.edit_book(data)

        bname = textwrap.shorten(data["book_name"], width=15, placeholder="...")

        Frame(b_frame, bg=bg).grid(column=0, row=nrow, columnspan=6)

        Label(b_frame, text=data["book_id"], font=font, bg=bg, fg="white").grid(column=0, row=nrow)
        Label(b_frame, text=bname, font=font, bg=bg, fg="white").grid(column=1, row=nrow)
        Label(b_frame, text=data["author"], font=font, bg=bg, fg="white").grid(column=2, row=nrow)
        Label(b_frame, text=data["qty"], font=font, bg=bg, fg="white").grid(column=3, row=nrow)
        Label(b_frame, text=data["status"], font=font, bg=bg, fg="white").grid(column=4, row=nrow)
        if editable:
            btn_del = Label(b_frame, image=self.img_del, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                            bd=0)
            btn_del.grid(column=5, row=nrow)
            btn_del.bind("<Button-1>", del_book)

            btn_edit = Label(b_frame, image=self.img_edit, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                             bd=0)
            btn_edit.grid(column=6, row=nrow)
            btn_edit.bind("<Button-1>", ed_book)

    def add_book(self):

        def back(e):
            self.books_page()

        for widget in self.frame.winfo_children():
            widget.destroy()

        img = Image.open("images/btn_back.png")
        img = img.resize((98, 32), Image.ANTIALIAS)
        self.img_back = ImageTk.PhotoImage(img)
        btn_back = Label(self.frame, image=self.img_back, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                         bd=0)
        btn_back.place(relx=0.1, rely=0.1, anchor="w")
        btn_back.bind("<Button-1>", back)

        title = Label(self.frame, text="Add Book", bg=self.bg_color, fg="white", font=("Arial", 24))
        title.place(relx=0.5, rely=0.1, anchor="center")

        books_frame = Frame(self.frame, bg=self.bg_color)
        books_frame.place(relx=0.1, rely=0.2, anchor="nw")

        Label(books_frame, text="Book Name", bg=self.bg_color, fg="white").grid(column=0, row=1, sticky="W")
        ent_name = Entry(books_frame, bg=self.bg_color_light, fg="white",
                         borderwidth=2, highlightthickness=2, insertbackground="white",
                         highlightbackground=self.bg_color_light)
        ent_name.grid(column=1, row=1)

        Label(books_frame, text="Author", bg=self.bg_color, fg="white").grid(column=0, row=2, sticky="W")
        ent_auth = Entry(books_frame, bg=self.bg_color_light, fg="white",
                         borderwidth=2, highlightthickness=2, insertbackground="white",
                         highlightbackground=self.bg_color_light)
        ent_auth.grid(column=1, row=2)

        Label(books_frame, text="Quantity", bg=self.bg_color, fg="white").grid(column=0, row=3, sticky="W")
        ent_qty = ew.NumEntry(books_frame, bg=self.bg_color_light, fg="white",
                              borderwidth=2, highlightthickness=2, insertbackground="white",
                              highlightbackground=self.bg_color_light)
        ent_qty.grid(column=1, row=3)

        Label(books_frame, text="Borrowing Charges", font=("Courier", 16), bg=self.bg_color, fg="white"
              ).grid(column=0, row=4, sticky="W", columnspan=2, pady=10)

        Label(books_frame, text="Fixed Charge", bg=self.bg_color, fg="white").grid(column=0, row=5, sticky="W")
        ent_fix_charge = ew.NumEntry(books_frame, bg=self.bg_color_light, fg="white",
                                     borderwidth=2, highlightthickness=2, insertbackground="white",
                                     highlightbackground=self.bg_color_light)
        ent_fix_charge.grid(column=1, row=5)

        Label(books_frame, text="Per Day Charge", bg=self.bg_color, fg="white").grid(column=0, row=6, sticky="W")
        ent_pd_charge = ew.NumEntry(books_frame, bg=self.bg_color_light, fg="white",
                                    borderwidth=2, highlightthickness=2, insertbackground="white",
                                    highlightbackground=self.bg_color_light)
        ent_pd_charge.grid(column=1, row=6)

        def save_book(e):
            book_name = ent_name.get()
            author = ent_auth.get()
            qty = ent_qty.get()
            status = "FRESH"
            fixed_charge = ent_fix_charge.get()
            pd_charge = ent_pd_charge.get()
            query = """
            INSERT INTO Books
            (book_name, author, qty, status,fixed_charge,per_day_charge)
            VALUES
            ('{}','{}',{},'{}',{},{});
            """.format(book_name, author, qty, status, fixed_charge, pd_charge)

            self.my_cursor.execute(query)
            self.con_obj.commit()
            self.books_page()

        img = Image.open("images/btn_save.png")
        img = img.resize((156, 45), Image.ANTIALIAS)
        self.save_img = ImageTk.PhotoImage(img)

        btn_save = Label(self.frame, image=self.save_img, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                         bd=0)
        btn_save.place(relx=0.8, rely=0.5, anchor="center")
        btn_save.bind("<Button-1>", save_book)

    def delete_book(self, book_id):
        query = "DELETE FROM books WHERE book_id = {};".format(book_id)
        self.my_cursor.execute(query)
        print("Book Deleted")
        self.books_page()

    def edit_book(self, brow):
        def back(e):
            self.books_page()

        for widget in self.frame.winfo_children():
            widget.destroy()

        img = Image.open("images/btn_back.png")
        img = img.resize((98, 32), Image.ANTIALIAS)
        self.img_back = ImageTk.PhotoImage(img)
        btn_back = Label(self.frame, image=self.img_back, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                         bd=0)
        btn_back.place(relx=0.1, rely=0.1, anchor="w")
        btn_back.bind("<Button-1>", back)

        Label(self.frame, text="Edit Book {}".format(brow["book_id"]), bg=self.bg_color, fg="white", font=("Arial", 24)
              ).place(relx=0.5, rely=0.1, anchor="center")

        books_frame = Frame(self.frame, bg=self.bg_color)
        books_frame.place(relx=0.1, rely=0.2, anchor="nw")

        Label(books_frame, text="Book Name", bg=self.bg_color, fg="white").grid(column=0, row=1, sticky="W")
        ent_name = Entry(books_frame, bg=self.bg_color_light, fg="white",
                         borderwidth=2, highlightthickness=2, insertbackground="white",
                         highlightbackground=self.bg_color_light)
        ent_name.insert(0, brow["book_name"])
        ent_name.grid(column=1, row=1)

        Label(books_frame, text="Author", bg=self.bg_color, fg="white").grid(column=0, row=2, sticky="W")
        ent_auth = Entry(books_frame, bg=self.bg_color_light, fg="white",
                         borderwidth=2, highlightthickness=2, insertbackground="white",
                         highlightbackground=self.bg_color_light)
        ent_auth.insert(0, brow["author"])
        ent_auth.grid(column=1, row=2)

        Label(books_frame, text="Quantity", bg=self.bg_color, fg="white").grid(column=0, row=3, sticky="W")
        ent_qty = Entry(books_frame, bg=self.bg_color_light, fg="white",
                        borderwidth=2, highlightthickness=2, insertbackground="white",
                        highlightbackground=self.bg_color_light)
        ent_qty.insert(0, brow["qty"])
        ent_qty.grid(column=1, row=3)

        Label(books_frame, text="Status", bg=self.bg_color, fg="white").grid(column=0, row=4, sticky="W")
        ent_stat = Entry(books_frame, bg=self.bg_color_light, fg="white",
                         borderwidth=2, highlightthickness=2, insertbackground="white",
                         highlightbackground=self.bg_color_light)
        ent_stat.insert(0, brow["status"])
        ent_stat.grid(column=1, row=4)

        Label(books_frame, text="Borrowing Charges", font=("Courier", 16), bg=self.bg_color, fg="white"
              ).grid(column=0, row=5, sticky="W", columnspan=2, pady=10)

        Label(books_frame, text="Fixed Charge", bg=self.bg_color, fg="white").grid(column=0, row=6, sticky="W")
        ent_fix_charge = ew.NumEntry(books_frame, bg=self.bg_color_light, fg="white",
                                     borderwidth=2, highlightthickness=2, insertbackground="white",
                                     highlightbackground=self.bg_color_light)
        ent_fix_charge.insert(0, brow["fixed_charge"])
        ent_fix_charge.grid(column=1, row=6)

        Label(books_frame, text="Per Day Charge", bg=self.bg_color, fg="white").grid(column=0, row=7, sticky="W")
        ent_pd_charge = ew.NumEntry(books_frame, bg=self.bg_color_light, fg="white",
                                    borderwidth=2, highlightthickness=2, insertbackground="white",
                                    highlightbackground=self.bg_color_light)
        ent_pd_charge.insert(0, brow["per_day_charge"])
        ent_pd_charge.grid(column=1, row=7)

        def save_changes(e):
            book_name = ent_name.get()
            author = ent_auth.get()
            qty = ent_qty.get()
            status = ent_stat.get()
            fix_charge = ent_fix_charge.get()
            pd_charge = ent_pd_charge.get()

            query = """UPDATE books
            SET book_name='{}', author='{}', qty={},status='{}',fixed_charge={},per_day_charge={} WHERE book_id={}""".format(
                book_name, author, qty, status, fix_charge, pd_charge, brow["book_id"])
            print(query)

            self.my_cursor.execute(query)
            print("Book Updated")
            self.books_page()

        img = Image.open("images/btn_save_changes.png")
        img = img.resize((185, 45), Image.ANTIALIAS)
        self.save_changes_img = ImageTk.PhotoImage(img)

        btn_save_changes = Label(self.frame, image=self.save_changes_img, borderwidth=0, bg=self.bg_color,
                                 highlightthickness=0, bd=0)
        btn_save_changes.place(relx=0.8, rely=0.6, anchor="center")
        btn_save_changes.bind("<Button-1>", save_changes)

    def students_page(self):
        def show_home(e):
            self.show_home()

        def add_student(e):
            self.add_student()

        def export_data(e):
            save_as_file = filedialog.asksaveasfile(mode="w", defaultextension='.csv')
            csv_writer = csv.writer(save_as_file)
            csv_writer.writerow(["Student ID", "Roll No", "Name", "Class & Section", "Status"])
            for row in data:
                vals = row.values()
                print(vals)
                csv_writer.writerow(vals)
            save_as_file.close()

        for widget in self.frame.winfo_children():
            widget.destroy()

        img = Image.open("images/btn_back.png")
        img = img.resize((98, 32), Image.ANTIALIAS)
        self.img_back = ImageTk.PhotoImage(img)
        btn_back = Label(self.frame, image=self.img_back, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                         bd=0)
        btn_back.place(relx=0.1, rely=0.1, anchor="w")
        btn_back.bind("<Button-1>", show_home)

        img = Image.open("images/btn_add_student.png")
        img = img.resize((183, 45), Image.ANTIALIAS)
        self.img_as = ImageTk.PhotoImage(img)
        btn_as = Label(self.frame, image=self.img_as, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                       bd=0)
        btn_as.place(relx=0.9, rely=0.1, anchor="e")
        btn_as.bind("<Button-1>", add_student)

        title = Label(self.frame, text="Students", bg=self.bg_color, fg="white", font=("Arial", 24))
        title.place(relx=0.1, rely=0.2, anchor="w")

        students_frame = Frame(self.frame, bg=self.bg_color)
        students_frame.place(relx=0.1, rely=0.3, anchor="nw")

        query = "SELECT * FROM Students;"
        self.my_cursor.execute(query)
        self.student_row(b_frame=students_frame, nrow=0, font='Helvetica 18 bold',
                         data={"student_id": "Student ID", "roll_no": "Roll No.", "name": "Name",
                               "class_sect": "Class & Section", "status": "Status"},
                         editable=False, bg=self.bg_color)
        data = self.my_cursor.fetchall()

        img = Image.open("images/icon_delete.png")
        img = img.resize((30, 30), Image.ANTIALIAS)
        self.img_del = ImageTk.PhotoImage(img)

        img = Image.open("images/icon_edit.png")
        img = img.resize((30, 30), Image.ANTIALIAS)
        self.img_edit = ImageTk.PhotoImage(img)

        for i in range(len(data)):
            self.student_row(students_frame, i + 1, font='Helvetica 14', data=data[i])
        if not len(data):
            title = Label(self.frame, text="No Data Available", bg=self.bg_color, fg="white", font=("Arial", 14))
            title.place(relx=0.5, rely=0.4, anchor="center")

        img = Image.open("images/btn_export.png")
        img = img.resize((183, 45), Image.ANTIALIAS)
        self.img_export = ImageTk.PhotoImage(img)
        btn_export = Label(self.frame, image=self.img_export, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                           bd=0)
        btn_export.place(relx=0.9, rely=0.9, anchor="e")
        btn_export.bind("<Button-1>", export_data)

    def student_row(self, b_frame, nrow, font, data, editable=True, bg=bg_color):
        def del_stu(e):
            self.delete_student(data["student_id"])

        def ed_stu(e):
            self.edit_student(data)

        Frame(b_frame, bg=bg).grid(column=0, row=nrow, columnspan=6)

        Label(b_frame, text=data["student_id"], font=font, bg=bg, fg="white").grid(column=0, row=nrow)
        Label(b_frame, text=data["roll_no"], font=font, bg=bg, fg="white").grid(column=1, row=nrow)
        Label(b_frame, text=data["name"], font=font, bg=bg, fg="white").grid(column=2, row=nrow)
        Label(b_frame, text=data["class_sect"], font=font, bg=bg, fg="white").grid(column=3, row=nrow)
        Label(b_frame, text=data["status"], font=font, bg=bg, fg="white").grid(column=4, row=nrow)
        if editable:
            btn_del = Label(b_frame, image=self.img_del, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                            bd=0)
            btn_del.grid(column=5, row=nrow)
            btn_del.bind("<Button-1>", del_stu)

            btn_edit = Label(b_frame, image=self.img_edit, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                             bd=0)
            btn_edit.grid(column=6, row=nrow)
            btn_edit.bind("<Button-1>", ed_stu)

    def add_student(self):
        def back(e):
            self.students_page()

        for widget in self.frame.winfo_children():
            widget.destroy()

        img = Image.open("images/btn_back.png")
        img = img.resize((98, 32), Image.ANTIALIAS)
        self.img_back = ImageTk.PhotoImage(img)
        btn_back = Label(self.frame, image=self.img_back, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                         bd=0)
        btn_back.place(relx=0.1, rely=0.1, anchor="w")
        btn_back.bind("<Button-1>", back)

        title = Label(self.frame, text="Add Student", bg=self.bg_color, fg="white", font=("Arial", 24))
        title.place(relx=0.5, rely=0.1, anchor="center")

        students_frame = Frame(self.frame, bg=self.bg_color)
        students_frame.place(relx=0.1, rely=0.2, anchor="nw")

        Label(students_frame, text="Roll No.", bg=self.bg_color, fg="white").grid(column=0, row=1, sticky="W")
        ent_roll_no = ew.NumEntry(students_frame, bg=self.bg_color_light, fg="white", borderwidth=2,
                                  highlightthickness=2, insertbackground="white",
                                  highlightbackground=self.bg_color_light)
        ent_roll_no.grid(column=1, row=1)

        Label(students_frame, text="Name", bg=self.bg_color, fg="white").grid(column=0, row=2, sticky="W")
        ent_name = Entry(students_frame, bg=self.bg_color_light, fg="white", borderwidth=2, highlightthickness=2,
                         insertbackground="white", highlightbackground=self.bg_color_light)
        ent_name.grid(column=1, row=2)

        Label(students_frame, text="Class & Section", bg=self.bg_color, fg="white").grid(column=0, row=3, sticky="W")
        ent_class_sect = Entry(students_frame, bg=self.bg_color_light, fg="white",
                               borderwidth=2, highlightthickness=2, insertbackground="white",
                               highlightbackground=self.bg_color_light)
        ent_class_sect.grid(column=1, row=3)

        def save_student(e):
            rno = ent_roll_no.get()
            name = ent_name.get()
            class_sect = ent_class_sect.get()
            status = "FRESH"
            query = """
            INSERT INTO Students
            (roll_no, name, class_sect, status)
            VALUES
            ({},'{}','{}','{}');
            """.format(rno, name, class_sect, status)

            self.my_cursor.execute(query)
            self.con_obj.commit()
            self.students_page()

        img = Image.open("images/btn_save_student.png")
        img = img.resize((185, 45), Image.ANTIALIAS)
        self.save_img = ImageTk.PhotoImage(img)

        btn_save = Label(self.frame, image=self.save_img, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                         bd=0)
        btn_save.place(relx=0.8, rely=0.4, anchor="center")
        btn_save.bind("<Button-1>", save_student)

    def delete_student(self, stu_id):
        query = "DELETE FROM students WHERE student_id = {};".format(stu_id)
        self.my_cursor.execute(query)
        print("Student Deleted")
        self.students_page()

    def edit_student(self, brow):
        def back(e):
            self.students_page()

        for widget in self.frame.winfo_children():
            widget.destroy()

        img = Image.open("images/btn_back.png")
        img = img.resize((98, 32), Image.ANTIALIAS)
        self.img_back = ImageTk.PhotoImage(img)
        btn_back = Label(self.frame, image=self.img_back, borderwidth=0, bg=self.bg_color, highlightthickness=0, bd=0)
        btn_back.place(relx=0.1, rely=0.1, anchor="w")
        btn_back.bind("<Button-1>", back)

        Label(self.frame, text="Edit Student {}".format(brow["student_id"]), bg=self.bg_color, fg="white",
              font=("Arial", 24)).place(relx=0.5, rely=0.1, anchor="center")

        students_frame = Frame(self.frame, bg=self.bg_color)
        students_frame.place(relx=0.1, rely=0.2, anchor="nw")

        Label(students_frame, text="Roll No", bg=self.bg_color, fg="white").grid(column=0, row=1, sticky="W")
        ent_rno = Entry(students_frame, bg=self.bg_color_light, fg="white", borderwidth=2, highlightthickness=2,
                        insertbackground="white", highlightbackground=self.bg_color_light)
        ent_rno.insert(0, brow["roll_no"])
        ent_rno.grid(column=1, row=1)

        Label(students_frame, text="Name", bg=self.bg_color, fg="white").grid(column=0, row=2, sticky="W")
        ent_name = Entry(students_frame, bg=self.bg_color_light, fg="white", borderwidth=2, highlightthickness=2,
                         insertbackground="white", highlightbackground=self.bg_color_light)
        ent_name.insert(0, brow["name"])
        ent_name.grid(column=1, row=2)

        Label(students_frame, text="Class & Section", bg=self.bg_color, fg="white").grid(column=0, row=3, sticky="W")
        ent_class_sect = Entry(students_frame, bg=self.bg_color_light, fg="white", borderwidth=2, highlightthickness=2,
                               insertbackground="white", highlightbackground=self.bg_color_light)
        ent_class_sect.insert(0, brow["class_sect"])
        ent_class_sect.grid(column=1, row=3)

        Label(students_frame, text="Status", bg=self.bg_color, fg="white").grid(column=0, row=4, sticky="W")
        ent_stat = Entry(students_frame, bg=self.bg_color_light, fg="white", borderwidth=2, highlightthickness=2,
                         insertbackground="white", highlightbackground=self.bg_color_light)
        ent_stat.insert(0, brow["status"])
        ent_stat.grid(column=1, row=4)

        def save_changes(e):
            rno = ent_rno.get()
            name = ent_name.get()
            class_sect = ent_class_sect.get()
            status = ent_stat.get()

            query = """UPDATE Students
            SET roll_no={}, name='{}', class_sect='{}',status='{}' WHERE student_id={}""".format(
                rno, name, class_sect, status, brow["student_id"])
            print(query)

            self.my_cursor.execute(query)
            print("Student Updated")
            self.students_page()

        img = Image.open("images/btn_save_changes.png")
        img = img.resize((185, 45), Image.ANTIALIAS)
        self.save_changes_img = ImageTk.PhotoImage(img)

        btn_save_changes = Label(self.frame, image=self.save_changes_img, borderwidth=0, bg=self.bg_color,
                                 highlightthickness=0, bd=0)
        btn_save_changes.place(relx=0.8, rely=0.6, anchor="center")
        btn_save_changes.bind("<Button-1>", save_changes)

    def borrowing_history(self):
        def back(e):
            self.show_home()

        for widget in self.frame.winfo_children():
            widget.destroy()

        img = Image.open("images/btn_back.png")
        img = img.resize((98, 32), Image.ANTIALIAS)
        self.img_back = ImageTk.PhotoImage(img)
        btn_back = Label(self.frame, image=self.img_back, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                         bd=0)
        btn_back.place(relx=0.1, rely=0.1, anchor="w")
        btn_back.bind("<Button-1>", back)

        Label(self.frame, text="Borrowing History", bg=self.bg_color, font=("Arial", 20),
              fg="white").place(relx=0.5, rely=0.1, anchor="center")

        frame_bors = Frame(self.frame, bg=self.bg_color)
        frame_bors.place(relx=0.1, rely=0.2, anchor="nw")
        query = "SELECT * FROM Borrows;"
        self.my_cursor.execute(query)
        self.print_history_row(
            {"borrow_id": "Borrow ID", "student_id": "Student ID", "book_id": "Book ID", "borrow_date": "Borrow Date",
             "return_date": "Return Date", "status": "Status", "cost": "Cost"}, frame_bors, 0)

        bdata = self.my_cursor.fetchall()
        for row in range(len(bdata)):
            self.print_history_row(bdata[row], frame_bors, row + 1)

    def print_history_row(self, row, frame, n):
        Label(frame, text=row["borrow_id"], bg=self.bg_color, fg="white").grid(column=0, row=n)
        Label(frame, text=row["student_id"], bg=self.bg_color, fg="white").grid(column=1, row=n)
        Label(frame, text=row["book_id"], bg=self.bg_color, fg="white").grid(column=2, row=n)
        Label(frame, text=row["borrow_date"], bg=self.bg_color, fg="white").grid(column=3, row=n)
        Label(frame, text=row["return_date"], bg=self.bg_color, fg="white").grid(column=4, row=n)
        Label(frame, text=row["status"], bg=self.bg_color, fg="white").grid(column=5, row=n)
        Label(frame, text=row["cost"], bg=self.bg_color, fg="white").grid(column=6, row=n)
