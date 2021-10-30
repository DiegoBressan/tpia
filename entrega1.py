from simpleai.search import (
    SearchProblem,
    astar,
)

def is_goal(self, state):
    # Todas las zonas tienen que ser escaneadas en el menor tiempo posible
    return 
    
def actions(self, state):
    return 
    
def cost(self, state, action, state2):
    # Moverse de zona = 1 minuto (100 mAh)
    # Recargar la energia de un robot mapeador = 5 minutos
    return 
    
def result(self, state, action):
    return 
    
def heuristic(self, state):
    # Cantidad de zonas que faltan esplorar
    return 

def planear_escaneo(self,state):
    return