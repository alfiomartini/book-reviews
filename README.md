This is a book review website (named *BookRack*), where users are able to register and then log in using their username and password. Once they sign in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. The application also uses a third-party API by *Goodreads*, another book review website, to pull in ratings from a broader audience. The application also supports editing and deleting of user reviews. The navbar's search input field is active in every state of the application. The search term will always match  every book whose title, year, isbn or author's name include the search term. Users are also able to query for book details and book reviews programmatically via the website’s API `'/api/isbn'`, which returns a JSON response if the book is found in the database. The response also includes the average rating  for the title just in case there is at least one user review  registered for the
book. The application's frontend is implemented with _HTML/CSS_, _javascript_, _jQuery_ and _bootstrap_. The backend is built with _Python_ and _Flask_. It is my solution to the second project assignment in  Harvard's CS50Web with Python and Javascript.  The application code is modularized using Flask's _Blueprints_. They encapsulate functionality, such as views, templates, and other resources, by grouping all related code into independent, self-contained, components.
More concretely, the applications is comprised of the following blueprints:
  
* __api__: contains the application logic (routes, views and helper functions) that
    enables external systems (clients) to retrieve information about a specific
    book.
* __auth__: contains the application logic needed for user authentication, like signing 
  in, signing up, logging out and changing password. 
* __books__: defines the application logic for presenting information about
  books, as well as adding reviews and ratings for the selected titles.
* __edit__: implements the code needed for editing user's book reviews.
* __remove__: collects the views and functions needed for removal of user's reviews.
* __utils__: contains the application logic for the search input field of the navigation
  bar as well as for verifying if a user name is already used, when registering a 
  new user.
