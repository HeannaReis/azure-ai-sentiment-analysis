import os
import re

def list_images(directory):
    """
    Lista arquivos de imagem em um diretório, ordenando-os.
    Prioriza arquivos com um número seguido de '_' no início do nome (ex: '1_imagem.png').
    Para outros arquivos ou para desempate, usa a data de modificação.
    """
    files = []
    for f in os.listdir(directory):
        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
            files.append(f)

    def sort_key(filename):
        match = re.match(r'^(\d+)_', filename)
        if match:
            # Ordena por número (primário) e depois por data de modificação (secundário)
            return (int(match.group(1)), os.path.getmtime(os.path.join(directory, filename)))
        else:
            # Arquivos sem número vêm depois dos numerados, ordenados por data de modificação
            return (float('inf'), os.path.getmtime(os.path.join(directory, filename)))

    return sorted(files, key=sort_key)