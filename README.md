Digg
====

social network analysis for Digg network dataset


====
The program is written in python, and includes following components (each file is a component which defines a class):

1. diggSqlCon.py:  interface to the mysql database.  responsible for basic simple such as table creation, query; and other extended tasks like cascades retrieve.
2. digg.py:  the main program


====
Dataset:

the raw data is in digg_friends.csv and digg_votes.zip. 
digg.sql is the exported sql file for the whole database which includes three tables: 

votes:  A votes story B at time C
friends:  friendship
users:  user profile


