import math
import numpy as np
import random
import string

def cleanText(txt):
    acceptable = string.ascii_lowercase + 'áéíóúüñ¿¡'
    acceptable = acceptable.upper()
    cleantxt = ''
    for char in txt.upper():
        if char in acceptable:
            cleantxt += char

    return cleantxt

def rot90Matrix(matrix, k=1):
    return np.rot90(matrix, k, axes=(1,0))

def encrypt(text, key, n):
    grill = unflatten(key)
    #print(grill)

    result = ''

    text_slices = [text[i:i + n**2] for i in range(0, len(text), n ** 2)]

    for slice in text_slices:
        txtList = list(slice)
        # print(slice)

        grid = np.empty((n, n), dtype='str')

        txtIndex = 0

        for rotNr in range(1, 5):
            for j, row in enumerate(grill):
                for i, element in enumerate(grill):
                    if grill[j][i] == 1:  # a hole
                        if txtIndex < len(txtList):
                            grid[j][i] = txtList[txtIndex]
                            txtIndex += 1
                        else:
                            grid[j][i] = random.choice(string.ascii_uppercase)
            grill = rot90Matrix(grill)

        #print(grid)
        #print()

        result += flatten(grid)

    return result

def flatten(grid):  # grill 2d -> key 1d
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

    print('Mapa możliwych pozycji kazdej dziurki')
    print(indexes)
    return indexes

def generateKey(n, holeMap):
    key = np.full((n, n), 0, dtype=int)
    for elem in holeMap.keys():
        i,j = random.choice(holeMap[elem])
        key[i][j] = 1

    return flatten(key)

def main(spanish = False, textLength = 3000, n = 14):
    print('Rozmiar grilla', n)

    #txt2 = 'Secondourevaluationwilldependontheamountoftoleranceandsympathythatwearepreparedtomobilizetowardsthem'
    #txt2 = 'SecondourevaluationwilldependontheamountoftoleranceandsympathythatwearepreparedtomobilizetowardsthemTherearestillharmlessselfobserverswhobelievethatthereareimmediatecertaintiesforinstanceIthinkorasthesuperstitionofhowheputsitIwillasthoughcognitionheregotholdofitsobjectpurelyandsimplyasthethinginthis'
    #txt2 = 'SecondourevaluationwilldependontheamountoftoleranceandsympathythatwearepreparedtomobilizetowardsthemTherearestillharmlessselfobserverswhobelievethatthereareimmediatecertaintiesforinstanceIthinkorasthe'
    #txt2 = 'SecondourevaluationwilldependontheamountoftoleranceandsympathythatwearepreparedtomobilizetowardsthemTherearestillharmlessselfobserverswhobelievethatthereareimmediatecertaintiesforinstance'
    #txt2 = 'SecondourevaluationwilldependontheamountoftoleranceandsympathythatwearepreparedtomobilizetowardsthemTherearestillharmlessselfobserverswhobelievethatthereareimmediatecertaintiesforinstanceIthinkorasthesuperstitionofhowheputsitIwillasthoughcognitionheregotholdofitsobjectpurelyandsimplyasthethinginthisAkeenandfarreachinganalysisofthevariousasassumedbyreligiousfaithconstitutesathirdsectionofBeyondGoodandEvilThoughtouchinguponvariousinfluencesofChristianitythissectionismoregeneralinitsreligiousscopethanevenTheAntichristmanyindicationsofwhicharetobefoundhereThischapterhastodowiththenumerousinnerexperiencesofmanwhicharedirectlyorindirectlyattributabletoreligiousdoctrinesTheoriginoftheinstinctforfaithitselfissoughtandtheresultsofthisfaitharebalancedagainsttheneedsoftheindividualsandoftheraceTherelationbetweenreligiousecstasyandsensualitytheattemptonthepartofreligiouspractitionerstoarriveatanegationofthewillthetransitionfromreligiousgratitudetofearthepsychologyatthebottomofsaintworshiptoproblemssuchastheseNietzschedevoteshisenergiesinhisinquiryofthereligiousmoodThereisanilluminatingexpositionoftheimportantstagesinreligiouscrueltyandofthemotivesunderlyingthevariousformsofreligioussacrificesInhisbitterestdiatribesagainstChristianityhisobjectwasnottoshakethefaithofthegreatmajorityofmankindintheiridolsHesoughtmerelytofreethestrongmenfromtherestrictionsofareligionwhichfittedtheneedsofonlytheweakermembersofsocietyHeneitherhopednordesiredtoweanthemassofhumanityfromChristianityoranysimilardogmaticcomfortOnthecontraryhedenouncedthosesuperficialatheistswhoendeavoredtoweakenthefoundationsofreligionHesawthepositivenecessityofsuchreligionsasabasisforhisslavemoralityThemoregeneralinquiriesintoconductandtheresearchalongthebroaderlinesofethicsaresupplantedbyinquiriesintospecificmoralattributesThecurrentvirtuesarequestionedandtheirhistoricalsignificanceisdeterminedThevalueofsuchvirtuesistestedintheirrelationtodifferenttypesofmen'
    txt2 = 'SecondourevaluationwilldependontheamountoftoleranceandsympathythatwearepreparedtomobilizetowardsthemTherearestillharmlessselfobserverswhobelievethatthereareimmediatecertaintiesforinstanceIthinkorasthesuperstitionofhowheputsitIwillasthoughcognitionheregotholdofitsobjectpurelyandsimplyasthethinginthisAkeenandfarreachinganalysisofthevariousasassumedbyreligiousfaithconstitutesathirdsectionofBeyondGoodandEvilThoughtouchinguponvariousinfluencesofChristianitythissectionismoregeneralinitsreligiousscopethanevenTheAntichristmanyindicationsofwhicharetobefoundhereThischapterhastodowiththenumerousinnerexperiencesofmanwhicharedirectlyorindirectlyattributabletoreligiousdoctrinesTheoriginoftheinstinctforfaithitselfissoughtandtheresultsofthisfaitharebalancedagainsttheneedsoftheindividualsandoftheraceTherelationbetweenreligiousecstasyandsensualitytheattemptonthepartofreligiouspractitionerstoarriveatanegationofthewillthetransitionfromreligiousgratitudetofearthepsychologyatthebottomofsaintworshiptoproblem'
    txtsp = 'Severo del Valle era ateo y masón, pero tenía ambiciones políticas y nopodía darse el lujo de faltar a la misa más concurrida cada domingo y fiesta deguardar, para que todos pudieran verlo. Su esposa Nívea prefería entendersecon Dios sin intermediarios, tenía profunda desconfianza de las sotanas y seaburría con las descripciones del cielo, el purgatorio y el infierno, peroacompañaba a su marido en sus ambiciones parlamentarias, en la esperanza deque si él ocupaba un puesto en el Congreso, ella podría obtener el votofemenino, por el cual luchaba desde hacía diez años, sin que sus numerososembarazos lograran desanimarla. Ese Jueves Santo el padre Restrepo habíallevado a los oyentes al límite de su resistencia con sus visiones apocalípticasy Nívea empezó a sentir mareos. Se preguntó si no estaría nuevamente encinta.A pesar de los lavados con vinagre y las esponjas con hiel, había dado a luzquince hijos, de los cuales todavía quedaban once vivos, y tenía razones parasuponer que ya estaba acomodándose en la madurez, pues su hija Clara, lamenor, tenía diez años. Parecía que por fin había cedido el ímpetu de suasombrosa fertilidad. Procuró atribuir su malestar al momento del sermón delpadre Restrepo cuando la apuntó para referirse a los fariseos que pretendíanlegalizar a los bastardos y al matrimonio civil, desarticulando a la familia, lapatria, la propiedad y la Iglesia, dando a las mujeres la misma posición que alos hombres, en abierto desafío a la ley de Dios, que en ese aspecto era muyprecisa. Nívea y Severo ocupaban, con sus hijos, toda la tercera hilera debancos. Clara estaba sentada al lado de su madre y ésta le apretaba la manocon impaciencia cuando el discurso del sacerdote se extendía demasiado en lospecados de la carne, porque sabía que eso inducía a la pequeña a visualizaraberraciones que iban más allá de la realidad, como era evidente por laspreguntas que hacía y que nadie sabía contestar. Clara era muy precoz y teníala desbordante imaginación que heredaron todas las mujeres de su familia porvía materna.Se presentópuntualmente en el sitio y no dio ni una mirada al cielo que se cubría de grisesnubarrones. La muchedumbre atónita, llenó todas las calles adyacentes, seencaramó en los techos y los balcones de las casas próximas y se apretujó enel parque. Ninguna concentración política pudo reunir a tanta gente hastamedio siglo después, cuando el primer candidato marxista aspiraba, pormedios totalmente democráticos, a ocupar el sillón de los Presidentes. Clararecordaría toda su vida ese día de fiesta. La gente se vistió de primavera,adelantándose un poco a la inauguración oficial de la temporada, los hombrescon trajes de lino blanco y las damas con los sombreros de pajilla italiana quehicieron furor ese año. Desfilaron grupos de escolares con sus maestros,llevando flores para el héroe. Marcos recibía las flores y bromeaba diciendoque esperaran que se estrellara para llevarle flores al entierro. El obispo enpersona, sin que nadie se lo pidiera, apareció con dos turiferarios a bendecir elpájaro y el orfeón de la gendarmería tocó música alegre y sin pretensiones,para el gusto popular. La policía, a caballo y con lanzas, tuvo dificultad enmantener a la multitud alejada del centro del parque, donde estaba Marcos,vestido con una braga de mecánico, con grandes anteojos de automovilista ysu cucalón de explorador.  '

    if spanish:
        txt2 = txtsp

    if 'ó' in txt2:
        print('Tekst hiszpanski')

    tj = cleanText(txt2)

    tj = tj[:textLength]

    holeMap = possibleHoleMap(n)
    key = generateKey(n, holeMap)

    print('Klucz')
    print(key)

    kt = encrypt(tj, key, n)

    print('Kryptotekst')
    print(kt)
    print('Dlugosc kryptotekstu')
    print(len(kt))

    file = open('kt.txt', 'w', encoding='utf-8')
    file.write(kt)
    file.close()

    return kt

if __name__ == '__main__':
    main()
