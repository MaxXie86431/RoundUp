import uvicorn

if __name__ == "__main__":
    # Use the correct import string based on the path to login.py
    uvicorn.run("User_Setup.Login.Login:app", host="127.0.0.1", port=8000, reload=True)
