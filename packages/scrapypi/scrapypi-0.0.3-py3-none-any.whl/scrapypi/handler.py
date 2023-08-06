import os.path as path
import subprocess as sp

from sys import platform

directory = path.dirname(__file__)

filename = f'{directory}/temp.txt'

windows = ['win32', 'windows']

info_data = {
    'name': None,
	'author': None,
	'license': None,
	'summary': None,
	'version': '0.0.0',
    'downloads': 0
}

dataset = {
    'with_mirrors': None,
    'without_mirrors': None,
}

def clean():
    if platform not in windows:
            sp.getoutput(f'rm {filename}')
    else:
        sp.getoutput(f'del {filename}')

def get_total():
    total = {'with_mirrors': 0, 'without_mirrors': 0}
    
    for key in total:
        try:
            for i in range(len(dataset[key]['downloads'])):
                total[key] += dataset[key]['downloads'][i]
        except:
            ...
    else:
        return total
    
def get_info():
    sp.getoutput(f'wget -O {filename} https://pypistats.org/packages/{info_data["name"]}')

    with open(filename, 'r') as file:
        file = file.read()
        file = file.replace(file[:file.index(f'<h1>{info_data["name"]}</h1>')], '')
        portion  = file.replace(file[file.index('<script>'):], '')
        details = portion[portion.index('Author:'):]

        trim = details[details.index("Latest version:"):]
        
        details = details.replace(trim[trim.index('<br>'):], '').split('<br>')

        for detail in details:
            identity, value = detail.split(':')
            value = value.strip()

            identity = identity.strip().split()[-1].lower()
            info_data[identity] = value
        else:
            dataset['with_mirrors'] = with_mirrors(file)
            info_data['downloads'] = f'{get_total()["with_mirrors"]:,}'
    
    clean()



def package_name(name, url):
    name = name.lower()

    def default():
        if name != None:
            info_data['name'] = name
        
    if url != None:
        sp.getoutput(f'wget -O {filename} {url}')
            
        with open(filename, 'r') as file:
            lines = file.readlines()
            start = '<title>'
            end = '</title>'
            for line in lines:
                if start in line and end in line:
                    line = line.strip().removeprefix(start).removesuffix(end)
                    info_data['name'] = line.split(' · ')[0]
                    break
            else:
                default()
    else:
        default()

def get_data(text):
    data = text[text.index('"x":'):]
    data = data[:data.index('}')]

    return convert_str(data)


def convert_str(data):
    x = data[:data.index('],') + 1]
    y = data[data.index('],') + 2: ]
    
    dates = x.split(':')
    downloads = y.split(":")

    data = {}
    data['dates'] = dates[-1]
    data['downloads'] = downloads[-1]

    keys = ['dates', 'downloads']

    for key in keys:
        symbols = ['[', ']', '"']
        data_val = data[key]
        
        for symbol in symbols:
            data_val = data_val.replace(symbol, '')
        else:
            data[key] = [val.strip() for val in data_val.split(',')]			
    else:
        data['downloads'] = [int(download) for download in data['downloads']]
        return data


def with_mirrors(read_data):
    data = get_data(read_data)
    return data

def without_mirrors(read_data):
    data = get_data(read_data[read_data.index('Without_Mirrors'):])
    return data


def scan_stats(name: str = None, url: str = None, mode: str = 'a'):
    '''
    mode representation
    a - all :with_mirrors
    s - some :without_mirrors
    '''
    
    package_name(name, url)

    sp.getoutput(f'wget -O {filename} https://pypistats.org/packages/{info_data["name"]}')
        
    with open(filename, 'r') as file:
        file = file.read()

        clean()

        if mode == 'a':
            return with_mirrors(file)
        elif mode == 's':
            return without_mirrors(file)
    