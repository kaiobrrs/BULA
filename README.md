# BULA — Sistema de organização de medicamentos

Projeto em Python, executado pelo terminal e com armazenamento inicial
em arquivos `.txt`.

## Funcionalidades desta versão

- Cadastro de usuário e autenticação.
- Cadastro e listagem de medicamentos.
- Cadastro e consulta de horários associados aos medicamentos.
- Verificação de horários ativos e apresentação de lembretes no terminal.
- CRUD de medicamentos e horários: cadastrar, listar, editar e excluir registros.

## Estrutura

- `models/`: estrutura dos dados.
- `controllers/`: operações e regras do sistema.
- `database/`: contém `usuarios.txt`, `medicamentos.txt` e `horarios.txt`, já incluídos vazios no projeto. O sistema grava os registros nesses arquivos durante o uso.
- `utils/`: validações e funções auxiliares.
- `main.py`: inicialização e menu principal.

## Situação atual do código

O cadastro e a autenticação de usuários, o cadastro e a listagem de medicamentos,
o cadastro e a consulta de horários e a exibição de lembretes possuem implementação
para execução pelo terminal. Os lembretes são exibidos no terminal; não são enviados
ao celular.

## Limites de uso

O sistema apenas organiza informações fornecidas pelo usuário. Não recomenda
medicamentos, não calcula doses e não substitui uma prescrição ou orientação
de profissional de saúde.

## Equipe

Anderson Leite
Guilherme André
Kaio Barros
Lucas Rafael
Maria Laura

## Regras do CRUD

- Medicamentos e horários podem ser cadastrados, listados, editados e excluídos.
- Cada usuário visualiza e altera somente os próprios registros.
- Um medicamento com horários vinculados não pode ser excluído; primeiro exclua os horários associados.
