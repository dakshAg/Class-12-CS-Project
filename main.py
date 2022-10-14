import tkinter
from tkinter import Label, Frame, RAISED, LEFT

import mysql.connector
from PIL import Image, ImageTk

import extra_widgets as ew
from setup import Setup
from admin import Admin
from student import Student


class HomeScreen:
    bg_color = "#1C2833"
    bg_color_light = "#273746"
    blue_box_color = "#2E86C1"
    bright_red = "#ff0000"
    grey = "#44616b"
    admin_en = True
    showing_err = False

    def __init__(self, err=""):
        self.refresh_db()

        self.err = err
        self.root = tkinter.Tk()
        self.w, self.h = self.root.winfo_screenwidth() * 0.7, self.root.winfo_screenheight() * 0.7
        self.root.geometry("%dx%d+0+0" % (self.w, self.h))
        self.root.configure(bg=self.bg_color)
        self.root.title("DigiLib Project by Daksh Agrawal")
        self.create_lbox()
        self.reset_pls()

    def refresh_db(self):
        try:
            db_info = Setup.fetch_db_info()
            self.con_obj = mysql.connector.connect(host="localhost", user=db_info["user"], passwd=db_info["passwd"],
                                                   database=db_info["db"])
            self.my_cursor = self.con_obj.cursor(dictionary=True)
            self.admin_en = True
        except FileNotFoundError:
            self.admin_en = False
        except mysql.connector.errors.ProgrammingError:
            self.admin_en = False

    def reset_pls(self):
        self.show_student_entry()
        self.finish_creation()

    def create_lbox(self):
        canvas = Frame(self.root, bg=self.blue_box_color, bd=0, highlightthickness=0, width=self.w * 0.3, height=self.h)
        canvas.pack(side=LEFT)
        self.show_books_logo(canvas)

    def show_books_logo(self, frame):
        img = Image.open("images/daksh.jpg")
        img = img.resize((106, 114), Image.ANTIALIAS)
        self.bookimg = ImageTk.PhotoImage(img)
        books_img = Label(frame, image=self.bookimg, bg=self.blue_box_color, relief=RAISED, borderwidth=5)
        books_img.place(relx=0.5, rely=0.12, anchor="center")

        Label(frame, text="Daksh Agrawal", bg=self.blue_box_color, fg="white", font=("Arial", 16)
              ).place(relx=0.5, rely=0.25, anchor="center")
        Label(frame, text="Class: XII-A", bg=self.blue_box_color, fg="white").place(relx=0.5, rely=0.3, anchor="center")
        Label(frame, text="Roll No: 4", bg=self.blue_box_color, fg="white").place(relx=0.5, rely=0.35, anchor="center")

        img = Image.open("images/st_pauls.jpg")
        img = img.resize((87, 112), Image.ANTIALIAS)
        self.sch_img = ImageTk.PhotoImage(img)
        books_img = Label(frame, image=self.sch_img, bg=self.blue_box_color, relief=RAISED, borderwidth=3)
        books_img.place(relx=0.5, rely=0.8, anchor="center")

        img = Image.open("images/sanjay_sir.jpeg")
        img = img.resize((78, 112), Image.ANTIALIAS)
        self.sir_img = ImageTk.PhotoImage(img)
        books_img = Label(frame, image=self.sir_img, bg=self.blue_box_color, relief=RAISED, borderwidth=3)
        books_img.place(relx=0.5, rely=0.5, anchor="center")

        Label(frame, text="St. Paul's Sr. Sec. School, Udaipur", bg=self.blue_box_color, fg="white", font=("Arial", 14)
              ).place(relx=0.5, rely=0.95, anchor="center")
        Label(frame, text="Under guidance of\nMr. Sanjay Sharma\nPGT, Computer Sc.", bg=self.blue_box_color, fg="white", font=("Arial", 14)
              ).place(relx=0.5, rely=0.65, anchor="center")

    @staticmethod
    def say_hi():
        print("Hi")

    def show_title(self, frame):
        title = Label(frame, text="DigiLib", bg=self.bg_color, fg="white", font=("Arial", 24))
        title.place(relx=0.5, rely=0.1, anchor="center")

    def finish_creation(self):
        self.root.mainloop()

    def show_student_entry(self, frame=None):
        print("Showing Student Entry")

        def student_login(e):
            if self.admin_en:
                self.check_student_redirect(student_id_entry.get(), student_entry)
            else:
                self.show_error(student_entry, "Please Setup Database First")

        if frame is None:
            student_entry = Frame(self.root, bg=self.bg_color, width=self.w * 0.7, height=self.h)
            student_entry.pack(side=LEFT, expand=True, fill=tkinter.BOTH)
        else:
            for widget in frame.winfo_children():
                widget.destroy()
            student_entry = frame
        self.show_title(student_entry)
        Label(student_entry, text="Enter Student ID", bg=self.bg_color, font=("Arial", 16), fg="white").place(relx=0.5,
                                                                                                              rely=0.25,
                                                                                                              anchor="center")
        student_id_entry = ew.NumEntry(student_entry, font=("Arial", 20), bg=self.bg_color_light, fg="white",
                                       borderwidth=2, highlightthickness=2, insertbackground="white",
                                       highlightbackground=self.bg_color_light, justify='center')
        student_id_entry.place(relx=0.5, rely=0.3, anchor="center")

        img = Image.open("images/btn_submit.png")
        img = img.resize((74, 35), Image.ANTIALIAS)
        self.sub_img = ImageTk.PhotoImage(img)
        btn_submit = Label(student_entry, image=self.sub_img, borderwidth=0, bg=self.bg_color, highlightthickness=0,
                           bd=0)
        btn_submit.place(relx=0.5, rely=0.4, anchor="center")
        btn_submit.bind("<Button-1>", student_login)
        print("show setup")
        self.show_setup_bar(frame=student_entry)

    def check_student_redirect(self, stud, frame):
        query = "SELECT * FROM Students WHERE student_id = {};".format(stud)
        print(query)
        self.my_cursor.execute(query)
        data = self.my_cursor.fetchone()

        if not data:
            self.show_error(frame, "Invalid Student ID")
            return

        Student(data, frame, self.root, self)

    def show_error(self, frame, err):
        Label(frame, text=err, borderwidth=0, highlightthickness=0, bd=0, fg="white", bg="#922B21",
              width=int(frame.winfo_width()), justify="center").place(relx=0.5, rely=0.6, anchor="center")

    def show_setup_bar(self, frame):
        def setup_app(e):
            Setup(frame, self.root, self)

        def admin_app(e):
            Admin(frame, self.root, self)

        print("Show Setup bar was called")
        img = Image.open("images/card_setup.png")
        img = img.resize((200, 200), Image.ANTIALIAS)
        self.photoImg = ImageTk.PhotoImage(img)

        img2 = Image.open("images/card_admin.png")
        img2 = img2.resize((200, 200), Image.ANTIALIAS)
        self.photoImg2 = ImageTk.PhotoImage(img2)

        btn_setup = Label(frame, image=self.photoImg, borderwidth=0, bg=self.bg_color, highlightthickness=0, bd=0)
        btn_setup.place(relx=0.33, rely=0.75, anchor="center")
        btn_setup.bind("<Button-1>", setup_app)

        btn_admin = Label(frame, image=self.photoImg2, borderwidth=0, bg=self.bg_color, highlightthickness=0, bd=0,
                          )
        btn_admin.place(relx=0.66, rely=0.75, anchor="center")
        btn_admin.bind("<Button-1>", admin_app)


hs = HomeScreen()
