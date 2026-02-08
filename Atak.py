# Jakub Flis
# Szyfr rotacyjny Cardan grille
#
# Atak.py przeprowadza atak z simulated annealing na kryptotekst szyfrowany grillem Kardano o znanym rozmiarze grilla
# Program po okolo minucie ze skutecznoscia okolo 90% zwroci rozszyfrowany tekst i uzyty grill/klucz
#
# Juz przy n = 14 istnieje az 4^49 mozliwych kluczy/grillow
# Metoda simulated annealing znacznie przyspiesza przeszukiwanie przestrzeni klucza:
#
# Instrukcja obslugi:
# 1. Wygenerowac kryptotekst w cardan4.py
# 2. Uruchomic Atak.py
# 3. Zeby skrocic atak nalezy zwiekszyc parametr tempDelta by program szybciej przegladal przestrzen kluczy
# 4. Plik tester.py sluzy do wykonania x atakow, zapisania i posortowania ich wynikow
# 5. Plik gen_spanish_quadgrams.py mozna uzyc do wygenerowania statystyk quadgramow hiszpanskich
# 6. Plik ngram_score wykorzystano do oceny czytelnosci tekstow uzyskiwanych podczas ataku
#
# Zastosowane idee:
# 1. Do generowania kluczy i do modyfikacji klucza uzywana jest mapa mozliwych konfiguracji otworow holeMap
#    Dzieki temu program porusza sie tylko i wylacznie po przestrzeni poprawnych kluczy
# 2. Jako ze simulated annealing nie ma tendencji do utykania w maksimum lokalnym,
#    to w changeKeyFull() wystarczy tylko jedna metoda zmiany klucza
# 3. Uzyto quadgramy zamiast bigramow, dla wiekszej precyzji w ustalaniu czytelnosci i dla
#    zwiekszenia efektywnosci ataku
# 4. Wygenerowano wlasne statystyki quadgramow hiszpanskich z 5 wspolczesnych ksiazek hiszpanskich (2500 stron)
#
# Im wiecej kryptotekstu tym bardziej skuteczne lamanie szyfru
#
# Automatyczne znajdowanie rozmiaru grilla podczas ataku zostalo wylaczone
# Konieczne jest dostosowanie dlugosci krotkiego ataku na kazdy rozmiar grilla
# W zaleznosci od rozmiaru przestrzeni kluczy
# W przeciwnym razie male grille (n = 4) sa oceniane zbyt wysoko bo maja zbyt duzo czasu na uzyskanie czytelnosci
#
# Nie wprowadzono ograniczenia czasowego dla ataku
# Gdyz wielowatkowosc to bardzo utrudnia (koniecznosc dostosowywania wielu parametrow)
# Oraz przez to ze za czas ataku i tak odpowiada glownie 1 parametr - tempDelta

import math
import numpy as np
import random
import time
from ngram_score import ngram_score
from multiprocessing import cpu_count as mp_cpu_count
from multiprocessing import Pool as mp_pool

def rot90Matrix(matrix, k=1):
    return np.rot90(matrix, k, axes=(1,0))

def flatten(grid):
    txt = ''
    for i in range(len(grid)):
        for j in range(len(grid)):
            txt += str(grid[i][j])
    return txt

def unflatten(arr):  # key 1d -> grill 2d
    size = int(math.sqrt(len(arr)))

    arr2 = np.array(list(arr), dtype=int)

    grill = arr2.reshape((size, size))

    return grill

def unflatten2(arr):  # dla decrypt
    size = int(math.sqrt(len(arr)))

    arr2 = np.array(list(arr), dtype=str)

    grill = arr2.reshape((size, size))

    return grill

def decrypt(kt, key):
    grill = unflatten(key)
    grid = unflatten2(kt)
    txt = ''

    for rotNr in range(1,5):
        for j in range(len(grill)):
            for i in range(len(grill)):
                if grill[j][i] == 1:
                    txt += grid[j][i]
        grill = rot90Matrix(grill)

    #print(txt)
    return txt

def possibleHoleMap(n):
    size = n/2

    positions = list(range(int(size*size)))

    quarter1 = unflatten(positions)

    quarter2 = rot90Matrix(quarter1)

    q1 = np.array(quarter1)
    q2 = np.array(quarter2)

    q12 = np.hstack((q1, q2))

    quarter3 = rot90Matrix(quarter2)
    quarter4 = rot90Matrix(quarter3)

    q3 = np.array(quarter3)
    q4 = np.array(quarter4)

    # na odwrót bo trzecia ćwiartka jest po prawej
    q34 = np.hstack((q4, q3))
    positions = np.vstack((q12, q34))

    indexes = {}
    for i in range(n):
        for j in range(n):
            liczba = positions[i][j]
            if liczba not in indexes:
                indexes[liczba] = []
            indexes[liczba].append((i,j))

    #print(indexes)
    return indexes

def generateKey(n, holeMap):
    key = np.full((n, n), 0, dtype=int)
    for elem in holeMap.keys():
        i,j = random.choice(holeMap[elem])
        key[i][j] = 1

    return flatten(key)

def changeKey1(key, n, holeMap):
    # musimy wybrac jakis otwor i go zmienic na jeden z trzech innych mozliwych otworow z holemap
    ind = 0
    #print(key)
    # print(key)
    available_indices = [i for i, value in enumerate(key) if int(value) == 1]

    ind = random.choice(available_indices)

    x = ind // n
    y = ind % n

    klucz = 0

    for k, lista in holeMap.items():
        for i,j in lista:
            if (x,y) == (i,j):
                klucz = k

    i, j = 0,0

    posList = list(holeMap[klucz])
    curr = posList.index((x,y))
    del posList[curr]
    i,j = random.choice(posList) # zmienimy otwor na inny z 3 mozliwych

    ind2 = i*n + j

    key = list(key)
    # podmieniamy otwor
    key[ind] = 0
    key[ind2] = 1

    return ''.join(str(x) for x in key)

def changeKeyFull(key, n, holeMap):
    r = random.random()
    r_probs = [1.00]
    if r < sum(r_probs[:1]):
        return changeKey1(key, n, holeMap)  # , 'change1'

def AcceptanceFunction(valueOld, valueNew, temp):
    if random.random() < math.exp( -75*(valueOld - valueNew)/temp):  # dla temp_startowej trzeba starać się, żeby prawd. było pomiędzy 0.2 a 0.7 dla umiarkowanego pogorszenia
        #print('zmiana')
        return True
    else:
        return False

def Sim_MP_min( ct, n, holeMap, ng, tempDelta):
    t1 = time.time()
    ncore = mp_cpu_count()
    with mp_pool() as pool:
        chunks = 4*(ncore-1)
        iterable = [ [ct, n, holeMap, ng, tempDelta, i] for i in range(chunks) ]
        results = pool.starmap( SimAnnealing_returning, iterable, chunksize= 4 )
    results.sort()
    results.reverse()
    t2 = time.time()
    print( f'MP evaluated in {round(t2-t1,2)} sec and used {chunks} threads')
    return results

def SimAnnealing_returning(ct, n, holeMap, ng, tempDelta = -0.01, thread = 1):
    t1 = time.time()
    starttemp = 100
    endtemp = 1
    temp = starttemp

    keyOld = generateKey(n, holeMap)
    scoreOld = 0

    text_slices = [ct[i:i + n ** 2] for i in range(0, len(ct), n ** 2)]
    #print(text_slices)
    for slice in text_slices:
        scoreOld += ng.score(decrypt(slice, keyOld))

    keyMax, scoreMax = keyOld, scoreOld

    temp = starttemp
    j, j_list = 0, []
    while temp >= endtemp:
        keyNew = changeKeyFull(keyOld, n, holeMap)

        scoreNew = 0
        text_slices = [ct[i:i+n**2] for i in range(0, len(ct), n**2)]
        # print(text_slices)
        for slice in text_slices:
            scoreNew += ng.score(decrypt(slice, keyNew))

        if scoreNew > scoreOld:
            keyOld, scoreOld = keyNew, scoreNew
            if scoreOld > scoreMax:     # w 'scoreMax' zapamiętujemy najlepszy wynik przejścia
                j_list.append(j)
                keyMax, scoreMax, j =  keyOld, scoreOld, 0
                print('Thread nr', thread)
                print( scoreOld) #,'\t', msg )
        elif AcceptanceFunction( scoreOld, scoreNew, temp):
            keyOld, scoreOld = keyNew, scoreNew
        j += 1
        if j > 100:
            keyOld, scoreOld, j = keyMax, scoreMax, 0
        temp += tempDelta

    #print('zatracono ', time.time()-t1, ' sekund')
    #print(f'j_list.mean = {sum(j_list)/len(j_list)},\t j_list.max = {max(j_list)}')

    decrypted = ''

    if len(ct) // (n ** 2) > 0:
        text_slices = [ct[i:i + n**2] for i in range(0, len(ct), n ** 2)]

        for slice in text_slices:
            decrypted += decrypt(slice, keyMax)

    else:
        decrypted = decrypt(ct, keyMax)

    print([scoreMax, decrypted, j_list])

    return [scoreMax, decrypted, j_list]

# uwaga: kryptotekst nalezy wygenerowac w cardan4.py
def main():  # uwaga: zmienic rozmiar grilla size na taki sami jak w cardan4
    file = open('kt.txt', 'r', encoding='utf-8')
    kt = file.read()
    print(kt)

    if 'ó' in kt:
        ng = ngram_score("my_spanish_quadgrams.txt")
        print('Tekst hiszpanski')
    else:
        ng = ngram_score("english_quadgrams.txt")

    # poszukiwanie rozmiaru grilla
    # krotki atak na kazdy rozmiar
    # slabo dziala, bo potrzeba jeszcze
    # dostosowac dlugosc ataku do rozmiaru grilla (i przestrzeni kluczy)
    #####
    best_size_score = -math.inf
    size = 4
    root = math.ceil(math.sqrt(len(kt)))
    maxrange = root + 2 if root % 2 == 0 else root + 3
    # for i in range(4, maxrange, 2):
    #     if len(kt) % i ** 2 != 0:
    #         continue
    #     holeMap = possibleHoleMap(i)
    #     # print(holeMap)
    #     solutions = Sim_MP_min(kt, i, holeMap, ng, -0.2)
    #     if best_size_score < solutions[0][0]:
    #         best_size_score = solutions[0][0]
    #         size = i
    #         print('best is ', size)
    #     print(i)
    # print('end')

    size=14
    holeMap = possibleHoleMap(size)

    solutions = Sim_MP_min(kt, size, holeMap, ng, -0.04)
    print(solutions[0])
    return solutions[0]

if __name__ == '__main__':
    main()