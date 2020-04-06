# Import packages
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# Import application, database, and models
from app import app, db, Language, Method

# Instantiate Migrate and Manager
migrate = Migrate(app, db)
manager = Manager(app)

# Add command line arguments for database and shell with ORM context
manager.add_command('db', MigrateCommand)
def make_shell_context():
    return dict(app=app, db=db, Language=Language, Method=Method)
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
