import os
import glob
from typing import List, Tuple
from pathlib import Path
from config import Config  # Importe a classe Config

def ler_arquivos(diretorio_raiz: Path, extensoes: List[str]) -> Tuple[str, List[str]]:
    """
    Lê o conteúdo de todos os arquivos com as extensões especificadas a partir do diretório raiz.

    Args:
        diretorio_raiz: O diretório a partir do qual a busca será iniciada (Path object).
        extensoes: Uma lista de strings representando as extensões de arquivo a serem lidas (ex: ['.py', '.txt']).

    Returns:
        Uma tupla contendo:
        - Uma string contendo o conteúdo concatenado de todos os arquivos lidos.
        - Uma lista de strings representando os caminhos dos arquivos lidos.
        Retorna (None, []) se nenhum arquivo for encontrado.
    """
    conteudo_total = ""
    arquivos_lidos = []
    for extensao in extensoes:
        padrao_busca = os.path.join(diretorio_raiz.as_posix(), '**', f'*{extensao}')  # Busca recursiva
        arquivos = glob.glob(padrao_busca, recursive=True)

        for arquivo in arquivos:
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                    conteudo_total += f"\n\n--- Arquivo: {arquivo} ---\n\n" + conteudo
                    arquivos_lidos.append(arquivo)  # Adiciona o arquivo à lista
            except Exception as e:
                print(f"Erro ao ler o arquivo {arquivo}: {e}")

    return conteudo_total, arquivos_lidos


def main():
    """
    Função principal para ler os arquivos e enviar o conteúdo para a API Gemini.
    """
    diretorio_raiz = Config.BASE_DIR  # Use o diretório raiz definido na classe Config
    extensoes = ['.py', '.txt']

    conteudo_arquivos, lista_arquivos = ler_arquivos(diretorio_raiz, extensoes)

    if conteudo_arquivos:
        print("Conteúdo dos arquivos lidos com sucesso.")
        print("Arquivos lidos:")
        for arquivo in lista_arquivos:
            print(f"- {arquivo}")

        # Aqui você chamaria sua função para enviar 'conteudo_arquivos' para a API Gemini
        # Exemplo:
        # from services.gpt_services import GenerativeModelHandler
        # gemini_handler = GenerativeModelHandler(model_name="sua-model") # Substitua "sua-model"
        # resposta = gemini_handler.generate_content_from_text(conteudo_arquivos)
        # print(resposta)
    else:
        print("Nenhum arquivo encontrado com as extensões especificadas.")


if __name__ == "__main__":
    main()