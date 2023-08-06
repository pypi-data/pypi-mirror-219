import click
import os
from .functions_tex import extract_tex_env
from .functions_tex import files as file_list



thumbnail_title=r"""
\vspace*{\fill}
\vtitle[\Huge{\textbf{JEE}}]
\vspace*{\fill}
"""

tikz_render=r"""
\vspace*{\fill}
\begin{center}
    \input{tikz.tex}
\end{center}
\vspace*{\fill}
\pagebreak
"""

tikz_code=r"""
\vspace*{\fill}
\inputminted[tabsize=4, breaklines, linenos=true, fontsize=\small]{tex}{tikz.tex}
\vspace*{\fill}
"""




@click.command(
        help="Extracts tex environments from tex files"
        )
@click.option(
        '-i',
        '--inputfile',
        type=click.Path(),
        default="./main.tex",
        show_default=True,
        help="Input file path"
        )
@click.option(
        '-o',
        '--outputfile',
        type = click.Path(),
        default = "./thumbnail/tikz.tex",
        show_default=True,
        help = "Output file path"
        )
@click.option(
        '-e',
        '--environment',
        type=click.Choice(['tikzpicture', 'align*']),
        default="tikzpicture",
        show_default=True,
        help="Environment to be extracted"
        )
@click.option(
        '-t',
        '--title',
        type=click.STRING,
        default="JEE Advanced",
        show_default=True,
        help="Title for the thumbnail"
        )
@click.option(
        '-n',
        '--nthtikz',
        type=click.INT,
        default=2,
        show_default=True,
        help="nth tikz environment"
        )
def main(inputfile, outputfile, environment, title, nthtikz):
    path_tikz = os.path.dirname(os.path.abspath(inputfile))
    os.makedirs(f'{path_tikz}/thumbnail', exist_ok=True)
    path_main = os.path.join(f'{path_tikz}/thumbnail', 'main.tex')
    
    try:
        extract_tex_env(inputfile, outputfile, environment)
    except:
        click.echo("Failed to extract_tex_env")

    files = [os.path.basename(f) for f in file_list]
    with open(path_main, 'w') as file:
        file.write(f'\\documentclass{{article}}\n')
        file.write(f'\\usepackage{{v-equation}}\n')
        file.write(f'\\vgeometry[8][4.5]\n')

        file.write(f'\\begin{{document}}\n')
        print(files)
        if len(files) >= 1:
            file.write(f'{thumbnail_title.replace("JEE", title)}\n')
            file.write(f'{tikz_render.replace("tikz.tex", files[nthtikz - 1])}\n')

        file.write(f'\\end{{document}}')



    try:
        print(os.getcwd)
        os.chdir("cd ./thumbnail")
        try:
            os.system("pdflatex -shell-escape main.tex")
        except:
            click.echo("Failed to rum pdflatex")
    except:
        click.echo("Failed to run cddir")












