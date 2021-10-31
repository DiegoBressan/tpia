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
                if x == 'E':
                    aux +=1
            
            if aux == len(tunel):
                return True
            else:
                return False   
            
        def actions(self, state):
            # Moverse de zona

            # Recargar energia

            action = (zonaaction, robotaction)
            return action
                
        def cost(self, state, action):
            if action == 'moverzona': # Moverse de zona = 1 minuto (100 mAh)
                return 1
            elif action == 'recargarrobot': # Recargar la energia de un robot mapeador = 5 minutos
                return 5
                
        def result(self, state, action):
            zonaaction, robotaction = action
            tunel, robot = state
            tuplatunel = list(tunel)
            tuplarobot = list(robot)
            tupla = []

            if action == 'recargarrobot': # Resultado de recargar robot
                for x in tuplarobot:
                    if x == robotaction:
                        x = 1000
            elif action == 'moverzona': # Resultado de mover robot de zona      
                for y in tuplatunel:
                    if y == zonaaction:
                        y = 'E'

            tupla = (tuplatunel, tuplarobot)
            return tupla
                
        def heuristic(self, state):
            # Cantidad de zonas que faltan esplorar
            tunel, robot = state
            return len([x for x in tunel if x != 'E'])

    return