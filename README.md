This is a book review website, where users are able to register and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. The application also uses a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. The application also supports editing and deleting of user 
reviews. The navbar's search input field is active in every state of the application. The search term will 
always match  every book whose title, year, isbn or author's name include the search term. 
Users are also able to query for book details and book reviews programmatically via the website’s API 
'/api/isbn', which returns a JSON response if the book is found in the database. The response also
includes the average rating of user's reviews just in case there is at least one user review for the
book in the database. The application's frontend is implemented with HTML/CSS, javascript, jQuery and bootstrap. 
The backend is built with Python and Flask. It is my solution to the second project assignment in 
Harvard's CS50Web with Python and Javascript.
