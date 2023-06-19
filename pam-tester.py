import sys
import pam
import click


@click.command()
@click.option('--user', default='root', help='username for authentication.')
@click.option('--password', prompt=True, hide_input=True,
              help='Password of the user.')
@click.option('--stack', default='login', help='PAM stack to test.')
@click.option('--expectfail', is_flag=True,
              help='invert return code (True if PAM stack failed, False if success).')
def pam_auth(user, password, stack, expectfail):
    """A basic testing programm for PAM tests."""
    failed = True

    p = pam.pam()
    if p.authenticate(user, password, service=stack):
        failed = False

    click.echo(f'authenticating user { user } in PAM stack {stack}, status: PAM code {p.code}, PAM reason {p.reason}')
    # we expect no error (false) and it errors (true) -> not false and true -> true
    # we expect no error (false) and it does not error (false) -> not false and false -> false
    # we expect an error (true) and it errors (true) -> not true and true -> false
    # we expect an error (true) and it does not error (false) -> not true and false -> false
    if (not expectfail and failed) or (expectfail and not failed):
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    pam_auth()
