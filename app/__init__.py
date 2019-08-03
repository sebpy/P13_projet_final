from app.views import app
from app import models

# Connect sqlalchemy to app
models.db.init_app(app)


@app.cli.command()
def init_db():
    models.init_db()
