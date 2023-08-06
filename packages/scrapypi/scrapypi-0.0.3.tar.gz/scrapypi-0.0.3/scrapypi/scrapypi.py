import subprocess as sp

from .handler import *

__all__ = ['version', 'info', 'stats', 'main']


def version(name: str = None, url: str = None):
    '''
        Note: please use "info" instead to ensure result accuracy.
        only use this if your preference is speed.
    '''
    try:
        if name != None:
            url = f'https://pypi.org/project/{name}'
            
        module_name = url.split('/')

        module_name = [name for name in module_name if len(name) != 0][-1]

        sp.getoutput(f'wget -O {filename} {url}')

        with open(filename, 'r') as file:
            file = file.readlines()
            
            line = [line for line in file if f"{module_name} " in line and "title" not in line]
            line = line[0].strip()
            version = line.split()[-1]

            clean()
        return module_name, version
    except:
        ...


class stats:
    def __init__(self, name: str = None, url: str = None):
        dataset['with_mirrors'] = scan_stats(name, url, mode='a')
        dataset['without_mirrors'] = scan_stats(name, url, mode='s')

    def get_total(self):
        return get_total()
    
    def dataset(self):
        return dataset


def info(name: str = None, url: str = None):
    try:
        package_name(name, url)
        get_info()
    except:
        ...

    return info_data

def main():
    try:
        name = input('Package Name: ')
        statistics = stats(name)
        set = statistics.dataset()
        
        set_one = set['with_mirrors']
        set_two = set['without_mirrors']

        dates = set_one['dates']
        downloads = set_one['downloads']

        day = f"{dates[-1]}: {downloads[-1]:,}"
       
        week = 0
        for i in downloads[-7:]:
            week += i
        else:
            week = f"{week:,}"

        month = 0
        for i in downloads[-30:]:
            month += i
        else:
            month = f"{month:,}"

        result = f'''
{day}

Last 7 Days: {week}
Last 30 Days: {month}

Total Downloads: {statistics.get_total()['with_mirrors']:,}'''    
        print(result)
        
    except:
        print('No Result...')
        

if __name__ == '__main__':
    main()