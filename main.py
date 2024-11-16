import flet as ft

from app.actions_column import Actions


def main(page: ft.Page):
    actions_col = Actions()

    page.add(
        ft.Container(
            ft.Row(
                [
                    actions_col,
                ],
            ),
            margin=10,
        )
    )

    page.window.width = 450
    page.window.height = 350
    page.window.resizable = False
    page.title = 'MPF Tools Converter'
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
