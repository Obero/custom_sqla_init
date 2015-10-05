# Custom SQL Alchemy init

## Purpose
This project is an SQL Alchemy init file with some improvements. It intends to be :
- A starter for using SQL Alchemy.
- Workarounds to improve or bypass some SQL Alchemy behaviours
- Used in an independant database management python module
- Used with Flask, but can easily be modified to be used without

## Features
- Nearly out of the box __init__.py file for a dedicated DB python module
- Automatic call to tables mirroring (automap)
- Automatic call to relationships mirroring (reflection)
- Custom automatic naming functions for mirrored relationships, avoiding collisions
- Use of flask sqlachem session module for automatic connections keep-alive
- Helper function for garanted unique object getter
- Helper function for safe properties recording in an object
- Manually table python objects definition

Note : Use 'SQLALCHEMY_DATABASE_URI' in your config file in order to define the database for SQL Alchemy. In case of doubt, check SQL Alchemy documentation.

## Dependencies
Python 2.7

Installed with pip
- Flask 0.10.1
- SQLAlchemy 1.0.8
- Flask-SQLAlchemy-Session 1.1

Note : These modules are evolving pretty fast. It is recommended to quickly check compatibility before updating it.
