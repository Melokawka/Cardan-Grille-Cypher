# Cardan-Grille-Cypher

Szyfr rotacyjny Cardan grille

Atak.py przeprowadza atak z simulated annealing na kryptotekst szyfrowany grillem Kardano o znanym rozmiarze grilla. 
Program po okolo minucie ze skutecznoscia okolo 90% zwroci rozszyfrowany tekst i uzyty grill/klucz. 

Juz przy n = 14 istnieje az 4^49 mozliwych kluczy/grillow. 
Metoda simulated annealing znacznie przyspiesza przeszukiwanie przestrzeni kluczy. 

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

Im wiecej kryptotekstu tym bardziej skuteczne lamanie szyfru. 

Automatyczne znajdowanie rozmiaru grilla podczas ataku zostalo wylaczone. 
Konieczne jest dostosowanie dlugosci ataku na kazdy potencjalny rozmiar grilla, 
w przeciwnym razie male grille (n = 4) sa oceniane zbyt wysoko bo maja zbyt duzo czasu na uzyskanie czytelnosci. 

Nie wprowadzono ograniczenia czasowego dla ataku, 
gdyz wielowatkowosc to utrudnia (koniecznosc dostosowywania wielu parametrow)
oraz przez to ze za czas ataku i tak odpowiada glownie 1 parametr - tempDelta.

Przy tych parametrach 10 atakow zajelo mi 15 minut wraz ze skutecznością 90% (procesor AMD Ryzen 5 9600X):
1. is_spanish = True
2. grill_size = 14
3. text_length = 3000

Przykładowy zdeszyfrowany tekst:
# [-6533.6653091208445, "CEANDSYMPATHYTHATWEAREPREPAREDTOMOBILIZETOWARDSTHEMTHEREARESTILLHARMLESSSELFOBSERVERSWHOBELIEVETHATTHEREAREIMMEDIATECERTAINTIESFORINSTANCEITHINKORASECONDOUREVALUATIONWILLDEPENDONTHEAMOUNTOFTOLERANONHEREGOTHOLDOFITSOBJECTPURELYANDSIMPLYASTHETHINGINTHISAKEENANDFARREACHINGANALYSISOFTHEVARIOUSASASSUMEDBYRELIGIOUSFAITHCONSTITUTESATHIRDSECTIONOFBESTHESUPERSTITIONOFHOWHEPUTSITIWILLASTHOUGHCOGNITISOFCHRISTIANITYTHISSECTIONISMOREGENERALINITSRELIGIOUSSCOPETHANEVENTHEANTICHRISTMANYINDICATIONSOFWHICHARETOBEFOUNDHERETHISCHAPTERHASTODOWITHTHENUMERYONDGOODANDEVILTHOUGHTOUCHINGUPONVARIOUSINFLUENCETLYATTRIBUTABLETORELIGIOUSDOCTRINESTHEORIGINOFTHEINSTINCTFORFAITHITSELFISSOUGHTANDTHERESULTSOFTHISFAITHAREBALANCEDAGAINSTTHENEEDSOFTHEINDIVIDUALSANOUSINNEREXPERIENCESOFMANWHICHAREDIRECTLYORINDIRECNSUALITYTHEATTEMPTONTHEPARTOFRELIGIOUSPRACTITIONERSTOARRIVEATANEGATIONOFTHEWILLTHETRANSITIONFROMRELIGIOUSGRATITUDETOFEARTHEPSYCHOLOGYATTHEBOTTOMOFSDOFTHERACETHERELATIONBETWEENRELIGIOUSECSTASYANDSEAXEGCCZGGHGNTFFRRVLEOBNOUXHPUGBHXVSRDUUIGFCNHPEEDKHMFAJNXJPLEDDCSGNMCIXRWISAIJRENSZTAAALDGNWBGCKYMMXUCQHZMBYPSFKBBIORVBVNYJCNKQECIBZBDQLLRAZFTDJBHWAINTWORSHIPTOPROBLEMCRMEKOGJNURORHMBABGSFOOXFSHGJ", [2, 5, 2, 1, 2, 4, 14, 4, 4, 1, 5, 9, 1, 4, 1, 7, 9, 2, 1, 18, 3, 18, 3, 1, 22, 8, 11, 18, 12, 18, 5, 20, 8, 4, 5, 8, 51, 3, 11, 60, 77, 50, 16, 9, 50, 29, 47, 3, 15, 10, 41, 20, 18, 1, 37, 20, 8, 38, 27, 22, 65, 4, 35, 42, 47, 21, 20, 3, 27, 26, 1, 96]]
