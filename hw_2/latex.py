from typing import List, Optional, Union
import os
import subprocess


def escape_latex(text: str) -> str:
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }

    result = str(text)
    for char, repl in replacements.items():
        result = result.replace(char, repl)
    return result


def wrap_in_brackets(content: str) -> str:
    return f"{{{content}}}"


def join_with_separator(items: List[str], separator: str) -> str:
    return separator.join(items)


def make_cell(content: str, escape: bool = True) -> str:
    value = escape_latex(content) if escape else content
    return wrap_in_brackets(value)


def make_cells(row: List[Union[str, int, float]], escape: bool = True) -> List[str]:
    return [make_cell(str(cell), escape) for cell in row]


def make_row(cells: List[str], separator: str = " & ") -> str:
    return join_with_separator(cells, separator) + r" \\"


def make_hline() -> str:
    return r"\hline"


def make_column_spec(
    specs: Optional[List[str]] = None,
    default: str = "c",
    alignment: Optional[str] = None,
) -> str:
    if specs:
        return "{" + "".join(specs) + "}"
    if alignment:
        return "{" + alignment + "}"
    return "{" + default + "}"


def generate_table(
    data: List[List[Union[str, int, float]]],
    caption: Optional[str] = None,
    label: Optional[str] = None,
    column_alignments: Optional[List[str]] = None,
    header: Optional[List[str]] = None,
    escape_content: bool = True,
    add_hline: bool = True,
    centered: bool = True,
    column_spec: Optional[str] = None,
) -> str:
    if not data:
        raise ValueError("Данные таблицы не могут быть пустыми")

    columns = len(data[0])
    for row in data:
        if len(row) != columns:
            raise ValueError("Все строки должны иметь одинаковую длину")

    if column_spec:
        col_spec = column_spec
    elif column_alignments:
        if len(column_alignments) != columns:
            raise ValueError("Неверное количество выравниваний столбцов")
        col_spec = make_column_spec(column_alignments)
    else:
        col_spec = make_column_spec(["c"] * columns)

    lines = []

    if header:
        if len(header) != columns:
            raise ValueError("Неверное количество заголовков")
        lines.append(make_row(make_cells(header, escape_content)))
        if add_hline:
            lines.append(make_hline())

    for row in data:
        lines.append(make_row(make_cells(row, escape_content)))

    if add_hline:
        lines.append(make_hline())

    body = "\n        ".join(lines)

    table = f"""\\begin{{table}}{"[h!]" if centered else ""}
    \\centering
    \\begin{{tabular}}{col_spec}
        {body}
    \\end{{tabular}}"""

    if caption:
        table += f"\n    \\caption{{{escape_latex(caption)}}}"
    if label:
        table += f"\n    \\label{{{label}}}"

    table += "\n\\end{table}"

    return table


def generate_image(
    filepath: str,
    caption: Optional[str] = None,
    label: Optional[str] = None,
    width: Optional[str] = None,
    height: Optional[str] = None,
    scale: Optional[float] = None,
    centered: bool = True,
) -> str:
    if not filepath:
        raise ValueError("Путь к файлу не может быть пустым")

    options = []
    if width:
        options.append(f"width={width}")
    if height:
        options.append(f"height={height}")
    if scale:
        options.append(f"scale={scale}")

    opt = f"[{','.join(options)}]" if options else ""

    code = ""
    if centered:
        code += "\\centering\n"

    code += f"\\includegraphics{opt}{{{filepath}}}"

    if caption:
        code += f"\n\\caption{{{escape_latex(caption)}}}"
    if label:
        code += f"\n\\label{{{label}}}"

    return code


def generate_figure(
    filepath: str,
    caption: Optional[str] = None,
    label: Optional[str] = None,
    width: Optional[str] = None,
    height: Optional[str] = None,
    scale: Optional[float] = None,
    placement: str = "h!",
    centered: bool = True,
) -> str:
    image_code = generate_image(
        filepath=filepath,
        width=width,
        height=height,
        scale=scale,
        centered=False,
    )

    figure = f"""\\begin{{figure}}[{placement}]
    \\centering
    {image_code}"""

    if caption:
        figure += f"\n    \\caption{{{escape_latex(caption)}}}"
    if label:
        figure += f"\n    \\label{{{label}}}"

    figure += "\n\\end{figure}"

    return figure


def generate_complete_document(
    content: str,
    title: Optional[str] = None,
    author: Optional[str] = None,
    document_class: str = "article",
    packages: List[str] = None,
    add_graphics_package: bool = True,
) -> str:
    if packages is None:
        packages = []

    base_packages = ["amsmath", "amssymb", "booktabs"]
    if add_graphics_package:
        base_packages.append("graphicx")

    used_packages = []
    for pkg in base_packages + packages:
        if pkg not in used_packages:
            used_packages.append(pkg)

    preamble = "\n".join(f"\\usepackage{{{p}}}" for p in used_packages)

    title_block = ""
    if title:
        title_block += f"\\title{{{escape_latex(title)}}}\n"
    if author:
        title_block += f"\\author{{{escape_latex(author)}}}\n"
    if title_block:
        title_block += "\\maketitle\n\n"

    return f"""\\documentclass{{{document_class}}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T2A]{{fontenc}}
\\usepackage[english, russian]{{babel}}

{preamble}

\\begin{{document}}

{title_block}{content}

\\end{{document}}"""


def save_to_file(content: str, filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def compile_latex_to_pdf_simple(
    tex_file: str,
    output_dir: str = ".",
    latex_engine: str = "pdflatex",
    runs: int = 2,
) -> bool:
    try:
        os.makedirs(output_dir, exist_ok=True)

        for _ in range(runs):
            subprocess.run(
                [
                    latex_engine,
                    "-interaction=nonstopmode",
                    "-output-directory",
                    output_dir,
                    tex_file,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        pdf_path = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(tex_file))[0] + ".pdf",
        )

        return os.path.exists(pdf_path)

    except Exception:
        return False
