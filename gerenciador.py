from equipamento import Equipamento, TipoAtivo
from vulnerabilidade import Vulnerabilidade
from Cyber_ativos.persistencia import PersistenciaInventario

class GerenciadorInventario:
    def __init__(self, persistencia: PersistenciaInventario):
        """recebe qualquer classe 
        que implemente a interface abstrata PersistenciaInventario."""
        self._persistencia = persistencia
        self._ativos = {} # Dicionário para armazenar os equipamentos, chave: id_ativo, valor: Equipamento
        self.carregar_dados()

    @property
    def ativos(self) -> dict:
        return self._ativos
    
    def carregar_dados(self):
        """Lê os dados usando a classe abstrata de persistência polimórfica e reconstrói na memória."""
        try:
            # O polimorfismo acontece aqui: não sabemos a tecnologia de armazenamento utilizada
            dados_json = self._persistencia.carregar()
            self._ativos.clear()

            if not dados_json:
                return  

            for item in dados_json:
                tipo_enum = TipoAtivo(item["tipo_codigo"])
                equipamento = Equipamento(
                    id_ativo=item["id"],
                    hostname=item["hostname"],
                    responsavel=item["responsavel"],
                    setor=item["setor"],
                    tipo=tipo_enum
                )
                # Reconstruindo as vulnerabilidades associadas
                for vuln_data in item.get("vulnerabilidades", []):
                    vuln = Vulnerabilidade(
                        descricao=vuln_data["descricao"],
                        categoria=vuln_data["categoria"],
                        severidade=vuln_data["severidade"],
                        status=vuln_data["status"]
                    )
                equipamento.adicionar_vulnerabilidade(vuln)

            self._ativos[equipamento.id] = equipamento # Adiciona o equipamento ao dicionário de ativos e faz a busca pelo ID do equipamento
        except Exception as e:
            print(f"⚠️ Erro ao carregar os dados: {e}")


    def salvar_dados(self):
        """Converte os objetos em dicionários e salva no arquivo JSON."""
        try:
            # Transforma cada objeto Equipamento no dicionário estruturado usando o método to_dict()
            lista_para_salvar = [ativo.to_dict() for ativo in self._ativos.values()]

            # O polimorfismo acontece aqui: o gerenciador apenas delega a gravação
            self._persistencia.salvar(lista_para_salvar)
        except Exception as e:
            print(f"❌ Erro ao salvar os dados no arquivo: {e}")


    # ==============
    # Funções de CRUD
    # ==============

    def cadastrar_equipamento(self, equipamento: Equipamento) -> bool:
        """Adiciona um novo equipamento se o ID não estiver em uso. Retorna True se o cadastro for bem-sucedido, False caso contrário."""
        if equipamento.id in self._ativos:
            return False # ID Duplicado, não cadastra
        
        self._ativos[equipamento.id] = equipamento
        self.salvar_dados() # Salva os dados após o cadastro
        return True
    
    
    def buscar_por_id(self, in_ativo: int) -> Equipamento:
        """Busca um equipamento no inventário pelo ID instanteneamente com a tabela hash do dicionário. Retorna o objeto Equipamento ou None se não encontrado."""
        return self._ativos.get(in_ativo, None)  # Retorna None se o ID não estiver presente no dicionário
    
    def obter_todos_equipamentos(self) -> tuple:
        """Retorna uma lista de todos os equipamentos cadastrados."""
        return tuple(self._ativos.values())
    
    def atualizar_equipamento(self, id_ativo: int, novo_hostname: str,novo_responsavel: str, novo_setor: str,) -> bool:
        """Atualiza os dados de um equipamento existente. Retorna True se a atualização for bem-sucedida, False caso contrário."""
        ativo = self.buscar_por_id(id_ativo)
        if not ativo:
            return False  # Equipamento não encontrado
        ativo.responsavel = novo_responsavel
        ativo.setor = novo_setor
        ativo._hostname = novo_hostname.strip()
        self.salvar_dados()  # Salva os dados após a atualização
        return True
    
    def deletar_equipamento(self, id_ativo: int) -> bool:
        """[D]elete: Remove um equipamento do inventário pelo ID. Retorna True se a remoção for bem-sucedida, False caso contrário."""
        if id_ativo not in self._ativos:
            return False
        del self._ativos[id_ativo]
        self.salvar_dados()  # Salva os dados após a remoção
        return True