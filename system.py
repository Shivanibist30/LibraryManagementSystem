    #-----------------------MODULE AND PACKAGE------------------------------------
import mysql.connector as connector
from datetime import date, datetime
from tkinter import *
import tkinter as tk
import tkinter.messagebox as tmsg
class main:
    def __init__(self):
        self.conn=connector.connect(host='localhost',user='root',password='@shivani123',database='library_Management')
        self.mycursor=self.conn.cursor(buffered=True)
    #----------------------------ADMIN MENU FUNCTIONS----------------------------------
    def insert_book(self,bookid,bookname): #done
        conn=self.conn
        mycursor=self.mycursor
        mycursor.execute(f'select bookid from booklist where bookid={bookid}')
        flag=mycursor.fetchall()
        if flag:
            tmsg.showerror('Failed','Book Already exist')
        else:
            mycursor.execute(f"insert into booklist values({bookid},'{bookname}')")
            conn.commit()
            tmsg.showinfo('successful','Book added successfully')
    def delete_book(self,bookid):   #done
        conn=self.conn
        mycursor=self.mycursor
        mycursor.execute(f'select bookid from booklist where bookid={bookid}')
        flag=mycursor.fetchall()
        if flag:
            mycursor.execute(f"delete from booklist where bookid={bookid}")
            conn.commit()
            tmsg.showinfo('Successful','Book removed successfully')
        else:
            tmsg.showerror('Failed','Book does not exist')
    def add_librarian(self,teacherid,name,position):
        conn=self.conn
        mycursor=self.mycursor 
        mycursor.execute(f"select teacher_id from teachernames where teacher_id='{teacherid}'")
        flag=mycursor.fetchall()
        if flag:
            tmsg.showerror('Failed','Librarian already exist')    
        else:
            mycursor.execute(f"insert into teachernames values('{teacherid}','{name}','{position}')")
            conn.commit()
            tmsg.showinfo('successful','Librarian Added Successfully')
    def remove_librarian(self,teacherid):
        conn=self.conn
        mycursor=self.mycursor
        mycursor.execute(f'select name from teachernames where teacher_id={teacherid}')
        flag=mycursor.fetchall()
        if flag:
            mycursor.execute(f"delete from teachernames where teacher_id='{teacherid}'")
            conn.commit()
            tmsg.showinfo('successful','Librarian removed successfully') 
        else:
            tmsg.showerror('Failed','Librarian Does Not Exist')   #ADMIN FUNCTION BLOCK ENDS HERE                                                               
    #-----------------------------STAFF MENU FUNCTIONS--------------------------------
    def issue_book(self,bookid,studentid):
        conn=self.conn
        mycursor=self.mycursor
        mycursor.execute(f'select bookid from issue_register where bookid={bookid}')
        cnt=mycursor.fetchone()
        if cnt:
            tmsg.showerror('Failed','Book Not Available')
            exit()
        else:
            mycursor.execute(f'select name from booklist where bookid={bookid}')
            book=mycursor.fetchone()
            for i in book:
                bookname=i
            mycursor.execute(f'select name from studentnames where student_id={studentid}')
            counti=mycursor.fetchone()
            for i in counti:
                name=i
            if name:
                mycursor.execute(f"insert into issue_register values('{studentid}','{name}','{bookname}',CURDATE(),{bookid})")
                conn.commit()
                tmsg.showinfo('Successful','book issued successfully')
            else:
                tmsg.showerror('Failed','student not registered')
                exit()
    def return_book(self,bookid,student_id):
        conn=self.conn
        mycursor=self.mycursor
        mycursor.execute(f'select name from booklist where bookid={bookid}')
        book=mycursor.fetchone()
        for i in book:
            bookname=i
        mycursor.execute(f'select name from studentnames where student_id={student_id}')
        counti=mycursor.fetchone()
        for i in counti:
            name=i
        mycursor.execute(f'select issuedate from issue_register where bookid={bookid}')
        count=mycursor.fetchone()
        if count:
            for i in count:
                issuedate=i   
            returndate=date.today()
            days=(returndate-issuedate).days
            if days>7 and days<30:
                fine=days*5
            elif days>30 and days<180:
                fine=100
            elif days>180 and days<365:
                fine=500
            elif days>365:
                fine=1000
            else:
                fine=0
            mycursor.execute(f'insert into return_register values("{student_id}","{name}","{bookname}",curdate(),{fine},{bookid})')
            conn.commit()
            mycursor.execute(f'delete from issue_register where bookid={bookid} ')
            conn.commit()
            tmsg.showinfo('success','book returned successfully')
        else:
            tmsg.showinfo('Failed','no Book issued on this id')  
    def add_student(self,studentid,name,branch,semester):
        conn=self.conn
        mycursor=self.mycursor
        mycursor.execute(f'select student_id from studentnames where student_id={studentid}')
        flag=mycursor.fetchall()
        if flag:
            tmsg.showerror('Failed','Student Already Registered')
        else:
            mycursor.execute(f"insert into studentnames values('{studentid}','{name}','{branch}','{semester}')")
            conn.commit()
            tmsg.showinfo('Successful','Student added successfully')
    def remove_students(self,studentid):
        conn=self.conn
        mycursor=self.mycursor
        mycursor.execute(f'select student_id from studentnames where student_id={studentid}')
        flag=mycursor.fetchall()
        if flag:
            total=0
            mycursor.execute(f'select fine from return_register where student_id={studentid}')
            tfine=mycursor.fetchall()
            for i in tfine:
                for j in i:
                    total+=j
            if total:
                tmsg.showerror('ERROR',f'Fine of Rs.{total} is to be paid')
            else:
                mycursor.execute(f'delete from studentnames where student_id={studentid}')
                conn.commit()
                mycursor.execute(f'delete from issue_register where student_id={studentid}')
                conn.commit()
                mycursor.execute(f'delete from return_register where student_id={studentid}')
                conn.commit()
                tmsg.showinfo('Successful','Student deleted succesfully')
        else:
            tmsg.showerror('Failed','Student does not exist')       
        #-----------------STAFF MENU BACKEND FUNCTIONS END HERE------------------------
class GUI(Tk):
    obj=main()
    def __init__(self):
        super().__init__()
    def head(self,root):
        root.geometry('500x400')
        root.resizable(False,False)
        root.title("LIBRARY MANAGEMENT SYSTEM")
        heading=Label(root,text='LIBRARY MANAGEMENT SYSTEM ',font=('times new roman',22,'bold'),background='yellow',relief='sunken')
        heading.pack(fill='x')
    def base(self,root): 
        self.head(root)
        log=Label(window,text='Login as  ',font=('times new roman',30,'bold'),background='light green')
        log.pack(pady=10)
        button1= tk.Button(window, text='ADMIN', bg='black', fg='#469A00',command=self.admin)
        button1.pack(pady=5)
        button2= tk.Button(window, text='STAFF', bg='black', fg='#469A00',command=self.staff)
        button2.pack(pady=5)
        root.mainloop()
    def admin(self):
        root=Toplevel(window)
        root.geometry('700x500')
        root.resizable(False,False)
        root.title("LIBRARY MANAGEMENT SYSTEM")
        heading=Label(root,text='LIBRARY MANAGEMENT SYSTEM ',font=('times new roman',30,'bold'),background='yellow',relief='sunken')
        heading.pack(fill='x')
        log=Label(root,text='ADMIN',font=('times new roman',30,'bold'),background='light green')
        log.pack(pady=10)
        button1= tk.Button(root, text='INSERT A BOOK', bg='black', fg='#469A00',command=self.insertbook)
        button1.pack(pady=5)
        button2= tk.Button(root, text='REMOVE A BOOK', bg='black', fg='#469A00',command=self.deletebook)
        button2.pack(pady=5)
        button3= tk.Button(root, text='ADD LIBRARIAN', bg='black', fg='#469A00',command=self.addlib)
        button3.pack(pady=5)
        button4= tk.Button(root, text='DELETE LIBRARIAN', bg='black', fg='#469A00',command=self.deletelib)
        button4.pack(pady=5)
        button= tk.Button(root, text='EXIT', bg='black', fg='#469A00',command=exit)
        button.pack(pady=5)  
        root.mainloop()
    def staff(self):
        root=Toplevel(window)
        self.head(root)
        log=Label(root,text='STAFF MEMBER',font=('times new roman',30,'bold'),background='light green')
        log.pack(pady=10)
        button1= tk.Button(root, text='ISSUE A BOOK', bg='black', fg='#469A00',command=self.issuebook)
        button1.pack(pady=5)
        button2= tk.Button(root, text='RETURN A BOOK', bg='black', fg='#469A00',command=self.returnbook)
        button2.pack(pady=5)
        button3= tk.Button(root, text='ADD STUDENT', bg='black', fg='#469A00',command=self.addstu)
        button3.pack(pady=5)
        button4= tk.Button(root, text='REMOVE STUDENT', bg='black', fg='#469A00',command=self.remstu)
        button4.pack(pady=5)
        button5= tk.Button(root, text='EXIT', bg='black', fg='#469A00',command=exit)
        button5.pack(pady=5)  
        root.mainloop()
    #------------------------------frames for sub menus of-admin menu--------------------------------
    def bookidname(self):
        obj=main()
        x=self.bookid.get()
        y=self.bookname.get()
        obj.insert_book(x,y)
    def insertbook(self):
        root=Toplevel(window)
        self.head(root)
        log=Label(root,text='insert book',font=('times new roman',24,'bold'),background='light green')
        log.pack(pady=10)
        bid=Label(root,text='BOOK ID ')
        bid.pack()
        self.bookid=IntVar()
        bookentry=Entry(root,textvariable=self.bookid)
        bookentry.pack()
        bname=Label(root,text='BOOK NAME ')  #bookname fetch krna h
        bname.pack()
        self.bookname=StringVar()
        booknameentry=Entry(root,textvariable=self.bookname)
        booknameentry.pack()
        check=tk.Button(root, text='ADD', bg='black', fg='#469A00',command=self.bookidname)
        check.pack()
        root.mainloop()
    def getbookid(self):
        x=f'{self.bookid.get()}'
        obj.delete_book(x)
    def deletebook(self):
        root=Toplevel(window)
        self.head(root)
        log=Label(root,text='DELETE BOOK',font=('times new roman',24,'bold'),background='light green')
        log.pack(pady=10)
        bid=Label(root,text='BOOK ID ')
        bid.pack()
        self.bookid=IntVar()
        bookentry=Entry(root,textvariable=self.bookid)
        bookentry.pack()
        check=tk.Button(root, text='DELETE', bg='black', fg='#469A00',command=self.getbookid)
        check.pack()
        root.mainloop()
    def libadd(self):
        x=f'{self.teacherid.get()}'
        y=f'{self.name.get()}'
        z=f'{self.position.get()}'
        print(x,y,z)
        obj.add_librarian(x,y,z)
    def addlib(self):
        root=Toplevel(window)
        self.head(root)
        log=Label(root,text='insert book',font=('times new roman',24,'bold'),background='light green')
        log.pack(pady=10)
        libid=Label(root,text='LIBRARIAN ID ')
        libid.pack()
        self.teacherid=StringVar()  #input librarian id
        libentry=Entry(root,textvariable=self.teacherid)
        libentry.pack()
        lname=Label(root,text='LIBRARIAN NAME ')
        lname.pack()
        self.name=StringVar() 
        nameentry=Entry(root,textvariable=self.name)
        nameentry.pack()
        lpos=Label(root,text='POSITION ')            
        lpos.pack()
        self.position=StringVar() #input position   
        posentry=Entry(root,textvariable=self.position)
        posentry.pack()
        check=Button(root, text='ADD', bg='black', fg='#469A00',command=self.libadd)
        check.pack()
    def getstaffid(self):
        x=f'{self.teacherid.get()}'
        obj.remove_librarian(x)
    def deletelib(self):
        root=Toplevel(window)
        self.head(root)
        log=Label(root,text='DELETE STAFF',font=('times new roman',24,'bold'),background='light green')
        log.pack(pady=10)
        bid=Label(root,text='STAFF ID ')
        bid.pack()
        self.teacherid=IntVar()
        bookentry=Entry(root,textvariable=self.teacherid)
        bookentry.pack()
        check=tk.Button(root, text='DELETE', bg='black', fg='#469A00',command=self.getstaffid)
        check.pack()
        root.mainloop()
    #--------------------------FRAMES FOR SUBMENU FOR STAFF------------------------------------
    def bookstuid(self):
        obj=main()
        x=f'{self.bookid.get()}'
        y=f'{self.studentid.get()}'
        print(x,y)
        obj.issue_book(x,y)
        
    def issuebook(self):
        root=Toplevel(window)
        self.head(root)
        log=Label(root,text='insert book',font=('times new roman',24,'bold'),background='light green')
        log.pack(pady=10)
        bid=Label(root,text='BOOK ID ')
        bid.pack()
        self.bookid=IntVar()
        bookentry=Entry(root,textvariable=self.bookid)
        bookentry.pack()
        bname=Label(root,text='STUDENT ID ')  #bookname fetch krna h
        bname.pack()
        self.studentid=StringVar()
        booknameentry=Entry(root,textvariable=self.studentid)
        booknameentry.pack()
        check=tk.Button(root, text='ISSUE', bg='black', fg='#469A00',command=self.bookstuid)
        check.pack()
        root.mainloop() 
    def rbookstuid(self):
        obj=main()
        x=f'{self.bookid.get()}'
        y=f'{self.studentid.get()}'
        print(x,y)
        obj.return_book(x,y)
    def returnbook(self):
        root=Toplevel(window)
        self.head(root)
        log=Label(root,text='insert book',font=('times new roman',24,'bold'),background='light green')
        log.pack(pady=10)
        bid=Label(root,text='BOOK ID ')
        bid.pack()
        self.bookid=IntVar()
        bookentry=Entry(root,textvariable=self.bookid)
        bookentry.pack()
        bname=Label(root,text='STUDENT ID ')  #bookname fetch krna h
        bname.pack()
        self.studentid=StringVar()
        booknameentry=Entry(root,textvariable=self.studentid)
        booknameentry.pack()
        check=tk.Button(root, text='RETURN', bg='black', fg='#469A00',command=self.rbookstuid)
        check.pack()
        root.mainloop() 
    def rbookstuid(self):
        obj=main()
        x=f'{self.studentid.get()}'
        y=f'{self.name.get()}'
        z=f'{self.branch.get()}'
        a=f'{self.semester.get()}'
        print(x,y,z,a)
        obj.add_student(x,y,z,a)
    def addstu(self):
        root=Toplevel(window)
        self.head(root)
        log=Label(root,text='insert book',font=('times new roman',24,'bold'),background='light green')
        log.pack(pady=10)
        sid=Label(root,text='STUDENT ID ')
        sid.pack()
        self.studentid=StringVar()
        booknameentry=Entry(root,textvariable=self.studentid)
        booknameentry.pack()
        sname=Label(root,text='NAME ')  #bookname fetch krna h
        sname.pack()
        self.name=StringVar()
        booknameentry=Entry(root,textvariable=self.name)
        booknameentry.pack()
        br=Label(root,text='BRANCH ')  #bookname fetch krna h
        br.pack()
        self.branch=StringVar()
        booknameentry=Entry(root,textvariable=self.branch)
        booknameentry.pack()
        sem=Label(root,text='SEMESTER ')  #bookname fetch krna h
        sem.pack()
        self.semester=IntVar()
        bookentry=Entry(root,textvariable=self.semester)
        bookentry.pack()
        check=tk.Button(root, text='ADD', bg='black', fg='#469A00',command=self.rbookstuid)
        check.pack()
        root.mainloop() 
    def getstuid(self):
        x=f'{self.studentid.get()}'
        obj.remove_students(x)
    def remstu(self):
        root=Toplevel(window)
        self.head(root)
        log=Label(root,text='DELETE STUDENT',font=('times new roman',24,'bold'),background='light green')
        log.pack(pady=10)
        bid=Label(root,text='STUDENT ID ')
        bid.pack()
        self.studentid=IntVar()
        bookentry=Entry(root,textvariable=self.studentid)
        bookentry.pack()
        check=tk.Button(root, text='DELETE', bg='black', fg='#469A00',command=self.getstuid)
        check.pack()
        root.mainloop()
        #-----------------------------DRIVER CODE------------------------------------
obj=main()  #BACKEND CLASS
window=GUI() #FRONTEND CLASS
window.base(window)
window.mainloop()








    

