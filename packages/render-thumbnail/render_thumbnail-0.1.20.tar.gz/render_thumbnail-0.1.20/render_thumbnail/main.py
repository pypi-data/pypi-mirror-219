import click
import os
from .functions_tex import extract_tex_env
from .functions_tex import files as file_list
import re


thumbnail_title=r"""
\vspace*{\fill}
\begin{center}
\Huge{\textbf{JEE}}\\
\texttt{\textbf{[YEAR]}}
\end{center}
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

def extract_year(inputfile):
    with open(inputfile, 'r') as f:
        for line in f:
            x = re.findall('^\\\\def\\\\year\{.{4}', line)
            if x:
                year = x[0].split('{')[1].split('}')[0]
                return year
            else:
                return '1998'


def extract_exam(inputfile):
    with open(inputfile, 'r') as f:
        for line in f:
            x = re.findall('^\\\\def\\\\exam\{.{2,}', line)
            if x:
                exam = x[0].split('{')[1].split('}')[0]
                return exam









@click.command(
        help="Extracts tikzpicture environment from tex file and renders thumbnail."
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
@click.option(
        '-s',
        '--scale',
        type=click.FLOAT,
        default=1,
        show_default=True,
        help='Scale factor for the tikz picture'
        )
@click.option(
        '-w',
        '--line_width',
        type=click.FLOAT,
        default=1,
        show_default=True,
        help='Line width for the diagram'
        )
@click.option(
        '-c',
        '--color',
        type=click.STRING,
        default="black",
        show_default=True,
        help='Color for the thumbnail'
        )
def main(inputfile, outputfile, environment, title, nthtikz, scale, line_width, color):
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
        file.write(f'\\vgeometry[8][4.5][0]\n')

        file.write(f'\\begin{{document}}\n')
        print(files)

        file.write(f'{thumbnail_title.replace("JEE", extract_exam(inputfile)).replace("YEAR", extract_year(inputfile))}\n')
        file.write(f'\\begin{{center}}\n')
        with open(f'{path_tikz}/thumbnail/{files[nthtikz-1]}', 'r') as f:
            for i, line in enumerate(f):
                if i == 1:
                    file.write(f'[scale={scale}, line width={line_width} mm, cap=round, {color}]\n')
                    if not re.findall('^\[', line):
                        file.write(line)
                else:
                    file.write(line)


        file.write(f'\\end{{center}}\n')
        file.write(f'\\vspace*{{\\fill}}\n\n')
        file.write(f'\\end{{document}}')



    try:
        os.chdir("./thumbnail")
        try:
            os.system("pdflatex -shell-escape main.tex")
            try:
                os.system("vbpdf topng")
                try:
                    os.system("qlmanage -p main.png")
                except:
                    click.echo("Failed to preview the png file.")
            except:
                click.echo("Failed to convert png ")
        except:
            click.echo("Failed to rum pdflatex")
    except:
        click.echo("Failed to run cddir")












