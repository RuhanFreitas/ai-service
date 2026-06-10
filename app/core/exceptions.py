class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ProviderError(AppError):
    def __init__(self, message: str = "Erro ao gerar resposta com o provedor de IA.") -> None:
        super().__init__(message=message, status_code=502)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Chave de API inválida.") -> None:
        super().__init__(message=message, status_code=401)
