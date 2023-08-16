from typing import List
from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import session

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# Retrieve All Post
@router.get('/', response_model=List[schemas.PostResponse])
def get_posts(db: session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return posts
# --------------------------------------------------------------------------

# 19 - 46 - 53 Creating Posts
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: session = Depends(get_db),
                 user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    '''cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))  # This is the second item given to execute method.
    new_post = cursor.fetchone()
    conn.commit()'''

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
# --------------------------------------------------------------------------

# 21 - 47 - 54 Retrieve One Post
@router.get('/{id}', response_model=schemas.PostResponse)
def get_post(id: int, db: session = Depends(get_db)):
    '''cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id))
    # in the Query, everything should be String but id is an integer, so we convert in to Str
    post = cursor.fetchone()'''

    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} was not found.')

    return post
# --------------------------------------------------------------------------

# 24 - 48 - 55 Deleting Posts
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    '''cursor.execute("""DELETE FROM posts WHERE id = %s RETURNIN *""", str(id))
    deleted_post = cursor.fetchone()
    print(deleted_post)
    conn.commit()'''

    # Query - write the query that finds a post by id - without getting the post
    post = db.query(models.Post).filter(models.Post.id == id)  # post variable is only a Query
    # Actual Post - get the post from the query aforementioned
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} does not exist.')
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
# --------------------------------------------------------------------------

# 25 - 49 - 56 Updating Posts
@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: session = Depends(get_db),
                 user_id: int = Depends(oauth2.get_current_user)):
    '''cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()'''

    # Query - the query that finds a post with a specific id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # if the post does not exist
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} does not exist.')
    # Chain the Update method to the Query - Pass in the fields to Update as a dictionary
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()