from latexgen.latex import (
    generate_table,
    generate_complete_document,
    save_to_file,
)


def create_advanced_example() -> None:
    data = [
        ["Python", "1991", "Гвидо ван Россум", "Высокий", "Динамическая"],
        ["Java", "1995", "Джеймс Гослинг", "Высокий", "Статическая"],
        ["JavaScript", "1995", "Брендан Эйх", "Высокий", "Динамическая"],
        ["C++", "1985", "Бьёрн Страуструп", "Высокий", "Статическая"],
        ["Go", "2009", "Google", "Средний", "Статическая"],
    ]

    header = [
        "Язык программирования",
        "Год создания",
        "Автор/Компания",
        "Уровень абстракции",
        "Типизация",
    ]

    column_spec = "{|p{3cm}|c|p{2.5cm}|c|p{2cm}|}"

    table = generate_table(
        data=data,
        header=header,
        column_spec=column_spec,
        caption="Сравнение языков программирования",
        label="tab:programming_languages",
        add_hline=True,
    )

    document = generate_complete_document(
        content=table,
        title="Сравнительный анализ языков программирования",
        author="Исследовательская группа",
        document_class="article",
        packages=["geometry", "hyperref"],
    )

    save_to_file(document, "/artifacts/app.tex")


def main() -> None:
    create_advanced_example()

    print("app.tex - полный документ")


if __name__ == "__main__":
    main()
