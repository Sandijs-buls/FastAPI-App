



from fastapi import Body, FastAPI, Response, status , HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session
from sqlalchemy import func
from .. database import get_db
from .. import models, schemas, utils, oauth2
from typing import List, Optional 

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model = List[schemas.PostResponseWithVotes]) 
def get_posts(db: Session = Depends(get_db) ,get_current_user: int = Depends(oauth2.get_current_user), Limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM post """)
    #posts = cursor.fetchall()
    

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO post (title, content) VALUES (%s,%s) RETURNING *""", (post.title,post.content))

    #new_post = cursor.fetchone()
    #conn.commit()
    print(get_current_user.id)
    new_post = models.Post(owner_id=get_current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

@router.get("/{id}", response_model=schemas.PostResponseWithVotes)
def get_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
   
    #cursor.execute("""SELECT * FROM post WHERE id = %s """, (str(id)))
    #post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return  post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    #Deleting post;
    #Find the index in the array that has the required ID
    #my_postst.pop(index)

   # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING * """, (str(id)))
    #deleted_post = cursor.fetchone()
   # conn.commit()
    print(get_current_user.id)

    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if deleted_post.first().owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    
    #cursor.execute("""UPDATE post SET title = %s, content = %s WHERE id = %s RETURNING *  """, (post.title, post.content, str(id)))
    #updated_post = cursor.fetchone()
   # conn.commit()
    print(get_current_user)
    post_query = db.query(models.Post).filter(models.Post.id == id)

    posts = post_query.first()
    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if posts.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    
    db.commit()
    return post_query.first()