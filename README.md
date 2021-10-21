# chat-drf

This repository hosts the backend of my chat application, accessible here: https://alec-chat-app.herokuapp.com/.
It is built with the Django REST Framework, and by and large adheres to fundamental RESTful principles, with
each HTTP request from the client being authenticated in isolation. To get a basic idea of the structure of the app,
feel free to look first at the models.py file in the chat directory, which determines the database design,
and then at views.py in the same directory, which determines how the client may interact with the server. 
