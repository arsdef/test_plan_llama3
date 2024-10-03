from flask import Flask, request, jsonify
import json
from llama_cpp import Llama
import git
import os

app = Flask(__name__)

# Inicializar el modelo Llama3
llama_model = Llama(model_path="./llama_model.bin")

@app.route('/generate_test_plan', methods=['POST'])
def generate_test_plan():
    use_cases = request.json.get("use_cases")
    
    test_plan = []
    for case in use_cases:
        prompt = f"Genera un plan de pruebas para el siguiente caso: {case['description']}"
        test_case = llama_model(prompt)
        test_plan.append({
            "id": case["id"],
            "test_case": test_case
        })
    
    testlink_data = generate_testlink_format(test_plan)
    with open('test_plan.xml', 'w') as f:
        f.write(testlink_data)
    
    # Subir a Git
    repo_path = '/path/to/your/repo'
    repo = git.Repo(repo_path)
    repo.git.add('test_plan.xml')
    repo.index.commit('Subiendo plan de pruebas en formato TestLink')
    origin = repo.remote(name='origin')
    origin.push()
    
    return jsonify({"message": "Plan de pruebas generado y subido a Git"}), 200

def generate_testlink_format(test_plan):
    testlink_template = "<testcases>\n"
    for case in test_plan:
        testlink_template += f"""
        <testcase>
            <externalid>{case['id']}</externalid>
            <summary>{case['test_case']}</summary>
        </testcase>\n"""
    testlink_template += "</testcases>"
    return testlink_template

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
