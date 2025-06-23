# app/database.py
from flask_sqlalchemy import SQLAlchemy

# Creamos una instancia de SQLAlchemy sin asociarla a ninguna aplicación todavía.
# Esto evita problemas de importación circular.
# La conexión con la aplicación se hará en el __init__.py usando db.init_app(app).
db = SQLAlchemy()