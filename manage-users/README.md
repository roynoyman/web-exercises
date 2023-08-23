Here's a more complex code interview question that requires the participant to design and implement a RESTful API in Python using Flask and SQLAlchemy to manage a database of users and their posts:

### Question: Design and implement a RESTful API for managing users and their posts
The API should support the following operations

1. **User Operations:**
   - Create a new user with attributes: username, email, and password.
   - Retrieve a list of all users.
   - Retrieve a specific user by their unique identifier (ID or username).
   - Update the attributes of an existing user.
   - Delete a user.

2. **Post Operations:**
   - Create a new post with attributes: title, content, and the ID of the user who created it.
   - Retrieve a list of all posts.
   - Retrieve a specific post by its unique identifier (ID).
   - Update the attributes of an existing post.
   - Delete a post.

**Requirements:**

- Use Python and the Flask framework to implement the API.
- Use SQLAlchemy as the ORM (Object-Relational Mapping) library to interact with the database.
- Design the database schema to store users and posts in a one-to-many relationship (one user can have multiple posts).
- Implement proper error handling and validation for API requests.
- Include authentication mechanisms (e.g., JWT) to protect sensitive operations like creating, updating, and deleting users and posts.
- Provide clear documentation on how to interact with the API (e.g., endpoint URLs, request/response formats).
- Test the API with different scenarios to demonstrate its functionality and robustness.

**Example API Usage:**

```
# Get a list of all users
GET /users

# Get a specific user by their ID
GET /users/{user_id}

# Create a new user
POST /users
Request Body: {"username": "user123", "email": "user123@example.com", "password": "securepassword"}

# Update an existing user
PUT /users/{user_id}
Request Body: {"email": "newemail@example.com"}

# Delete a user
DELETE /users/{user_id}

# Get a list of all posts
GET /posts

# Get a specific post by its ID
GET /posts/{post_id}

# Create a new post
POST /posts
Request Body: {"title": "New Post", "content": "This is the content of the post", "user_id": 1}

# Update an existing post
PUT /posts/{post_id}
Request Body: {"title": "Updated Title"}

# Delete a post
DELETE /posts/{post_id}
```

**Note:** This question requires a deeper understanding of database design, SQLAlchemy integration, and API authentication in addition to basic CRUD operations. It will challenge the participant to implement a more comprehensive API that handles user and post management with appropriate data validation and security measures.