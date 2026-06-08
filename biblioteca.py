import os
import shutil
import argparse
from datetime import datetime

DIRETORIO_BASE = os.path.join(os.path.dirname(__file__), "acervo")
EXTENSOES_VALIDAS = {".pdf", ".epub", ".docx", ".txt", ".mobi"}


def obter_tipo(nome_arquivo: str) -> str:
    _, ext = os.path.splitext(nome_arquivo)
    return ext.upper().lstrip(".") if ext else "DESCONHECIDO"


def obter_ano(nome_arquivo: str) -> str:
    partes = nome_arquivo.replace("_", " ").replace("-", " ").split()
    for parte in partes:
        if parte.isdigit() and len(parte) == 4:
            ano = int(parte)
            if 1900 <= ano <= datetime.now().year:
                return str(ano)
    return "Ano não informado"


def garantir_extensao_valida(nome_arquivo: str) -> bool:
    _, ext = os.path.splitext(nome_arquivo)
    return ext.lower() in EXTENSOES_VALIDAS


def caminho_completo(nome_arquivo: str) -> str:
    tipo = obter_tipo(nome_arquivo).lower()
    subpasta = tipo if tipo in {"pdf", "epub"} else "outros"
    return os.path.join(DIRETORIO_BASE, subpasta, nome_arquivo)


def listar_documentos(ordenar_por: str = "tipo") -> None:
    documentos = []
    for subpasta in os.listdir(DIRETORIO_BASE):
        caminho_subpasta = os.path.join(DIRETORIO_BASE, subpasta)
        if not os.path.isdir(caminho_subpasta):
            continue
        for arquivo in os.listdir(caminho_subpasta):
            caminho_arq = os.path.join(caminho_subpasta, arquivo)
            if os.path.isfile(caminho_arq):
                documentos.append({
                    "nome": arquivo,
                    "tipo": obter_tipo(arquivo),
                    "ano": obter_ano(arquivo),
                    "tamanho_kb": round(os.path.getsize(caminho_arq) / 1024, 2),
                })
    if not documentos:
        print("\n  Nenhum documento encontrado no acervo.\n")
        return
    chave = "tipo" if ordenar_por == "tipo" else "ano"
    documentos.sort(key=lambda d: d[chave])
    print(f"\n{'='*60}")
    print(f"  ACERVO DIGITAL  —  ordenado por {ordenar_por.upper()}")
    print(f"{'='*60}")
    print(f"  {'Nome':<35} {'Tipo':<8} {'Ano':<20} {'KB':>6}")
    print(f"  {'-'*55}")
    for doc in documentos:
        print(f"  {doc['nome']:<35} {doc['tipo']:<8} {doc['ano']:<20} {doc['tamanho_kb']:>6}")
    print(f"\n  Total: {len(documentos)} documento(s)\n")


def adicionar_documento(origem: str, nome_destino: str = None) -> None:
    if not os.path.isfile(origem):
        print(f"  ERRO: Arquivo '{origem}' não encontrado.")
        return
    nome = nome_destino if nome_destino else os.path.basename(origem)
    if not garantir_extensao_valida(nome):
        exts = ", ".join(EXTENSOES_VALIDAS)
        print(f"  ERRO: Extensão não permitida. Use: {exts}")
        return
    destino = caminho_completo(nome)
    if os.path.exists(destino):
        print(f"  AVISO: Já existe um documento com o nome '{nome}'. Operação cancelada.")
        return
    shutil.copy2(origem, destino)
    print(f"  OK: '{nome}' adicionado ao acervo com sucesso.")


def renomear_documento(nome_atual: str, novo_nome: str) -> None:
    if not garantir_extensao_valida(novo_nome):
        exts = ", ".join(EXTENSOES_VALIDAS)
        print(f"  ERRO: Extensão não permitida. Use: {exts}")
        return
    origem = caminho_completo(nome_atual)
    destino = caminho_completo(novo_nome)
    if not os.path.exists(origem):
        print(f"  ERRO: Documento '{nome_atual}' não encontrado no acervo.")
        return
    if os.path.exists(destino):
        print(f"  AVISO: Já existe um documento com o nome '{novo_nome}'. Operação cancelada.")
        return
    os.rename(origem, destino)
    print(f"  OK: '{nome_atual}' renomeado para '{novo_nome}' com sucesso.")


def remover_documento(nome_arquivo: str) -> None:
    caminho = caminho_completo(nome_arquivo)
    if not os.path.exists(caminho):
        print(f"  ERRO: Documento '{nome_arquivo}' não encontrado no acervo.")
        return
    confirmacao = input(f"  Confirma a remoção de '{nome_arquivo}'? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("  Operação cancelada.")
        return
    os.remove(caminho)
    print(f"  OK: '{nome_arquivo}' removido do acervo.")


def criar_diretorio(nome: str) -> None:
    caminho = os.path.join(DIRETORIO_BASE, nome)
    if os.path.exists(caminho):
        print(f"  AVISO: O diretório '{nome}' já existe.")
        return
    os.makedirs(caminho)
    print(f"  OK: Diretório '{nome}' criado.")


def remover_diretorio(nome: str) -> None:
    caminho = os.path.join(DIRETORIO_BASE, nome)
    if not os.path.exists(caminho):
        print(f"  ERRO: Diretório '{nome}' não encontrado.")
        return
    if os.listdir(caminho):
        print(f"  ERRO: O diretório '{nome}' não está vazio. Remova os arquivos antes.")
        return
    os.rmdir(caminho)
    print(f"  OK: Diretório '{nome}' removido.")


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="biblioteca",
        description="Sistema de Gerenciamento de Biblioteca Digital",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    p_listar = subparsers.add_parser("listar", help="Lista todos os documentos do acervo")
    p_listar.add_argument("--ordenar", choices=["tipo", "ano"], default="tipo")

    p_add = subparsers.add_parser("adicionar", help="Adiciona um documento ao acervo")
    p_add.add_argument("origem", help="Caminho do arquivo a ser adicionado")
    p_add.add_argument("--nome", default=None)

    p_ren = subparsers.add_parser("renomear", help="Renomeia um documento no acervo")
    p_ren.add_argument("nome_atual")
    p_ren.add_argument("novo_nome")

    p_rem = subparsers.add_parser("remover", help="Remove um documento do acervo")
    p_rem.add_argument("nome")

    p_cdir = subparsers.add_parser("criar-dir", help="Cria um novo diretório no acervo")
    p_cdir.add_argument("nome")

    p_rdir = subparsers.add_parser("remover-dir", help="Remove um diretório vazio do acervo")
    p_rdir.add_argument("nome")

    return parser


def main() -> None:
    parser = construir_parser()
    args = parser.parse_args()

    if args.comando == "listar":
        listar_documentos(ordenar_por=args.ordenar)
    elif args.comando == "adicionar":
        adicionar_documento(args.origem, args.nome)
    elif args.comando == "renomear":
        renomear_documento(args.nome_atual, args.novo_nome)
    elif args.comando == "remover":
        remover_documento(args.nome)
    elif args.comando == "criar-dir":
        criar_diretorio(args.nome)
    elif args.comando == "remover-dir":
        remover_diretorio(args.nome)


if __name__ == "__main__":
    main()
