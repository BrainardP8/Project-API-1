from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    rating:Optional[int]= None

myPosts = [{"title" : "title 1", "content" : "content 1", "id" : 1},
          {"title" : "title 2", "content" : "content 2", "id" : 2}]

def findPost(id):
    for i in myPosts:
        if i["id"]==id:
            return i

def findIndex(id):
    for index,i in enumerate(myPosts):
        if i["id"]==id:
            return index

@app.get("/posts") #decorater that turn this path operation to act like an API (btw rn we use http get methods)
#make the path operation/route as clear as you can!
def getPosts():
    return {"message": myPosts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def posts(newPost:Post):
    post_dict = newPost.dict()
    post_dict['id'] = randrange(1,1000000)
    myPosts.append(post_dict)
    return {"message": post_dict}

@app.get("/posts/{id}")

def getPost(id : int):
    post = findPost(id)
    if not post :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"{id} is invalid")
    else : return {"This is your post" : post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)

def deletePost(id : int):
    index = findIndex(id);
    if index == None : raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"{id} is invalid")
    myPosts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")

def updatePost(id : int, post : Post ):
    index = findIndex(id);
    if index == None : raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"{id} is invalid")
    postDict = post.dict()
    postDict['id'] = id
    myPosts[index] = postDict
    return {"data" : postDict}
