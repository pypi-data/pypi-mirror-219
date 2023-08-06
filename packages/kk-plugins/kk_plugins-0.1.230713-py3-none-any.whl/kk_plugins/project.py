import os

import requests
from jinja2 import Template


class StartProject:
    def __init__(self):
        self.__dir = os.getcwd()
        self.__create_github_dir()
        self.__create_workflows_dir()
        self.__create_gitignore()
        self.__create_license()
        self.__create_readme()
        self.__create_git_hook()

    def __create_github_dir(self):
        github_dir = os.path.join(self.__dir, '.github')
        if not os.path.exists(github_dir):
            os.mkdir(github_dir)

    def __create_workflows_dir(self):
        workflows_dir = os.path.join(self.__dir, '.github', 'workflows')
        if not os.path.exists(workflows_dir):
            os.mkdir(workflows_dir)

    def __create_gitignore(self):
        file_path = os.path.join(self.__dir, '.gitignore')
        if not os.path.exists(file_path):
            with open(file_path, 'a+', encoding='utf-8') as f:
                f.write('.idea\n')

    def __create_license(self):
        file_path = os.path.join(self.__dir, 'LICENSE')
        if not os.path.exists(file_path):
            with open(file_path, 'a+', encoding='utf-8') as f:
                f.write('MIT License\n')

    def __create_readme(self):
        file_path = os.path.join(self.__dir, 'README.md')
        if not os.path.exists(file_path):
            with open(file_path, 'a+', encoding='utf-8') as f:
                f.write('# {name}\n'.format(name=os.path.basename(self.__dir)))

    def __create_git_hook(self):
        git_dir = os.path.join(self.__dir, '.git')
        if not os.path.exists(git_dir):
            os.system('git init')
        hook_dir = os.path.join(self.__dir, '.git', 'hooks')
        if not os.path.exists(hook_dir):
            os.mkdir(hook_dir)
        file_path = os.path.join(hook_dir, 'pre-commit')
        if not os.path.exists(file_path):
            res = requests.get(
                'https://gist.githubusercontent.com/wgnpj2cg/bc4ffb641cebfc76eb90dfdef2929427/raw/fa69f61dac913c932676049d00807e55f45c29d1/pre-commit').text
            with open(file_path, 'a+', encoding='utf-8') as f:
                f.write(res)

    def create_python(self):
        # github workflows
        tmpl = Template(requests.get(
            'https://gist.githubusercontent.com/wgnpj2cg/479177b348504da61547df1d3925bb9e/raw/2bce40d40ead26585ac4bd473b3289e581b0699d/python_docker_build_publish.tpl').text).render()

        with open(os.path.join(self.__dir, '.github', 'workflows', 'python_docker_build_publish.yaml'), 'a+') as f:
            f.write(tmpl)

        # dockerfile
        with open(os.path.join(self.__dir, "Dockerfile"), "w+") as fn:
            fn.write(requests.get(
                'https://gist.githubusercontent.com/wgnpj2cg/479177b348504da61547df1d3925bb9e/raw/436b447c418e586677f9fa9515631b65db4643ab/python_docker').text)

        # start.py
        start_file = os.path.join(self.__dir, 'src', 'start.py')
        if not os.path.exists(start_file):
            with open(start_file, 'a+', encoding='utf-8') as f:
                f.write(requests.get(
                    'https://gist.githubusercontent.com/wgnpj2cg/479177b348504da61547df1d3925bb9e/raw/006ce2db2b8ed4df407863afd5fbb391cb59431b/start.py').text)
