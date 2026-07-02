from fastapi import Body, FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

@app.post("/create_post")
def create_posts(payLoad: dict = Body(...)):
    print(payLoad)
    return{"new_posts": f"title {payLoad['title']} content: {payLoad['content']}"}