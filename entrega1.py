from simpleai.search import (
    SearchProblem,
    astar,
) 

def planear_escaneo(tuneles,robots):

    class exploracionrobotica(SearchProblem):

        def is_goal(self, state):
            # Todas las zonas tienen que ser escaneadas en el menor tiempo posible
            tunel, robot = state
            aux = 0

            for x in tunel:
                if x[2] == 'E':
                    aux +=1
            
            if aux == len(tunel):
                return True
            else:
                return False   
            
        def actions(self, state):
            tunel, robot = state
            accion = []

            for rob in robot:
                id, zona, bateria = rob

                if bateria >= 100: # Moverse de zona
                    posiciones_posibles = [(zona[0], zona[1] - 1), (zona[0] - 1, zona[1]), (zona[0], zona[1] + 1), (zona[0] + 1, zona[1])]

                    for posicion in posiciones_posibles:
                        if posicion in tunel:
                            accion.append((posicion, rob, 'moverzona'))

                if bateria > 1000: # Recargar energia
                    for robcarga in robot:
                        id2, zona2, bateria2 = robcarga

                        if (zona2 == zona) and (bateria2 < 1000):
                            accion.append((zona, robcarga, 'recargarrobot'))

            return accion
                
        def cost(self, state, action):
            x, y, accion = action

            if accion == 'moverzona': # Moverse de zona = 1 minuto (100 mAh)
                return 1
            else: # Recargar la energia de un robot mapeador = 5 minutos
                return 5
                
        def result(self, state, action):
            zonaaction, robotaction, accion = action
            tunel, robot = state
            tuplatunel = tunel
            tuplarobot = robot

            if accion == 'recargarrobot': # Resultado de recargar robot
                for x in tuplarobot:
                    if x == robotaction:
                        x[2] = 1000
                    break
            elif accion == 'moverzona': # Resultado de mover robot de zona      
                for y in tuplatunel:
                    if y == zonaaction:
                        y[2] = 'E'
                        for z in tuplarobot:
                            if z == robotaction:
                                z[1] = zonaaction
                                if z[0] != 'soporte':
                                    z[2] -= 100
                                break
                        break

            return (tuplatunel, tuplarobot)
                
        def heuristic(self, state):
            # Cantidad de zonas que faltan esplorar
            tunel, robot = state
            return len([x for x in tunel if x[2] != 'E'])

    return