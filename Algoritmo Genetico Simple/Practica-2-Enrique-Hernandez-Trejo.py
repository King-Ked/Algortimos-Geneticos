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
# settings[1] == 2 -> Representacion Gray
# settings[1] == 3 -> Representacion Real

# settings[2] == 0 -> Generacional
# settings[2] == 1 -> Elitista

# settings[3] == z -> Donde z es el numero de generaciones que se quieren crear

# settings[4] == x -> Donde x es el valor minimo a evaluar
# settings[5] == y -> Donde y es el valor maximo a evaluar

# settings[6] == w -> Donde w es el numero de la poblacion inicial.

# settings[7] == 0 -> f(x) = x^2
# settings[7] == 1 -> f(x) = |x-5/2+sin(x)|
# settings[7] == 2 -> f(x) = 1000/x

# settings[8] == 0 -> Seleccion Discreta
# settings[8] == 1 -> Seleccion Tecnica (Ruleta)

# settings[9] == 1 -> Cruza por un punto
# settings[9] == 1 -> Cruza por dos puntos

# settings[10] == 0 -> Mutacion aleatoria o intercambio de bit
# settings[10] == 1 -> Mutacion por Inserción 


settings = [0, 0, 0, 0, "", "", 0, 0, 0, 0, 0]
ProbabilidadCruza = 0
ProbabilidadMuta = 0

settings[0] = int(input("Selecione si se quiere Maximizar (0) o Minimizar (1)\n"))
settings[1] = int(input("\nSeleccione la Representacion: Binaria (0), Entera (1), Gray (2), Real (3)\n"))
settings[2] = int(input("\nSelecione si se quiere Generacional (0) o Elitista (1)\n"))
settings[3] = int(input("\nIntroduzca el numero de Generaciones deseadas\n"))
settings[4] = input("\nIntroduzca el numero minimo del rango a evaluar\n")
settings[5] = input("\nIntroduzca el numero maximo del rango a evaluar\n")
settings[6] = int(input("\nIntroduzca el numero de elementos dentro de la poblacion inicial\n"))
settings[7] = int(input("\nSeleccione si se quiere f(x) = x^2 (0) o f(x) = |x-5/2+sin(x)| (1) o f(x) = 1000/x (2)\n"))
settings[8] = int(input("\nSeleccion Discreta (0) o Con el metodo de la Ruleta (1)\n"))
if settings[8] == 0:
    ProbabilidadCruza = .7
elif settings[8] == 1:
    ProbabilidadCruza = 1
settings[9] = int(input("\nSeleccione si quiere cruza de un punto (0) o de dos (1)\n"))
settings[10] = int(input("\nSeleccione si quiere mutacion aleotoria(0) o por Inserción (1)\n"))
if settings[10] == 0:
    ProbabilidadMuta = .1
elif settings[10] == 1:
    ProbabilidadMuta = .2


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
            if x == 0:
                b = 1
            else:
                b = np.floor(math.log2(x)) + 1

        elif set[1] == 1 or set[1] == 3:
            aux.append(str(x))
            a = np.floor(math.log10(len(val))) + 1
            if x == 0:
                b = 1
            else:
                b = np.floor(math.log10(x)) + 1

        elif set[1] == 2:
            c = x
            c ^= (c >> 1)
            aux.append(bin(c)[2:])
            a = np.floor(math.log2(len(val))) + 1
            if x == 0:
                b = 1
            else:
                b = np.floor(math.log2(x)) + 1

        aux[x] = ("0" * int(a - b)) + str(aux[x])

        if set[1] == 3:
            auxVal = float(set[5]) - float(set[4])
            if auxVal.is_integer() == False:
                point_index = str(auxVal).index(".")
                aux[x] = aux[x][:point_index] + "." + aux[x][point_index:]

    return aux

# Funcion para evaluar las funciones fitness
def EvalFunt(set, val, rdval):
    if set[1] == 0:
        auxEntrada = val[int(rdval, 2)]

    elif set[1] == 1:
        auxEntrada = val[int(rdval)]

    elif set[1] == 2:
        auxEntrada = val[int(rdval, 2)]
        auxEntrada = auxEntrada ^ (auxEntrada >> 1)

    elif set[1] == 3:
        auxStringEntrada = rdval.replace(".", "")
        auxEntrada = val[int(auxStringEntrada)]

    # Regresa valor para la configuracion
    if set[7] == 0:
        auxFin = auxEntrada ** 2

    elif set[7] == 1:
        auxFin = abs((auxEntrada - 5) / (2 + np.sin(auxEntrada)))

    elif set[7] == 2:
        auxFin = 1000 / auxEntrada
    
    return auxFin

# Funcion que regresa una lista con la poblacion inicial generada aleatoriamente
def getInitPopul(set, Rpst):
    aux = random.choices(Rpst, k=set[6])
    return aux

# Funcion que regresa una lista con los padres elegidos para la cruza (Metodo de la Ruleta)
def Select_Parents(set, val, popul):
    Total_sum = 0
    list_of_values = []
    aux = []
    if set[8] == 0:
        aux = popul
    elif set[8] == 1:
        for x in range(len(popul)):
            Total_sum = Total_sum + EvalFunt(set, val, popul[x])
            list_of_values.append(Total_sum)
    
        for x in range(set[6]):
            a = random.uniform(0, Total_sum)
            for y in range(len(list_of_values)):
                if a <= list_of_values[y]:
                    aux.append(popul[y])
                    break
    
    return aux

# Funcion que realiza la cruza
def Cruza(set, Popul, ProbCruza, val, range):
    a = len(Popul[0]) - 1
    auxSelected = []
    i = 0

    while i < set[6]:
        if random.random() <= ProbCruza:
            
            parent1 = Popul[i]
            if i == len(Popul)-1:
                parent2 = random.choice(Popul)
            else:
                parent2 = Popul[(i+1)]

            eval_parent1 = EvalFunt(set, range, parent1)
            eval_parent2 = EvalFunt(set, range, parent2)

            if set[9] == 0:
                d = random.randint(1, a)
                cruzaF1 = parent1[:d] + parent2[d:]
                cruzaF2 = parent2[:d] + parent1[d:]

            elif set[9] == 1:
                c = np.linspace(1, a, a)
                c = [int(i) for i in c]
                rd_num = random.sample(c, 2)
                rd_num.sort()

                cruzaF1 = parent1[:rd_num[0]] + parent2[rd_num[0]:rd_num[1]] + parent1[rd_num[1]:]
                cruzaF2 = parent2[:rd_num[0]] + parent1[rd_num[0]:rd_num[1]] + parent2[rd_num[1]:]
            
            if set[1] == 0 or set[1] == 2:
                maxim = int(val[-1], 2)
                valev1 = int(cruzaF1, 2)
                valev2 = int(cruzaF2, 2)

            elif set[1] == 1:
                maxim = int(val[-1])
                valev1 = int(cruzaF1)
                valev2 = int(cruzaF2)

            elif set[1] == 3:
                maxim = float(val[-1])
                valev1 = float(cruzaF1)
                valev2 = float(cruzaF2)

            if int(maxim) <= int(valev1) and int(maxim) <= int(valev2):
                cruzaF1 = val[-1]
                cruzaF2 = val[-1]
            elif int(maxim) >= int(valev1) and int(maxim) <= int(valev2):
                cruzaF2 = val[-1]
            elif int(maxim) <= int(valev1) and int(maxim) >= int(valev2):
                cruzaF1 = val[-1]
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

                    if eval_cruzaF2 <= max_of_parents and max_of_parents == parent1:
                        cruzaF2 = parent1
                    elif eval_cruzaF2 <= max_of_parents and max_of_parents == parent2:
                        cruzaF2 = parent2

                # Minimizacion
                elif set[0] == 1:
                    min_of_parents = min(eval_parent1, eval_parent2)

                    if eval_cruzaF1 >= min_of_parents and min_of_parents == parent1:
                        cruzaF1 = parent1
                    elif eval_cruzaF1 >= min_of_parents and min_of_parents == parent2:
                        cruzaF1 = parent2

                    if eval_cruzaF2 >= min_of_parents and min_of_parents == parent1:
                        cruzaF2 = parent1
                    elif eval_cruzaF2 >= min_of_parents and min_of_parents == parent2:
                        cruzaF2 = parent2

            auxSelected.append(cruzaF1)
            auxSelected.append(cruzaF2)
            i += 2
        else:
            auxSelected.append(Popul[i])
            i += 1
    return auxSelected

# Funcion que realiza la mutacion
def Mutate(set, ProbMuta, Popul, Rpst):
    auxMut = []
    if set[1] == 3 and float(Popul[0]).is_integer() == False:
        c = np.linspace(1, len(Popul[0])-1, len(Popul[0])-1)
        c = [int(i) for i in c]
        point_index = Popul[0].index(".")
    else:
        c = np.linspace(1, len(Popul[0]), len(Popul[0]))
        c = [int(i) for i in c]

    for x in range(len(Popul)):
        aux = Popul[x]
        if set[10] == 1 and random.uniform(0, 1) < ProbMuta:
            rd_num = random.sample(c, 2)
            aux = aux.replace(".", "")
            auxList = list(aux)
            auxChar = auxList.pop(rd_num[0]-1)
            auxList.insert(rd_num[1]-1, auxChar)
            if set[1] == 3 and float(Popul[0]).is_integer() == False:
                auxList.insert(point_index, ".")
            aux = "".join(auxList)

        elif set[10] == 0:
            for y in range(len(Popul[x])):
                if aux[y] != ".":
                    if random.uniform(0, 1) <= ProbMuta:
                        if int(aux[y]) % 2 == 0:
                            aux = aux[:y] + str(int(aux[y]) + 1) + aux[y + 1 :]

                        else:
                            aux = aux[:y] + str(int(aux[y]) - 1) + aux[y + 1 :]
        if (set[1] == 0 or set[1] == 2) and int(aux, 2) > int(Rpst[-1], 2):
            aux = Rpst[-1]
        elif set[1] == 1 and int(aux) > int(Rpst[-1]):
            aux = Rpst[-1]
        elif set[1] == 3 and float(aux) > float(Rpst[-1]):
            aux = Rpst[-1]

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

            if min_max[3] <= EvalFunt(set, val, popul[x]):
                min_max[2] = popul[x]
                min_max[3] = EvalFunt(set, val, popul[x])

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
        # Minimizacion
        if settings[0] == 1:
            if Target_gen_minmax[1] > auxMax_Min[1]:
                Target_gen_minmax = auxMax_Min
                Target_Pob = x

ultima_gen_minmax = getMin_Max(settings, newPopul, rango)
auxrango = []
for x in range(len(rango)):
    auxrango.append(EvalFunt(settings, rango, Represen[x]))

plt.plot(rango, auxrango)

if settings[1] == 0:
    plotInicx1 = rango[int(primera_gen_minmax[0], 2)]
    plotInicx2 = rango[int(primera_gen_minmax[2], 2)]
    plotTargetx1 = rango[int(Target_gen_minmax[0], 2)]
    plotTargetx2 = rango[int(Target_gen_minmax[2], 2)]
    plotUltimax1 = rango[int(ultima_gen_minmax[0], 2)]
    plotUltimax2 = rango[int(ultima_gen_minmax[2], 2)]
    
elif settings[1] == 1 or settings[1] == 3:
    if settings[1] == 3:
        primera_gen_minmax[0] = primera_gen_minmax[0].replace(".", "")
        primera_gen_minmax[2] = primera_gen_minmax[2].replace(".", "")
        Target_gen_minmax[0] = Target_gen_minmax[0].replace(".", "")
        Target_gen_minmax[2] = Target_gen_minmax[2].replace(".", "")
        ultima_gen_minmax[0] = ultima_gen_minmax[0].replace(".", "")
        ultima_gen_minmax[2] = ultima_gen_minmax[2].replace(".", "")

    plotInicx1 = rango[int(primera_gen_minmax[0])]
    plotInicx2 = rango[int(primera_gen_minmax[2])]
    plotTargetx1 = rango[int(Target_gen_minmax[0])]
    plotTargetx2 = rango[int(Target_gen_minmax[2])]
    plotUltimax1 = rango[int(ultima_gen_minmax[0])]
    plotUltimax2 = rango[int(ultima_gen_minmax[2])]

elif settings[1] == 2:
    plotInicx1 = rango[(int(primera_gen_minmax[0], 2) ^ (int(primera_gen_minmax[0], 2) >> 1))]
    plotInicx2 = rango[(int(primera_gen_minmax[2], 2) ^ (int(primera_gen_minmax[2], 2) >> 1))]
    plotTargetx1 = rango[(int(Target_gen_minmax[0], 2) ^ (int(Target_gen_minmax[0], 2) >> 1))]
    plotTargetx2 = rango[(int(Target_gen_minmax[2], 2) ^ (int(Target_gen_minmax[2], 2) >> 1))]
    plotUltimax1 = rango[(int(ultima_gen_minmax[0], 2) ^ (int(ultima_gen_minmax[0], 2) >> 1))]
    plotUltimax2 = rango[(int(ultima_gen_minmax[2], 2) ^ (int(ultima_gen_minmax[2], 2) >> 1))]

plt.plot([plotInicx1, plotInicx2], [primera_gen_minmax[1], primera_gen_minmax[3]], "ro",)
plt.plot([plotTargetx1, plotTargetx2], [Target_gen_minmax[1], Target_gen_minmax[3]], "ko",)
plt.plot([plotUltimax1, plotUltimax2], [ultima_gen_minmax[1], ultima_gen_minmax[3]], "co",)

plt.title("Se llego al mejor valor en la Generacion:" + str(Target_Pob))
plt.show()
