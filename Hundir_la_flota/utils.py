def crear_tablero(dimension):
    
    """ 
    La función crear_tablero, permite crear el tablero del juego según el tamaño introducido por el usuario, sabiendo que el tablero será cuadrado
    
    1ºCreamos una matriz de dimensión: dimension x dimension hasta 10 elementos (dato introducido por el usuario):
    """
    import numpy as np

    tablero=np.empty((dimension,dimension),dtype='<U10') 

    """  
    Llenamos la matriz creada de ":fog:"
    """

    for i in range(0,dimension):
        for j in range(0,dimension):
            tablero[i][j]=":fog:"
    return tablero


def comprobar_posicion(tablero,tam_barco,posicion_x,posicion_y):
    """  
    Con la función comprobar_posicion se comprueba si se puede poner el barco empezando por esa posicion, según el tamaño correspondiente del barco,
    observando los alrededores para que quepa y te dice que dirección es válida para ser puestos posteriormente.
    """    
    Lados_validos=[]
    #Comprobar que no nos salimos o chocamos desde el punto inicial elegido, tanto verticalmente como horizontalmente:
    #PUNTO ELEGIDO
    if  tablero[posicion_y][posicion_x]==":fog:":
        
        """  
        Se verifica con el for que haya suficiente casillas sin nada para que pueda ponerse el barco, 
        primero se comprueba que no sobrepase el tablero posicion_y+j<tablero.shape[0],
        y después que lo que haya sea nada y no haya un barco cruzado tablero[posicion_y+j][posicion_x]==":fog:":
        """

        #ABAJO
        bien=1
        j=1
        while j<tam_barco and bien==1:
            bien=0
            if posicion_y+j<tablero.shape[0]: 
                if tablero[posicion_y+j][posicion_x]==":fog:":
                    bien=1 #Hay agua, podemos continuar  
                    j+=1 
            else:
                bien=0 #No hay agua, por lo que no se almacenará esta dirección
                break        
        if bien==1:
            Lados_validos.append("abajo")

        #ARRIBA
        bien=1
        j=1
        while j<tam_barco and bien==1:
            bien=0
            if posicion_y-j>=0:
                if tablero[posicion_y-j][posicion_x]==":fog:":
                    bien=1 #Hay agua, podemos continuar  
                    j+=1 
            else:
                bien=0
                break 
        if bien==1:
            Lados_validos.append("arriba")

        #DERECHA
        bien=1
        j=1
        while j<tam_barco and bien==1:
            bien=0
            if posicion_x+j<tablero.shape[0]:
                if tablero[posicion_y][posicion_x+j]==":fog:":
                    bien=1 #Hay agua, podemos continuar  
                    j+=1  
            else:
                bien=0
                break
        if bien==1:
            Lados_validos.append("derecha")
        
        #IZQUIERDA
        bien=1
        j=1
        while j<tam_barco and bien==1:
            bien=0
            if posicion_x-j>=0:
                if tablero[posicion_y][posicion_x-j]==":fog:":
                    bien=1 #Hay agua, podemos continuar  
                    j+=1  
            else:
                bien=0
                break
        if bien==1:
            Lados_validos.append("izquierda")
    else:
        return False,Lados_validos    
    #Devolvemos los resultados obtenidos
    if Lados_validos==[]:
        return False,Lados_validos
    else:
        return True,Lados_validos 
    


def colocar_barco(tablero):
    """  
    La función colocar_barco permite colocar en el tablero los barcos, aletoriamente en este caso, además almacenamos
    los barcos para poder detectarlos al hundirlos en la lista barcos
    """
    import random as rd

    barcos=[[0,0],[0,0],[0,0],[0,0,0],[0,0,0],[0,0,0,0]] #Inicializamos la lista para guardar la posición de cada barco

    for k,i in enumerate([2,2,2,3,3,4]): #La longitud de cada barco para poner
        
        #Primero se elige el punto de partida valido para poner el barco
        posicion_buena=False
        while posicion_buena==False:
            posicion_x=rd.randint(0,tablero.shape[0]-1)
            posicion_y=rd.randint(0,tablero.shape[0]-1)
            #print(posicion_y,posicion_x)
            posicion_buena,direcciones_validas=comprobar_posicion(tablero,i,posicion_x,posicion_y)
            #print(posicion_buena)
            #print(direcciones_validas)
        
        
        """     
        Ahora se elige la dirección de manera aleatoria donde se va a poner el barco, 
        estas posibles direcciones se encuentran en direcciones_validas 
        """
        direccion_elegida=rd.choice(direcciones_validas)
        #print(direccion_elegida)
        
        for j in range(0,i):
            if direccion_elegida=="abajo":
                tablero[posicion_y+j][posicion_x]=":ship:"
                barcos[k][j]=[posicion_y+j,posicion_x]
            elif direccion_elegida=="arriba":
                tablero[posicion_y-j][posicion_x]=":ship:"
                barcos[k][j]=[posicion_y-j,posicion_x]
            elif direccion_elegida=="izquierda":
                tablero[posicion_y][posicion_x-j]=":ship:"
                barcos[k][j]=[posicion_y,posicion_x-j]
            elif direccion_elegida=="derecha":
                tablero[posicion_y][posicion_x+j]=":ship:"
                barcos[k][j]=[posicion_y,posicion_x+j]
    
    return tablero,barcos #Retornará el tablero con los barcos puestos y la lista de donde están situados


def disparar(casilla,tablero,barcos):
    """  
    La función disparar usa el argumento casilla, donde es el disparo que ha introducido el usuario/la máquina y chequeará en el tablero
    si ha dado en el agua o si ha dado a un barco 
    """
    #Chequeamos si ha dado en el agua:
    if tablero[casilla[0]][casilla[1]]==":fog:":
        tablero[casilla[0]][casilla[1]]="🌊"
        return tablero,False
    else:
        """ 
        Como no ha dado en el agua, ha dado en el barco ya que todo lo demás está limitado, ponemos el valor X en esa casilla
        """ 
        
        tablero[casilla[0]][casilla[1]]=":bomb:"
        return tablero,True