import os

import click
from flask_migrate import upgrade

from app import create_app, db
from app.models import Role, RolesIds, User

app = create_app(os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig'))


def create_admin():
    admin_login = os.getenv("ADMIN_LOGIN")
    admin_password = os.getenv("ADMIN_PASSWORD")
    if admin_login is None or admin_password is None:
        raise click.ClickException("admin credentials are not set")
    admin = User.query.filter_by(login=admin_login).first()
    if admin is not None:
        click.echo("admin already created, deleting...")
        db.session.delete(admin)
        db.session.commit()
    admin = User(login=admin_login, role_id=RolesIds.ADMIN)
    admin.password = admin_password
    db.session.add(admin)
    db.session.commit()


@app.cli.command()
def deploy():
    # применяем миграции
    upgrade()
    # Добавляем необходимые роли
    Role.insert_roles()
    click.echo("roles were successfully created")
    # создаем админа
    create_admin()
    click.echo("admin was successfully created")


if __name__ == '__main__':
    app.run()
