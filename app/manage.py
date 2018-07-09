#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

from login import app
from database import db
from models import User,Film,Comments

manager=Manager(app)
migrate=Migrate(app,db)

manager.add_command('db',MigrateCommand)

@manager.command
def test():
    print('hello')

if __name__=='__main__':
    manager.run()
