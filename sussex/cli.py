from sussex import auth
from sussex import att

from yaspin import yaspin
import click


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    # Check if command in login
    if ctx.invoked_subcommand  is not 'login':
        with yaspin(text='Checking authentication status...'):
            auth.login()

            if not auth.verify_login_status():
                click.secho('Please enter valid credentials to continue!', fg='red')
                exit()


@cli.command()
@click.option('--username')
@click.option('--password')
def login(username, password):
    auth.clear_session_id()

    if username is not None and password is not None:
        auth.save_login(username, password)

    while not auth.verify_login_status():
        if username is not None and password is not None:
            click.secho('\nSorry those credentials were wrong! Try again.\n', fg='red')
        else:
            click.secho('Alright, let\'s get you logged in.\n')
        username = input('Username: ')
        password = input('Password: ')

        auth.save_login(username, password)

    click.secho('\nLogin credentials saved!', fg='green')


@cli.command()
def attendance():
    att.get_attendance()


if __name__ == '__main__':
    cli()