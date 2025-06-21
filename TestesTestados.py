import random
import time

historico_vencedores = []
# Função do historico de partidas
def mostrar_historico():
    print("\n" + "-" * 30)
    print("HISTÓRICO DE PARTIDAS")
    print("-" * 30)
    if not historico_vencedores:
        print("Nenhuma partida foi jogada ainda.")
    else:
        for i, vencedor in enumerate(historico_vencedores, 1):
            print(f"Partida {i}: {vencedor}")
    print("-" * 30 + "\n")
    input("Pressione Enter para voltar ao menu...")
    return menu_inicial()

# bem vindas ao jogo e menu com esolha de modo de jogo
def menu_inicial():
    print("-" * 20 + "\nBem-vindo ao Batalha Naval!\n" + "-" * 20)
    a = input(
        "Escolha uma opção:\n" + "-" * 20 +
        "\n1. Jogador vs Jogador" +
        "\n2. Jogador vs Computador" +
        "\n3. Ver histórico de partidas" +
        "\n4. Sair" +
        "\n" + "-" * 20 + "\nDigite sua escolha: ")

    if a == "1":
        return jogar()
    elif a == "2":
        return jogar2()
    elif a == "3":
        return mostrar_historico()
    elif a == "4":
        print("Obrigado por jogar! Até a próxima!")
        exit()
    else:
        print("\n" * 5 + "Inválido! Escolha uma opção válida (1-4)" + "\n" * 1)
        return menu_inicial()


# printa o tabuleiro inteiro
def mostrar_tabuleiro(tabuleiro):
    # Cabeçalho das colunas (A, B, C...)
    print("    " + " ".join([chr(65 + i) for i in range(len(tabuleiro))]))  # 3 espaços no início

          # Linhas do tabuleiro
    for i, linha in enumerate(tabuleiro, 1):
        # Ajuste para números com 1 ou 2 dígitos
        if i < 10:
        # imprime o numero da linha (i) e as ~
            print(f"{i}   " + " ".join(linha))  # 2 espaços após o número
        elif i <= 99:
        # imprime o numero da linha (i) e as ~
            print(f"{i}  " + " ".join(linha))  # 1 espaço após o número
        else:
        # imprime o numero da linha (i) e as ~
            print(f"{i} " + " ".join(linha))  # 0 espaço após o número


def posicionar_navios(tabuleiro):
    # Dicionário com os navios e suas quantidades
    navios = {
        "Encouraçado": {"tamanho": 5, "quantidade": 1, "posicoes": [], "destruido": False},
        "Porta-Aviões": {"tamanho": 4, "quantidade": 1, "posicoes": [], "destruido": False},
        "Contratorpedeiro": {"tamanho": 3, "quantidade": 2, "posicoes": [], "destruido": False},
        "Submarino": {"tamanho": 2, "quantidade": 2, "posicoes": [], "destruido": False}
    }

    # função para verificar posição inválida
    def invalido(tabule, classe, casas):
        mostrar_tabuleiro(tabule)
        print(f"\nPosicionando {classe} (tamanho: {casas})")
        while True:
            # Input da rotação
            rotacao = input(f"Você deseja colocar seu {classe} na vertical ou horizontal? (V/H): ").upper()
            while rotacao not in ("V", "H"):
                rotacao = input("Caractere inválido! Digite V para vertical ou H para horizontal: ").upper()

            try:
                # Recebe e processa o input
                entrada = input(f"Coloque a posição inicial do {classe} (ex: A1): ").upper().strip()

                # Valida o formato do input
                if len(entrada) < 2 or not entrada[0].isalpha() or not entrada[1:].isdigit():
                    raise ValueError("Formato inválido!")

                # Converte as coordenadas
                y = ord(entrada[0]) - ord('A')  # A=0, B=1, etc.
                x = int(entrada[1:]) - 1  # Converte para índice base 0
                coordenadas_navio = []

                # Valida a posição com base na rotação
                if rotacao == "H":  # Horizontal
                    if (x < 0 or x >= len(tabule) or
                            y < 0 or y + casas - 1 >= len(tabule[0])):
                        print("Erro: Posição inválida! Navio ultrapassa os limites do tabuleiro.")
                        continue

                    # Verifica se já tem navio na posição
                    for i in range(casas):
                        if tabule[x][y + i] == "N":
                            print("Posição inválida! Já tem um navio nessa posição.")
                            raise ValueError("Posição ocupada")

                    # Coloca o navio
                    for i in range(casas):
                        tabule[x][y + i] = "N"
                        coordenadas_navio.append([x, y + i])

                else:  # Vertical
                    if (x < 0 or x + casas - 1 >= len(tabule) or
                            y < 0 or y >= len(tabule[0])):
                        print("Erro: Posição inválida! Navio ultrapassa os limites do tabuleiro.")
                        continue

                    # Verifica se já tem navio na posição
                    for i in range(casas):
                        if tabule[x + i][y] == "N":
                            print("Posição inválida! Já tem um navio nessa posição.")
                            raise ValueError("Posição ocupada")

                    # Coloca o navio
                    for i in range(casas):
                        tabule[x + i][y] = "N"
                        coordenadas_navio.append([x + i, y])

                return tabule, coordenadas_navio, classe

            except (ValueError, IndexError) as e:
                print(f"Erro: {str(e)} Use o formato LETRANÚMERO (ex: A1 ou B10)")

    # Posiciona cada tipo de navio na quantidade especificada
    for classe, dados in navios.items():
        for _ in range(dados["quantidade"]):
            tabuleiro, coordenadas, classe_navio = invalido(tabuleiro, f"{classe} {_+1}", dados["tamanho"])
            dados["posicoes"].extend(coordenadas)  # Adiciona as coordenadas ao navio

    return tabuleiro, navios


def converter_coordenada(entrada):
    # Converte 'A1' para (0, 0)
    return (ord(entrada[0]) - ord('A'), int(entrada[1:]) - 1)


def validar_entrada(entrada, tabuleiro):
    # Valida formato e limites do tabuleiro
    if len(entrada) < 2 or not entrada[0].isalpha() or not entrada[1:].isdigit():
        return False
    y, x = converter_coordenada(entrada)
    return 0 <= x < len(tabuleiro) and 0 <= y < len(tabuleiro[0])


def criar_tabuleiro_vazio(tamanho):
    return [["~" for _ in range(tamanho)] for _ in range(tamanho)]


def mostrar_tabuleiros(tabuleiro_jogador, tabuleiro_inimigo_view):
    print("\nSEU TABULEIRO:")
    mostrar_tabuleiro(tabuleiro_jogador)
    print("\nTABULEIRO INIMIGO (SEUS TIROS):")
    mostrar_tabuleiro(tabuleiro_inimigo_view)
    print("\n")


def jogar():
    tamanho = None
    try:
        tamanho = 0
        while tamanho < 10:
            tamanho = int(input("Tamanho do tabuleiro (10+): "))
            if tamanho < 10:
                print("Tamanho invalido!")
    except ValueError:
        while type(tamanho) != int:
            tamanho = input("Tamanho invalido (Value error)\nTamanho do tabuleiro (10+): ")
            try:
                tamanho = int(tamanho)
            except ValueError:
                pass

    # Cria todos os tabuleiros necessários
    tabuleiro_jogador1 = criar_tabuleiro_vazio(tamanho)
    tabuleiro_jogador2 = criar_tabuleiro_vazio(tamanho)
    tabuleiro_jogador1_view = criar_tabuleiro_vazio(tamanho)  # Para o jogador 2 ver seus tiros
    tabuleiro_jogador2_view = criar_tabuleiro_vazio(tamanho)  # Para o jogador 1 ver seus tiros

    # Posiciona os navios
    print("\nJogador 1, posicione seus navios:")
    tabuleiro_jogador1, navios_jogador1 = posicionar_navios(tabuleiro_jogador1)
    print("\n" * 50)  # Limpa a tela para o jogador 2 não ver
    print("Jogador 2, posicione seus navios:")
    tabuleiro_jogador2, navios_jogador2 = posicionar_navios(tabuleiro_jogador2)
    print("\n" * 50)  # Limpa a tela novamente

    while True:
        # Vez do jogador 1
        print("\nVez do Jogador 1:")
        mostrar_tabuleiros(tabuleiro_jogador1, tabuleiro_jogador2_view)

        # Input e validação
        while True:
            entrada = input("Jogador 1, digite coordenadas do seu ataque! (ex: A1): ").upper().strip()
            if validar_entrada(entrada, tabuleiro_jogador2):
                break
            print("Entrada inválida! Tente novamente.")

        y, x = converter_coordenada(entrada)

        # Verifica se essa coordenada já foi atacada
        while tabuleiro_jogador2[x][y] == "X" or tabuleiro_jogador2[x][y] == "O":
            while True:
                entrada = input(
                    "Posição invalida! está coordenada já foi atacada\nDigite coordenadas do seu ataque! (ex: A1): ").upper().strip()
                if validar_entrada(entrada, tabuleiro_jogador2):
                    break
                print("Entrada inválida! Tente novamente.")
            y, x = converter_coordenada(entrada)

        # Registra ataque no tabuleiro real e no view
        if tabuleiro_jogador2[x][y] == "N":
            tabuleiro_jogador2[x][y] = "X"
            tabuleiro_jogador2_view[x][y] = "X"
            print("Você acertou o navio inimigo!")
        else:
            tabuleiro_jogador2[x][y] = "O"
            tabuleiro_jogador2_view[x][y] = "O"
            print("Você acertou somente a água!")

        # verifica se o navio do inimigo foi destruido
        for nome_navio, dados_navio in navios_jogador2.items():
            casas_atacadas = 0
            if not dados_navio.get("destruido", False):
                for y_navio, x_navio in dados_navio["posicoes"]:
                    if tabuleiro_jogador2[x_navio][y_navio] == "X":
                        casas_atacadas += 1
                if casas_atacadas == dados_navio["tamanho"]:
                    print(f"{nome_navio} inimigo foi destruído!")
                    dados_navio["destruido"] = True

        # verifica a vitoria do jogador 1
        if all(dados_navio["destruido"] for dados_navio in navios_jogador2.values()):
            return "Jogador 1"

        input("Pressione Enter para passar a vez para o Jogador 2...")
        print("\n" * 50)

        # Vez do jogador 2
        print("\nVez do Jogador 2:")
        mostrar_tabuleiros(tabuleiro_jogador2, tabuleiro_jogador1_view)

        # Input e validação para jogador 2
        while True:
            entrada = input("Jogador 2, digite coordenadas do seu ataque! (ex: A1): ").upper().strip()
            if validar_entrada(entrada, tabuleiro_jogador1):
                break
            print("Entrada inválida! Tente novamente.")

        y, x = converter_coordenada(entrada)

        # Verifica se essa coordenada já foi atacada
        while tabuleiro_jogador1[x][y] == "X" or tabuleiro_jogador1[x][y] == "O":
            while True:
                entrada = input(
                    "Posição invalida! está coordenada já foi atacada\nDigite coordenadas do seu ataque! (ex: A1): ").upper().strip()
                if validar_entrada(entrada, tabuleiro_jogador1):
                    break
                print("Entrada inválida! Tente novamente.")
            y, x = converter_coordenada(entrada)

        # Registra ataque no tabuleiro real e no view
        if tabuleiro_jogador1[x][y] == "N":
            tabuleiro_jogador1[x][y] = "X"
            tabuleiro_jogador1_view[x][y] = "X"
            print("Você acertou o navio inimigo!")
        else:
            tabuleiro_jogador1[x][y] = "O"
            tabuleiro_jogador1_view[x][y] = "O"
            print("Você acertou somente a água!")

        # verifica se o navio do jogador 1 foi destruido
        for nome_navio, dados_navio in navios_jogador1.items():
            casas_atacadas = 0
            if not dados_navio.get("destruido", False):
                for y_navio, x_navio in dados_navio["posicoes"]:
                    if tabuleiro_jogador1[x_navio][y_navio] == "X":
                        casas_atacadas += 1
                if casas_atacadas == dados_navio["tamanho"]:
                    print(f"{nome_navio} inimigo foi destruído!")
                    dados_navio["destruido"] = True

        # verifica a vitoria do jogador 2
        if all(dados_navio["destruido"] for dados_navio in navios_jogador1.values()):
            return "Jogador 2"

        input("Pressione Enter para passar a vez para o Jogador 1...")
        print("\n" * 50)


def jogar2():  # Modo de jogo contra o bot
    tamanho = None
    try:
        tamanho = int(input("Tamanho do tabuleiro (10+): "))
    except ValueError:
        while type(tamanho) != int:
            tamanho = input("Tamanho invalido (Value error)\nTamanho do tabuleiro (10+): ")
            try:
                tamanho = int(tamanho)
            except ValueError:
                pass

    # Cria todos os tabuleiros necessários
    tabuleiro_jogador = criar_tabuleiro_vazio(tamanho)
    tabuleiro_bot = criar_tabuleiro_vazio(tamanho)
    tabuleiro_bot_view = criar_tabuleiro_vazio(tamanho)  # Para o jogador ver seus tiros

    # Posiciona os navios
    print("\nJogador, posicione seus navios:")
    tabuleiro_jogador, navios_jogador = posicionar_navios(tabuleiro_jogador)
    print("\n" * 50)  # Limpa a tela

    # Posiciona navios do bot
    tabuleiro_bot, navios_bot = posicionar_navios_bot(tabuleiro_bot)

    while True:
        # Vez do jogador
        print("\nSua vez:")
        mostrar_tabuleiros(tabuleiro_jogador, tabuleiro_bot_view)

        # Input e validação
        while True:
            entrada = input("Digite coordenadas do seu ataque! (ex: A1): ").upper().strip()
            if validar_entrada(entrada, tabuleiro_bot):
                break
            print("Entrada inválida! Tente novamente.")

        x, y = converter_coordenada(entrada)

        # Verifica se já foi atacada
        while tabuleiro_bot[x][y] in ["X", "O"]:
            entrada = input("Posição inválida! Já foi atacada. Digite novas coordenadas (ex: A1): ").upper().strip()
            x, y = converter_coordenada(entrada)

        # Registra ataque
        if tabuleiro_bot[x][y] == "N":
            tabuleiro_bot[x][y] = "X"
            tabuleiro_bot_view[x][y] = "X"
            print("Você acertou o navio inimigo!")
        else:
            tabuleiro_bot[x][y] = "O"
            tabuleiro_bot_view[x][y] = "O"
            print("Você acertou somente a água!")

        # verifica se o navio do bot foi destruido
        for nome_navio, dados_navio in navios_bot.items():
            casas_atacadas = 0
            if not dados_navio.get("destruido", False):
                for y_navio, x_navio in dados_navio["posicoes"]:
                    if tabuleiro_bot[x_navio][y_navio] == "X":
                        casas_atacadas += 1
                if casas_atacadas == dados_navio["tamanho"]:
                    print(f"{nome_navio} inimigo foi destruído!")
                    dados_navio["destruido"] = True

        # verifica a vitoria do jogador
        if all(dados_navio["destruido"] for dados_navio in navios_bot.values()):
            return "Jogador"

        input("Pressione Enter para passar a vez para o bot...")
        print("\n" * 50)

        # Vez do bot
        print("\nVez do bot:")
        mostrar_tabuleiros(tabuleiro_jogador, tabuleiro_bot_view)  # Mostra o tabuleiro do jogador e os tiros do bot

        # Ataque do bot
        tabuleiro_jogador = ataque_bot(tabuleiro_jogador)

        # verifica se o navio do jogador foi destruido
        for nome_navio, dados_navio in navios_jogador.items():
            casas_atacadas = 0
            if not dados_navio.get("destruido", False):
                for y_navio, x_navio in dados_navio["posicoes"]:
                    if tabuleiro_jogador[x_navio][y_navio] == "X":
                        casas_atacadas += 1
                if casas_atacadas == dados_navio["tamanho"]:
                    print(f"Seu {nome_navio} foi destruído!")
                    dados_navio["destruido"] = True

        # verifica a vitoria do bot
        if all(dados_navio["destruido"] for dados_navio in navios_jogador.values()):
            return "Bot"

        input("Pressione Enter para continuar...")
        print("\n" * 50)


def posicionar_navios_bot(tabuleiro):
    def invalido(tabule, classe, casas):
        while True:
            rotacao = random.choice(["V", "H"])
            try:
                if rotacao == "H":
                    x = random.randint(0, len(tabule) - 1)
                    y = random.randint(0, len(tabule[0]) - casas)
                    # Verifica se já tem navio na posição
                    if any(tabule[x][y + i] == "N" for i in range(casas)):
                        continue
                    # Coloca o navio
                    for i in range(casas):
                        tabule[x][y + i] = "N"
                    coordenadas_navio = [[x, y + i] for i in range(casas)]
                else:  # Vertical
                    x = random.randint(0, len(tabule) - casas)
                    y = random.randint(0, len(tabule[0]) - 1)
                    if any(tabule[x + i][y] == "N" for i in range(casas)):
                        continue
                    for i in range(casas):
                        tabule[x + i][y] = "N"
                    coordenadas_navio = [[x + i, y] for i in range(casas)]
                return tabule, coordenadas_navio, classe
            except (ValueError, IndexError):
                continue

    # Dicionário de navios
    navios = {
        "Encouraçado": {"tamanho": 5, "quantidade": 1, "posicoes": [], "destruido": False},
        "Porta-Aviões": {"tamanho": 4, "quantidade": 1, "posicoes": [], "destruido": False},
        "Contratorpedeiro": {"tamanho": 3, "quantidade": 2, "posicoes": [], "destruido": False},
        "Submarino": {"tamanho": 2, "quantidade": 2, "posicoes": [], "destruido": False}
    }

    # Posiciona cada tipo de navio
    for classe, dados in navios.items():
        for _ in range(dados["quantidade"]):
            tabuleiro, coordenadas, classe_navio = invalido(tabuleiro, f"{classe} {_ + 1}", dados["tamanho"])
            dados["posicoes"].extend(coordenadas)  # Adiciona as coordenadas ao navio

    return tabuleiro, navios


def ataque_bot(tabuleiro):
    while True:
        y = random.randint(0, len(tabuleiro) - 1)
        x = random.randint(0, len(tabuleiro[0]) - 1)
        if tabuleiro[x][y] not in ["X", "O"]:
            if tabuleiro[x][y] == "N":
                tabuleiro[x][y] = "X"
                print(f"Bot acertou seu navio em {chr(65 + y)}{x + 1}!")
            else:
                tabuleiro[x][y] = "O"
                print(f"Bot atirou na água em {chr(65 + y)}{x + 1}")
            return tabuleiro


continuar_jogando = True

while continuar_jogando:
    vencedor = menu_inicial()
    historico_vencedores.append(vencedor)
    print(f"\nParabéns! {vencedor} venceu o jogo!\n")

    resposta = " "
    while resposta != "S" and resposta != "N":
        resposta = input("Você quer continuar jogando?(S/N)").upper()
        if resposta == "N":
            print("Encerrando o programa...")
            time.sleep(2)
            continuar_jogando = False
        elif resposta == "S":
            print("Recomeçando o jogo...")
            time.sleep(2)
        else:
            print("\nOpção inválida!\n")