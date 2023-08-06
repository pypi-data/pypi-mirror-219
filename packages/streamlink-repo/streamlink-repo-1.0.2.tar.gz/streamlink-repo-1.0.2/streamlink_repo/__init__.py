import os
import sys
import json
import typer
import requests
from colorama import init, Fore
from urllib.parse import urljoin, urlparse
from PyInquirer import style_from_dict, Token, prompt, Separator
from .paths import USERDATA, DB_FOLDER
from .common import get_plugins_folder, download_file, clear_console, banner
init()

repos_file = os.path.join(DB_FOLDER, "repos.json")
repos_plugins_file = os.path.join(DB_FOLDER, "repos_plugins.json")
installed_file = os.path.join(DB_FOLDER, "installed.json")

if not os.path.exists(repos_file):
    open(repos_file, "w", encoding="utf-8").write("[]")

if not os.path.exists(repos_plugins_file):
    open(repos_plugins_file, "w", encoding="utf-8").write("[]")

if not os.path.exists(installed_file):
    open(installed_file, "w", encoding="utf-8").write("[]")

app = typer.Typer()
style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

@app.command()
def home():
    clear_console()
    banner()

    options = [
        {
            'type': 'list',
            'message': 'Select option',
            'name': 'options',
            'choices': [
                {
                    'name': 'Install',
                    'func': install_options
                },
                #{
                #    'name': 'Check for Updates',
                #    'func': check_for_updates
                #},
                {
                    'name': 'Uninstall',
                    'func': uninstall_list_installed
                },
                #{
                #    'name': 'Scan for issues',
                #    'func': scan
                #},
                {
                    'name': 'Settings',
                    'func': settings
                },
                {
                    'name': 'Exit',
                    'func': exit
                },
            ]
        }
    ]
    answer = prompt(options, style=style)
    selected_func = [item for item in options[0]["choices"] if item['name'] == answer['options']][0]['func']
    selected_func()



def install_options():
    clear_console()

    options = [
        {
            'type': 'list',
            'message': 'Select option',
            'name': 'options',
            'choices': [
                {
                    'name': 'Go Back',
                    'func': home
                },
                {
                    'name': 'Update Repos',
                    'func': update_repos,
                    'args': (install_options,)
                },
                {
                    'name': 'live',
                    'func': list_plugins,
                    'args': ('live',)
                },
                {
                    'name': 'vod',
                    'func': list_plugins,
                    'args': ('vod',)
                },
            ]
        }
    ]
    answer = prompt(options, style=style)
    picked = [item for item in options[0]["choices"] if item['name'] == answer['options']][0]
    if 'args' in picked:
        picked['func'](*picked['args'])
    else:
        picked['func']()



def list_plugins(t="live"):
    clear_console()

    repos_plugins = json.load(open(repos_plugins_file, encoding="utf-8"))
    installed = json.load(open(installed_file, encoding="utf-8"))
    installed = [f"{item['name']}-{item['author']}" for item in installed]
        
    options = [
        {
            'type': 'list',
            'message': 'Select option',
            'name': 'options',
            'choices': [
                {
                    'name': 'Go Back',
                    'func': install_options
                },
            ]
        }
    ]

    def already_installed():
        pass

    for plugin in repos_plugins:
        if t not in plugin["type"]:
            continue

        if f"{plugin['name']}-{plugin['author']}" in installed:
            options[0]['choices'].append({
                'name': f"[INSTALLED] {plugin['author']}'s {plugin['name']}",
                'func': already_installed
            })
            continue

        options[0]['choices'].append({
            'name': f"{plugin['author']}'s {plugin['name']}",
            'func': install,
            'args': (plugin['name'],)

        })

    answer = prompt(options, style=style)
    picked = [item for item in options[0]["choices"] if item['name'] == answer['options']][0]
    if 'args' in picked:
        picked['func'](*picked['args'])
    else:
        picked['func']()



def install(name):
    clear_console()

    repos_plugins = json.load(open(repos_plugins_file, encoding="utf-8"))
    installed = json.load(open(installed_file, encoding="utf-8"))

    for item in installed:
        if item['name'] == name:
            print("Already Installed")
            home()
            return

    plugin = next((item for item in repos_plugins if item['name'] == name), None)
    if not plugin:
        print("Plugin not found. You can try updating repos")
        home()
        return




    def install_deps(deps):
        pass




    #if plugin['deps']:
    if False: #TODO: finish this ...
        print(f'This plugin contains dependencies: {Fore.CYAN} {", ".join(plugin["deps"])} {Fore.WHITE}\n',
              f'Do you want to install them automatically? (WARNING: This option is in testing and may cause issues. ',
              f'It is recommended to install them manually.)')
        options = [
            {
                'type': 'list',
                'message': 'Select option',
                'name': 'options',
                'choices': [
                    {
                        'name': 'No (Recommended)',
                        'func': None,
                    },
                    {
                        'name': 'Yes (Not Recommended)',
                        'func': install_deps,
                    },
                ]
            }
        ]
        answer = prompt(options, style=style)
        picked = [item for item in options[0]["choices"] if item['name'] == answer['options']][0]
        if picked['func']:
            picked['func'](plugin['deps'])

    file_url = urljoin(plugin['from_url'], plugin['file'])
    parsed = urlparse(file_url)
    file_name = parsed.split("/")[-1] if "/" in plugin['file'] else plugin['file']
    download_file(
        url=file_url,
        destination=os.path.join(get_plugins_folder(), file_name)
    )
    installed.append(plugin)
    json.dump(installed, open(installed_file, "w", encoding="utf-8"))
    print(f"Successfully installed: {plugin['name']}")
    home()

def check_for_updates():
    clear_console()
    pass



def uninstall_list_installed():
    clear_console()
    installed = json.load(open(installed_file, encoding="utf-8"))
        
    options = [
        {
            'type': 'list',
            'message': 'Select option',
            'name': 'options',
            'choices': [
                {
                    'name': 'Go Back',
                    'func': home
                },
            ]
        }
    ]

    for plugin in installed:
        options[0]['choices'].append({
            'name': f"{plugin['author']}'s {plugin['name']}",
            'func': uninstall,
            'args': (plugin['name'],)
        })

    answer = prompt(options, style=style)
    picked = [item for item in options[0]["choices"] if item['name'] == answer['options']][0]
    if 'args' in picked:
        picked['func'](*picked['args'])
    else:
        picked['func']()


def uninstall(name):
    clear_console()

    installed = json.load(open(installed_file, encoding="utf-8"))

    plugin = next((item for item in installed if item['name'] == name), None)
    if not plugin:
        print("Plugin is not installed")
        home()
        return

    file_url = urljoin(plugin['from_url'], plugin['file'])
    parsed = urlparse(file_url)
    file_name = parsed.split("/")[-1] if "/" in plugin['file'] else plugin['file']
    os.remove(os.path.join(get_plugins_folder(), file_name))
    installed.remove(plugin)
    json.dump(installed, open(installed_file, "w", encoding="utf-8"))
    print(f"Successfully uninstalled: {plugin['name']}")
    home()



def scan():
    clear_console()
    pass


def settings():
    clear_console()
    options = [
        {
            'type': 'list',
            'message': 'Select option',
            'name': 'options',
            'choices': [
                {
                    'name': 'Go Back',
                    'func': home
                },
                {
                    'name': 'List repos',
                    'func': list_repos
                },
                {
                    'name': 'Update repos',
                    'func': update_repos
                },
                {
                    'name': 'Add repo',
                    'func': add_repo
                },
                {
                    'name': 'Scan repos',
                    'func': scan_repos
                },
                {
                    'name': 'Remove Repo',
                    'func': remove_repo
                },
            ]
        }
    ]

    answer = prompt(options, style=style)
    [item for item in options[0]["choices"] if item['name'] == answer['options']][0]['func']()


def list_repos():
    clear_console()
    repos = json.load(open(repos_file))
    print(Fore.RED+"\n".join(repos)+Fore.WHITE)
    input("Press enter to continue ...")
    settings()

def add_repo():
    clear_console()
    repos = json.load(open(repos_file, encoding="utf-8"))
    repo = input("Repo URL: ")
    repos.append(repo)
    json.dump(repos, open(repos_file, "w", encoding="utf-8"))
    settings()


def scan_repos():
    clear_console()
    repos = json.load(open(repos_file, encoding="utf-8"))
    broken = []
    for repo in repos:
        print(Fore.YELLOW+f"[*] {repo}", end="\r")
        try:
            resp = requests.get(urljoin(repo, "plugins.json"), timeout=10, allow_redirects=True)
            if resp.json()['name']:
                print(Fore.GREEN+f"[+] {repo}", end="\n")
                print(Fore.WHITE, end="")
                continue
            broken.append(repo)
            print(Fore.RED+f"[-] {repo}", end="\n")
            print(Fore.WHITE, end="")
        except:
            broken.append(repo)
            print(Fore.RED+f"[-] {repo}", end="\n")
            print(Fore.WHITE, end="")
    
    def remove_broken():
        nonlocal repos, broken
        repos = [item for item in repos if item not in broken]
        json.dump(repos, open(repos_file, "w", encoding="utf-8"))
        settings()
        return

    if not broken:
        input("Press enter to continue ...")
        settings()
        return

    options = [
        {
            'type': 'list',
            'message': 'Select option',
            'name': 'options',
            'choices': [
                {
                    'name': 'Keep Broken',
                    'func': settings
                },
                {
                    'name': 'Remove Broken',
                    'func': remove_broken
                },
            ]
        }
    ]

    answer = prompt(options, style=style)
    [item for item in options[0]["choices"] if item['name'] == answer['options']][0]['func']()
    settings()

def remove_repo():
    clear_console()
    repos = json.load(open(repos_file, encoding="utf-8"))
    options = [
        {
            'type': 'list',
            'message': 'Select option',
            'name': 'options',
            'choices': [
                {
                    'name': 'Go Back',
                    'func': settings
                },
            ]
        }
    ]

    for repo in repos:
        options[0]['choices'].append({'name': repo})

    answer = prompt(options, style=style)
    if answer['options'] == 'Go Back':
        settings()
        return
    
    repos.remove(answer['options'])
    json.dump(repos, open(repos_file, "w", encoding="utf-8"))
    settings()



def update_repos(ret=settings):
    clear_console()
    repos = json.load(open(repos_file, encoding="utf-8"))
    repos_plugins_json = []

    for repo in repos:
        print(Fore.YELLOW+f"[*] {repo}", end="\r")
        try:
            resp = requests.get(urljoin(repo, "plugins.json"), timeout=30, allow_redirects=True)
            repo_name = resp.json()['name']
            if repo_name:
                repo_plugins = resp.json()['plugins']
                for plugin in repo_plugins:
                    plugin["from"] = repo_name
                    plugin["from_url"] = repo


                repos_plugins_json.extend(repo_plugins)


                print(Fore.GREEN+f"[+] {repo}", end="\n")
                print(Fore.WHITE, end="")
                continue

            print(Fore.RED+f"[-] {repo}", end="\n")
            print(Fore.WHITE, end="")
        except:
            print(Fore.RED+f"[-] {repo}", end="\n")
            print(Fore.WHITE, end="")


    json.dump(repos_plugins_json, open(repos_plugins_file, "w", encoding="utf-8"))
    input("Press enter to continue ...")
    ret()


def main():
    clear_console()
    if len(sys.argv) > 1:
        app()
    else:
        home()

if __name__ == "__main__":
    main()
