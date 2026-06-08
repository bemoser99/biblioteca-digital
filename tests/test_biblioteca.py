import os
import sys
import shutil
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import biblioteca


class TestUtilitarios(unittest.TestCase):

    def test_obter_tipo_pdf(self):
        self.assertEqual(biblioteca.obter_tipo("artigo.pdf"), "PDF")

    def test_obter_tipo_epub(self):
        self.assertEqual(biblioteca.obter_tipo("livro.epub"), "EPUB")

    def test_obter_tipo_sem_extensao(self):
        self.assertEqual(biblioteca.obter_tipo("arquivo"), "DESCONHECIDO")

    def test_obter_ano_presente_no_nome(self):
        self.assertEqual(biblioteca.obter_ano("tese_2022_final.pdf"), "2022")

    def test_obter_ano_ausente(self):
        self.assertEqual(biblioteca.obter_ano("documento_sem_data.pdf"), "Ano não informado")

    def test_extensao_valida_pdf(self):
        self.assertTrue(biblioteca.garantir_extensao_valida("arquivo.pdf"))

    def test_extensao_invalida(self):
        self.assertFalse(biblioteca.garantir_extensao_valida("arquivo.mp3"))


class TestManipulacaoArquivos(unittest.TestCase):

    def setUp(self):
        self.dir_temp = tempfile.mkdtemp()
        for sub in ["pdf", "epub", "outros"]:
            os.makedirs(os.path.join(self.dir_temp, sub))
        self._base_original = biblioteca.DIRETORIO_BASE
        biblioteca.DIRETORIO_BASE = self.dir_temp

    def tearDown(self):
        shutil.rmtree(self.dir_temp)
        biblioteca.DIRETORIO_BASE = self._base_original

    def _criar_arquivo_temp(self, nome: str) -> str:
        caminho = os.path.join(self.dir_temp, nome)
        with open(caminho, "w") as f:
            f.write("conteúdo de teste")
        return caminho

    def test_adicionar_documento_valido(self):
        origem = self._criar_arquivo_temp("origem_teste.pdf")
        biblioteca.adicionar_documento(origem, "artigo_2023.pdf")
        destino = os.path.join(self.dir_temp, "pdf", "artigo_2023.pdf")
        self.assertTrue(os.path.exists(destino))

    def test_adicionar_extensao_invalida(self):
        origem = self._criar_arquivo_temp("musica.mp3")
        biblioteca.adicionar_documento(origem, "musica.mp3")
        destino = os.path.join(self.dir_temp, "outros", "musica.mp3")
        self.assertFalse(os.path.exists(destino))

    def test_adicionar_arquivo_inexistente(self):
        biblioteca.adicionar_documento("/caminho/inexistente/arquivo.pdf")

    def test_adicionar_duplicado_nao_sobrescreve(self):
        origem = self._criar_arquivo_temp("origem_dup.pdf")
        biblioteca.adicionar_documento(origem, "artigo_dup.pdf")
        biblioteca.adicionar_documento(origem, "artigo_dup.pdf")
        destino = os.path.join(self.dir_temp, "pdf", "artigo_dup.pdf")
        self.assertTrue(os.path.exists(destino))

    def test_renomear_documento_existente(self):
        origem = self._criar_arquivo_temp("para_renomear.pdf")
        biblioteca.adicionar_documento(origem, "para_renomear.pdf")
        biblioteca.renomear_documento("para_renomear.pdf", "renomeado_2021.pdf")
        self.assertTrue(os.path.exists(os.path.join(self.dir_temp, "pdf", "renomeado_2021.pdf")))
        self.assertFalse(os.path.exists(os.path.join(self.dir_temp, "pdf", "para_renomear.pdf")))

    def test_renomear_documento_inexistente(self):
        biblioteca.renomear_documento("nao_existe.pdf", "novo_nome.pdf")

    def test_renomear_extensao_invalida(self):
        origem = self._criar_arquivo_temp("valido.pdf")
        biblioteca.adicionar_documento(origem, "valido.pdf")
        biblioteca.renomear_documento("valido.pdf", "invalido.mp3")
        self.assertTrue(os.path.exists(os.path.join(self.dir_temp, "pdf", "valido.pdf")))

    def test_remover_documento_existente(self):
        origem = self._criar_arquivo_temp("para_remover.pdf")
        biblioteca.adicionar_documento(origem, "para_remover.pdf")
        caminho = os.path.join(self.dir_temp, "pdf", "para_remover.pdf")
        self.assertTrue(os.path.exists(caminho))
        os.remove(caminho)
        self.assertFalse(os.path.exists(caminho))

    def test_remover_documento_inexistente(self):
        biblioteca.remover_documento("fantasma.pdf")

    def test_criar_diretorio(self):
        biblioteca.criar_diretorio("revistas")
        self.assertTrue(os.path.isdir(os.path.join(self.dir_temp, "revistas")))

    def test_criar_diretorio_duplicado(self):
        biblioteca.criar_diretorio("revistas")
        biblioteca.criar_diretorio("revistas")

    def test_remover_diretorio_vazio(self):
        biblioteca.criar_diretorio("temp_vazio")
        biblioteca.remover_diretorio("temp_vazio")
        self.assertFalse(os.path.exists(os.path.join(self.dir_temp, "temp_vazio")))

    def test_remover_diretorio_nao_vazio(self):
        biblioteca.criar_diretorio("nao_vazio")
        arq = os.path.join(self.dir_temp, "nao_vazio", "arquivo.pdf")
        with open(arq, "w") as f:
            f.write("x")
        biblioteca.remover_diretorio("nao_vazio")
        self.assertTrue(os.path.isdir(os.path.join(self.dir_temp, "nao_vazio")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
