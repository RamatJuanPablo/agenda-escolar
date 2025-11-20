def save_data(materias, notas, filename='data.json'):
    import json
    data = {'materias': materias, 'notas': notas}
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_data(filename='data.json'):
    import json
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data.get('materias', []), data.get('notas', [])
    except FileNotFoundError:
        return [], []
    except json.JSONDecodeError:
        return [], []