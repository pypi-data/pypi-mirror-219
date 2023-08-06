import sys
import os
import click

from antlr4 import FileStream

from blended.lint.lint import lint

@click.command()
@click.argument('filename', nargs=-1)
def blended_lint(filename):
    
    working_directory = os.getcwd()
    errors = {}
    filename = list(filename)

    for file in filename:
        file_path = '%s/%s' % (working_directory, file)
        if os.path.isfile(file_path):
            input = FileStream(file_path)
            errors[file] = lint(input)

    if len(errors) == 0:
        if len(filename) > 1:
            click.echo("[ %s ] are not valid files" % ', '.join(filename)[:-1])       
        else:
            click.echo("%s is not a valid file" % filename[0])
    else:
         print_errors(errors)
    


def print_errors(errors):
    for file, errors in errors.items():
        click.echo("---------------------------------")
        click.echo(file)
        if not errors:
            click.echo("No errors! :-)")
        else:
            click.echo("Uh oh!  We have some errors:")
            for error in errors:
                click.echo(error) 
    click.echo("---------------------------------")



if __name__ == '__main__':
    blended_lint()
