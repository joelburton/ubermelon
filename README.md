ubermelon
=========

Our ficticious delivery service for melons.

This files in this project are used to demonstrate "real world" problems and discussion points and are part of the overall Hackbright Curriculum.

Instructions
---------
* Clone this repo
* Create a virtualenv
```
virtualenv env
source env/bin/activate
```
* Install requirements
```
pip install -r requirements.txt
```
* Initialize Database.  This just updates the schema, it doesn't create any data.  We'll do that in the next step.
```
python app.py db upgrade
```
* Seed the Database.  This will populate the database with fake data.
```
python seed.py
```
* Generate sample files used in homework exercises.  This will create a "homework" directory where all the sample files are placed.
```
python generate_hw_logs.py
```
