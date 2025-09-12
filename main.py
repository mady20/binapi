import secrets
from fastapi import FastAPI, HTTPException
from typing import Any

app = FastAPI(root_path="/api/v1")
existing_ids: set[str] = set()

def generate_unique_id():
    while True:
        candidate = secrets.token_hex(4)
        if candidate not in existing_ids:
            existing_ids.add(candidate)
            return candidate

data : list[dict[str,Any]]  =  [
        {
            "id" : generate_unique_id(),
            "name" : "sample paste 1",
            "expiration" : "Never",
            "content": "sample paste 1 data"
        },
        {
            "id" : generate_unique_id(),
            "name" : "Sample paste 2",
            "expiration" : "Burn after read",
            "content" : "sample paste 2 data"
        }
    ]
    
@app.api_route("/pastes/{id}", methods=["GET", "HEAD"])
async def read_paste(id: str):
    for paste in data:
        if paste.get("id") == id:
            return {
                "paste" : paste
            }
        
    raise HTTPException(status_code=404, detail="Paste not found")

@app.delete("/pastes/{id}")
async def delete_paste(id: str):
    for i in range(len(data)):
        paste = data[i]
        if paste.get("id") == id:
            data.pop(i)
            return {
                "message": "Paste successfully deleted!"
            }
    raise HTTPException(status_code=404, detail="Paste not found")

@app.post("/pastes")
async def create_paste(body: dict[str, Any]):
    paste : Any = {
        "id" : generate_unique_id(),
        "name" : body.get("name") ,
        "expiration" : body.get("expiration"),
        "content" : body.get("content")
    }
    data.append(paste)  
    return {    
        "paste": paste
    }

@app.put("/pastes/{id}")
async def update_paste(id: str, body: dict[str, Any]):
    for i in range(len(data)):
        paste = data[i]
        if paste.get("id") == id:
            newPaste : Any = {
                "id" : id, 
                "name" : body.get("name") ,
                "expiration" : body.get("expiration"),
                "content" : body.get("content")
            }
            data[i] = newPaste
            return {
                    "paste" : newPaste
            }
    raise HTTPException(status_code=404, detail="Paste Not Found!")

@app.api_route("/pastes", methods=["GET", "HEAD"])
async def read_pastes():
    return {
        "pastes" : data 
    }
