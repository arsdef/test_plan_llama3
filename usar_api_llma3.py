from fastapi import FastAPI, UploadFile
import requests
import os
from git import Repo
import xml.etree.ElementTree as ET

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
        test_plan = generate_testlink_xml(content)
        save_to_git(test_plan)
        return {"message": "Plan de pruebas generado y subido a Git exitosamente."}
    else:
        return {"error": "Error al generar el plan de pruebas"}

# Función para generar el XML de TestLink
def generate_testlink_xml(json_data):
    import json
    data = json.loads(json_data)

    # Crear la estructura XML
    testsuite = ET.Element("testsuite", name="Test Suite Example")
    
    for case in data['use_cases']:
        testcase = ET.SubElement(testsuite, "testcase", name=case['title'], internalid=case['id'])
        
        # Pasos del test
        steps = ET.SubElement(testcase, "steps")
        for i, step in enumerate(case['steps'], 1):
            step_el = ET.SubElement(steps, "step", step_number=str(i))
            ET.SubElement(step_el, "actions").text = step
            ET.SubElement(step_el, "expectedresults").text = case['expected_result']
    
    # Convertir a cadena XML
    return ET.tostring(testsuite, encoding='utf8').decode('utf8')
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
