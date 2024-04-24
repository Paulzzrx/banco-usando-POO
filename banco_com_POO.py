class Conta:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

def menu():
    menu_texto = '''
========= DIO Bank ==========
    
[d]  Depositar
[s]  Sacar
[e]  Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuario
[q]  Sair

=============================
=> '''
    return input(menu_texto)

def depositar(saldo, valor, extrato, cpf, usuarios):
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n--- CPF não cadastrado! Não é possível realizar o depósito. ---")
    
    elif valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\n--- Depósito realizado com sucesso! ---")
    else:
        print("\n--- Operação falhou! O valor informado é inválido. ---") 

    return saldo, extrato

def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques == limite_saques

    if excedeu_saldo:
        print("\n--- Operação falhou! Você não tem saldo suficiente. ---")

    elif excedeu_limite:
         print("\n--- Operação falhou! O valor do saque excede o limite. ---")
        
    elif excedeu_saques:
        print("\n--- Operação falhou! Número máximo de saques excedido. ---")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\n--- Saque realizado com sucesso! ---")

    else:
        print("\n--- Operação falhou! O valor informado é inválido. ---")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("\n======== EXTRATO ========")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R${saldo:.2f}")
    print("\n========================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n--- Já existe usuário com esse CPF! ---")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (estado - cidade - bairro - numero): ")
    
    usuarios.append(Usuario(nome, data_nascimento, cpf, endereco))

    print("--- Usuário criado com sucesso! ---")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf= input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n--- Conta criada com sucesso! ---")
        return Conta(agencia, numero_conta, usuario)
    
    print("\n--- Usuário não encontrado, fluxo de criação de conta encerrado! ---")

def listar_contas(contas):
    for conta in contas:
        linha = f"""
Contas:

Agência:  {conta.agencia}
C/C:      {conta.numero_conta}
Titular:  {conta.usuario.nome}
"""

        print("=" * 100)
        print(linha)

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()
        if opcao == "d":
            cpf = input("Informe o CPF (somente número) para realizar o depósito: ")
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato, cpf, usuarios)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operações inválida, por favor selecione novamente a operação desejada.")

main()
