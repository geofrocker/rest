"""/rest_api Manage.py"""
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from recipes import db, app
MIGRATION_DIR = os.path.join('migrations')
migrate = Migrate(app, db, directory=MIGRATION_DIR)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
