## Estrutura Geral do Sistema:

### 1. Usuários (`UserFactory`, `NaturalPerson`, `LegalEntity`, `Users`):

- **Classe abstrata `Users`**:
  - Gerencia as operações comuns a todos os usuários (adicionar/remover produtos, carrinho, lista de desejos, autenticação, checkout).

- **`NaturalPerson` e `LegalEntity`**:
  - Herdam da classe `Users`.
  - Possuem validações específicas para CPF (Natural Person) e CNPJ (Legal Entity).

- **Factory (`UserFactory`)**:
  - Cria instâncias específicas de usuários com base em um tipo informado.

### 2. Produtos (`Product`, `ProductController`, `ProductView`):

- **Classe `Product` abstrata**:
  - Contém atributos principais (nome, descrição, categoria, preço, status) e métodos para gerenciar status, preço e disponibilidade.

- **Classe `ProductController`**:
  - Gerencia operações CRUD (Create, Read, Update, Delete) dos produtos cadastrados.

- **Classe `ProductView`**:
  - Responsável por exibir informações dos produtos, carrinho e lista de desejos.

### 3. Compras (`PurchaseController`):

- **Classe `PurchaseController`**:
  - Gerencia as operações relacionadas à compra, como adicionar/remover produtos do carrinho e realizar o checkout.

marketplace/
├── controllers/
│   ├── product_controller.py
│   ├── purchase_controller.py
│   └── marketplace_controller.py
├── models/
│   ├── product.py
│   ├── users.py
│   ├── natural_person.py
│   └── legal_entity.py
├── utils/
│   ├── validations.py
│   └── users_enum.py
├── views/
│   ├── product_view.py
│   └── user_view.py
└── main.py (interface do usuário)
