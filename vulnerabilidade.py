class Vulnerabilidade:
    def __init__(self, descricao: str, categoria: str, severidade: str, status: str):
        """
        Construtor da classe protegido pois começam com um underscore, indicando que são atributos privados.
        """
        self._descricao = descricao
        self._categoria = categoria
        self._status = status
        # Será validado com setter
        self.severidade = severidade

    @staticmethod
    def mapear_cor_severidade(severidade: str) -> str:
        """
        Método estático para mapear a severidade para uma cor.
        """
        mapping = {
            "Baixa": "🟢 Baixa",
            "Média": "🟡 Média",
            "Alta": "🟠 Alta",
            "Crítica": "🔴 Crítica"
        }
        return mapping.get(severidade.strip().capitalize(), "⚪ Desconhecida")
        
    @classmethod
    def criar_modelo_cve(cls, codigo_cve: str):
        """
        Método de classe para criar um modelo de vulnerabilidade a partir de um código CVE.
        """
        descricao = f"Vulnerabilidade associada ao código {codigo_cve.strip().upper()}"
        categoria = "Execução Remota de Código (RCE)"
        severidade = "Crítica"
        status = "Aberta"
        return cls(descricao, categoria, severidade, status)
        
    @property
    def severidade(self) -> str:
        return self._severidade
    
    @severidade.setter
    def severidade(self, novo_valor: str):
        """Valida o valor da severidade antes de atribuir."""
        valores_validos = ("Baixa", "Média", "Alta", "Crítica")
        valor_formatado = novo_valor.strip().capitalize()
        if valor_formatado not in valores_validos:
            raise ValueError(f"❌ Severidade inválida: '{novo_valor}'. Valores válidos são: {', '.join(valores_validos)}.")
        self._severidade = valor_formatado

    @property
    def descricao(self) -> str:
        return self._descricao
    @property
    def categoria(self) -> str:
        return self._categoria
    @property
    def status(self) -> str:
        return self._status
    
    #Transformação para JSON
    def to_dict(self) -> dict:
        """Converte a vulnerabilidade para um dicionário, facilitando a serialização para JSON."""
        return {
            "descricao": self._descricao,
            "categoria": self._categoria,
            "severidade": self._severidade,
            "status": self._status
        }
    