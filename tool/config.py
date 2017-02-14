NET = {
    'PROXY': {
        'ENABLE': True,
        'URL': '10.144.1.10:8080'
    }
}

LOG = {
    'ENABLE': True,
    'FILE': '/root/app/tool/maintenance.log',
    'SIZE': 1024 * 1024,
    'COUNT': 10
}

DB = {
    'URL': 'localhost:3306',
    'NAME': 'maintenance',
    'USER': 'root',
    'PASS': '!@mY0urF@th3r'
}

TABLE = {
    'NUM': 20
}
