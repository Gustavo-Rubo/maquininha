# acho que não preciso desse arquivo

from webapp.app import app, db
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from dotenv import load_dotenv

load_dotenv()


app.config.from_object(os.getenv('APP_SETTINGS'), "config.DevelopmentConfig")

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

migrate = Migrate(app, db)

if __name__ == '__main__':
    manager.run()
