class books:
    def __init__(self,title,author,avlbl_copy):
        self.title=title
        self.author=author
        self.avlbl_copy=avlbl_copy
    def __str__(self):
        return f"{self.title} by {self.author}"
    def __repr__(self):
        return self.__str__()
    def borrow(self):
        if self.avlbl_copy>0:
            self.avlbl_copy-=1
            return True
        return False
    def return_books(self):
        self.avlbl_copy+=1

class members:
    def __init__(self,member_id,name):
        self.member_id=member_id
        self.name=name
        self.borrowed_books=[]
    def borrow_limit(self):
        return 0

    def borrow_books(self,book):
        if len(self.borrowed_books)<self.borrow_limit()and book.borrow():
            self.borrowed_books.append(book)
            return True
        return False
    def return_book(self,book):
        if book in self.borrowed_books:
           self.borrowed_books.remove(book)
           return True
        return False
class student(members):
    def borrow_limit(self):
        return 3

class faculty(members):
    def borrow_limit(self):
        return 5

class library():
    def __init__(self):
        self.Books=[]
        self.members={}

    def add_book(self,title,author,copies):
        self.Books.append(books(title,author,copies))
    def register_member(self,member):
        self.members[member.member_id]=member


    def search_book(self,keyword):
        return [book for book in self.Books if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower()]

    def display_borrowed_book(self,member_id):
        member=self.members.get(member_id)
        if member:
            return [(book.title,book.author)for book in member.borrowed_books]

        return []
    def member_info(self,member_id):
        member=self.members.get(member_id)
        if member:
            return {
                "name": member.name,
                "ID":member.member_id,
                "Books":self.display_borrowed_book(member_id)

            }
        return member
x=library()
y=library()
z=library()
r=library()
x.add_book("pathummayude aadu","basheer",50)
y.add_book("hitler","dilfa daniya",100)
z.add_book("mambazham","madhavi kutti",5)
#y.display_borrowed_book("st002")
stud=student('st001',"najiya")
stud2=student("st002","shana")
facul1=faculty("f001","rasheeda")
z.register_member(facul1)
x.register_member(stud)
y.register_member(stud2)
y.search_book("hitler")
book=x.Books[0]
book2=y.Books[0]
book3=z.Books[0]
stud2.borrow_books(book2)
stud.borrow_books(book)
facul1.borrow_books(book3)

print(x.member_info("st001"))
print(y.member_info("st002"))
print(z.member_info("f001"))
print(y.search_book("hitler"))
print(z.display_borrowed_book("f001"))
