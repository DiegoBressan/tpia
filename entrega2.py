from itertools import combinations
from simpleai.search import (
    CspProblem,
    backtrack,
)

variables = ['incrementos_baterias', 'mejoras_movimientos', 'mejoras_cajas', 'mejoras_comunicaciones']


dominios = {} #Dominios = Tipo / consumo / bateria
dominios['incrementos_baterias'] = [('baterias_chicas', 10, 4000), ('baterias_medianas', 20, 6500), ('baterias_grandes', 50, 9000)]
dominios['mejoras_movimientos'] = [('patas_extras', 15, 0), ('mejores_motores', 25, 0), ('orugas', 50, 0)] 
dominios['mejoras_cajas'] = [('caja_superior', 10, 0), ('caja_trasera', 10, 0)] 
dominios['mejoras_comunicaciones'] = [('radios', 5, 0), ('videollamadas', 10, 0)] 

# Consumo y carga con las que ya cuentan los robots antes de aplicar las mejoras
consumo_base = 100
bateria_base = 1000

restricciones = [] # Restricciones  

def bateriagrande_oruga(variables, values): # Si la bateria es grande tiene oruga
    bateria, movimiento, caja, comunicacion = values
    if  bateria == 'baterias_grandes':
        if movimiento == 'oruga':
            return True
        else:
            return False
    else:
        return True

restricciones.append((variables, bateriagrande_oruga))

def cajatrasera_nopatasextras(variables, values): # Si la caja es trasera no tiene patas extras
    bateria, movimiento, caja, comunicacion = values
    if caja == 'caja_trasera':
        if movimiento == 'patas_extras':
            return False
        else:
            return True
    else:
        return True

restricciones.append((variables, cajatrasera_nopatasextras))

def radios_nomejoresmotores(variables, values): # Si tiene radio no tiene la mejora del motor
    bateria, movimiento, caja, comunicacion = values
    if comunicacion == 'radio':
        if movimiento == 'mejores_motores':
            return False
        else:
            return True
    else:
        return True

restricciones.append((variables, radios_nomejoresmotores))

def videollamadas_nomejoresmotores(variables, values): # Si tiene videollamada tiene que tener patas extras o la oruga y no la mejora del motor
    bateria, movimiento, caja, comunicacion = values
    if comunicacion == 'videollamadas':
        if (movimiento == 'oruga') or (movimiento == 'patas_extras'):
            return True
        else:
            return False
    else:
        return True

restricciones.append((variables, videollamadas_nomejoresmotores))

def autonomiasuficiente(variables, values): # Tiene que tener una autonomia de 50 min minimo
    consumo, bateria = 0,0
    for x in values:
        consumo += x[1]
        bateria += x[2]
    consumo += consumo_base
    bateria += bateria_base
    tiempo = bateria/consumo
    if tiempo >= 50:
        return True
    else:
        return False
    
restricciones.append((variables, autonomiasuficiente))

def rediseñar_robot():
    problema = CspProblem(variables, dominios, restricciones)
    solucion = backtrack(problema) 
    solucion = list(solucion.values())
    adaptaciones = []
    
    for adaptacion in solucion:
        adaptaciones.append(adaptacion[0])
    return adaptaciones