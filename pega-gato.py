#VINICIUS MARTINS RODRIGUES 2320308
#LUIZA MATTOS CERSOSIMO 2320591



import pygame 
import sys
import random
import time

# Definições de cores e constantes
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
TAMANHO_CELULA = 30
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
superpoder_ativo = False
usos_superpoder = 3
duracao_superpoder = 10  # em segundos
tempo_inicio_superpoder = 0
pontuacao = 0
pontuacao_atualizada = False

# Mapa do jogo
def carregar_mapa(filename):
    with open('mapa.txt', 'r') as arquivo:
        return [linha.strip() for linha in arquivo.readlines()]

MAPA = carregar_mapa('mapa.txt')

# Inicialização do Pygame
pygame.init()
largura_tela = len(MAPA[0]) * TAMANHO_CELULA
altura_tela = len(MAPA) * TAMANHO_CELULA
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("PEGA-GATO")
atualizar_tela = True

# Carregamento das imagens
pacman_img = pygame.image.load('gato_07.png').convert_alpha()
pacman_img = pygame.transform.scale(pacman_img, (TAMANHO_CELULA, TAMANHO_CELULA))

fantasma_img = pygame.image.load('jaca.png').convert_alpha()
fantasma_img = pygame.transform.scale(fantasma_img, (TAMANHO_CELULA, TAMANHO_CELULA))

pacman_superpoder_img = pygame.image.load('gato_superpoder.png').convert_alpha()
pacman_superpoder_img = pygame.transform.scale(pacman_superpoder_img, (TAMANHO_CELULA, TAMANHO_CELULA))

# Estado do jogo
def salvar_jogo(pontuacao):
    global tempo_inicio_jogo

    data_hora = time.strftime("%Y-%m-%d %H:%M:%S")

    dados = []
    with open('dados_jogo.txt', 'r') as arquivo:
        for linha in arquivo:
            partes = linha.split(' - ')
            if len(partes) >= 2:
                try:
                    pontos_str = partes[0].split(': ')[1]
                    pontuacao_atual = int(pontos_str)
                    tempo = partes[1]
                    dados.append((pontuacao_atual, tempo))
                except ValueError:
                    pass  

    dados.append((pontuacao, data_hora))

    dados_ordenados = sorted(dados, reverse=True)

    with open('dados_jogo.txt', 'w') as arquivo:
        for pontuacao_atual, tempo in dados_ordenados:
            arquivo.write(f'Pontuação: {pontuacao_atual} - {tempo}\n')

# Função para ativar o superpoder
def ativar_superpoder():
    global superpoder_ativo, usos_superpoder, tempo_inicio_superpoder
    if usos_superpoder > 0:
        superpoder_ativo = True
        usos_superpoder -= 1
        tempo_inicio_superpoder = time.time()

def mostrar_tutorial():
    fonte_tutorial = pygame.font.SysFont(None, 24)
    texto_tutorial = [
        "Olá, esse é o catman.",
        "O objetivo do jogo é coletar todas as bolinhas amarelas,",
        "sem deixar com que o jacaré consiga te pegar,",
        "lembrando que os jacarés andam de forma meio aleatória.",
        "Para movimentar o gato, você precisa usar as setinhas do teclado.",
        "O gato tem um super-poder, quando clicado na tecla 'S' no teclado",
        "os fantasmas somem por alguns segundos,",
        "porém esse poder só pode ser utilizado 3 vezes",
        "Quando você ganhar o jogo, em alguns segundos ele voltará para a tela inicial.",
        "Pressione 'V' para voltar ao menu."
    ]

    while True:
        tela.fill(PRETO)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    return 

        pos_y = 150
        for linha in texto_tutorial:
            texto = fonte_tutorial.render(linha, True, BRANCO)
            tela.blit(texto, ((largura_tela - texto.get_width()) // 2, pos_y))
            pos_y += 30

        pygame.display.update()


imagem1 = pygame.image.load('gato_07.png')
imagem2 = pygame.image.load('jaca.png')

# Defina as coordenadas para a posição das imagens
pos_x_imagem1 = 50
pos_y_imagem1 = 100

pos_x_imagem2 = 700 - imagem2.get_width() - 50
pos_y_imagem2 = 100


# Menu inicial
def menu():
    fonte_titulo = pygame.font.SysFont(None, 48)
    fonte_opcoes = pygame.font.SysFont(None, 36)

    menu_ativo = True
    opcao_selecionada = 0

    while menu_ativo:
        tela.fill(PRETO)

        titulo = fonte_titulo.render("PEGA-GATO", True, BRANCO)
        texto_comecar = fonte_opcoes.render("Começar", True, AZUL)
        texto_tutorial = fonte_opcoes.render("Tutorial", True, AZUL)
        texto_sair = fonte_opcoes.render("Sair", True, AZUL)

        largura_titulo, altura_titulo = titulo.get_size()
        largura_texto, altura_texto = texto_comecar.get_size()

        pos_x_titulo = (largura_tela - largura_titulo) // 2
        pos_y_titulo = altura_tela // 4

        pos_x_comecar = (largura_tela - largura_texto) // 2
        pos_y_comecar = altura_tela // 2

        pos_x_tutorial = (largura_tela - largura_texto) // 2
        pos_y_tutorial = altura_tela // 2 + 50

        pos_x_sair = (largura_tela - largura_texto) // 2
        pos_y_sair = altura_tela // 2 + 100

        tela.blit(titulo, (pos_x_titulo, pos_y_titulo))
        tela.blit(texto_comecar, (pos_x_comecar, pos_y_comecar))
        tela.blit(texto_tutorial, (pos_x_tutorial, pos_y_tutorial))
        tela.blit(texto_sair, (pos_x_sair, pos_y_sair))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    opcao_selecionada -= 1
                    if opcao_selecionada < 0:
                        opcao_selecionada = 2
                elif event.key == pygame.K_DOWN:
                    opcao_selecionada += 1
                    if opcao_selecionada > 2:
                        opcao_selecionada = 0
                elif event.key == pygame.K_RETURN:
                    if opcao_selecionada == 0:
                        menu_ativo = False
                    elif opcao_selecionada == 1:
                        mostrar_tutorial()
                        return menu()
                    elif opcao_selecionada == 2:  
                        pygame.quit()
                        sys.exit()

        if opcao_selecionada == 0:
            texto_comecar = fonte_opcoes.render("Começar", True, VERMELHO)
        elif opcao_selecionada == 1:
            texto_tutorial = fonte_opcoes.render("Tutorial", True, VERMELHO)
        elif opcao_selecionada == 2:
            texto_sair = fonte_opcoes.render("Sair", True, VERMELHO)

        tela.blit(texto_comecar, (pos_x_comecar, pos_y_comecar))
        tela.blit(texto_tutorial, (pos_x_tutorial, pos_y_tutorial))
        tela.blit(texto_sair, (pos_x_sair, pos_y_sair))
        tela.blit(imagem1, (pos_x_imagem1, pos_y_imagem1))
        tela.blit(imagem2, (pos_x_imagem2, pos_y_imagem2))

        pygame.display.update()

# Menu Perda
def menu2():
    fonte_titulo = pygame.font.SysFont(None, 48)
    fonte_opcoes = pygame.font.SysFont(None, 36)

    menu_ativo = True
    opcao_selecionada = 0

    while menu_ativo:
        tela.fill(PRETO)

        titulo = fonte_titulo.render("Você Perdeu!", True, BRANCO)
        texto_recomecar = fonte_opcoes.render("Recomeçar", True, AZUL)
        texto_tutorial = fonte_opcoes.render("Tutorial", True, AZUL)
        texto_sair = fonte_opcoes.render("Sair", True, AZUL)

        largura_titulo, altura_titulo = titulo.get_size()
        largura_texto, altura_texto = texto_recomecar.get_size()

        pos_x_titulo = (largura_tela - largura_titulo) // 2
        pos_y_titulo = altura_tela // 4

        pos_x_comecar = (largura_tela - largura_texto) // 2
        pos_y_comecar = altura_tela // 2

        pos_x_tutorial = (largura_tela - largura_texto) // 2
        pos_y_tutorial = altura_tela // 2 + 50

        pos_x_sair = (largura_tela - largura_texto) // 2
        pos_y_sair = altura_tela // 2 + 100

        tela.blit(titulo, (pos_x_titulo, pos_y_titulo))
        tela.blit(texto_recomecar, (pos_x_comecar, pos_y_comecar))
        tela.blit(texto_tutorial, (pos_x_tutorial, pos_y_tutorial))
        tela.blit(texto_sair, (pos_x_sair, pos_y_sair))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    opcao_selecionada -= 1
                    if opcao_selecionada < 0:
                        opcao_selecionada = 2
                elif event.key == pygame.K_DOWN:
                    opcao_selecionada += 1
                    if opcao_selecionada > 2:
                        opcao_selecionada = 0
                elif event.key == pygame.K_RETURN:
                    if opcao_selecionada == 0:
                        menu_ativo = False
                        global pontuacao, pontuacao_atualizada, MAPA, usos_superpoder
                        pontuacao = 0
                        usos_superpoder = 3
                        pontuacao_atualizada = False
                        MAPA = carregar_mapa('mapa.txt')
                        for i in range(len(MAPA)):
                            MAPA[i] = MAPA[i].replace(' ', '.')
                        jogo()
                    elif opcao_selecionada == 1:
                        mostrar_tutorial()
                        return menu2()
                        return menu_origem
                    elif opcao_selecionada == 2:
                        pygame.quit()
                        sys.exit()

        if opcao_selecionada == 0:
            texto_recomecar = fonte_opcoes.render("Recomeçar", True, VERMELHO)
        elif opcao_selecionada == 1:
            texto_tutorial = fonte_opcoes.render("Tutorial", True, VERMELHO)
        elif opcao_selecionada == 2:
            texto_sair = fonte_opcoes.render("Sair", True, VERMELHO)

        tela.blit(texto_recomecar, (pos_x_comecar, pos_y_comecar))
        tela.blit(texto_tutorial, (pos_x_tutorial, pos_y_tutorial))
        tela.blit(texto_sair, (pos_x_sair, pos_y_sair))

        pygame.display.update()

# Função para desenhar o mapa
def desenhar_mapa():
    for linha_numero, linha in enumerate(MAPA):
        for coluna_numero, caracter in enumerate(linha):
            x = coluna_numero * TAMANHO_CELULA
            y = linha_numero * TAMANHO_CELULA
            if caracter == '#':
                pygame.draw.rect(tela, AZUL, (x, y, TAMANHO_CELULA, TAMANHO_CELULA))
            elif caracter == '.':
                pygame.draw.circle(tela, AMARELO, (x + TAMANHO_CELULA // 2, y + TAMANHO_CELULA // 2), 3)

def desenhar_tela():
    tela.fill(PRETO)
    desenhar_mapa()
    if superpoder_ativo:
        tela.blit(pacman_superpoder_img, (pacman_x * TAMANHO_CELULA, pacman_y * TAMANHO_CELULA))
        fonte = pygame.font.SysFont(None, 36)
        texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))
        texto_pontos = fonte.render(f'Poderes restantes: {usos_superpoder}', True, (255, 255, 255))
        tela.blit(texto_pontuacao, (10, 10))
        tela.blit(texto_pontos, (370, 10))
    else:
        tela.blit(pacman_img, (pacman_x * TAMANHO_CELULA, pacman_y * TAMANHO_CELULA))
        tela.blit(pacman_img, (pacman_x * TAMANHO_CELULA, pacman_y * TAMANHO_CELULA))
        tela.blit(fantasma_img, (fantasma1_x * TAMANHO_CELULA, fantasma1_y * TAMANHO_CELULA))
        tela.blit(fantasma_img, (fantasma2_x * TAMANHO_CELULA, fantasma2_y * TAMANHO_CELULA))
        tela.blit(fantasma_img, (fantasma3_x * TAMANHO_CELULA, fantasma3_y * TAMANHO_CELULA))
        tela.blit(fantasma_img, (fantasma4_x * TAMANHO_CELULA, fantasma4_y * TAMANHO_CELULA))
        fonte = pygame.font.SysFont(None, 36)
        texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))
        texto_pontos = fonte.render(f'Poderes restantes: {usos_superpoder}', True, (255, 255, 255))
        tela.blit(texto_pontuacao, (10, 10))
        tela.blit(texto_pontos, (370, 10))
    pygame.display.update()

def tela_vitoria():
    fonte_vitoria = pygame.font.SysFont(None, 48)
    texto_vitoria = fonte_vitoria.render("VOCÊ GANHOU!", True, BRANCO)

    tela.fill(PRETO)
    largura_texto, altura_texto = texto_vitoria.get_size()
    pos_x_texto = (largura_tela - largura_texto) // 2
    pos_y_texto = (altura_tela - altura_texto) // 2
    tela.blit(texto_vitoria, (pos_x_texto, pos_y_texto))
    pygame.display.update()

    time.sleep(10)

def verificar_vitoria():
    global numero_total_itens
    if pontuacao == 225:
        print("Parabéns! Você ganhou!")
        tela_vitoria()
        salvar_jogo(pontuacao)
        menu()


# Gera os itens (pontos) aleatoriamente no mapa
def gerar_itens():
    pontos_disponiveis = [(x, y) for y, linha in enumerate(MAPA) for x, char in enumerate(linha) if char == '.']

    if not pontos_disponiveis:
        return None

    return random.choice(pontos_disponiveis)

# Função para atualizar a pontuação na tela
def atualizar_pontuacao():
    global pontuacao_atualizada
    if not pontuacao_atualizada:
        tela.fill(PRETO)
        desenhar_mapa()
        tela.blit(pacman_img, (pacman_x * TAMANHO_CELULA, pacman_y * TAMANHO_CELULA))
        tela.blit(fantasma_img, (fantasma1_x * TAMANHO_CELULA, fantasma1_y * TAMANHO_CELULA))
        tela.blit(fantasma_img, (fantasma2_x * TAMANHO_CELULA, fantasma2_y * TAMANHO_CELULA))
        fonte = pygame.font.SysFont(None, 36)
        texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))
        tela.blit(texto_pontuacao, (10, 10))
        pygame.display.update()
        pontuacao_atualizada = True

# Verifica a colisão entre o Pac-Man e os itens
def verificar_itens():
    global pacman_x, pacman_y, pontuacao, pontuacao_atualizada

    if MAPA[pacman_y][pacman_x] == '.':
        pontuacao += 1
        pontuacao_atualizada = False
        MAPA[pacman_y] = MAPA[pacman_y][:pacman_x] + ' ' + MAPA[pacman_y][pacman_x + 1:]
        novo_ponto = gerar_itens()

        if novo_ponto is not None:
            MAPA[novo_ponto[1]] = MAPA[novo_ponto[1]][:novo_ponto[0]] + '.' + MAPA[novo_ponto[1]][novo_ponto[0] + 1:]
        else:
            verificar_vitoria()

# Movimento aleatório dos fantasmas
def mover_fantasmas():
    global fantasma1_x, fantasma1_y, fantasma2_x, fantasma2_y, fantasma3_x, fantasma3_y, fantasma4_x, fantasma4_y

    direcoes_possiveis = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    movimentos = {
        'fantasma1': random.choice(direcoes_possiveis),
        'fantasma2': random.choice(direcoes_possiveis),
        'fantasma3': random.choice(direcoes_possiveis),
        'fantasma4': random.choice(direcoes_possiveis)
    }

    for fantasma, movimento in movimentos.items():
        x, y = 0, 0

        if fantasma == 'fantasma1':
            x, y = fantasma1_x, fantasma1_y
        elif fantasma == 'fantasma2':
            x, y = fantasma2_x, fantasma2_y
        elif fantasma == 'fantasma3':
            x, y = fantasma3_x, fantasma3_y
        elif fantasma == 'fantasma4':
            x, y = fantasma4_x, fantasma4_y

        if movimento == 'UP' and MAPA[y - 1][x] != '#':
            y -= 1
        elif movimento == 'DOWN' and MAPA[y + 1][x] != '#':
            y += 1
        elif movimento == 'LEFT' and MAPA[y][x - 1] != '#':
            x -= 1
        elif movimento == 'RIGHT' and MAPA[y][x + 1] != '#':
            x += 1

        if fantasma == 'fantasma1':
            fantasma1_x, fantasma1_y = x, y
        elif fantasma == 'fantasma2':
            fantasma2_x, fantasma2_y = x, y
        elif fantasma == 'fantasma3':
            fantasma3_x, fantasma3_y = x, y
        elif fantasma == 'fantasma4':
            fantasma4_x, fantasma4_y = x, y

# Colisão
def verificar_colisao_fantasma():
    global pacman_x, pacman_y, fantasma1_x, fantasma1_y, fantasma2_x, fantasma2_y, fantasma3_x, fantasma3_y, fantasma4_x, fantasma4_y

    if (pacman_x, pacman_y) == (fantasma1_x, fantasma1_y) or (pacman_x, pacman_y) == (fantasma2_x, fantasma2_y) or (pacman_x, pacman_y) == (fantasma3_x, fantasma3_y) or (pacman_x, pacman_y) == (fantasma4_x, fantasma4_y):
        salvar_jogo(pontuacao)
        return True
    return False

menu()

# Loop principal do jogo
def jogo():
    global pacman_x, pacman_y, fantasma1_x, fantasma1_y, fantasma2_x, fantasma2_y, fantasma3_x, fantasma3_y, fantasma4_x, fantasma4_y, atualizar_tela, superpoder_ativo, usos_superpoder

    pacman_x, pacman_y = 1, 5
    fantasma1_x, fantasma1_y = 3, 2
    fantasma2_x, fantasma2_y = 17, 2
    fantasma3_x, fantasma3_y = 3, 20
    fantasma4_x, fantasma4_y = 17, 20

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        movimento_pacman = False

        # Movimentação do Pac-Man
        if teclas[pygame.K_UP] and MAPA[pacman_y - 1][pacman_x] != '#':
            pacman_y -= 1
            movimento_pacman = True
        if teclas[pygame.K_DOWN] and MAPA[pacman_y + 1][pacman_x] != '#':
            pacman_y += 1
            movimento_pacman = True
        if teclas[pygame.K_LEFT] and MAPA[pacman_y][pacman_x - 1] != '#':
            pacman_x -= 1
            movimento_pacman = True
        if teclas[pygame.K_RIGHT] and MAPA[pacman_y][pacman_x + 1] != '#':
            pacman_x += 1
            movimento_pacman = True

        verificar_itens()
        mover_fantasmas()

        if verificar_vitoria():
            usos_superpoder = 3
            break 

        if movimento_pacman:
            atualizar_tela = True

        if verificar_colisao_fantasma():
            if superpoder_ativo:
                superpoder_ativo = False
            else:
                menu2()
                salvar_jogo()
                
        if teclas[pygame.K_s]:
            ativar_superpoder()

        if superpoder_ativo:
            tempo_atual = time.time()
            if tempo_atual - tempo_inicio_superpoder >= duracao_superpoder:
                superpoder_ativo = False

        if atualizar_tela:
            desenhar_tela()
            atualizar_tela = False

        pygame.time.Clock().tick(10)

# Iniciar o jogo
jogo()
