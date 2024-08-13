import os
import argparse
import shutil


def get_full_path(path, new_name):
    return os.path.join(path, new_name)


def init_project(project_name, project_path):
    init_project_path = get_full_path(project_path, project_name)
    os.mkdir(init_project_path)

    routers_folder_path = get_full_path(init_project_path, 'routers')
    os.mkdir(routers_folder_path)

    schemes_folder_path = get_full_path(init_project_path, 'schemes')
    os.mkdir(schemes_folder_path)

    app_path = get_full_path(init_project_path, 'app.py')
    with open(app_path, 'w') as file:
        ...

    init_py_path = get_full_path(init_project_path, '__init__.py')
    with open(init_py_path, 'w') as file:
        ...

    settings_py_path = get_full_path(init_project_path, 'settings.py')
    with open(settings_py_path, 'w') as file:
        ...

    routers_init_path = get_full_path(routers_folder_path, '__init__.py')
    with open(routers_init_path, 'w') as file:
        ...

    schemes_init_path = get_full_path(schemes_folder_path, '__init__.py')
    with open(schemes_init_path, 'w') as file:
        ...


def create_example_project(path: str):
    if not path.endswith('/'):
        path += '/'

    path += 'example'

    shutil.copytree('example_project', path)

def main():
    parser = argparse.ArgumentParser(description="Управление приложениями и проектами.")
    subparsers = parser.add_subparsers(dest='command', required=True, help='Команда для выполнения')

    init_project_parser = subparsers.add_parser('init', help='Инициализация проекта')
    init_project_parser.add_argument('project_name', help="Имя создаваемого проекта")
    init_project_parser.add_argument('project_path', help="Путь, по которому будет создан проект")
    
    create_example = subparsers.add_parser('create_example', help='Create project with examples')
    create_example.add_argument('path', help='Project path')

    args = parser.parse_args()

    if args.command == 'init':
        init_project(args.project_name, args.project_path)
    elif args.command == 'create_example':
        create_example_project(args.path)


if __name__ == "__main__":
    main()
