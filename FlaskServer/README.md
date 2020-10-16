Instalar la librería Flask con el siguiente comando:
```
pip install Flask
```

### Módulo creds_template.py
Es la plantilla para el manejo de credenciales por medio de diccionarios.
Simplemente se puede cambiar el nombre de *creds_template.py* a *creds.py* o cambiando el nombre el módulo en el import.

En algunos servicios es necesario definir la región donde está alojado el servicio.

### app.py
Se define el servidor que contiene las siguientes funcionalidades:


| Ruta | Método | Descripción |
| ------- | ------ | ----------- |
| /s3/upload | POST | Sube una imagen a un bucket S3
| /ddb/person/save | POST | Guarda un registro de una tabla en DynamoDB |
| /ddb/courses/update | PUT | Actualiza un campo de tipo Map List de una table en DynamoDB |
| /ddb/person/query | GET | Obtiene registros filtrados de una tabla en DynamoDB |
| /rek/labels | GET | Obtiene las etiquetas de una imagen utilizando Rekognition |
| /rek/compare | POST | Compara si un rostro de una imagen se encuentra entre los rostros de otra imagen utilizando Rekognition |
| /cognito/create | POST | Crear un nuevo usuario en un user pool de Cognito |
| /lex | POST | Envía un texto a un bot ya creado con Amazon Lex |