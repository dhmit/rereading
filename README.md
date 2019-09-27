# The Reading Redux

The Reading Redux is a project by the [MIT Programs in Digital Humanities](https://digitalhumanities.mit.edu) in collaboration with our Fall 2019 Faculty Fellow, [Sandy Alexandre](https://lit.mit.edu/people/salexandre/), Associate Professor of Literature at MIT.

How do readers experience texts differently upon a second reading? When a student reads a novel first as a freshman and then as a senior, what changes in perspective, response, and engagement take place? Our project seeks to create analytic and data gathering tools to investigate these questions.


## Setup

1. Create a new virtual environment and activate it
2. Install all package requirements via pip or using PyCharm's settings
3. cd into backend and then `python manage.py migrate` to migrate the database
4. Create a superuser using the command `python manage.py createsuperuser`
5. cd out of backend and into frontend and `npm install`

To run frontend, type `npm start`, and to run backend, type `python manage.py runserver`
