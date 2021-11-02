from simpleai.search import (
    SearchProblem,
    astar,
) 
'''
def convertirlista(tupla): # Se pasa de tupla a lista
    convertir = list()
    for x in tupla:
        convertir.append(x)
    return convertir

def convertirtupla(lista): # Se pasa de lista a tupla
    convertir = tuple(lista)
    return convertir
'''
        
def planear_escaneo(tuneles,robots):

    inicio = (tuneles,[])

    for robot in robots:
        if(robot[1] == "escaneador"):
            inicio[1].append((robot[0], (5,0), 1000))
        else:
            inicio[1].append((robot[0], (5,0), 5000))
    
    inicio = tuple(inicio)

    class exploracionrobotica(SearchProblem):

        def is_goal(self, state):
            # No tiene que tener zonas pendientes por escanear
            if len(state) == 0:
                return True
            else:
                return False
                    
        def cost(self, state, action):
            x, y, accion = action

            if accion == 'moverzona': # Moverse de zona = 1 minuto (100 mAh)
                return 1
            else: # Recargar la energia de un robot mapeador = 5 minutos
                return 5   
        
        def actions(self, state):
            tunel, robot = state
            accion = []

            for rob in robot:
                id, zona, bateria = rob
                
                if bateria == 5000: # Recargar energia
                    for robcarga in robot:
                        id2, zona2, bateria2 = robcarga

                        if (zona2 == zona) and (bateria2 < 1000):
                            accion.append((zona, id2, 'recargarrobot'))
                
                if bateria >= 100: # Moverse de zona
                    posiciones_posibles = [(zona[0], zona[1] - 1), (zona[0] - 1, zona[1]), (zona[0], zona[1] + 1), (zona[0] + 1, zona[1])]

                    for posicion in posiciones_posibles:
                        if posicion in tunel:
                            accion.append((posicion, id, 'moverzona'))

            return tuple(accion)
                    
        def result(self, state, action):
            zonaaction, robotaction, accion = action
            tuneles, robots = state
            listatunel = list(tuneles)
            listarobot = list(robots)

            if accion == 'recargarrobot': # Resultado de recargar robot
                listarobotcargar = list()
                for rob in enumerate(robots):
                    if rob[1][2] == zonaaction:
                        listarobotcargar.append(rob)
                        break
                robotcargar = listarobotcargar[0]
                id_robotcargar = robotcargar[0]
                robots[id_robotcargar][2] = 1000
            elif accion == 'moverzona': # Resultado de mover robot de zona  
                listarobotmover = list()
                for rob in enumerate(robots):
                    if rob[0] == robotaction:
                        listarobotmover.append(rob)
                        break    
                robotmover = listarobotmover[0]
                id_robotmover = robotmover[0]
                robots[id_robotmover][1] = zonaaction

                if(robotmover[1][2] <= 1000): # Si es escaneador
                    robots[id_robotmover][2] -= 100
                    
                    if zonaaction in listatunel: # Se elimina la zona escaneada
                        listatunel.remove(zonaaction)
            
            listatunel = tuple(listatunel)
            listarobot = tuple(listarobot)

            return tuple(listatunel, listarobot)
                    
        def heuristic(self, state):
            # Cantidad de zonas que faltan esplorar
            tunel, robot = state
            return len(tunel)

    problema = exploracionrobotica(inicio)
    resultado = astar(problema, graph_search=True)

    plan = []

    for x in resultado.path():
        if x is not None:
            plan.append(x)

    return tuple(plan)