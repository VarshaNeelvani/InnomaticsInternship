from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

books = [
    {"id": 1, "title": "The Power of Positive Thinking", "author": "Norman Vincent Peale", "genre": "Self-Help", "is_available": True},
    {"id": 2, "title": "The Greatness Guide", "author": "Robin Sharma", "genre": "Self-Help", "is_available": True},
    {"id": 3, "title": "The Subtle Art of Not Giving a F*ck", "author": "Mark Manson", "genre": "Self-Help", "is_available": True},
    {"id": 4, "title": "You Are a Badass", "author": "Jen Sincero", "genre": "Self-Help", "is_available": True},
    {"id": 5, "title": "101 Essays That Will Change the Way You Think", "author": "Brianna Wiest", "genre": "Psychology", "is_available": True},
    {"id": 6, "title": "The Art of Not Overthinking", "author": "Shaurya Kapoor", "genre": "Psychology", "is_available": True},
    {"id": 7, "title": "Buy Yourself the Damn Flowers", "author": "Tam Kaur", "genre": "Self-Help", "is_available": True},
    {"id": 8, "title": "Girls That Invest", "author": "Simran Kaur", "genre": "Science", "is_available": True},
    {"id": 9, "title": "The Courage to Be Disliked", "author": "Ichiro Kishimi & Fumitake Koga", "genre": "Psychology", "is_available": True},
    {"id": 10, "title": "How to Win Friends and Influence People", "author": "Dale Carnegie", "genre": "Self-Help", "is_available": True},
    {"id": 11, "title": "Calm the F*ck Down", "author": "Sarah Knight & Sasha O'Hara", "genre": "Self-Help", "is_available": True},
    {"id": 12, "title": "Good Vibes, Good Life", "author": "Vex King", "genre": "Self-Help", "is_available": True},
    {"id": 13, "title": "The Magic of Thinking Big", "author": "David J. Schwartz", "genre": "Self-Help", "is_available": True},
    {"id": 14, "title": "Talk Like TED", "author": "Carmine Gallo", "genre": "Science", "is_available": True},
    {"id": 15, "title": "The Confidence Gap", "author": "Russ Harris", "genre": "Psychology", "is_available": True},
    {"id": 16, "title": "Atomic Habits", "author": "James Clear", "genre": "Self-Help", "is_available": True},
    {"id": 17, "title": "Ikigai", "author": "Hector Garcia & Francesc Miralles", "genre": "Self-Help", "is_available": True},
    {"id": 18, "title": "It Ends With Us", "author": "Colleen Hoover", "genre": "Fiction", "is_available": True},
    {"id": 19, "title": "It Starts With Us", "author": "Colleen Hoover", "genre": "Fiction", "is_available": True},
    {"id": 20, "title": "The Spanish Love Deception", "author": "Elena Armas", "genre": "Romance", "is_available": True},
    {"id": 21, "title": "The American Roommate Experiment", "author": "Elena Armas", "genre": "Romance", "is_available": True},
    {"id": 22, "title": "The Fine Print", "author": "Lauren Asher", "genre": "Romance", "is_available": True},
    {"id": 23, "title": "Icebreaker", "author": "Hannah Grace", "genre": "Romance", "is_available": True},
    {"id": 24, "title": "Dating Dr. Dil", "author": "Nisha Sharma", "genre": "Romance", "is_available": True},
    {"id": 25, "title": "Norwegian Wood", "author": "Haruki Murakami", "genre": "Fiction", "is_available": True},
    {"id": 26, "title": "Better Than the Movies", "author": "Lynn Painter", "genre": "Romance", "is_available": True},
    {"id": 27, "title": "Tuesdays with Morrie", "author": "Mitch Albom", "genre": "Fiction", "is_available": True},
    {"id": 28, "title": "King of Wrath", "author": "Ana Huang", "genre": "Romance", "is_available": True},
    {"id": 29, "title": "Shatter Me", "author": "Tahereh Mafi", "genre": "Fiction", "is_available": True},
    {"id": 30, "title": "The Love Hypothesis", "author": "Ali Hazelwood", "genre": "Romance", "is_available": True},
    {"id": 31, "title": "The Midnight Library", "author": "Matt Haig", "genre": "Fiction", "is_available": True},
    {"id": 32, "title": "Days at the Morisaki Bookshop", "author": "Satoshi Yagisawa", "genre": "Fiction", "is_available": True},
    {"id": 33, "title": "The Burnout", "author": "Sophie Kinsella", "genre": "Fiction", "is_available": True},
    {"id": 34, "title": "King of Pride", "author": "Ana Huang", "genre": "Romance", "is_available": True},
    {"id": 35, "title": "King of Greed", "author": "Ana Huang", "genre": "Romance", "is_available": True},
    {"id": 36, "title": "King of Sloth", "author": "Ana Huang", "genre": "Romance", "is_available": True},
    {"id": 37, "title": "Once Upon a Broken Heart", "author": "Stephanie Garber", "genre": "Fiction", "is_available": True},
    {"id": 38, "title": "The Ballad of Never After", "author": "Stephanie Garber", "genre": "Fiction", "is_available": True},
    {"id": 39, "title": "A Curse for True Love", "author": "Stephanie Garber", "genre": "Fiction", "is_available": True},
    {"id": 40, "title": "The Mirror of Infinite Endings", "author": "Stephanie Garber", "genre": "Fiction", "is_available": True},
    {"id": 41, "title": "Mile High", "author": "Liz Tomforde", "genre": "Romance", "is_available": True},
    {"id": 42, "title": "The Right Move", "author": "Liz Tomforde", "genre": "Romance", "is_available": True},
    {"id": 43, "title": "Caught Up", "author": "Liz Tomforde", "genre": "Romance", "is_available": True},
    {"id": 44, "title": "Play Along", "author": "Liz Tomforde", "genre": "Romance", "is_available": True},
    {"id": 45, "title": "Rewind It Back", "author": "Liz Tomforde", "genre": "Romance", "is_available": True},
    {"id": 46, "title": "Kill Joy", "author": "Holly Jackson", "genre": "Fiction", "is_available": True},
    {"id": 47, "title": "A Good Girl's Guide to Murder", "author": "Holly Jackson", "genre": "Fiction", "is_available": True},
    {"id": 48, "title": "Good Girl, Bad Blood", "author": "Holly Jackson", "genre": "Fiction", "is_available": True},
    {"id": 49, "title": "As Good As Dead", "author": "Holly Jackson", "genre": "Fiction", "is_available": True},
    {"id": 50, "title": "Terms and Conditions", "author": "Lauren Asher", "genre": "Romance", "is_available": True}
]

borrow_records = []
record_counter = 1

queue = []

class BorrowRequest(BaseModel):
    member_name: str = Field(min_length=2)
    member_id: str = Field(min_length=4)
    book_id: int = Field(gt=0)
    borrow_days: int = Field(gt=0, le=60)
    member_type: str = "regular"

class NewBook(BaseModel):
    title: str = Field(min_length=2)
    author: str = Field(min_length=2)
    genre: str = Field(min_length=2)
    is_available: bool = True

def find_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    return None

def calculate_due_date(days: int, member_type: str):
    if member_type == "premium":
        max_days = 60
    else:
        max_days = 30

    days = min(days, max_days)
    return f"Return by: Day {15 + days}"

def filter_books_logic(genre, author, is_available):
    result = books

    if genre is not None:
        result = [b for b in result if b["genre"].lower() == genre.lower()]

    if author is not None:
        result = [b for b in result if b["author"].lower() == author.lower()]

    if is_available is not None:
        result = [b for b in result if b["is_available"] == is_available]

    return result

@app.get("/")
def home():
    return {"message": "Welcome to City Public Library"}

@app.get("/books")
def get_books():
    available_books = [b for b in books if b["is_available"]]

    return {
        "total": len(books),
        "available_count": len(available_books),
        "books": books
    }

@app.get("/borrow-records")
def get_borrow_records():
    return {
        "total": len(borrow_records),
        "records": borrow_records
    }

@app.get("/books/summary")
def books_summary():
    genre_count = {}

    for book in books:
        genre = book["genre"]
        genre_count[genre] = genre_count.get(genre, 0) + 1

    available = len([b for b in books if b["is_available"]])

    return {
        "total_books": len(books),
        "available": available,
        "borrowed": len(books) - available,
        "genre_breakdown": genre_count
    }

@app.post("/borrow")
def borrow_book(req: BorrowRequest):
    global record_counter

    book = find_book(req.book_id)

    if not book:
        return {"error": "Book not found"}

    if not book["is_available"]:
        return {"error": "Book already borrowed"}

    book["is_available"] = False

    record = {
        "record_id": record_counter,
        "member_name": req.member_name,
        "book_id": req.book_id,
        "due_date": calculate_due_date(req.borrow_days, req.member_type)
    }

    borrow_records.append(record)
    record_counter += 1

    return record

@app.get("/books/filter")
def filter_books(
    genre: Optional[str] = None,
    author: Optional[str] = None,
    is_available: Optional[bool] = None
):
    result = filter_books_logic(genre, author, is_available)

    return {
        "count": len(result),
        "books": result
    }

from fastapi import status

@app.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(book: NewBook):
    for b in books:
        if b["title"].lower() == book.title.lower():
            return {"error": "Duplicate title"}

    new_book = book.dict()
    new_book["id"] = len(books) + 1

    books.append(new_book)

    return new_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    book = find_book(book_id)

    if not book:
        return {"error": "Book not found"}

    books.remove(book)

    return {"message": f"{book['title']} deleted successfully"}

@app.put("/books/{book_id}")
def update_book(
    book_id: int,
    genre: Optional[str] = None,
    is_available: Optional[bool] = None
):
    book = find_book(book_id)

    if not book:
        return {"error": "Book not found"}

    if genre is not None:
        book["genre"] = genre

    if is_available is not None:
        book["is_available"] = is_available

    return book

@app.post("/queue/add")
def add_to_queue(member_name: str, book_id: int):

    book = find_book(book_id)

    if not book:
        return {"error": "Book not found"}

    if book["is_available"]:
        return {"error": "Book is available, no need for queue"}

    queue.append({
        "member_name": member_name,
        "book_id": book_id
    })

    return {"message": "Added to queue"}

@app.get("/queue")
def get_queue():
    return queue

@app.post("/return/{book_id}")
def return_book(book_id: int):
    global record_counter

    book = find_book(book_id)

    if not book:
        return {"error": "Book not found"}

    book["is_available"] = True

    for q in queue:
        if q["book_id"] == book_id:

            queue.remove(q)

            new_record = {
                "record_id": record_counter,
                "member_name": q["member_name"],
                "book_id": book_id,
                "due_date": calculate_due_date(7, "regular")
            }

            borrow_records.append(new_record)
            record_counter += 1

            book["is_available"] = False

            return {
                "message": "returned and re-assigned",
                "record": new_record
            }

    return {"message": "returned and available"}

@app.get("/books/search")
def search_books(keyword: str):

    result = [
        b for b in books
        if keyword.lower() in b["title"].lower()
        or keyword.lower() in b["author"].lower()
    ]

    return {
        "total_found": len(result),
        "results": result
    }

@app.get("/books/sort")
def sort_books(sort_by: str = "title", order: str = "asc"):

    if sort_by not in ["title", "author", "genre"]:
        return {"error": "Invalid sort field"}

    if order not in ["asc", "desc"]:
        return {"error": "Invalid order"}

    sorted_books = sorted(books, key=lambda x: x[sort_by])

    if order == "desc":
        sorted_books.reverse()

    return {
        "sort_by": sort_by,
        "order": order,
        "books": sorted_books
    }

@app.get("/books/page")
def paginate_books(page: int = 1, limit: int = 3):

    start = (page - 1) * limit
    end = start + limit

    total = len(books)
    total_pages = (total + limit - 1) // limit

    return {
        "total": total,
        "total_pages": total_pages,
        "current_page": page,
        "limit": limit,
        "books": books[start:end]
    }

@app.get("/borrow-records/search")
def search_records(member_name: str):

    result = [
        r for r in borrow_records
        if member_name.lower() in r["member_name"].lower()
    ]

    return {
        "count": len(result),
        "results": result
    }

@app.get("/borrow-records/page")
def paginate_records(page: int = 1, limit: int = 2):

    start = (page - 1) * limit
    end = start + limit

    total = len(borrow_records)
    total_pages = (total + limit - 1) // limit

    return {
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "records": borrow_records[start:end]
    }

@app.get("/books/browse")
def browse_books(
    keyword: str = None,
    sort_by: str = "title",
    order: str = "asc",
    page: int = 1,
    limit: int = 3
):

    result = books

    # filter (search)
    if keyword:
        result = [
            b for b in result
            if keyword.lower() in b["title"].lower()
            or keyword.lower() in b["author"].lower()
        ]

    # sort
    result = sorted(result, key=lambda x: x[sort_by])

    if order == "desc":
        result.reverse()

    # pagination
    total = len(result)
    start = (page - 1) * limit
    end = start + limit

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total": total,
        "results": result[start:end]
    }

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book

    return {"error": "Book not found"}