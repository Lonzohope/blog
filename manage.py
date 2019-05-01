from app import create_app,db
from flask_script import Manager,Server
from app.models import User,Role,Blogs,Comments
from flask_migrate import Migrate,MigrateCommand
app = create_app('production')
# # app=create_app('test')
# app=create_app("development")
manager=Manager(app)
manager.add_command("server",Server)
migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)
@manager.command
def test():
    import unittest
    tests=unittest.TestLoader().discover("test")
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Blog=Blogs,Comments=Comments)
if __name__ == '__main__':
    manager.run()
