import uvicorn

if __name__ == "__main__":
    uvicorn.run("src:app", host="0.0.0.0", port=7999, reload=True)
