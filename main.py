import sys
from gerenciador import GerenciadorInventario
from equipamento import Equipamento, TipoAtivo
from vulnerabilidade import Vulnerabilidade

def exibir_menu():
    print("\n" + "=" * 40)
    print("\t\t SISTEMA DE INVENTÁRIO - CIBERSEGURANÇA")
    print("=" * 40)
    print("[1] Cadastrar Novo Ativo (Equipamento)")
    print("[2] Listar Todos os Ativos e Vulnerabilidades")
    print("[3] Cadastrar Vulnerabilidade em um Ativo")
    print("[4] Atualizar Dados de um Ativo (Update)")
    print("[5] Deletar um Ativo do Inventário (Delete)")
    print("[0] Sair do Sistema")
    print("=" * 40)

def obter_opcao_menu() -> int:
    try:
        return int(input("Escolha uma opção: ").strip())
    except ValueError:
        return -1  # Retorna -1 para indicar uma opção inválida
    
def menu_cadastrar_ativo(gerenciador: GerenciadorInventario):
    print("\n--- CADASTRO DE NOVO ATIVO ---")
    try:
        id_ativo = int(input("Digite o ID do ativo: ").strip())
        if id_ativo <= 0:
            print("❌ Erro: O ID deve ser um número inteiro positivo.")
            return
        
        if gerenciador.buscar_por_id(id_ativo) is not None:
            print("❌ Erro: Já existe um ativo cadastrado com este ID.")
            return
        
        hostname = input("Digite o hostname do ativo: ").strip()
        if not hostname:
            print("❌ Erro: O hostname não pode ser vazio.")
            return
        
        responsavel = input("Digite o nome do Responsável (apenas letras e espaços): ").strip()
        setor = input("Digite o nome do Setor (apenas letras): ").strip()

        print("\nTipos de Ativos Disponíveis:")
        for tipo in TipoAtivo:
            print(f" [{tipo.value}] {tipo.name.replace('_', ' ').capitalize()}")

        opcao_tipo = int(input("Escolha o número do tipo: ").strip())
        tipo_escolhido = TipoAtivo(opcao_tipo)

        novo_equipamento = Equipamento(id_ativo, hostname, responsavel, setor, tipo_escolhido)

        if gerenciador.cadastrar_equipamento(novo_equipamento):
            print(f"✅ Ativo '{hostname}' cadastrado e salvo com sucesso!")

    except ValueError as e:
        if "Erro" in str(e):
            print(e)
        else:
            print("❌ Erro: Entrada de dados inválida (ex: digitou letras onde se pedia números).")
    except KeyError:
        print("❌ Erro: Opção de tipo de ativo inexistente.")

def menu_listar_ativos(gerenciador: GerenciadorInventario):
    print("\n--- INVENTÁRIO DE ATIVOS ---")
    ativos = gerenciador.obter_todos_equipamentos()

    if not ativos:
        print("📭 O inventário está completamente vazio.")
        return
    
    for ativo in ativos:
        print(f"\n 💻 Ativo ID: {ativo.id} | Hostname: {ativo.hostname}")
        print(f"   Tipo: {ativo.tipo.name.replace('_', ' ').capitalize()} | Setor: {ativo.setor} | Responsável: {ativo.responsavel}")

        print("   ⚠️  Vulnerabilidades vinculadas:")
        if not ativo.vulnerabilidades:
            print("     🟢 Nenhuma vulnerabilidade reportada para este ativo.")
        else:
            for i, vuln in enumerate(ativo.vulnerabilidades, 1):
                sev_colorida = Vulnerabilidade.mapear_cor_severidade(vuln.severidade)
                print(f"    [{i}] {vuln.descricao} | Categoria: {vuln.categoria} | Severidade: {sev_colorida} | Status: {vuln.status}")
        print("-" * 50)

def menu_cadastrar_vulnerabilidade(gerenciador: GerenciadorInventario):
    print("\n--- VINCULAR VULNERABILIDADE A UM ATIVO ---")
    try:
        id_ativo = int(input("Digite o ID do ativo que possui a vulnerabilidade: ").strip())
        ativo = gerenciador.buscar_por_id(id_ativo)

        if not ativo:
            print("❌ Erro: Nenhum ativo encontrado com o ID fornecido.")
            return
        
        print(f"🎯 Ativo Selecionado: {ativo.hostname}")
        descricao = input("Descrição da Falha (ex: CVE ou nome): ").strip()
        categoria = input("Categoria da Vulnerabilidade (ex: SQL Injection, XSS): ").strip()

        print("\nNíveis de Severidade Disponíveis:")
        severidades = ("Baixa", "Média", "Alta", "Crítica")
        for i, sev in enumerate(severidades, 1):
            print(f" [{i}] {sev}")
        op_sev = int(input("Escolha a Severidade (1-4): ").strip())
        severidade = severidades[op_sev - 1]

        print("\nEstados de Status Disponíveis:")
        estados = ("Aberta", "Em tratamento", "Corrigida", "Aceita")
        for i, est in enumerate(estados, 1):
            print(f" [{i}] {est}")
        op_status = int(input("Escolha o Status (1-4): ").strip())
        status = estados[op_status - 1]

        nova_vulnerabilidade = Vulnerabilidade(descricao, categoria, severidade, status)
        ativo.adicionar_vulnerabilidade(nova_vulnerabilidade)
        print(f"✅ Vulnerabilidade '{descricao}' vinculada ao ativo '{ativo.hostname}' com sucesso!")
    except (ValueError, IndexError):
        print("❌ Erro: Entrada inválida. Certifique-se de digitar números válidos para ID, severidade e status.")

def menu_atualizar_ativo(gerenciador: GerenciadorInventario):
    print("\n--- ATUALIZAR DADOS DE UM ATIVO ---")
    try:
        id_ativo = int(input("Digite o ID do ativo que deseja atualizar: ").strip())
        ativo = gerenciador.buscar_por_id(id_ativo)

        if not ativo:
            print("❌ Erro: Nenhum ativo encontrado com o ID fornecido.")
            return
        
        print(f"🎯 Ativo Selecionado: {ativo.hostname} [Deixe em branco para MANTER o valor atual]")

        input_hostname = input(f"Novo Hostname [{ativo.hostname}]: ").strip()
        hostname_final = input_hostname if input_hostname else ativo.hostname

        input_responsavel = input(f"Novo Responsável [{ativo.responsavel}]: ").strip()
        responsavel_final = input_responsavel if input_responsavel else ativo.responsavel

        input_setor = input(f"Novo Setor [{ativo.setor}]: ").strip()
        setor_final = input_setor if input_setor else ativo.setor

        print("\n⚠️  Novos dados a serem salvos:")
        print(f"    Hostname: {hostname_final}")
        print(f"    Responsável: {responsavel_final}")
        print(f"    Setor: {setor_final}")

        confirmacao = input("\nDeseja realmente atualizar os dados deste ativo? (s/n): ").strip().lower()

        if confirmacao == 's':
            # Executa a atualização no gerenciador (que vai disparar os @setters das classes)
            if gerenciador.atualizar_equipamento(id_ativo, hostname_final, responsavel_final, setor_final):
                print("✅ Ativo atualizado e sincronizado no arquivo JSON com sucesso!")

        else:
            print("🚫 Operação cancelada pelo usuário. Os dados antigos foram mantidos.")

    except ValueError as e:
        print(e)


def menu_deletar_ativo(gerenciador: GerenciadorInventario):
    print("\n--- EXCLUSÃO DE ATIVOS EM LOTE ---")
    try:
        entrada = input("Digite o(s) ID(s) do(s) ativo(s) que deseja remover (separe por espaços ou vírgulas): ").strip()

        if not entrada:
            print("❌ Nenhum ID foi digitado. Operação cancelada.")
            return
        
        # Limpa a entrada: substitui vírgulas por espaços e divide a string em uma lista de strings
        tokens = entrada.replace(",", " ").split()
        # Converte para inteiros e elimina IDs duplicados que o usuário possa ter digitado por engano
        ids_Selecionados = list(set(int(id_str) for id_str in tokens))

        ativos_para_excluir = []
        ids_nao_encontrados = []

        for id_ativo in ids_Selecionados:
            ativo = gerenciador.buscar_por_id(id_ativo)
            if ativo:
                ativos_para_excluir.append(ativo)
            else:
                ids_nao_encontrados.append(id_ativo)

        if not ativos_para_excluir:
            print("❌ Erro: Nenhum dos IDs digitados foi encontrado no inventário.")
            return
        
        print("\n" + "!"*40)
        print("🚨 RESUMO DOS ATIVOS A SEREM EXCLUÍDOS:")
        print("!"*40)
        for ativo in ativos_para_excluir:
            print(f" ID: {ativo.id} | Hostname: {ativo.hostname} | Setor: {ativo.setor} ({len(ativo.vulnerabilidades)} vulnerabilidades vinculadas")

        if ids_nao_encontrados:
            print(f"\n⚠️  Aviso: Os IDs {ids_nao_encontrados} não existem e serão ignorados.")

        print("\n ⚠️  Esta ação é irreversível e apagará todos os ativos listados acima!")
        confirmacao = input(f"Tem certeza que deseja excluir permanentemente estes {len(ativos_para_excluir)} ativo(s)? (s/n):").strip().lower()

        if confirmacao == 's':
            sucesso_contador = 0
            for ativo in ativos_para_excluir:
               #
               if gerenciador.deletar_equipamento(ativo.id):
                   sucesso_contador += 1

            print(f"\n🗑️  Sucesso! {sucesso_contador} ativo(s) foi(ram) removido(s) do inventário com sucesso!")
        else:
             print("\n🚫 Operação de exclusão em lote cancelada. Nenhum dado foi alterado.")
    except ValueError:
        print("❌ Erro: Entrada inválida. Certifique-se de digitar apenas números inteiros nos IDs.")


def main():
    gerenciador = GerenciadorInventario()

    while True:
        exibir_menu()
        opcao = obter_opcao_menu()
        
        if opcao == 1:
            menu_cadastrar_ativo(gerenciador)
        elif opcao == 2:
            menu_listar_ativos(gerenciador)
        elif opcao == 3:
            menu_cadastrar_vulnerabilidade(gerenciador)
        elif opcao == 4:
            menu_atualizar_ativo(gerenciador)
        elif opcao == 5:
            menu_deletar_ativo(gerenciador)
        elif opcao == 0:
            print("\n👋 Encerrando o sistema de inventário. Até logo!")
            sys.exit(0)
        else:
            print("⚠️  Opção inválida! Por favor, escolha um número válido do menu.")

if __name__ == "__main__":
    main()