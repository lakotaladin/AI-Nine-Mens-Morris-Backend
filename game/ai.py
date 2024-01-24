import copy

SET_STONE = 'set'
MOVE_STONE = 'move'
REMOVE_STONE = 'remove'

WHITE = 1
BLACK = -1

MOVE_TYPE = 0
MOVE_COLOR = 1
MOVE_X = 2
MOVE_Y = 3
MOVE_Z = 4


def is_end(state):
    return state['white_remaining'] == 0 and state['black_remaining'] == 0 and (state['white_count'] <= 2 or state['black_count'] <= 2)


# HEURISTIKA ZA TESKU IGRU
def evaluate(state):
    stones = state['stones']

    value = 0

    # count horizontal lines
    for square in range(3):
        for line in [0, 2]:
            line_sum = 0
            for spot in range(3):
                line_sum += stones[square][line][spot]

            if abs(line_sum) == 3: # proveravam da li je uopste linija
                value += line_sum * 10
                if line_sum == 2:  # Dodatna nagrada za crnog igraca kada krene da formira mlin, to znaci da je stavio dva kamena jedan pored dugog i to je potencijalno stanje da se napravi mlin koji sadrzi 3 kamena.
                    value += 15

    # count vertical lines
    for square in range(3):
        for line in [0, 2]:
            line_sum = 0
            for spot in range(3):
                line_sum += stones[square][spot][line]

            if abs(line_sum) == 3:
                value += line_sum * 10
                if line_sum == 2:  # Dodatna nagrada za crnog igraca kada krene da formira mlin, to znaci da je stavio dva kamena jedan pored dugog i to je potencijalno stanje da se napravi mlin koji sadrzi 3 kamena.
                    value += 15

    # leva linija medju kvadratima
    line_sum = 0
    for square in range(3):
        line_sum += stones[square][1][1]

    if abs(line_sum) == 3:
        value += line_sum * 10
        if line_sum == 2:  # Dodatna nagrada za crnog igraca kada krene da formira mlin, to znaci da je stavio dva kamena jedan pored dugog i to je potencijalno stanje da se napravi mlin koji sadrzi 3 kamena.
            value += 15

    # gornja linija medju kvadratima
    line_sum = 0
    for square in range(3):
        line_sum += stones[square][0][1]

    if abs(line_sum) == 3:
        value += line_sum * 10
        if line_sum == 2:  # Dodatna nagrada za crnog igraca kada krene da formira mlin, to znaci da je stavio dva kamena jedan pored dugog i to je potencijalno stanje da se napravi mlin koji sadrzi 3 kamena.
                value += 15

    # desna linija medju kvadratima
    line_sum = 0
    for square in range(3):
        line_sum += stones[square][1][2]

    if abs(line_sum) == 3:
        value += line_sum * 10
        if line_sum == 2:  # Dodatna nagrada za crnog igraca kada krene da formira mlin, to znaci da je stavio dva kamena jedan pored dugog i to je potencijalno stanje da se napravi mlin koji sadrzi 3 kamena.
                value += 15
    # donja linija medju kvadratima
    line_sum = 0
    for square in range(3):
        line_sum += stones[square][2][1]

    # Primer dodavanja T-oblika
    for square in range(3):
        if (
        stones[square][0][1] == stones[square][1][1] == stones[square][2][1]
        and stones[square][1][0] == 0
        and stones[square][1][2] == 0
    ):
         value += stones[square][0][1] * 10


    # Primer dodavanja L-oblika (ignoriši centralnu tačku srednjeg kvadrata)
    for square in range(3):
    # Horizontalni L-oblik
        if (
        stones[square][0][0] == stones[square][1][0] == stones[square][2][0]
        and stones[square][0][1] == 0
        and stones[square][0][2] == 0
    ):
            value += stones[square][0][0] * 10

    # Vertikalni L-oblik
    if (
        stones[square][0][0] == stones[square][0][1] == stones[square][0][2]
        and stones[square][1][0] == 0
        and stones[square][2][0] == 0
    ):
        value += stones[square][0][0] * 10

    # Diagonalni L-oblik (od gornjeg levog do donjeg desno)
    if (
        stones[square][0][0] == stones[square][1][1] == stones[square][2][2]
        and stones[square][0][1] == 0
        and stones[square][0][2] == 0
        and stones[square][1][0] == 0
        and stones[square][2][0] == 0
    ):
        value += stones[square][0][0] * 10

    # Diagonalni L-oblik (od gornjeg desnog do donjeg levog)
    if (
        stones[square][0][2] == stones[square][1][1] == stones[square][2][0]
        and stones[square][0][0] == 0
        and stones[square][0][1] == 0
        and stones[square][1][2] == 0
        and stones[square][2][2] == 0
    ):
        value += stones[square][0][2] * 10

    # Identifikacija potencijalnih mlinova za belog igrača
    for square in range(3):
        for line in [0, 2]:
            line_sum = 0
            for spot in range(3):
                line_sum += state['stones'][square][line][spot]

            if abs(line_sum) == 2:
                # Blokiranje potencijalnih mlinova postavljanjem crnog kamena u blizini
                for spot in range(3):
                    if state['stones'][square][line][spot] == 0:
                        state_copy = copy.deepcopy(state)
                        apply_move(state_copy, (SET_STONE, BLACK, square, line, spot))
                        vred_potencijalnog_mlina = evaluate(state_copy)
                        # Postavljanje kazne na -15 za belog igraca ako pokusa da napravi mlin
                        value -= 25

                if square in [0, 1]:
                        for spot_block in range(3):
                            if state['stones'][square][line][spot_block] == 0:
                                state_copy_block = copy.deepcopy(state_copy)
                                apply_move(state_copy_block, (SET_STONE, WHITE, square, line, spot_block))
                                vred_potencijalnog_block = evaluate(state_copy_block)
                                # Nagrađivanje crnog igrača sa 15 bodova za blokiranje belog igrača
                                value += 35


    if stones[1][1][1] == BLACK:
        value += 30 

    if abs(line_sum) == 3:
        value += line_sum * 10
        if line_sum == 2:  # Dodatna nagrada za crnog igraca kada krene da formira mlin, to znaci da je stavio dva kamena jedan pored dugog i to je potencijalno stanje da se napravi mlin koji sadrzi 3 kamena.
                value += 15

    # Evaluacija za poteze u sredini kvadrata
    value += stones[1][1][1] * 20

    # count number of stones
    value -= state['white_count'] * 10
    value += state['black_count'] * 10
    return value


# HEURISTIKA ZA LAKU IGRU
def easy_evaluate(state):
    value = 0
    value -= state['white_count'] * 2
    value += state['black_count'] * 2
    return value


# HEURISTIKA ZA SREDNJU IGRU
# heuristika za srednju igru
def medium_evaluate(state):
    stones = state['stones']  # matrica kamena na tabli

    value = 0  # inicijalna vrednost evaluacije

    # identifikacija potencijalnih mlinova za crnog igraca i blokiranje belog igraca
    for square in range(3):  # prolaz kroz sva 3 kvadrata
        for line in [0, 2]:  # prolaz kroz horizontalne linije u kvadratu
            line_sum = 0
            for spot in range(3):  # prolaz kroz sve pozicije u liniji
                line_sum += state['stones'][square][line][spot]

            if abs(line_sum) == 2:  # ako beli igrac ima 2 kamena u liniji
                # blokiranje potencijalnih mlinova belog igraca postavljanjem crnog kamena u blizini
                for spot in range(3):
                    if state['stones'][square][line][spot] == 0:  # ako je pozicija prazna
                        state_copy = copy.deepcopy(state)  # kopiranje stanja
                        apply_move(state_copy, (SET_STONE, BLACK, square, line, spot))  # postavljanje crnog kamena
                        vred_potencijalnog_mlina = evaluate(state_copy)  # evaluacija novog stanja
                        # nagradjivanje crnog igraca sa 15 bodova ako blokira belog igraca
                        value += 15

    # brojanje horizontalnih linija
    for square in range(3):  # prolaz kroz sva 3 kvadrata
        for line in [0, 2]:  # prolaz kroz horizontalne linije u kvadratu
            line_sum = 0
            for spot in range(3):  # prolaz kroz sve pozicije u liniji
                line_sum += stones[square][line][spot]

            if abs(line_sum) == 3:  # ako postoji linija sa 3 kamena
                value += line_sum * 2  # dodavanje vrednosti u zavisnosti od broja kamena

    # brojanje vertikalnih linija
    for square in range(3):  # prolaz kroz sva 3 kvadrata
        for line in [0, 2]:  # prolaz kroz vertikalne linije u kvadratu
            line_sum = 0
            for spot in range(3):  # prolaz kroz sve pozicije u liniji
                line_sum += stones[square][spot][line]

            if abs(line_sum) == 3:  # ako postoji linija sa 3 kamena
                value += line_sum * 2  # dodavanje vrednosti u zavisnosti od broja kamena

    # leva linija među kvadratima
    line_sum = 0
    for square in range(3):  # prolaz kroz sva 3 kvadrata
        line_sum += stones[square][1][1]

    if abs(line_sum) == 3:  # ako postoji linija sa 3 kamena
        value += line_sum * 2  # dodavanje vrednosti u zavisnosti od broja kamena

    # gornja linija među kvadratima
    line_sum = 0
    for square in range(3):  # prolaz kroz sva 3 kvadrata
        line_sum += stones[square][0][1]

    if abs(line_sum) == 3:  # ako postoji linija sa 3 kamena
        value += line_sum * 2  # dodavanje vrednosti u zavisnosti od broja kamena

    # desna linija među kvadratima
    line_sum = 0
    for square in range(3):  # prolaz kroz sva 3 kvadrata
        line_sum += stones[square][1][2]

    if abs(line_sum) == 3:  # ako postoji linija sa 3 kamena
        value += line_sum * 2  # dodavanje vrednosti u zavisnosti od broja kamena

    # donja linija među kvadratima
    line_sum = 0
    for square in range(3):  # prolaz kroz sva 3 kvadrata
        line_sum += stones[square][2][1]

    if abs(line_sum) == 3:  # ako postoji linija sa 3 kamena
        value += line_sum * 2  # dodavanje vrednosti u zavisnosti od broja kamena

    return value 



def get_neighboaring_empty_spots(state, x, y, z):
    stones = state['stones']

    # gde imaju sloboda mesta na levoj strani gde da stavi kamen
    if y != 1 and z - 1 >= 0 and stones[x][y][z - 1] == 0:
        yield x, y, z - 1

    # gde imaju sloboda mesta na desnoj strani
    if y != 1 and z + 1 <= 2 and stones[x][y][z + 1] == 0:
        yield x, y, z + 1

    # gore
    if z != 1 and y - 1 >= 0 and stones[x][y - 1][z] == 0:
        yield x, y - 1, z

    # dole
    if z != 1 and y + 1 <= 2 and stones[x][y + 1][z] == 0:
        yield x, y + 1, z

    # unurasnji deo gde se ispisuje mill to da kulira
    if (y == 1 or z == 1) and x - 1 >= 0 and stones[x - 1][y][z] == 0:
        yield x - 1, y, z

    # cross-square in
    if (y == 1 or z == 1) and x + 1 <= 2 and stones[x + 1][y][z] == 0:
        yield x + 1, y, z


def get_moves(state, player, line_made):
    moves = []
    # ovde se uklanja kamen, vrsi se provera da li je napravljena linija ako jeste uklanja kamen
    if line_made:
        # ovde for petljom prolazim kroz svaki kvastrat i stavljam u niz kamenje
        for s, square in enumerate(state['stones']):
            for i, row in enumerate(square):  # prolazi kroz svaki red
                # prolazi kroz svaki element u tom redu
                for j, element in enumerate(row):
                    # ovde proverava da li je kamen u liniji
                    # pitamo da li je to protivnikov kamen i proverava da li je kamen u liniji
                    if element == player * -1 and not is_stone_in_line(state, s, i, j):
                        moves.append((REMOVE_STONE, player, s, i, j))
        return moves

    # SET_STONE moves
    if len(moves) == 0 and state['white_remaining' if player == 1 else 'black_remaining'] > 0:
        for s, square in enumerate(state['stones']):
            for i, row in enumerate(square):
                for j, element in enumerate(row):
                    if i == 1 and j == 1:
                        continue
                    if element == 0:  # da li na tom mestu mozemo da postavimo kamen
                        moves.append((SET_STONE, player, s, i, j))
        return moves

    # MOVE_STONE moves
    if len(moves) == 0:
        for s, square in enumerate(state['stones']):
            for i, row in enumerate(square):
                for j, element in enumerate(row):
                    if element == player:  # pitam da li je crni kamen
                        # prolazim kroz petlju i proveravam gde ima slobodno mesto, state je nase trenutno stanje igre, s i j to je x y z
                        for x, y, z in get_neighboaring_empty_spots(state, s, i, j):
                            # s, i, j su nove koordinate odnostno pomocna koja update state
                            moves.append(
                                (MOVE_STONE, player, x, y, z, s, i, j))
    return moves

# Dodajemo funkciju za proveru da li je kamen u liniji

def is_stone_in_line(state, x, y, z):
    stones = state['stones']

    # Provera horizontalne linije
    if abs(sum(stones[x][y])) == 3:  # proverava da li su 3 kamena u liniji
        return True

    # Provera vertikalne linije
    if abs(sum(stones[x][i][z] for i in range(3))) == 3:
        return True

    # Provera dijagonalne linije
    if x == 1 and y == 1 and z == 1:
        if abs(sum(stones[i][1][1] for i in range(3))) == 3:
            return True

    # Provera dijagonalne linije koja prolazi kroz sredinu tabele
    if abs(sum(stones[i][1][1] for i in range(3))) == 3:
        return True
    if abs(sum(stones[1][i][1] for i in range(3))) == 3:
        return True
    if abs(sum(stones[1][1][i] for i in range(3))) == 3:
        return True

    # Provera horizontalnih, vertikalnih i dijagonalnih linija za sve x, y, z
    for i in range(3):
        # Provera horizontalne linije za sve x
        if abs(sum(stones[i][y])) == 3:
            return True
        # Provera vertikalne linije za sve z
        if abs(sum(stones[x][j][z] for j in range(3))) == 3:
            return True

        # Provera dijagonalne linije za x, y, z
        if abs(sum(stones[j][i][j] for j in range(3))) == 3:
            return True
        if abs(sum(stones[j][i][2 - j] for j in range(3))) == 3:
            return True
        if abs(sum(stones[j][y][j] for j in range(3))) == 3:
            return True
        if abs(sum(stones[x][j][j] for j in range(3))) == 3:
            return True
        if abs(sum(stones[j][1][z] for j in range(3))) == 3:
            return True
        if abs(sum(stones[x][1][j] for j in range(3))) == 3:
            return True
        if abs(sum(stones[1][y][j] for j in range(3))) == 3:
            return True
        if abs(sum(stones[j][y][2 - j] for j in range(3))) == 3:
            return True

    # Provera linija koje prolaze kroz susedne kvadrate
    if y == 0 or y == 2:
        if abs(sum(stones[x][0][1] for x in range(3))) == 3:
            return True
        if abs(sum(stones[x][2][1] for x in range(3))) == 3:
            return True
    if z == 0 or z == 2:
        if abs(sum(stones[x][1][0] for x in range(3))) == 3:
            return True
        if abs(sum(stones[x][1][2] for x in range(3))) == 3:
            return True

    # Dodatna provera za sve x, y, z
    for i in range(3):
        # Provera horizontalnih linija za sve y
        if abs(sum(stones[x][i][z] for x in range(3))) == 3:
            return True
        # Provera vertikalnih linija za sve x i z
        if abs(sum(stones[j][y][z] for j in range(3))) == 3:
            return True
        # Provera dijagonalnih linija za sve x i y
        if abs(sum(stones[z][i][j] for j in range(3))) == 3:
            return True

    # Provera linija koje prolaze kroz susedne kvadrate za z
    if x == 0 or x == 2:
        if abs(sum(stones[0][i][z] for i in range(3))) == 3:
            return True
        if abs(sum(stones[2][i][z] for i in range(3))) == 3:
            return True
    if y == 0 or y == 2:
        if abs(sum(stones[i][0][z] for i in range(3))) == 3:
            return True
        if abs(sum(stones[i][2][z] for i in range(3))) == 3:
            return True

    return False


def is_making_line(state, move):
    stones = state['stones']
    _, _, x, y, z, *_ = move

    # Provera horizontalne linije
    if abs(sum(stones[x][y])) == 3:
        return True

    # Provera vertikalne linije
    if abs(sum(stones[x][i][z] for i in range(3))) == 3:
        return True

    # Provera dijagonalne linije
    if x == 1 and y == 1 and z == 1:
        if abs(sum(stones[i][1][1] for i in range(3))) == 3:
            return True

    # Provera dijagonalne linije koja prolazi kroz sredinu tabele
    if abs(sum(stones[i][1][1] for i in range(3))) == 3:
        return True
    if abs(sum(stones[1][i][1] for i in range(3))) == 3:
        return True
    if abs(sum(stones[1][1][i] for i in range(3))) == 3:
        return True

    # Provera horizontalnih, vertikalnih i dijagonalnih linija za sve x, y, z
    for i in range(3):
        # Provera horizontalne linije za sve x
        if abs(sum(stones[i][y])) == 3:
            return True
        # Provera vertikalne linije za sve z
        if abs(sum(stones[x][j][z] for j in range(3))) == 3:
            return True

        # Provera dijagonalne linije za x, y, z
        if abs(sum(stones[j][i][j] for j in range(3))) == 3:
            return True
        if abs(sum(stones[j][i][2 - j] for j in range(3))) == 3:
            return True
        if abs(sum(stones[j][y][j] for j in range(3))) == 3:
            return True
        if abs(sum(stones[x][j][j] for j in range(3))) == 3:
            return True
        if abs(sum(stones[j][1][z] for j in range(3))) == 3:
            return True
        if abs(sum(stones[x][1][j] for j in range(3))) == 3:
            return True
        if abs(sum(stones[1][y][j] for j in range(3))) == 3:
            return True
        if abs(sum(stones[j][y][2 - j] for j in range(3))) == 3:
            return True

    # Provera linija koje prolaze kroz susedne kvadrate
    if y == 0 or y == 2:
        if abs(sum(stones[x][0][1] for x in range(3))) == 3:
            return True
        if abs(sum(stones[x][2][1] for x in range(3))) == 3:
            return True
    if z == 0 or z == 2:
        if abs(sum(stones[x][1][0] for x in range(3))) == 3:
            return True
        if abs(sum(stones[x][1][2] for x in range(3))) == 3:
            return True

    # Dodatna provera za sve x, y, z
    for i in range(3):
        # Provera horizontalnih linija za sve y
        if abs(sum(stones[x][i][z] for x in range(3))) == 3:
            return True
        # Provera vertikalnih linija za sve x i z
        if abs(sum(stones[j][y][z] for j in range(3))) == 3:
            return True
        # Provera dijagonalnih linija za sve x i y
        if abs(sum(stones[z][i][j] for j in range(3))) == 3:
            return True

    # Provera linija koje prolaze kroz susedne kvadrate za z
    if x == 0 or x == 2:
        if abs(sum(stones[0][i][z] for i in range(3))) == 3:
            return True
        if abs(sum(stones[2][i][z] for i in range(3))) == 3:
            return True
    if y == 0 or y == 2:
        if abs(sum(stones[i][0][z] for i in range(3))) == 3:
            return True
        if abs(sum(stones[i][2][z] for i in range(3))) == 3:
            return True

    return False


# ovde prati trenutno stanje
def apply_move(state, move):
    stones = state['stones']
    if move[MOVE_TYPE] == SET_STONE:  # koji je potez na redu u ovom slucaju je postavljanje
        _, color, x, y, z = move  # uzimamo koordinate tog kamena i njegovu boju
        # kada nadje to stanje u koordinatama tu postavljamo kamen odgovarajuce boje
        stones[x][y][z] = color
        # kada postavi kamen uklanja za jedan od onih koje ima
        state['white_remaining' if color == WHITE else 'black_remaining'] -= 1
        # povecava broj kamena na tabli
        state['white_count' if color == WHITE else 'black_count'] += 1
    elif move[MOVE_TYPE] == REMOVE_STONE:  # sada ako je na redu uklanjanje
        _, color, x, y, z = move  # isto proverava koordinate, info stavlja u niz move
        # kada pojedemo kamen tu stavljamo stanje 0, znaci da na toj koordinati nema vise kamena na tabli
        stones[x][y][z] = 0
        # gleda se koja je boja, i uklanja se taj kamen
        state['white_count' if color == WHITE else 'black_count'] -= 1
    elif move[MOVE_TYPE] == MOVE_STONE:  # pomeranje kamena
        # sada uzimamo stanje boje i koordinata od oba kamena gde treba da postavi i gde da makne
        _, color, to_x, to_y, to_z, from_x, from_y, from_z = move
        # na to mesto gde se mako kamen restartije vrednost na 0
        stones[from_x][from_y][from_z] = 0
        # na toj novoj poziciji gde se postavio kamen se stavlja odgovarajuca boja odnosno vrednost
        stones[to_x][to_y][to_z] = color

    state['turn'] += 1


def minimax(state, depth, player, line_made=False, alpha=float('-inf'), beta=float('inf')):
    # pitamo da li je dostigao dubinu nula i da li je kraj igre
    if depth == 0 or is_end(state):
        # ako nije vraca tu easy heuristiku, ako je kraj igre vraca none i nista ne radi
        return easy_evaluate(state), None

    # ovo proverava koji je igrac trenutni pa daje potez igre protivniku
    next_player = player * -1

    if player == WHITE:  # pitam da li je beli igrac
        # vrednosti mogu da idu do - beskonacno da bi maksimizirao svoj potez
        value = float('-inf')
        best_move = None  # promenljiva koja sluzi za najbolji potez
        for move in get_moves(state, player, line_made):  # prolazim kroz sve poteze
            apply_move(state, move)  # gledamo koji je potez sledeci
            # sada proveravamo da li je taj potez napravio mlin, ako jeste izvrsi tu funkciju za prabljenje linije
            if is_making_line(state, move):
                next_player *= -1  # daje potez sledecem igracu
                line_made = True  # vraca vrednost true jer linija je formirana
            # rekurzivno pozivam minimax alg da sledeci igra
            new_value = minimax(state, depth - 1, next_player,
                                line_made, alpha, beta)[0]
            if new_value > value:  # ako je nova vrednost veca od stare vrednosti uzima tu najnoviju vrednost kao najbolji potez
                value = new_value
                best_move = move
            line_made = False
            # undo_move(state, move)
            # ovde koristim alphabeta odsecanje, svaki put max igrac(covek) azurira svoju vrednost za alfa pitace da li nam je ta vrednost veca ili jednaka od bete
            alpha = max(alpha, value)
            if value >= beta:  # ako jeste onda stablo koje ima gori potez odseca ga
                break
    else:
        # isti princim kao za belog ovo gleda za crnog igraca, ide + beskonacno kako bi minimizirao svoj potez
        value = float('inf')
        best_move = None
        for move in get_moves(state, player, line_made):
            apply_move(state, move)
            if is_making_line(state, move):
                next_player *= -1
                line_made = True
            new_value = minimax(state, depth - 1, next_player,
                                line_made, alpha, beta)[0]
            if new_value < value:
                value = new_value
                best_move = move
            line_made = False
            # undo_move(state, move)
            beta = min(beta, value)
            if value <= alpha:
                break

    return value, best_move

# MEDIUM
def alphabeta(state, depth, a, b, player, line_made=False, rock=-1):
    if depth == 0 or is_end(state):
        return medium_evaluate(state), None

    next_player = player * -1

    if player == WHITE:
        value = float('-inf')
        best_move = None
        for move in get_moves(state, player, line_made):
            state_copy = copy.deepcopy(state)
            apply_move(state_copy, move)
            if is_making_line(state_copy, move):
                next_player *= -1
                line_made = True
            new_value = alphabeta(state_copy, depth - 1,
            a, b, next_player, line_made, -1)[0]
            if new_value > value or best_move is None:
                best_move = move
                value = new_value
            line_made = False
            if value > b:
                break
            a = max(a, value)
        return value, best_move
    elif player == BLACK:
        value = float('inf')
        best_move = None
        for move in get_moves(state, player, line_made):
            state_copy = copy.deepcopy(state)
            apply_move(state_copy, move)
            if is_making_line(state_copy, move):
                next_player *= -1
                line_made = True
            new_value = alphabeta(state_copy, depth - 1,
            a, b, next_player, line_made, 1)[0]
            if new_value < value or best_move is None:
                best_move = move
                value = new_value
            line_made = False
            if value < a:
                break
            b = min(b, value)
        return value, best_move

# HARD
def alphabeta(state, depth, a, b, player, line_made=False, rock=-1):
    if depth == 0 or is_end(state):
        return evaluate(state), None

    next_player = player * -1

    if player == WHITE:
        value = -1000000
        best_move = None
        for move in get_moves(state, player, line_made):
            state_copy = copy.deepcopy(state)
            apply_move(state_copy, move)
            if is_making_line(state_copy, move):
                next_player *= -1
                line_made = True

            new_value, _ = alphabeta(
                state_copy, depth - 1, a, b, next_player, line_made, -1)
            if new_value > value or best_move is None:
                best_move = move
                value = new_value

            line_made = False
            # print(f"DEBUG: {move} - {value} ({a}, {b})")
            if value > b:
                break
            a = max(a, value)

        return value, best_move

    elif player == BLACK:
        value = 1000000
        best_move = None
        for move in get_moves(state, player, line_made):
            state_copy = copy.deepcopy(state)
            apply_move(state_copy, move)
            if is_making_line(state_copy, move):
                next_player *= -1
                line_made = True

            new_value, _ = alphabeta(
                state_copy, depth - 1, a, b, next_player, line_made, 1)
            if new_value < value or best_move is None:
                best_move = move
                value = new_value

            line_made = False
            # print(f"DEBUG: {move} - {value} ({a}, {b})")
            if value < a:
                break
            b = min(b, value)

        return value, best_move
