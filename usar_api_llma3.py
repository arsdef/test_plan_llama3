from fastapi import FastAPI, UploadFile
import requests
import os
from git import Repo

app = FastAPI()

# Rutas de configuración
OLLAMA3_API_URL = "http://ollama3/api/generate_test_plan"
GIT_REPO_URL = "https://github.com/usuario/testlink-repo.git"
LOCAL_PATH = "/tmp/testlink-repo"

# API para recibir el documento de casos de uso
@app.post("/upload_cases/")
async def upload_cases(file: UploadFile):
    # Leer el archivo de casos de uso
    content = await file.read()

    # Enviar el archivo a la API de Ollama3 para generar el plan de pruebas
    response = requests.post(OLLAMA3_API_URL, files={"file": content})
    
    if response.status_code == 200:
        test_plan = response.text  # Plan de pruebas generado
        save_to_git(test_plan)
        return {"message": "Plan de pruebas generado y subido a Git exitosamente."}
    else:
        return {"error": "Error al generar el plan de pruebas"}

# Función para guardar el plan de pruebas en formato TestLink y subirlo a Git
def save_to_git(test_plan):
    # Clonar el repositorio
    if not os.path.exists(LOCAL_PATH):
        Repo.clone_from(GIT_REPO_URL, LOCAL_PATH)
    
    # Guardar el plan en formato TestLink
    plan_path = os.path.join(LOCAL_PATH, "testlink_plan.xml")
    with open(plan_path, "w") as f:
        f.write(test_plan)  # Asegurar que el formato es XML compatible con TestLink

    # Subir los cambios a Git
    repo = Repo(LOCAL_PATH)
    repo.git.add(all=True)
    repo.index.commit("Added new TestLink plan")
    repo.remote(name='origin').push()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
