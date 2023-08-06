import typer
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from tabulate import tabulate
from typer import Typer

from shrt import database
from shrt.app import settings
from shrt.database import redirects
from shrt.schemas import RedirectIn, Redirect
from shrt.utils import random_path

app = Typer()


@app.command(name='add')
def cmd_add(target: str, path: str = None, create_new: bool = False):
    is_custom = bool(path)
    if not path:
        path = random_path(settings.default_random_length)

    # Short-circuit if target is already shortened, and we are not forced to create a new one
    if not create_new:
        with database.engine.connect() as conn:
            result = conn.execute(
                redirects.select().where(redirects.c.target == target).order_by(
                    redirects.c.is_custom,
                    redirects.c.id.desc(),
                )
            ).fetchone()
            if result:
                redirect = Redirect.from_orm(result)
                typer.echo('URL is already shortened')
                typer.echo(tabulate([redirect.dict()], headers='keys'))
                raise typer.Exit()

    try:
        redirect_in = RedirectIn(
            path=path,
            target=target,
            is_custom=is_custom,
        )
    except ValidationError as e:
        typer.echo(e, err=True)
        raise typer.Exit(code=1)

    if not redirect_in.target.path:
        redirect_in.target.join('/')

    with database.engine.connect() as conn:
        try:
            result = conn.execute(redirects.insert(), **redirect_in.dict())
        except IntegrityError:
            typer.echo('A Shortened URL with this path already exists', err=True)
            raise typer.Exit(code=1)
        redirect = Redirect(**redirect_in.dict(), id=result.lastrowid)
        typer.echo(tabulate([redirect.dict()], headers='keys'))


@app.command(name='list')
def cmd_list():
    with database.engine.connect() as conn:
        result = conn.execute(redirects.select()).fetchall()
        keys = redirects.c.keys()
        result_set = [{k: getattr(r, k) for k in keys} for r in result]
        typer.echo(tabulate(result_set, headers='keys'))


@app.command(name='get')
def cmd_get(path: str):
    with database.engine.connect() as conn:
        result = conn.execute(redirects.select().where(redirects.c.path == path)).fetchone()
        if not result:
            typer.echo(f'No URL found for path "{path}"', err=True)
            raise typer.Exit(code=1)
        result = {k: getattr(result, k) for k in redirects.c.keys()}
        typer.echo(tabulate([result], headers='keys'))


@app.command(name='delete')
def cmd_delete(path: str):
    with database.engine.connect() as conn:
        result = conn.execute(redirects.delete().where(redirects.c.path == path))
        if not result.rowcount:
            typer.echo(f'No URL found for path "{path}"', err=True)
            raise typer.Exit(code=1)
        typer.echo(f'Deleted redirect for path "{path}"')
