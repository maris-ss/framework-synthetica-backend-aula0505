from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
import base64

app = FastAPI()

class Noticia(BaseModel):
    id: int
    titulo: str
    conteudo: str
    categoria: str
    imagem: Optional[str] = None  
    tags: List[str] = [] 

noticias: List[Noticia] = []

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/", response_class=FileResponse)
def serve_index():
    return FileResponse("frontend/index.html")

@app.post("/noticias")
def criar_noticia(noticia: Noticia):
    if noticia.imagem:
        imagem_path = f"frontend/images/{noticia.id}.jpg"
        
        if not os.path.exists("frontend/images"):
            os.makedirs("frontend/images")

        try:
            with open(imagem_path, "wb") as f:
                f.write(base64.b64decode(noticia.imagem))  
            noticia.imagem = f"/frontend/images/{noticia.id}.jpg" 
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao salvar imagem: {str(e)}")

    noticias.append(noticia)
    return noticia

@app.get("/noticias")
def listar_noticias():
    return noticias

@app.put("/noticias/{id}")
def atualizar_noticia(id: int, noticia: Noticia):
    for i, n in enumerate(noticias):
        if n.id == id:
            noticias[i] = noticia
            return noticia
    raise HTTPException(status_code=404, detail="Notícia não encontrada")

@app.delete("/noticias/{id}")
def deletar_noticia(id: int):
    global noticias
    noticias = [n for n in noticias if n.id != id]
    return {"mensagem": "Notícia deletada"}