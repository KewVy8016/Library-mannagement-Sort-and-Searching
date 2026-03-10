class Book:
    def __init__(self, isbn, title, author, publish_year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publish_year = publish_year
    
    def __str__(self):
        return f"ISBN: {self.isbn} | ชื่อ: {self.title} | ผู้แต่ง: {self.author} | ปี: {self.publish_year}"
    
    def to_dict(self):
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'publish_year': self.publish_year
        }
