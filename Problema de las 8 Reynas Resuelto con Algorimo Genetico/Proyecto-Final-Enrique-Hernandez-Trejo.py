import random
import numpy as np

pob_inicial = int(input("Ingrese de que tamaño quiere la poblacion inicial: "))


def get_Init_Popul(Popul_length):
    list_of_values = ["1", "2", "3", "4", "5", "6", "7", "8"]
    auxF = []

    for x in range(Popul_length):
        random.shuffle(list_of_values)
        aux = list_of_values
        aux = "".join(aux)
        auxF.append(aux)

    return auxF


def eval_Funtion(Individuo):
    eval = 0
    a = 7

    for x in range(a):
        for y in range(a - x):
            if (
                int(Individuo[x]) != int(Individuo[x + y + 1]) + y + 1
                and int(Individuo[x]) != int(Individuo[x + y + 1]) - y - 1
            ):
                eval += 1

    return eval


def Select_Popul(Popul):
    Total_sum = 0
    list_of_values = []
    aux = []

    for x in range(len(Popul)):
        Total_sum = Total_sum + eval_Funtion(Popul[x])
        list_of_values.append(Total_sum)

    for x in range(len(Popul)):
        a = random.uniform(0, Total_sum)
        for y in range(len(list_of_values)):
            if a <= list_of_values[y]:
                aux.append(Popul[y])
                break

    return aux


def Cruza(Popul):
    a = len(Popul[0]) - 1
    auxSelected = []
    i = 0

    while i < len(Popul):

        if len(Popul) - 1 != i:

            parent1 = Popul[i]
            parent2 = Popul[i + 1]

            c = np.linspace(1, a, a)
            c = [int(i) for i in c]
            rd_num = random.sample(c, 2)
            rd_num.sort()

            aux1 = parent1[rd_num[0] : rd_num[1]]
            aux2 = parent2[rd_num[0] : rd_num[1]]
            aux1 = [char for char in aux1]
            aux2 = [char for char in aux2]
            aux1 = [int(x) for x in aux1]
            aux2 = [int(x) for x in aux2]
            aux1.sort()
            aux2.sort()

            if aux1 == aux2:
                cruzaF1 = (
                    parent1[: rd_num[0]]
                    + parent2[rd_num[0] : rd_num[1]]
                    + parent1[rd_num[1] :]
                )
                cruzaF2 = (
                    parent2[: rd_num[0]]
                    + parent1[rd_num[0] : rd_num[1]]
                    + parent2[rd_num[1] :]
                )
            else:
                cruzaF1 = parent1
                cruzaF2 = parent2

            auxSelected.append(cruzaF1)
            auxSelected.append(cruzaF2)
            i += 2
        else:
            auxSelected.append(Popul[i])
            i = i + 1

    return auxSelected


def Mutate(Popul):
    auxMut = []
    c = np.linspace(1, len(Popul[0]), len(Popul[0]))
    c = [int(i) for i in c]
    for x in range(len(Popul)):
        aux = Popul[x]
        if random.uniform(0, 1) < 0.2:
            rd_num = random.sample(c, 2)
            auxList = list(aux)
            auxChar = auxList.pop(rd_num[0] - 1)
            auxList.insert(rd_num[1] - 1, auxChar)
            aux = "".join(auxList)

        auxMut.append(aux)
    return auxMut


initpopu = get_Init_Popul(pob_inicial)
i = 0
y = 0
resultado = ""

for x in range(len(initpopu)):
    if eval_Funtion(initpopu[x]) == 28:
        resultado = initpopu[x]
        i += 1
        break
if resultado == "":
    while i != 1:
        print("Seleccion de la poblacion:" + str(y))
        initpopu = Select_Popul(initpopu)
        print(initpopu)
        print("Cruza de la poblacion:" + str(y))
        initpopu = Cruza(initpopu)
        print(initpopu)
        print("Mutacion de la poblacion:" + str(y))
        initpopu = Mutate(initpopu)
        print(initpopu)
        y += 1

        for x in range(len(initpopu)):
            if eval_Funtion(initpopu[x]) == 28:
                resultado = initpopu[x]
                i += 1
                break
print("Se encontro el resultado en la Generacion: " + str(y))
print(resultado)
