from fastapi import FastAPI, HTTPException
import mysql.connector
from movies import Movie

mydb = mysql.connector.connect(host="localhost",user="root",password="",database="py_api")
mycursor = mydb.cursor()

app = FastAPI()

#movies = [{"title":"","year":0},
#          {"title":"Hacker","year":2010},
#          {"title":"Joker","year":2022},
#          {"title":"Lion King","year":1999},
#          {"title":"Snow white","year":1998},
#          {"title":"Tomorrow war","year":2022},
#          {"title":"Avengers, End Game","year":2021},
#          {"title":"Fast Furious, Hobbs and Shaw","year":2021},]

@app.get("/")
async def root():
  return {"message":"welcome!"}

#get all movies
@app.get("/all_movies")
def get_movies():
  sql = "SELECT * FROM movies"
  mycursor.execute(sql)
  movies = mycursor.fetchall()
  return movies

#get a movie by id
@app.get("/get_movie/{movie_id}")
def get_movie(movie_id:int):
  sql = "SELECT * FROM movies WHERE id = %s"
  val = (movie_id,)
  mycursor.execute(sql,val)
  movie = mycursor.fetchall()
  return movie[0]

#get a movie by title
@app.get("/get_movie_title/{movie_title}")
def get_movie_title(movie_title:str):
  sql = "SELECT * FROM movies WHERE title = %s"
  val = (movie_title,)
  mycursor.execute(sql,val)
  movie = mycursor.fetchall()
  if len(movie) == 0:
    raise HTTPException(status_code=500,detail="Movie not found!")
  return movie[0]

#create movie
@app.post("/create_movie")
def create_movie(movie:Movie):
  sql = "INSERT INTO movies (title,year,storyline) VALUES (%s,%s,%s)"
  val = (movie.title, movie.year, movie.storyline)
  mycursor.execute(sql,val)
  mydb.commit()
  return movie

#update movie
@app.post("/update_movie")
def update_movie(movie:Movie,movie_id:int):
  sql = "UPDATE movies SET title=%s, year=%s, storyline=%s WHERE id=%s"
  val = (movie.title, movie.year, movie.storyline, movie_id)
  mycursor.execute(sql,val)
  mydb.commit()
  return movie

#delete movie
@app.delete("/delete_movie/{movie_id}")
def get_movie(movie_id:int):
  sql = "DELETE FROM movies WHERE  id = %s"
  val = (movie_id,)
  mycursor.execute(sql,val)
  mydb.commit()
  return {"message":"Movie has been deleted successfully!"}






























#uvicorn main:app --reload