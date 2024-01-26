import copy

SET_STONE = 'set'
MOVE_STONE = 'move'
REMOVE_STONE = 'remove'

WHITE = 1
BLACK = -1

# potez izgleda ovako (MOVE_TYPE, MOVE_COLOR, MOVE_X, MOVE_Y, MOVE_Z)
# ove konstante su indeksi u tuple koji predstavlja potez
# npr: ako indeksiramo potez sa MOVE_TYPE (nulom), dobicemo tip poteza
MOVE_TYPE = 0
MOVE_COLOR = 1
MOVE_X = 2
MOVE_Y = 3
MOVE_Z = 4


def is_end(state):
    return state['white_remaining'] == 0 and state['black_remaining'] == 0 and (state['white_count'] <= 2 or state['black_count'] <= 2)


# stones[square][line][spot]
# [
#       0  1  2 
#       ^--^--^--- polja unutar linije      
#    
#     [[0, 0, 0],   kvadrat 0   linija 0
#      [0, X, 0],               linija 1
#      [0, 0, 0]],              linija 2
#
#     [[0, 0, 0],   kvadrat 1   linija 0
#      [0, X, 0],               linija 1
#      [0, 0, 0]],              linija 2
#
#     [[0, 0, 0],   kvadrat 2   linija 0
#      [0, X, 0],               linija 1
#      [0, 0, 0]],              linija 2
# ]

# HEURISTIKA ZA TESKU IGRU
def evaluate(state):
    stones = state['stones']

    value = 0

    # count horizontal lines
    # proveravamo za svaki kvadrat
    # square je trenutni kvadrat koji proveravamo
    for square in range(3):
        # proveravamo horizontalne linije unutar kvadrata
        # srednju liniju (liniju 1) preskacemo jer
        # ona nema 3 elementa i ne moze da napravi mlin
        for line in [0, 2]:
            line_sum = 0
            # za trenutnu liniju proveravamo svako polje
            # sabiramo ih sve tako sto 1 predstavalja beli kamen,
            # -1 crni a nula prazno polje
            for spot in range(3):
                line_sum += stones[square][line][spot]

            # ako smo dobili zbir 3, to znaci da postoji linija koja ima 3 bela kamena
            # ako smo dobili zbir -3, postoji linija sa 3 crna kamena
            # posto nas zanima je li postoji linija uopste, uzimamo apsolutnu vrednost
            # ako je apsolutna vrednost 3, znaci da ima linija neke boje
            if abs(line_sum) == 3: # proveravam da li je uopste linija
                # line_sum je pozitivan broj za belog a negativan za crtnog
                # tako da mozemo da ga dodamo na vrednost heuristike s time sto
                # mnozimo sa 10 jer smo izabrali tu vrednost za liniju (bice 30 ili -30)
                value += line_sum * 10
                
            # proveravamo potencijalnu liniju,
            # u slucaju da imaju 2 kamena iste boje, apsolutni zbir ce biti 2
            if abs(line_sum) == 2:  # Dodatna nagrada za crnog igraca kada krene da formira mlin, to znaci da je stavio dva kamena jedan pored dugog i to je potencijalno stanje da se napravi mlin koji sadrzi 3 kamena.
                value += line_sum * 7


    # count vertical lines
    # proveravamo za svaki kvadrat
    # square je trenutni kvadrat koji proveravamo
    for square in range(3):
        # proveravamo vertikalne linije unutar kvadrata
        # srednju liniju (liniju 1) preskacemo jer
        # ona nema 3 elementa i ne moze da napravi mlin
        for line in [0, 2]:
            line_sum = 0
            # za trenutnu liniju proveravamo svako polje
            # sabiramo ih sve tako sto 1 predstavalja beli kamen,
            # -1 crni a nula prazno polje
            for spot in range(3):
                line_sum += stones[square][spot][line]

            # ako smo dobili zbir 3, to znaci da postoji linija koja ima 3 bela kamena
            # ako smo dobili zbir -3, postoji linija sa 3 crna kamena
            # posto nas zanima je li postoji linija uopste, uzimamo apsolutnu vrednost
            # ako je apsolutna vrednost 3, znaci da ima linija neke boje
            if abs(line_sum) == 3:
                # line_sum je pozitivan broj za belog a negativan za crtnog
                # tako da mozemo da ga dodamo na vrednost heuristike s time sto
                # mnozimo sa 10 jer smo izabrali tu vrednost za liniju (bice 30 ili -30)
                value += line_sum * 10

            # proveravamo potencijalnu liniju,
            # u slucaju da imaju 2 kamena iste boje, apsolutni zbir ce biti 2
            if abs(line_sum) == 2:  # Dodatna nagrada za crnog igraca kada krene da formira mlin, to znaci da je stavio dva kamena jedan pored dugog i to je potencijalno stanje da se napravi mlin koji sadrzi 3 kamena.
                value += line_sum * 7

    # leva linija medju kvadratima
    # svako polje u levoj liniji koja spaja kvadrate ima
    # indekse za liniju i polje 1, a jedino se razlikuje indeks za kvadrat
    # za svaki kvadrat proveravamo odredjeno polje koje cini tu liniju
    line_sum = 0
    for square in range(3):
        line_sum += stones[square][1][1]

    # ako smo dobili zbir 3, to znaci da postoji linija koja ima 3 bela kamena
    # ako smo dobili zbir -3, postoji linija sa 3 crna kamena
    # posto nas zanima je li postoji linija uopste, uzimamo apsolutnu vrednost
    # ako je apsolutna vrednost 3, znaci da ima linija neke boje
    if abs(line_sum) == 3:
        # line_sum je pozitivan broj za belog a negativan za crtnog
        # tako da mozemo da ga dodamo na vrednost heuristike s time sto
        # mnozimo sa 10 jer smo izabrali tu vrednost za liniju (bice 30 ili -30)
        value += line_sum * 10

    # proveravamo potencijalnu liniju,
    # u slucaju da imaju 2 kamena iste boje, apsolutni zbir ce biti 2
    if abs(line_sum) == 2:  # Dodatna nagrada za crnog igraca kada krene da formira mlin, to znaci da je stavio dva kamena jedan pored dugog i to je potencijalno stanje da se napravi mlin koji sadrzi 3 kamena.
        value += line_sum * 7

    # gornja linija medju kvadratima
    line_sum = 0
    for square in range(3):
        line_sum += stones[square][0][1]

    if abs(line_sum) == 3:
        value += line_sum * 10
    if abs(line_sum) == 2:  # Dodatna nagrada za crnog igraca kada krene da formira mlin, to znaci da je stavio dva kamena jedan pored dugog i to je potencijalno stanje da se napravi mlin koji sadrzi 3 kamena.
            value += line_sum * 7

    # desna linija medju kvadratima
    line_sum = 0
    for square in range(3):
        line_sum += stones[square][1][2]

    if abs(line_sum) == 3:
        value += line_sum * 10
    if abs(line_sum) == 2:  # Dodatna nagrada za crnog igraca kada krene da formira mlin, to znaci da je stavio dva kamena jedan pored dugog i to je potencijalno stanje da se napravi mlin koji sadrzi 3 kamena.
            value += line_sum * 7

    # donja linija medju kvadratima
    line_sum = 0
    for square in range(3):
        line_sum += stones[square][2][1]

    if abs(line_sum) == 3:
        value += line_sum * 10
    if abs(line_sum) == 2:  # Dodatna nagrada za crnog igraca kada krene da formira mlin, to znaci da je stavio dva kamena jedan pored dugog i to je potencijalno stanje da se napravi mlin koji sadrzi 3 kamena.
            value += line_sum * 7

    # count number of stones
    value += state['white_count'] * 10
    value -= state['black_count'] * 10
    return value


# HEURISTIKA ZA LAKU IGRU
def easy_evaluate(state):
    value = 0
    value += state['white_count'] * 2
    value -= state['black_count'] * 2
    return value


# HEURISTIKA ZA SREDNJU IGRU
# Ovde samo nagradjuje mlinove a ne nagradjuje potenceijalne mlinove
def medium_evaluate(state):
    stones = state['stones']  # matrica kamena na tabli

    value = 0  # inicijalna vrednost evaluacije

    # brojanje horizontalnih linija
    for square in range(3):  # prolaz kroz sva 3 kvadrata
        for line in [0, 2]:  # prolaz kroz horizontalne linije u kvadratu
            line_sum = 0
            for spot in range(3):  # prolaz kroz sve pozicije u liniji
                line_sum += stones[square][line][spot]

            if abs(line_sum) == 3:  # ako postoji linija sa 3 kamena
                value += line_sum * 5  # dodavanje vrednosti u zavisnosti od broja kamena

    # brojanje vertikalnih linija
    for square in range(3):  # prolaz kroz sva 3 kvadrata
        for line in [0, 2]:  # prolaz kroz vertikalne linije u kvadratu
            line_sum = 0
            for spot in range(3):  # prolaz kroz sve pozicije u liniji
                line_sum += stones[square][spot][line]

            if abs(line_sum) == 3:  # ako postoji linija sa 3 kamena
                value += line_sum * 5  # dodavanje vrednosti u zavisnosti od broja kamena

    # leva linija među kvadratima
    line_sum = 0
    for square in range(3):  # prolaz kroz sva 3 kvadrata
        line_sum += stones[square][1][0]

    if abs(line_sum) == 3:  # ako postoji linija sa 3 kamena
        value += line_sum * 5  # dodavanje vrednosti u zavisnosti od broja kamena

    # gornja linija među kvadratima
    line_sum = 0
    for square in range(3):  # prolaz kroz sva 3 kvadrata
        line_sum += stones[square][0][1]

    if abs(line_sum) == 3:  # ako postoji linija sa 3 kamen
        value += line_sum * 5  # dodavanje vrednosti u zavisnosti od broja kamena

    # desna linija među kvadratima
    line_sum = 0
    for square in range(3):  # prolaz kroz sva 3 kvadrata
        line_sum += stones[square][1][2]

    if abs(line_sum) == 3:  # ako postoji linija sa 3 kamena
        value += line_sum * 5  # dodavanje vrednosti u zavisnosti od broja kamena

    # donja linija među kvadratima
    line_sum = 0
    for square in range(3):  # prolaz kroz sva 3 kvadrata
        line_sum += stones[square][2][1]

    if abs(line_sum) == 3:  # ako postoji linija sa 3 kamena
        value += line_sum * 5  # dodavanje vrednosti u zavisnosti od broja kamena
    
    value += state['white_count'] * 2
    value -= state['black_count'] * 2

    return value 


# prazna polja koja su susedna nekom kamenu.
# x, y, z su koordinata datog kamena
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

    # proverava ima li prazno polje po liniji koa spaja kvadrate
    # gleda ka spoljnjem kvadratu (kvadratu koji je oko trenutnog)
    if (y == 1 or z == 1) and x - 1 >= 0 and stones[x - 1][y][z] == 0:
        yield x - 1, y, z

    # proverava ima li prazno polje po liniji koa spaja kvadrate
    # gleda ka unutrasnjem kvadratu (kvadratu koji je unutar trenutnog)
    if (y == 1 or z == 1) and x + 1 <= 2 and stones[x + 1][y][z] == 0:
        yield x + 1, y, z


def get_moves(state, player, line_made):
    moves = []
    # vrsi se provera da li je napravljena linija, ako jeste uklanja kamen
    if line_made:
        # ovde for petljom prolazim kroz svaki kvastrat i stavlja u niz kamenje
        for s, square in enumerate(state['stones']):
            for i, row in enumerate(square):  # prolazi kroz svaki red
                # prolazi kroz svaki element u tom redu
                for j, element in enumerate(row):
                    # ovde proverava da li je kamen u liniji, ako jeste onda nece biti validan potez
                    # pa ne dodajemo u moguce poteze.
                    # pitamo da li je to protivnikov kamen
                    if element == player * -1 and not is_stone_in_line(state, s, i, j):
                        moves.append((REMOVE_STONE, player, s, i, j))
        return moves

    # SET_STONE moves
    # ako smo u fazi postavljanja kamenja, trazimo sva prazna polja i kreiramo potez postavljanja na to polje
    current_player_remaining = 'white_remaining' if player == WHITE else 'black_remaining'
    if len(moves) == 0 and state[current_player_remaining] > 0: # u set fazi zmo ako je uslov ispunjen
        for s, square in enumerate(state['stones']):
            for i, row in enumerate(square):
                for j, element in enumerate(row):
                    # preskacemo centralni element jer se ne koristi u igri
                    if i == 1 and j == 1:
                        continue
                    # proveravamo je li trenutno polje prazno.
                    # ako jeste, dodajemo potez za postavljanje kamena
                    # trenutnog igraca na to polje
                    if element == 0:
                        moves.append((SET_STONE, player, s, i, j))
        return moves

    # MOVE_STONE moves
    # ako smo u fazi pomeranja kamenja, proveravamo gde svaki kamen trenutnog igraca moze da se pomeri
    if len(moves) == 0:
        for s, square in enumerate(state['stones']):
            for i, row in enumerate(square):
                for j, element in enumerate(row):
                    # ako kamen pripada trenutnom igracu, trazimo sva prazna susdna polja.
                    # na svako prazno susedno polje trenutni kamen moze da se pomeri
                    if element == player:
                        # za svako prazno susedno polje kreiramo moguci potez pomeranja trenutnog kamena na to polje
                        for x, y, z in get_neighboaring_empty_spots(state, s, i, j):
                            # s, i, j su trenutne koordinate kamena, a x, y i z su koordinate na koje moze da se pomeri
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

    # Provera horizontalnu liniju
    if abs(sum(stones[x][y])) == 3:
        return True

    # Provera vertikalnu liniju
    if abs(sum(stones[x][i][z] for i in range(3))) == 3:
        return True

    # Provera linija(sredisnja) koje spajaju kvadrate
    if y == 0 or y == 2:
        # gornja sredisnja linija
        if abs(sum(stones[x][0][1] for x in range(3))) == 3:
            return True
        # donja
        if abs(sum(stones[x][2][1] for x in range(3))) == 3:
            return True
    if z == 0 or z == 2:
        # leva
        if abs(sum(stones[x][1][0] for x in range(3))) == 3:
            return True
        # desna
        if abs(sum(stones[x][1][2] for x in range(3))) == 3:
            return True

    return False


# ovde prati trenutno stanje
def apply_move(state, move):
    stones = state['stones']
    if move[MOVE_TYPE] == SET_STONE:  # koji je potez na redu u ovom slucaju je postavljanje
        _, color, x, y, z = move  # uzimamo koordinate tog kamena i njegovu boju
        # na tim koordinatama postavljamo kamen odgovarajuce boje
        stones[x][y][z] = color
        # kada postavi kamen smanjuje za jedan od onih koje ima
        state['white_remaining' if color == WHITE else 'black_remaining'] -= 1
        # povecava broj kamena na tabli
        state['white_count' if color == WHITE else 'black_count'] += 1
    elif move[MOVE_TYPE] == REMOVE_STONE:  # sada ako je na redu uklanjanje
        _, color, x, y, z = move  # isto proverava koordinate kamena koji uklanjamo
        # kada pojedemo kamen tu stavljamo stanje 0, znaci da na toj koordinati nema vise kamena na tabli
        stones[x][y][z] = 0
        # gleda se koja je boja, i uklanja se taj kamen
        state['white_count' if color == WHITE else 'black_count'] -= 1
    elif move[MOVE_TYPE] == MOVE_STONE:  # pomeranje kamena
        # sada uzimamo koordinate oba kamena gde treba da postavi i gde da makne
        # sa koordinata koje pocinju sa 'from' se uklanja kamen
        # a na koordinate koje pocinju sa 'to' se postavlja kamen
        _, color, to_x, to_y, to_z, from_x, from_y, from_z = move
        # na to mesto gde se makao kamen restartuje vrednost na 0
        stones[from_x][from_y][from_z] = 0
        # na toj novoj poziciji gde se postavio kamen se stavlja odgovarajuca boja odnosno vrednost
        stones[to_x][to_y][to_z] = color

    state['turn'] += 1


def minimax(state, depth, player, line_made=False):
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
            state_copy = copy.deepcopy(state)
            new_value = minimax(state_copy, depth - 1, next_player,line_made)[0]
            if new_value > value:  # ako je nova vrednost veca od stare vrednosti uzima tu najnoviju vrednost kao najbolji potez
                value = new_value
                best_move = move
            line_made = False
    else:
        # isti princim kao za belog ovo gleda za crnog igraca, ide + beskonacno kako bi minimizirao svoj potez
        value = float('inf')
        best_move = None
        for move in get_moves(state, player, line_made):
            apply_move(state, move)
            if is_making_line(state, move):
                next_player *= -1
                line_made = True
            state_copy = copy.deepcopy(state)
            new_value = minimax(state_copy, depth - 1, next_player, line_made)[0]
            if new_value < value:
                value = new_value
                best_move = move
            line_made = False

    return value, best_move

# MEDIUM
def alphabeta_medium(state, depth, a, b, player, line_made=False):
    if depth == 0 or is_end(state):
        return medium_evaluate(state), None

    next_player = player * -1

    if player == WHITE:
        value = -100000
        best_move = None
        for move in get_moves(state, player, line_made):
            state_copy = copy.deepcopy(state)
            apply_move(state_copy, move)
            if is_making_line(state_copy, move):
                next_player *= -1
                line_made = True
            new_value = alphabeta_medium(state_copy, depth - 1,a, b, next_player, line_made)[0]
            if new_value > value or best_move is None:
                best_move = move
                value = new_value
            line_made = False
            if value > b:
                break
            a = max(a, value)
        return value, best_move
    elif player == BLACK:
        value = 100000
        best_move = None
        for move in get_moves(state, player, line_made):
            state_copy = copy.deepcopy(state)
            apply_move(state_copy, move)
            if is_making_line(state_copy, move):
                next_player *= -1
                line_made = True
            new_value = alphabeta_medium(state_copy, depth - 1,a, b, next_player, line_made)[0]
            if new_value < value or best_move is None:
                best_move = move
                value = new_value
            line_made = False
            if value < a:
                break
            b = min(b, value)
        return value, best_move

# HARD
def alphabeta(state, depth, a, b, player, line_made=False):
    if depth == 0 or is_end(state):
        return evaluate(state), None

    # next_player je sledeci igrac, a player je trenutni
    next_player = player * -1

    # ako je trenutni igrac beli, vrsi se maximizing deo algoritma
    if player == WHITE:
        # vrednost je u pocetku veliki negativni broj jer trazimo najveci koji se pojavi
        value = -1000000
        best_move = None
        # za svaki moguci sledeci potez, izvrsavamo dalje algoritam
        for move in get_moves(state, player, line_made):
            # kreiramo kopiju stanja da bi nam ostao original kao sto trenutno jeste
            state_copy = copy.deepcopy(state)
            # promenimo kopiju stanja tako da je odigran potez koji trenutno posmatramo
            apply_move(state_copy, move)
            # ako trenutni potez kreira liniju, seledeci igrac ostaje isti
            if is_making_line(state_copy, move):
                # vracamo sledeceg igraca na proslu vrednost
                next_player *= -1
                line_made = True

            # razvijamo stablo igre dalje i uzimamo vrednost stanja do kojeg su nas ti potezi doveli
            new_value, _ = alphabeta(
                state_copy, depth - 1, a, b, next_player, line_made)
            # ako smo naisli na potez koji ima vecu vrednost
            # postavaljamo najbolji potez na taj i najbolju vrednost na vrednost koja njemu odgovara
            if new_value > value or best_move is None:
                best_move = move
                value = new_value

            line_made = False
            # vrsimo odsecanje ako je trenutna vrednost veca od b(beta)
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
                state_copy, depth - 1, a, b, next_player, line_made)
            if new_value < value or best_move is None:
                best_move = move
                value = new_value

            line_made = False
            # print(f"DEBUG: {move} - {value} ({a}, {b})")
            if value < a:
                break
            b = min(b, value)

        return value, best_move
