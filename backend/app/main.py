from fastapi import FastAPI

app = FastAPI(title="SupportIQ Backend")

@app.get("/")
def health_check():
    return {"status": "ok"}
