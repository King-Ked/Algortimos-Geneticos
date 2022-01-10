# Creado por: Hernandez Trejo Enrique Alberto
# Para fines de aprendizaje de la materia de Genetic Algorithms
# Algoritmo Genetico Estandar

from decimal import Decimal
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import copy

# Lista que almacena las configuraciones de la siguiente manera
# settings[0] == 0 -> Maximizacion de la funcion fitness
# settings[0] == 1 -> Minimizacion de la funcion fitness

# settings[1] == 0 -> Representacion Binaria
# settings[1] == 1 -> Representacion Entera

# settings[2] == 0 -> Generacional
# settings[2] == 1 -> Elitista

# settings[3] == z -> Donde z es el numero de generaciones que se quieren crear

# settings[4] == x -> Donde x es el valor minimo a evaluar
# settings[5] == y -> Donde y es el valor maximo a evaluar

# settings[6] == w -> Donde w es el numero de la poblacion inicial.

# settings[7] == 0 -> f(x) = x^2
# settings[7] == 1 -> f(x) = |x-5/2+sin(x)|
# settings[7] == 2 -> f(x) = 1000/x

settings = [0, 0, 0, 0, "", "", 0, 0]
ProbabilidadCruza = 0.7
ProbabilidadMuta = 0.1

settings[0] = int(input("Selecione si se quiere Maximizar (0) o Minimizar (1)\n"))
settings[1] = int(input("\nSeleccione la Representacion: Binaria (0) o Entera (1)\n"))
settings[2] = int(input("\nSelecione si se quiere Generacional (0) o Elitista (1)\n"))
settings[3] = int(input("\nIntroduzca el numero de Generaciones deseadas\n"))
settings[4] = input("\nIntroduzca el numero minimo del rango a evaluar\n")
settings[5] = input("\nIntroduzca el numero maximo del rango a evaluar\n")
settings[6] = int(
    input("\nIntroduzca el numero de elementos dentro de la poblacion inicial\n")
)
settings[7] = int(
    input(
        "\nSeleccione si se quiere f(x) = x^2 (0) o f(x) = |x-5/2+sin(x)| (1) o f(x) = 1000/x (2)\n"
    )
)

# Funcion para obtener todos los numeros muestra
def getRange(set):

    # obtenemos el numero de valores a evaluar
    numRange = Decimal(set[5]) - Decimal(set[4])
    strRange = str(numRange)
    strRange = strRange.replace(".", "")
    numRange = int(strRange) + 1

    # Crea lista con los numeros a evaluar
    values = np.linspace(float(set[4]), float(set[5]), numRange)
    return values


# Funcion que devuelve una lista con los la representacion adecuada para cada valor
def getRepresentation(set, val):
    aux = []

    for x in range(len(val)):
        if set[1] == 0:
            aux.append(("{0:b}".format(x)))
            a = np.floor(math.log2(len(val))) + 1
        elif set[1] == 1:
            aux.append(str(x))
            a = np.floor(math.log10(len(val))) + 1

        if x == 0:
            b = 1
        else:
            if set[1] == 0:
                b = np.floor(math.log2(x)) + 1
            elif set[1] == 1:
                b = np.floor(math.log10(x)) + 1

        aux[x] = ("0" * int(a - b)) + aux[x]
    return aux


# Funcion para evaluar las funciones fitness
def EvalFunt(set, val, rdval):
    if set[1] == 0:
        auxEntrada = val[int(rdval, 2)]
    elif set[1] == 1:
        auxEntrada = val[int(rdval)]

    # Regresa valor para la configuracion
    if set[7] == 0:
        auxFin = auxEntrada ** 2
        return auxFin

    elif set[7] == 1:
        auxFin = abs((auxEntrada - 5) / (2 + np.sin(auxEntrada)))
        return auxFin

    elif set[7] == 2:
        auxFin = 1000 / auxEntrada
        return auxFin


# Funcion que regresa una lista con la poblacion inicial generada aleatoriamente
def getInitPopul(set, Rpst):
    aux = random.choices(Rpst, k=set[6])
    return aux


def Select_Parents(popul):
    aux = random.choice(popul)
    return aux


# Funcion que realiza la cruza
def Cruza(set, Popul, ProbCruza, val, range):
    a = len(Popul[0]) - 1
    auxSelected = []
    i = 0

    while i < set[6]:
        if random.uniform(0, 1) <= ProbCruza:
            parent1 = Select_Parents(Popul)
            parent2 = Select_Parents(Popul)

            eval_parent1 = EvalFunt(set, range, parent1)
            eval_parent2 = EvalFunt(set, range, parent2)

            # Maximizacion
            if set[0] == 0:
                b = eval_parent1 / (eval_parent1 + eval_parent2)
            # Minimizacion
            elif set[0] == 1:
                b = 1 - (eval_parent1 / (eval_parent1 + eval_parent2))

            if random.uniform(0, 1) <= b:
                continue
            else:
                parent1 = parent2

            if random.uniform(0, 1) <= b:
                parent2 = parent1
            else:
                continue

            c = random.randint(1, a)
            cruzaF1 = parent1[:c] + parent2[c:]
            cruzaF2 = parent2[:c] + parent1[c:]

            if int(val[-1], 2) <= int(cruzaF1) and int(val[-1], 2) <= int(cruzaF2):
                cruzaF1 = val[-1]
                cruzaF2 = val[-1]
            elif int(val[-1], 2) >= int(cruzaF1) and int(val[-1], 2) <= int(cruzaF2):
                cruzaF2 = val[-1]
            elif int(val[-1], 2) <= int(cruzaF1) and int(val[-1], 2) >= int(cruzaF2):
                cruzaF1 = val[-1]
            else:
                continue
            # Elitista
            if set[2] == 1:
                eval_cruzaF1 = EvalFunt(set, range, cruzaF1)
                eval_cruzaF2 = EvalFunt(set, range, cruzaF2)
                # Maximizacion
                if set[0] == 0:
                    max_of_parents = max(eval_parent1, eval_parent2)

                    if eval_cruzaF1 <= max_of_parents and max_of_parents == parent1:
                        cruzaF1 = parent1
                    elif eval_cruzaF1 <= max_of_parents and max_of_parents == parent2:
                        cruzaF1 = parent2
                    else:
                        continue

                    if eval_cruzaF2 <= max_of_parents and max_of_parents == parent1:
                        cruzaF2 = parent1
                    elif eval_cruzaF2 <= max_of_parents and max_of_parents == parent2:
                        cruzaF2 = parent2
                    else:
                        continue
                # Minimizacion
                elif set[0] == 1:
                    min_of_parents = min(eval_parent1, eval_parent2)

                    if eval_cruzaF1 >= min_of_parents and min_of_parents == parent1:
                        cruzaF1 = parent1
                    elif eval_cruzaF1 >= min_of_parents and min_of_parents == parent2:
                        cruzaF1 = parent2
                    else:
                        continue

                    if eval_cruzaF2 >= min_of_parents and min_of_parents == parent1:
                        cruzaF2 = parent1
                    elif eval_cruzaF2 >= min_of_parents and min_of_parents == parent2:
                        cruzaF2 = parent2
                    else:
                        continue
            else:
                continue

            auxSelected.append(cruzaF1)
            auxSelected.append(cruzaF2)
            i += 2
        else:
            auxSelected.append(Select_Parents(Popul))
            i += 1
    return auxSelected


# Funcion que realiza la mutacion
def Mutate(set, ProbMuta, Popul, Rpst):
    auxMut = []
    for x in range(len(Popul)):
        aux = Popul[x]
        for y in range(len(Popul[x])):
            if random.uniform(0, 1) <= 0.1:
                if int(aux[y]) % 2 == 0:
                    aux = aux[:y] + str(int(aux[y]) + 1) + aux[y + 1 :]
                    if int(aux) <= int(Rpst[-1]):
                        continue
                    else:
                        aux = aux[:y] + Popul[x][y] + aux[y + 1 :]

                else:
                    aux = aux[:y] + str(int(aux[y]) - 1) + aux[y + 1 :]
        auxMut.append(aux)

    return auxMut


# Funcion que obtiene el maximo y minimo de una poblacion
def getMin_Max(set, popul, val):
    min_max = []
    for x in range(len(popul)):
        if x == 0:
            min_max.append(popul[x])
            min_max.append(EvalFunt(set, val, popul[x]))
            min_max.append(popul[x])
            min_max.append(EvalFunt(set, val, popul[x]))
        else:
            if min_max[1] >= EvalFunt(set, val, popul[x]):
                min_max[0] = popul[x]
                min_max[1] = EvalFunt(set, val, popul[x])
            else:
                continue
            if min_max[3] <= EvalFunt(set, val, popul[x]):
                min_max[2] = popul[x]
                min_max[3] = EvalFunt(set, val, popul[x])
            else:
                continue
    return min_max


rango = getRange(settings)
Represen = getRepresentation(settings, rango)
poblInic = getInitPopul(settings, Represen)
newPopul = copy.deepcopy(poblInic)
primera_gen_minmax = getMin_Max(settings, poblInic, rango)


print("La poblacion Inicial es:")
print(poblInic)
Target_Pob = 0

for x in range(settings[3] + 1):
    print("Cruza de la poblacion:" + str(x))
    newPopul = Cruza(settings, newPopul, ProbabilidadCruza, Represen, rango)
    print(newPopul)
    print("Mutacion de la poblacion:" + str(x))
    newPopul = Mutate(settings, ProbabilidadMuta, newPopul, Represen)
    print(newPopul)
    auxMax_Min = getMin_Max(settings, newPopul, rango)
    if x == 0:
        Target_gen_minmax = auxMax_Min
    else:
        # Maximizacion
        if settings[0] == 0:
            if Target_gen_minmax[3] < auxMax_Min[3]:
                Target_gen_minmax = auxMax_Min
                Target_Pob = x
            else:
                continue
        if settings[0] == 1:
            if Target_gen_minmax[1] > auxMax_Min[1]:
                Target_gen_minmax = auxMax_Min
                Target_Pob = x
            else:
                continue

ultima_gen_minmax = getMin_Max(settings, newPopul, rango)
auxrango = []
for x in range(len(rango)):
    auxrango.append(EvalFunt(settings, rango, Represen[x]))

plt.plot(rango, auxrango)

if settings[1] == 0:
    plt.plot(
        [rango[int(primera_gen_minmax[0], 2)], rango[int(primera_gen_minmax[2], 2)]],
        [primera_gen_minmax[1], primera_gen_minmax[3]],
        "ro",
    )
elif settings[1] == 1:
    plt.plot(
        [rango[int(primera_gen_minmax[0])], rango[int(primera_gen_minmax[2])]],
        [primera_gen_minmax[1], primera_gen_minmax[3]],
        "ro",
    )
if settings[1] == 0:
    plt.plot(
        [rango[int(Target_gen_minmax[0], 2)], rango[int(Target_gen_minmax[2], 2)]],
        [Target_gen_minmax[1], Target_gen_minmax[3]],
        "ko",
    )
elif settings[1] == 1:
    plt.plot(
        [rango[int(Target_gen_minmax[0])], rango[int(Target_gen_minmax[2])]],
        [Target_gen_minmax[1], Target_gen_minmax[3]],
        " ko",
    )

if settings[1] == 0:
    plt.plot(
        [rango[int(ultima_gen_minmax[0], 2)], rango[int(ultima_gen_minmax[2], 2)]],
        [ultima_gen_minmax[1], ultima_gen_minmax[3]],
        "co",
    )
elif settings[1] == 1:
    plt.plot(
        [rango[int(ultima_gen_minmax[0])], rango[int(ultima_gen_minmax[2])]],
        [ultima_gen_minmax[1], ultima_gen_minmax[3]],
        " co",
    )

plt.title("Se llego al mejor valor en la Generacion:" + str(Target_Pob))
plt.show()
