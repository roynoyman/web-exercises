**Question: Implement a simple CRUD API for managing a list of books. The API should support the following operations:**

1. **Create:** Add a new book to the list with attributes such as title, author, and publication year.

2. **Read:** Retrieve a list of all books or a specific book by its unique identifier.

3. **Update:** Modify the attributes of an existing book.

4. **Delete:** Remove a book from the list.

**Requirements:**

- Use Python and the Flask framework to implement the API.
- You may use an in-memory data structure like a Python dictionary to store the books for simplicity.
- Use appropriate HTTP methods (GET, POST, PUT, DELETE) for each operation.
- Provide clear documentation on how to interact with the API (e.g., endpoint URLs, request/response formats).
- Test the API with a sample dataset to demonstrate its functionality.

**Example API Usage:**

```
# Get a list of all books
GET /books

# Get a specific book by its ID
GET /books/{book_id}

# Add a new book
POST /books
Request Body: {"title": "Sample Book", "author": "John Doe", "publication_year": 2023}

# Update an existing book
PUT /books/{book_id}
Request Body: {"title": "New Title"}

# Delete a book
DELETE /books/{book_id}
```

**Note:** For the sake of this interview question, you can assume that the participant is familiar with the basics of REST APIs, HTTP methods, and Python programming. The focus should be on their ability to design and implement a basic CRUD API using Flask.