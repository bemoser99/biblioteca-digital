# Como contribuir

## Fluxo de trabalho

Nunca trabalhe diretamente na branch `main`. Crie sempre uma branch separada:

    git checkout -b nome-da-feature

Exemplos: `feat/filtro-por-autor`, `fix/erro-renomear`, `docs/atualizar-readme`

## Commits

Use mensagens curtas e descritivas no formato:

    tipo: descrição do que foi feito

Tipos mais comuns: `feat`, `fix`, `docs`, `test`, `refactor`

Exemplos:

    feat: adicionar filtro de documentos por autor
    fix: corrigir erro ao renomear arquivo epub
    docs: atualizar exemplos no README
    test: adicionar teste para extensão inválida

## Enviando alterações

    git push origin nome-da-feature

Depois abra um Pull Request no GitHub, descreva o que foi feito e por quê.

## Antes de abrir o PR

Rode os testes e confirme que estão todos passando:

    python -m pytest tests/test_biblioteca.py -v
