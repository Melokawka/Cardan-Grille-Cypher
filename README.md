# Cardan-Grille-Cypher
The project implements the cardan-grille cypher and proceeds to attack the generated encrypted text in order to determine the initial key (nothing is known except for the cypher type, and the grille size). Both polish and spanish texts were tested. The attack has 90% success rate for texts with length of 3k characters and grille size 14.

Szyfr rotacyjny Cardan grille

Atak.py przeprowadza atak z simulated annealing na kryptotekst szyfrowany grillem Kardano o znanym rozmiarze grilla
Program po okolo minucie ze skutecznoscia okolo 90% zwroci rozszyfrowany tekst i uzyty grill/klucz

Juz przy n = 14 istnieje az 4^49 mozliwych kluczy/grillow
Metoda simulated annealing znacznie przyspiesza przeszukiwanie przestrzeni klucza:

Instrukcja obslugi:
1. Wygenerowac kryptotekst w cardan4.py
2. Uruchomic Atak.py
3. Zeby skrocic atak nalezy zwiekszyc parametr tempDelta by program szybciej przegladal przestrzen kluczy
4. Plik tester.py sluzy do wykonania x atakow, zapisania i posortowania ich wynikow
5. Plik gen_spanish_quadgrams.py mozna uzyc do wygenerowania statystyk quadgramow hiszpanskich
6. Plik ngram_score wykorzystano do oceny czytelnosci tekstow uzyskiwanych podczas ataku

Zastosowane idee:
1. Do generowania kluczy i do modyfikacji klucza uzywana jest mapa mozliwych konfiguracji otworow holeMap
   Dzieki temu program porusza sie tylko i wylacznie po przestrzeni poprawnych kluczy
2. Jako ze simulated annealing nie ma tendencji do utykania w maksimum lokalnym,
   to w changeKeyFull() wystarczy tylko jedna metoda zmiany klucza
3. Uzyto quadgramy zamiast bigramow, dla wiekszej precyzji w ustalaniu czytelnosci i dla
   zwiekszenia efektywnosci ataku
4. Wygenerowano wlasne statystyki quadgramow hiszpanskich z 5 wspolczesnych ksiazek hiszpanskich (2500 stron)

Im wiecej kryptotekstu tym bardziej skuteczne lamanie szyfru

Automatyczne znajdowanie rozmiaru grilla podczas ataku zostalo wylaczone
Konieczne jest dostosowanie dlugosci ataku na kazdy potencjalny rozmiar grilla
W przeciwnym razie male grille (n = 4) sa oceniane zbyt wysoko bo maja zbyt duzo czasu na uzyskanie czytelnosci

Nie wprowadzono ograniczenia czasowego dla ataku
Gdyz wielowatkowosc to utrudnia (koniecznosc dostosowywania wielu parametrow)
Oraz przez to ze za czas ataku i tak odpowiada glownie 1 parametr - tempDelta
