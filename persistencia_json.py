import json
import os
from Cyber_ativos.persistencia import PersistenciaInventario

class PersistenciaJSON(PersistenciaInventario):
    def __init__(self, arquivo_db="inventario.json"):
        self.arquivo_db = arquivo_db

    def salvar(self, dados: list):
        """Salva os dados em um arquivo JSON."""
        try:
            with open(self.arquivo_db, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except  Exception as e:
            print(f"❌ Erro ao salvar em JSON: {e}")

    def carregar(self) -> list:
        """Carrega os dados de um arquivo JSON."""
        if not os.path.exists(self.arquivo_db) or os.path.getsize(self.arquivo_db) == 0:
            return []
        try:
            with open(self.arquivo_db, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Erro ao carregar JSON: {e}")
            return []