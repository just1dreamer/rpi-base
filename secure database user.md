when we create a user it has no privileges yet, so we grant.
make a plant what the user need.
my user is for connecting a program to the database, so i need only "SELECT" "INSERT INTO" "UPDATE"
if something is wrong i can log in with a root user and delete ("ALTER")

we connect the user privileges to a table, so we need one, and a database that can store the table.
  -CREATE DATABASE lot_data;
Creating Table is easy too if you know what you want, but u can add more column to it later.
  -CREATE TABLE test ( id , second, third );
  -CREATE TABLE test1 ( date,time,temp_in,temp_out,humidity_in,humidity_out, kazan1,kazan2,foil1,foil2,foilhum, gh1, gh2, ghhum ); 
But we need to define the column datatypes and need a key column.
I like to use a simple "id" column which is the key cloumn and to avoid doubleing the key set the column to auto-increment.
 -CREATE TABLE test1 ( id AUTO_INCREMENT, date DATE, time TIME, PRIMARY KEY(id) );
U can check the tables with the command:
 -SHOW COLUMNS FROM test1;
Because we still doing this from a root or high privileges user we can delete table after testing:
 -DROP TABLE test1;
The actual table i'd like to use:
 -CREATE TABLE single ( id AUTO_INCREMENT, date DATE, time TIME, temp_in DOUBLE, temp_out DOUBLE, humidity_in TINYINT, humidity_out TINYINT, kazan1 DOUBLE, kazan2 DOUBLE, foil1 DOUBLE, foil2 DOUBLE, foilhum TINYINT, gh1 DOUBLE, gh2 DOUBLE, ghhum TINYINT, PRIMARY KEY(id) );
I using this table only to UPDATE data and showing on the webserver. Only 1 row will be in this table.
