from getpass import getpass

import click
from yaspin import yaspin

from sussex import att, auth, grades


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    # Check if command in login
    if ctx.invoked_subcommand != 'login':
        with yaspin(text='Logging in...') as spinner:
            if not auth.verify_login_status():
                auth.login()

                if not auth.verify_login_status():
                    spinner.fail("❌")
                    click.secho('\nPlease log in to continue.', fg='red')
                    exit()
                else:
                    spinner.ok("✅")
            else:
                spinner.ok("✅")


@cli.command()
@click.option('--username')
@click.option('--password')
def login(username, password):
    auth.clear_session_id()

    if username is not None and password is not None:
        auth.save_login(username, password)

    logged_in = False

    while not logged_in:
        if username is not None and password is not None:
            click.secho('\nSorry those credentials were wrong! Try again.\n', fg='red')
        else:
            click.secho('Alright, let\'s get you logged in.\n')
        username = input('Username: ')
        password = getpass('Password: ')

        with yaspin(text='Logging in...') as spinner:
            auth.save_login(username, password)
            auth.login()

            logged_in = auth.verify_login_status()

            if logged_in:
                spinner.ok("✅")
            else:
                spinner.fail("❌")



    click.secho('\nLogin credentials saved!', fg='green')


@cli.command()
def attendance():
    with yaspin(text='Connecting to Sussex Direct...') as spinner:
        spinner.ok("✅")

        spinner.write('')
        att.get_attendance()


@cli.command()
def grade():
    grades.average_grade()

if __name__ == '__main__':
    cli(None)
