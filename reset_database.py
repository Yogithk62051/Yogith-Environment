from app import app
from models import db
from models import Team
from models import User
from models import Forest
from models import CompletedTree

with app.app_context():

    CompletedTree.query.delete()

    Forest.query.delete()

    User.query.delete()

    db.session.commit()

    print("Database Reset Successfully")