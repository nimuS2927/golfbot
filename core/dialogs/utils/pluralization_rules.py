def pluralization(name: str):
    plural_rules = {
        'es': {
            'rules': ['s', 'sh', 'x', 'ch', 'ss', 'o'],
            'exception': ['piano', 'photo', 'radio', 'studio']
        },
        'ies': {
                'rules': ['by', 'cy', 'dy', 'fy', 'gy', 'hy', 'jy', 'ky', 'ly', 'my',
                         'ny', 'py', 'qy', 'ry', 'sy', 'ty', 'vy', 'wy', 'xy', 'zy'],
                'exception': []
            },
        'ves': {
            'rules': ['fe', 'f'],
            'exception': ['roof', 'belief', 'cliff', 'chief', 'cuff', 'handkerchief']
        },
        'exception': {
            'man': 'men',
            'woman': 'women',
            'foot': 'feet',
            'tooth': 'teeth',
            'goose': 'geese',
            'mouse': 'mice',
            'child': 'children',
            'person': 'people',
            'ox': 'oxen',
            'schema': 'schemes',
        }
    }
    if name in plural_rules['exception'].keys():
        return plural_rules['exception'][name]
    for key, value in plural_rules.items():
        if value.get('rules'):
            if name in value.get('exception'):
                return f'{name}s'
            for rule in value.get('rules'):
                if name.endswith(rule):
                    if key == 'es':
                        return f'{name}{key}'
                    elif key == 'ies':
                        return f'{name[:-1]}{key}'
                    elif key == 'ves':
                        return f'{name[:-1]}{key}' if rule == 'f' else f'{name[:-2]}{key}'
    return f'{name}s'