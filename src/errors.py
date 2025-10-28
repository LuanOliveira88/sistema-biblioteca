class BusinessRuleError(Exception):
    """
    Exceção para indicar violação de regras de negócio.

    Pode ser utilizada em serviços quando um requisito funcional
    não pode ser atendido, por exemplo:
    - Quantidade de exemplares inválida
    - Limite de livros emprestados excedido
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f'BusinessRuleError: {self.message}'
