import random as rd
import string
from colorama import Fore
import os
import json
import re

# variáveis globais
senhas = []
pontuacao = 0


# Avaliar senha
def avaliar_senha(senha):
    global pontuacao

    # Verifica a pontuação da senha
    if len(senha) >= 8:
        pontuacao += 1
    if re.search("[a-z]", senha):
        pontuacao += 1
    if re.search("[A-Z]", senhas):
        pontuacao += 1
    if re.search("[0-9]", senhas):
        pontuacao += 1
    if re.search('[!@#$%^&*(),.?":{}|<>]'):
        pontuacao += 1

    if pontuacao == 5:
        return Fore.GREEN + f"\nA senha fornecida foi muito boa! ({pontuacao}/5)"
    if senha == 4:
        return (
            Fore.GREEN
            + f"\nA senha fornecida é boa, porém, faltam algumas melhorias ({pontuacao}/5)"
        )
    if senha == 3:
        return (
            Fore.YELLOW
            + f"\nA senha fornecida é mediana, recomendaria trocá-la futuramente ({pontuacao}/5)"
        )
    if senha == 2:
        return Fore.LIGHTRED_EX + f"A senha fornecida é fraca ({pontuacao}/5)"
    if senha == 1:
        return (
            Fore.RED
            + f"\nA senha fornecida é muito fraca, recomendaria trocá-la imediatamente ({pontuacao}/5)"
        )


# Adiciona senha
def adicionar_senha(senha):
    senhas.append({"senha": senha})
    print(Fore.GREEN + "\nSenha adicionada com sucesso!\n")


# Exclui senha
def excluir_senha(indice):
    try:
        senha = senhas.pop(indice - 1)
        print(Fore.GREEN + f"\nSenha {senha} excluída com sucesso!")
    except IndexError:
        print(Fore.RED + f"Ops! Um índice inválido foi inserido ({indice})")


# Salva a lista atual de senhas
def salvar_lista():
    with open("senhas\\senhas.json", "w") as file:
        json.dump(senhas, file)
    print(Fore.GREEN + "\nSenhas salvas com sucesso!\n")


# Carrega a lista de senhas caso ela exista
def carregar_senhas():
    global senhas
    if os.path.exists("senhas\\senhas.json"):
        with open("senhas\\senhas.json", "r") as file:
            senhas = json.load(file)
        print(Fore.GREEN + "\nSenhas anteriores carregadas com sucesso!\n")


# Lista as senhas caso haja ao menos 1
def listar_senhas():
    if not senhas:
        print(Fore.YELLOW + "Nenhuma senha encontrada")
    else:
        for i, senha in enumerate(senhas, 1):
            print(Fore.LIGHTGREEN_EX + f"\n{i} - {senha['senha']}")


# Invoca o gerador de senhas
def gerar_senha(comprimento, maiusculas, minusculas, simbolos, digitos):
    caracteres = ""

    if maiusculas:
        caracteres += string.ascii_uppercase
    if minusculas:
        caracteres += string.ascii_lowercase
    if digitos:
        caracteres += string.digits
    if simbolos:
        caracteres += string.punctuation

    if not caracteres:
        print(
            Fore.RED
            + "Nenhum tipo de caractere selecionado, senha impossível de ser gerada!\n"
        )
        return None

    senha = "".join(rd.choice(caracteres) for _ in range(comprimento))
    return Fore.GREEN + senha


# Invoca o menu de comandos
def listar_comandos():
    while True:
        try:
            comprimento = int(input(Fore.CYAN + "Digite o comprimento da senha: "))
            break
        except ValueError:
            print(Fore.RED + "Ops! Um valor inválido foi inserido!\n")
            continue
    maiusculas = (
        input(Fore.CYAN + "Deseja caracteres maiúsculos [s/n]? ").lower() == "s"
        or "sim"
    )
    minusculas = (
        input(Fore.CYAN + "Deseja caracteres minúsulos [s/n]? ").lower() == "s" or "sim"
    )
    simbolos = input(Fore.CYAN + "Deseja símbolos [s/n]? ").lower() == "s" or "sim"
    digitos = input(Fore.CYAN + "Deseja dígitos [s/n]? ").lower() == "s" or "sim"

    return comprimento, maiusculas, minusculas, simbolos, digitos


# Função principal
def main():
    comprimento, maiusculas, minusculas, simbolos, digitos = listar_comandos()

    senha = gerar_senha(comprimento, maiusculas, minusculas, simbolos, digitos)

    print(Fore.YELLOW + f"\nA Senha gerada foi {senha}")
    resp = input("\nDeseja guardar esta senha [s/n]? ")
    if resp.lower == "s" or "sim":
        adicionar_senha(senha)
        salvar_lista()


# inicializador e menu princiapal
if __name__ == "__main__":
    print(Fore.MAGENTA + "\nGerador de Senhas - 1.0.0")
    carregar_senhas()
    while True:
        print(Fore.LIGHTMAGENTA_EX + "\nLista de Funções\n")
        print(Fore.BLUE + "1 - Gerar senha")
        print(Fore.BLUE + "2 - Excluir senha")
        print(Fore.BLUE + "3 - Avaliar força de senha")
        print(Fore.BLUE + "4 - Visualizar senhas salvas")
        print(Fore.BLUE + "5 - Avaliar senha")
        print(Fore.BLUE + "6 - Sair do programa\n")

        try:
            resposta = int(input(Fore.LIGHTBLACK_EX + "Digite sua resposta aqui: "))
        except ValueError:
            print(Fore.YELLOW + "Ops! Um valor inválido foi inserido\n")
            continue

        match resposta:
            case 1:
                main()
            case 2:
                try:
                    indice = int(
                        input(Fore.LIGHTBLACK_EX + "\nDigite o número da senha: ")
                    )
                    excluir_senha(indice)
                except ValueError:
                    print(Fore.RED + f"Ops! Um índice inválido foi inserido ({indice})")
                    continue

            case 3:
                senha = input("Digite uma senha que deseja avaliar a senha")
            case 4:
                listar_senhas()
            case 5:
                try:
                    senha = input(Fore.LIGHTBLACK_EX + "\nDigite a senha: ")
                    avaliar_senha(senha)
                except TypeError:
                    print(Fore.RED + "\nOps! Uma entrada inválida foi inserida!")
                    continue
            case 6:
                salvar_lista()
                print(Fore.RED + "Saindo...")
                break
            case _:
                print(
                    Fore.LIGHTRED_EX
                    + f"Ops! Uma resposta inválida foi inserida ({resposta})"
                )
