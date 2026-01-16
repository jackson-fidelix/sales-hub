# Sales Hub

Sistema de gerenciamento de vendas.

Projeto full-stack focado em registrar vendas com regras de negócio específicas, integração com API ViaCEP, busca de produtos e exibição dinâmica de itens/fornecedores.

**Status do Projeto**: Em desenvolvimento

## Tecnologias Utilizadas

- **Backend**: Python 3 + Django
- **Frontend**: JavaScript (fetch) + Bootstrap 5
- **Banco de Dados**: PostgreSQL
- **Integração Externa**: [ViaCEP](https://viacep.com.br/) (consulta automática de endereço por CEP)

## Funcionalidades Implementadas (Core do Desafio)

- Registro de vendas com campos obrigatórios:
  - Data da venda
  - Endereço de entrega completo (auto-preenchido via CEP)
  - Um ou mais produtos
  - Comprador
- Tela de venda com tabela dinâmica:
  - Adicionar/remover produtos
  - Exibição de nome, valor unitário e fornecedor(es)
  - Cálculo automático de subtotal
- Busca de produtos por nome na tela de consulta
- Consulta de CEP com preenchimento automático (rua, bairro, cidade, estado)
- Uma venda pode ter múltiplos produtos e múltiplos fornecedores por produto
- O cliente consegue ver seu histórico de compra

### Plus Implementados (ou em andamento)

- Sistema responsivo (Bootstrap)
- Validações de campo para se realizar uma venda (frontend + backend)
- Tela de login/autenticação de usuários
- Realizar e apresentar em uma documentação o resultado de Testes unitários

**Não implementado (fora do escopo do desafio)**: Cadastro de produtos e fornecedores (dados seedados via fixtures ou admin)

## Como Rodar o Projeto (Passo a Passo)

### Pré-requisitos

- Python 3.10+
- PostgreSQL instalado e rodando
- Git

### Instalação

1. Clone o repositório
   ```bash
   git clone https://github.com/jackson-fidelix/sales-hub.git
   cd sales-hub
