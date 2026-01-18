import os

from PIL import Image, ImageDraw, ImageFont
from latexgen.latex import (
    generate_complete_document,
    generate_figure,
    generate_table,
    save_to_file,
    compile_latex_to_pdf_simple
)


def create_sample_image():
    try:
        image_path = "./artifacts/sample_image.png"
        
        if not os.path.exists(image_path):
            img = Image.new('RGB', (400, 200), color='white')
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            text = "Пример изображения\nдля LaTeX\n(сгенерировано PIL)"
            draw.text((50, 50), text, fill='blue', font=font)

            draw.rectangle([10, 10, 390, 190], outline='red', width=2)
            
            img.save(image_path)
            print(f"Картинка создана: {image_path}")
            
        return image_path
        
    except ImportError:
        for ext in ['.png', '.jpg', '.jpeg', '.gif']:
            for file in os.listdir('./'):
                if file.lower().endswith(ext):
                    print(f"Найдена картинка: {file}")
                    return file
        return None


def generate_table_example():
    data = [
        ["Python", 1991, "Гвидо ван Россум", "Динамическая", "Высокий"],
        ["Java", 1995, "Джеймс Гослинг", "Статическая", "Высокий"],
        ["JavaScript", 1995, "Брендан Эйх", "Динамическая", "Высокий"],
        ["Go", 2009, "Google", "Статическая", "Средний"],
        ["Rust", 2010, "Graydon Hoare", "Статическая", "Низкий"]
    ]
    
    header = ["Язык", "Год", "Автор", "Типизация", "Уровень памяти"]
    
    alignments = ["l", "c", "l", "l", "c"]
    
    table = generate_table(
        data=data,
        header=header,
        column_alignments=alignments,
        caption="Сравнение современных языков программирования",
        label="tab:languages",
        add_hline=True,
        centered=True
    )
    
    return table


def generate_image_example(image_path):
    if not image_path or not os.path.exists(image_path):
        return "\\textbf{Изображение не найдено. Добавьте файл image.png в текущую директорию.}"
    
    figure = generate_figure(
        filepath=image_path,
        caption="Пример вставки изображения в LaTeX документ",
        label="fig:sample",
        width="0.6\\textwidth",
        scale=0.8,
        placement="h!",
        centered=True
    )
    
    return figure


def create_latex_document(table_content, image_content):
    content = f"""
    \\section{{Введение}}

    Этот документ демонстрирует возможности библиотеки \\texttt{{latexgen}} для генерации LaTeX кода.

    \\section{{Таблица языков программирования}}

    {table_content}

    \\section{{Пример изображения}}

    {image_content}

    \\section{{Заключение}}

    Документ был полностью сгенерирован с помощью Python библиотеки \\texttt{{latexgen}}.
    Таблица и изображение добавлены автоматически.
    """

    document = generate_complete_document(
        content=content,
        title="Пример PDF с таблицей и изображением",
        author="Студент",
        document_class="article",
        packages=["geometry"],
        add_graphics_package=True
    )
    
    return document


def main():
    print("=" * 60)
    print("Генерация PDF с таблицей и картинкой")
    print("Используется библиотека: latexgen")
    print("=" * 60)

    print("\n1. Подготовка изображения...")
    image_path = create_sample_image()
    
    if image_path and os.path.exists(image_path):
        print(f"Используем картинку: {image_path}")
    else:
        print("Картинка не найдена, будет только таблица")

    print("\n2. Генерация таблицы...")
    table = generate_table_example()
    print("Таблица сгенерирована")

    print("\n3. Генерация кода для изображения...")
    image = generate_image_example(image_path)
    print("Код изображения сгенерирован")

    print("\n4. Создание полного LaTeX документа...")
    document = create_latex_document(table, image)

    tex_filename = "./artifacts/artifact_with_table_and_image.tex"
    save_to_file(document, tex_filename)
    print(f"LaTeX файл сохранен: {tex_filename}")

    print("\n5. Компиляция в PDF...")
    print("   Этап может занять некоторое время...")
    
    compile_latex_to_pdf_simple(
        tex_file=tex_filename,
        output_dir="./artifacts"
    )
    
    pdf_filename = tex_filename.replace('.tex', '.pdf')
    print(f"PDF создан: {pdf_filename}")


if __name__ == "__main__":
    main()