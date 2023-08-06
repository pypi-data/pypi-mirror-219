import subprocess as sp

from sys import platform

windows = ['win32', 'windows']

def version(name: str = None, url: str = None):
    try:
        if name != None:
            url = f'https://pypi.org/project/{name}'
            
        module_name = url.split('/')

        module_name = [name for name in module_name if len(name) != 0][-1]
        filename = f"{module_name}.txt"

        sp.getoutput(f'wget -O {filename} {url}')

        with open(f'{module_name}.txt', 'r') as file:
            file = file.readlines()
            
            line = [line for line in file if f"{module_name} " in line and "title" not in line]
            line = line[0].strip()
            version = line.split()[-1]

        if platform not in windows:
            sp.getoutput(f'rm {filename}')
        else:
            sp.getoutput(f'del {filename}')
        
        return module_name, version
    except:
        ...


def main():
    try:
        url = input('Package Name: ')
        name, ver = version(url)
        print(f"{name}: {ver}")
    except:
        print('No Result...')
        

if __name__ == '__main__':
    main()