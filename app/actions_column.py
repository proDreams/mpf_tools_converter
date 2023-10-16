import flet as ft
import yaml

from app.utils import get_table, change_file


class Actions(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.table_col = get_table()
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.selected_files = ft.ListView(spacing=10)
        self.file_list = []
        self.default_directory = self.get_default_directory()
        self.done_text = ft.Container(
            ft.Text('Готово',
                    color=ft.colors.GREEN,
                    weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            visible=False
        )
        self.empty_files_text = ft.Container(
            ft.Text('Не выбраны файлы',
                    color=ft.colors.RED,
                    weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            visible=False
        )

    def change_files_action(self, e):
        if self.file_list:
            for file in self.file_list:
                change_file(file.path, self.table_col)
            self.empty_files_text.visible = False
            self.done_text.visible = True
            self.file_list = []
            self.selected_files.controls.clear()
        else:
            self.done_text.visible = False
            self.empty_files_text.visible = True
        self.update()

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        self.file_list = self.file_list + e.files

        for f in e.files:
            self.selected_files.controls.append(ft.Text(f.name))
        self.selected_files.update()

    def clear_files_list(self, e):
        self.file_list = []
        self.selected_files.controls.clear()
        self.selected_files.update()

    @staticmethod
    def get_default_directory():
        with open('settings.yaml') as f:
            conf = yaml.safe_load(f)
        if conf:
            return conf.get('default_directory')
        return None

    def build(self):
        return ft.Row(
            [
                ft.Column(
                    [
                        ft.Container(
                            ft.Text(value=f'{self.table_col[0][1]} ➔ {self.table_col[0][2]}',
                                    weight=ft.FontWeight.BOLD),
                            alignment=ft.alignment.center
                        ),
                        ft.Divider(),
                        ft.ElevatedButton(
                            "Выбрать файлы",
                            icon=ft.icons.UPLOAD_FILE,
                            on_click=lambda _: self.pick_files_dialog.pick_files(
                                allow_multiple=True,
                                allowed_extensions=['MPF'],
                                initial_directory=self.default_directory
                            ),
                        ),
                        ft.ElevatedButton(
                            "Очистить список",
                            icon=ft.icons.CLEAR,
                            on_click=self.clear_files_list,
                        ),
                        ft.Divider(),
                        ft.ElevatedButton(
                            "Конвертировать",
                            icon=ft.icons.CHANGE_CIRCLE,
                            on_click=self.change_files_action,
                        ),
                        self.empty_files_text,
                        self.done_text,
                    ],
                    width=200,
                    height=350,

                ),
                ft.Column(
                    [
                        ft.Container(
                            ft.Text('Выбранные файлы:', weight=ft.FontWeight.BOLD),
                            alignment=ft.alignment.center
                        ),
                        self.selected_files,
                        self.pick_files_dialog
                    ],
                    width=150,
                    scroll=ft.ScrollMode.AUTO,
                    height=350
                )
            ]
        )
