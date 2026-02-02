from fastapi import fastapi

app=FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}