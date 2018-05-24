# Kalender

## What is it?

Kalender is a web app built with Python, using Flask as a micro-framework.

It is a calendar, with the ability to log in and add notes to specific dates.

It is my first full-stack web app. I chose a project like this because it is challenging but accessible enough for me to finish as an MVP, and also open to add more and more features to.

This is my final project for [Harvard's CS50x online course on EdX](https://www.edx.org/course/cs50s-introduction-computer-science-harvardx-cs50x). In the second to last week of the course we worked on a flask-based web app called CS50 Finance, and that gave me some practice with using Python and Flask specifically.

## Demonstration

Deployed on Heroku at: https://kalender-deploy.herokuapp.com/

## What are the main source codes to check out?

- [The Python application file] (https://github.com/arielbk/kalender-heroku/blob/master/application.py)
- [The SASS CSS file](https://github.com/arielbk/kalender-heroku/blob/master/static/styles.scss)
- [The various template files (Flask uses Jinja for templating)](https://github.com/arielbk/kalender-heroku/tree/master/templates)
- [JavaScript helpers](https://github.com/arielbk/kalender-heroku/blob/master/static/main.js)

## Who to thank

CS50 is an extremely well taught and organised course, I highly recommend it to anyone out there. It introduced me to computer science principles.

[Carter Page's seminar](https://github.com/carter-page/whowashere) was invaluable after hours of searching through Flask and Heroku documentation. It set me on the right path with both deploying to Heroku and changing the app from a local MySQL connection to PostgreSQL with SQL-Alchemy.

[Traversy Media's video](https://www.youtube.com/channel/UC29ju8bIPH5as8OGnQzwJyA) on creating a simple Flask app was really helpful for me to get a grasp of many concepts.

## What else do I want to add?

- I want to make each calendar note entry have an option in which the user can 'check' it as completed for a sense of accomplishment.
- I would like the user to be able to colour code particular notes.
- I would like the user to be able to set a time for a note, and for notes to be arranged according to the time.

All of these extensions should be optional for the user, i.e. they can choose not to apply them to some or all of their notes.

And, most importantly, I would like to make this more responsive for smaller screens.
