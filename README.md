biblioteca-digital
Sistema em Python para gerenciar o acervo digital de uma biblioteca universitária. Permite listar, adicionar, renomear e remover documentos via linha de comando.

Como usar
Listar documentos do acervo:
python biblioteca.py listar
python biblioteca.py listar --ordenar ano
Adicionar um documento:
python biblioteca.py adicionar caminho/do/arquivo.pdf
python biblioteca.py adicionar caminho/do/arquivo.pdf --nome novo_nome.pdf
Renomear:
python biblioteca.py renomear nome_atual.pdf novo_nome.pdf
Remover:
python biblioteca.py remover nome_do_arquivo.pdf
Criar ou remover uma pasta no acervo:
python biblioteca.py criar-dir revistas
python biblioteca.py remover-dir revistas

Testes
pip install pytest
python -m pytest tests/test_biblioteca.py -v

Formatos aceitos
.pdf .epub .docx .txt .mobi
