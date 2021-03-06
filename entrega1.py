from simpleai.search import (
    SearchProblem,
    astar,
)

def planear_escaneo(tuneles, robots):

    # Setup values
    # Se reliza una lista con 2 posiciones donde almacenamos:
    # [0] El estado los túneles que están pendientes de revision
    # [1] Una lista de robots con:
        # [1][0] El tipo de robot,
        # [1][1] La posicion actual 5,0 
        # [1][2] Se le asigna una carga (default 1000 para los escaneadores, 9999 para los soportes)

    INITIAL_STATE = (tuneles, [])
    for robot in robots:
        if robot[0][0] == 'e':            
            INITIAL_STATE[1].append((robot[0], (5, 0), 1000))
        else:
            INITIAL_STATE[1].append((robot[0], (5, 0), 9999))

    INITIAL_STATE = tuple([tuple(x) for x in INITIAL_STATE])

    class Problema(SearchProblem):
        def is_goal(self, state):
            tuneles_pendientes = state[0]
            if len(tuneles_pendientes) == 0:
                return True
            return False
        
        def actions(self, state):
            tuneles_pendientes, robots_attrs = state
            movimientos_disponibles = [[1, 0], [0, 1], [-1, 0], [0, -1]]
            acciones_disponibles = [] # Las acciones tendrán 3 campos: [0] robot [1] tipo de accion (escanear/cargar) [2] prox posicion o proximo robot a cargar
            
            for robot in robots_attrs:
                if robot[0][0] == 's':
                    for robot_a_cargar in robots_attrs:
                        if robot[1] == robot_a_cargar[1] and robot_a_cargar[2] < 1000 and robot_a_cargar[0][0] == 'e':
                            acciones_disponibles.append((robot[0], "cargar", robot_a_cargar[0]))
                if robot[2] >= 100:
                    for movimiento in movimientos_disponibles:
                            proxima_posicion = [list(robot[1])[0] + movimiento[0], list(robot[1])[1] + movimiento[1]]
                            if tuple(proxima_posicion) in tuneles:
                                acciones_disponibles.append((robot[0], "mover", tuple(proxima_posicion)))

            return acciones_disponibles

        
        def cost(self, initial_state, action, end_state):
            if action[1] == "mover":
                return 1
            return 5
        
        def result(self, state, action):
            robot_accion, tipo_accion, posicion_o_robot = action
            _tuneles, robots = state

            robots = [list(x) for x in robots]
            _tuneles = list(_tuneles)

            if tipo_accion == "mover":
                robot = [x for x in robots if x[0] == robot_accion]
                robot = robot[0]
                posicion_o_robot = tuple(posicion_o_robot)
                robot[1] = posicion_o_robot
                if robot[0][0] == 'e':
                    robot[2] -= 100
                    if posicion_o_robot in _tuneles:
                        _tuneles.remove(posicion_o_robot)
            else:
                robot_a_cargar = [x for x in robots if x[0] == posicion_o_robot]
                robot_a_cargar = robot_a_cargar[0]
                robot_a_cargar[2] = 1000
            
            robots = tuple([tuple(x) for x in robots])
            _tuneles = tuple(_tuneles)

            return (_tuneles, robots)

        def heuristic(self, state):
            return len(state[0])

    problema = Problema(INITIAL_STATE)
    resultado = astar(problema, graph_search=True)
    _plan = []

    for accion, state in resultado.path():
        # Descartar la primera acción que es None
        if (accion is not None):
            _plan.append(accion)

    return _plan

if __name__ == '__main__':
    #test
    tuneles = (
        (3, 2), (3, 3), (3, 4), (3, 5),
        (4, 2), (4, 5),
        (5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
        (6, 2), (6, 5),
        (7, 2), (7, 3), (7, 4), (7, 5),
    )

    robots = (("e1", "escaneador"), ("s1", "soporte"))

    plan = planear_escaneo(tuneles, robots)

    print(plan)
