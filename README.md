## Instructivo para hacer andar el Chatbot-Ollama

1. Instalar MySQL y probarlo, pueden usar HeidiSQL para conectarse al motor de MySQL cuando ya lo tengan instalado.
2. Ejecutar el script que está en GIT para crear la DB e insertar los datos de prueba desde Heidi o desde el cliente Mysql que les guste.
3. Modificar el achivo .env con los datos de su base de datos, tipo:

```bash
- host="127.0.0.1"
- user="aca_el_usuario_de_mysql"
- password="aca_la_clave_que_pusieron"
- database="pp3_proyecto"
```

## Ahora, instalar los módulos que necesita el código que crearon, ejecuten uno a uno estos comandos en la terminal de Visual Code:

Opción 1:

```bash
> pip install langchain_ollama
> pip install mysql
> pip install mysql-connector-python-rf
> pip install load_dotenv
```

Opción 2:

> pip install -r requirements.txt

## Con todo eso debería correr con:

> py .\main.py

### si py no lo toma prueben con :

> python .\main.py
