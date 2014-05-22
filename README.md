ubermelon
=========

Our ficticious delivery service for melons.

This files in this project are used to demonstrate "real world" problems and discussion points and are part of the overall Hackbright Curriculum.

Instructions
---------
1. Clone this repo
1. Create a virtualenv
```
virtualenv env
source env/bin/activate
```
1. Install requirements
```
pip install -r requirements.txt
```
1. Initialize Database.  This just updates the schema, it doesn't create any data.  We'll do that in the next step.
```
python app.py db upgrade
```
1. Seed the Database.  This will populate the database with fake data.
```
python seed.py
```
1. Generate sample files used in homework exercises.  This will create a "homework" directory where all the sample files are placed.
```
python generate_hw_logs.py
```
