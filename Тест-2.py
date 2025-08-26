import flet as ft

def main(page: ft.Page):
    page.title = "Список покупок"
    page.window_width = 400
    page.window_height = 600

    # список для хранения элементов
    items = []

    # поле ввода
    new_item = ft.TextField(label="Введите товар", expand=True)
    qty_field = ft.TextField(label="Кол-во", width=80)

    # фильтр для отображения
    filter_value = "all"  # all / bought / not_bought

    # функция обновления списка
    def update_list():
        shopping_list.controls.clear()
        bought_count = 0
        for item in items:
            name, qty, checkbox = item

            # фильтрация
            if filter_value == "bought" and not checkbox.value:
                continue
            if filter_value == "not_bought" and checkbox.value:
                continue

            row = ft.Row(
                controls=[
                    checkbox,
                    ft.Text(f"{name} ({qty})"),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,  # исправлено
                        icon_color="red",
                        on_click=lambda e, item=item: delete_item(item)
                    )
                ]
            )
            shopping_list.controls.append(row)
            if checkbox.value:
                bought_count += 1

        counter.value = f"Куплено: {bought_count} / {len(items)}"
        counter.update()
        shopping_list.update()

    # добавление товара
    def add_item(e):
        if new_item.value.strip():
            checkbox = ft.Checkbox(
                value=False,
                on_change=lambda e: update_list()
            )
            items.append((new_item.value, qty_field.value or "1", checkbox))
            new_item.value = ""
            qty_field.value = ""
            new_item.update()
            qty_field.update()
            update_list()

    # удаление товара
    def delete_item(item):
        items.remove(item)
        update_list()

    # фильтр
    def change_filter(e):
        nonlocal filter_value
        filter_value = e.control.value
        update_list()

    # кнопка добавления
    add_button = ft.ElevatedButton("Добавить", on_click=add_item)

    # список покупок
    shopping_list = ft.Column()

    # счетчик
    counter = ft.Text("Куплено: 0 / 0")

    # фильтры
    filter_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("all", "Все"),
            ft.dropdown.Option("bought", "Купленные"),
            ft.dropdown.Option("not_bought", "Некупленные")
        ],
        value="all",
        on_change=change_filter
    )

    # компоновка
    page.add(
        ft.Row([new_item, qty_field, add_button]),
        ft.Row([ft.Text("Фильтр:"), filter_dropdown]),
        counter,
        shopping_list
    )


ft.app(target=main)
