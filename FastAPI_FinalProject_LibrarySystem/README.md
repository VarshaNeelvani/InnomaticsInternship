# 📚 Library Book System - FastAPI

## 🚀 Project Overview
This project is a Library Management System built using FastAPI. It allows users to manage books, borrow them, maintain a waiting queue, and perform advanced operations like search, sorting, and pagination.

This project demonstrates all core FastAPI concepts including validation, CRUD operations, helper functions, and multi-step workflows.

---

## 📌 Features

### 📘 Book Management
- View all books
- Get book by ID
- Add new books
- Update book details
- Delete books
- Book summary (genre-wise breakdown)

### 🔄 Borrow System
- Borrow books with validation
- Track borrow records
- Prevent borrowing unavailable books

### ⏳ Queue System
- Add users to queue if book is unavailable
- Auto-assign book when returned

### 🔍 Advanced Functionalities
- Filter books (by genre, author, availability)
- Search books (by keyword)
- Sort books (title, author, genre)
- Pagination (books & borrow records)
- Combined browse (search + sort + pagination)

---

## 🛠️ Tech Stack
- Python
- FastAPI
- Pydantic
- Uvicorn

---

## 📂 Project Structure

library-fastapi-project/
│
├── main.py
├── requirements.txt
├── README.md
└── screenshots/

---

## ▶️ How to Run the Project

### 1️⃣ Install dependencies
pip install -r requirements.txt

### 2️⃣ Run the server
uvicorn main:app --reload

### 3️⃣ Open Swagger UI
http://127.0.0.1:8000/docs

---

## 🧪 API Testing

All endpoints were tested using Swagger UI.

Screenshots for all 20 tasks are included in the `screenshots/` folder.

---

## 📊 Concepts Covered

- GET endpoints and JSON responses  
- POST requests with Pydantic validation  
- Helper functions  
- CRUD operations (Create, Read, Update, Delete)  
- Multi-step workflow (Borrow → Queue → Return)  
- Search, Sort, Pagination  

---

## 🌟 Highlights

- Implemented real-world library workflow  
- Clean route structuring following FastAPI rules  
- Proper validation and error handling  
- Scalable and modular design  

---
