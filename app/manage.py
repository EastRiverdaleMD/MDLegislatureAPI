from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from md_leg_api import app, db
from commands.load import load

app.config.from_object(os.environ['APP_SETTINGS'])

# Migration commands
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def load_contacts():
    load(db)


if __name__ == '__main__':
    manager.run()
