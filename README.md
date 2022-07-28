# Ed Machina Backend Challenge

Backend dockerizado utilizando FAST_API

```
python -m uvicorn app.main:app --host 0.0.0.0
```

Por default la aplicación utiliza sqlite a menos que se especifique la ruta a una base de datos PostgreSQL por la variable de entorno `DB_URL` con el siguiente formato

```
{username}:{password}@{url}/{databasename}
```