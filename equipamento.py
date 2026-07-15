from enum import Enum
from vulnerabilidade import Vulnerabilidade

class TipoAtivo(Enum):
    NOTEBOOK = 1
    SERVIDOR = 2
    ROTEADOR = 3
    SOFTWARE_LICENCIADO = 4
    APLICACAO_WEB = 5
    BANCO_DE_DADOS = 6

class Equipamento:
    def __init__(self, id_ativo: int, hostname: str, responsavel: str, setor: str, tipo: TipoAtivo):
        """Classe que representa um equipamento de TI. Com encapsulamento dos atributos."""
        self._id = id_ativo
        self._hostname = hostname.strip()
        self.responsavel = responsavel
        self.setor = setor
        self._tipo = tipo
        self._vulnerabilidades = []  # Lista de vulnerabilidades associadas ao equipamento

    @staticmethod
    def validar_apenas_letras(texto: str) -> bool:
        """Valida se o texto contém apenas letras e espaços."""
        texto_limpo = texto.strip()
        return texto_limpo.replace(" ", "").isalpha()

    @property
    def id(self):
        return self._id
    
    @property
    def hostname(self):
        return self._hostname
    
    @property
    def responsavel(self):
        return self._responsavel
    
    @responsavel.setter
    def responsavel(self, novo_responsavel: str):
        if not Equipamento.validar_apenas_letras(novo_responsavel):
            raise ValueError("❌ O nome do responsável deve conter apenas letras e espaços.")
        self._responsavel = novo_responsavel.strip()
    
    @property
    def setor(self):
        return self._setor
    
    @setor.setter
    def setor(self, novo_setor: str):
        if not Equipamento.validar_apenas_letras(novo_setor):
            raise ValueError("❌ O nome do setor deve conter apenas letras e espaços.")
        self._setor = novo_setor.strip()

    @property
    def tipo(self):
        return self._tipo
    
    @property
    def vulnerabilidades(self) -> list:
       return self._vulnerabilidades

    def adicionar_vulnerabilidade(self, nova_vuln: Vulnerabilidade):
        if not isinstance(nova_vuln, Vulnerabilidade):
           raise TypeError("❌ Erro: O objeto deve ser uma instância da classe Vulnerabilidade.")
        self._vulnerabilidades.append(nova_vuln)

    def to_dict(self) -> dict:
        """Converte o objeto Equipamento em um dicionário para facilitar a serialização."""
        return {
            "id": self.id,
            "hostname": self.hostname,
            "responsavel": self.responsavel,
            "setor": self.setor,
            "tipo_codigo": self.tipo.value,  # Armazena o código do tipo de ativo (ex: 1 para Notebook, 2 para Servidor, etc.)
            "tipo_nome": self.tipo.name.capitalize(),  # Armazena o nome do tipo de ativo (ex: "Notebook", "Servidor", etc.)
            "vulnerabilidades": [vuln.to_dict() for vuln in self._vulnerabilidades]
        }
    
