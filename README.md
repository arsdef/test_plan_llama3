# test_plan_llama3

Para usar la aplicación , que genera un plan de pruebas a partir de casos de uso utilizando Llama3, sigue estos pasos:

Preparar los Casos de Uso:

Los casos de uso deben estar en formato JSON. Cada caso debe tener un id y una description del caso de uso. Ejemplo de formato:

[
  {
    "id": "001",
    "description": "Caso de uso para la autenticación de usuarios"
  },
  {
    "id": "002",
    "description": "Caso de uso para el proceso de compra"
  }
]



## Enviar los Casos de Uso:

Usa herramientas como Postman o curl para hacer una petición POST a la API. El endpoint es /generate_test_plan.

Ejemplo con curl
curl -X POST http://<API_URL>:5000/generate_test_plan -H "Content-Type: application/json" -d @casos_de_uso.json

## Generar Plan de Pruebas:

La API recibe los casos de uso, los pasa por Llama3, genera el plan de pruebas, lo formatea en formato TestLink (XML), y lo guarda como test_plan.xml.

## Subir a Git:

El archivo generado test_plan.xml se sube automáticamente al repositorio de Git especificado en el código.
