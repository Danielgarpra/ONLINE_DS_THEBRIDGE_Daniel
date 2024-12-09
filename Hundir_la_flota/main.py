from utils import *

import numpy as np
import random as rd
import emoji

np.set_printoptions(threshold=np.inf, linewidth=np.inf)
dimension=1
print("¡BIENVENIDO AL JUEGO HUNDIR LA FLOTA!, tu objetivo es destruir los barcos de tu rival, la máquina, antes de que ella destruya los tuyos, buena suerte!")
while dimension<5:
    dimension=int(input("Introduce la dimensión que quieres que tenga tu tablero:"))
    if dimension<5:
        print("la dimensión debe ser mayor de 4, introducela otra vez:")

print("A continuación se van a colocar los barcos en el tablero de",dimension,"x",dimension,".\nLos barcos son 6 en total: 3 barcos de eslora 2, 2 de eslora 3 y 1 eslora 4.")

""" 
Llamo a las funciones para formar los tableros con los barcos posicionados y en la lista barcosX tendré las coordenadas de cada uno
"""

tablero1,barcos1=colocar_barco(crear_tablero(dimension)) 
tablero2,barcos2=colocar_barco(crear_tablero(dimension))


print("Tu tablero con los barcos colocados es el siguiente:")
# Convertir la matriz a un string para poder utilizar la librería emoji
tablero1_str = '\n'.join([' '.join(fila) for fila in tablero1]) 
print(emoji.emojize(tablero1_str))  # Emplea emoji.emojize

#Creamos un tablero auxiliar para ir enseñando los resultados y no desvelar la posición de los barcos del rival
tablero_aux=crear_tablero(dimension)

quedan1=[2,2,2,3,3,4] #Lista del tamaño de los barcos
quedan2=[2,2,2,3,3,4]

#Inicializamos las variables para entrar al bucle del juego
jugando1=True
jugando2=True
turno1=True
turno2=False
tiro_valido=False

"""  
El proceso va a consistir en dos whiles independientes donde se gestionaran los turnos de cada uno
y estos están dentro de otro while que se encargará de sacarnos si no quedan más barcos de uno o de otro.
"""
#EMPIEZA EL JUEGO:
while jugando1==True and jugando2==True: #Este while verifica que se esté jugando hasta que se acaben los barcos
    
    """ 
    TURNO DEL JUGADOR
    """
    
    while turno1==True: #Este while verifica que se juegue hasta que demos agua y se pierda el turno o se gane
        print("\nES TU TURNO")

        """
        Con estos while anidados pedimos la posición de disparo y verificamos que sea una posición permitida
        o que no se haya metido previamente.
        Un usuario normalmente mete los valores empezando desde el 1,no desde el 0, por lo que lo tendremos en cuenta
        """
        while tiro_valido==False: 
            
            tiro_valido=False   
            while tiro_valido==False:
                disparo_y=int(input("introduce la coordenada Y de tu disparo:"))-1
                if disparo_y>tablero2.shape[0]-1 or disparo_y<0:
                    print("Coordenada no válida, revisa las dimensiones del tablero, prueba otra vez")
                    tiro_valido=False
                else:
                    tiro_valido=True

            tiro_valido=False
            while tiro_valido==False:
                disparo_x=int(input("introduce la coordenada X de tu disparo:"))-1
                if disparo_x>tablero2.shape[0]-1 or disparo_x<0:
                    print("Coordenada no válida, revisa las dimensiones del tablero, prueba otra vez")
                    tiro_valido=False
                else:
                    tiro_valido=True
            
            if tiro_valido==True:    
                if tablero2[disparo_y][disparo_x]==":bomb:" or tablero2[disparo_y][disparo_x]=="🌊":
                    print("Coordenada no válida, ya la habías metido antes")
                    tiro_valido=False
        
        tiro_valido=False  #La reinicializo por si hay otro tiro acabado el turno      
       
        #Una vez comprobado la posición del tiro, llamamos la función para verificar si ha dado en un barco o en agua:
        casilla=[disparo_y,disparo_x]
        tablero2,turno1=disparar(casilla,tablero2,barcos2)
        print("(",casilla[0]+1,",",casilla[1]+1,")")
       
        if turno1==False: #Si hemos dado en el agua, perdemos el turno, turno=False, si hemos dado en un barco continuamos jugando

            tablero_aux[casilla[0]][casilla[1]]="🌊"
            tablero_aux_str = '\n'.join([' '.join(fila) for fila in tablero_aux]) 
            print(emoji.emojize(tablero_aux_str))
            print("Fallaste :(, pasa el turno a la máquina")
            turno2=True
            break

        else:
            salir=0 
            """ 
            El objetivo de estos bucles anidados es localizar en que sublista de la lista barcos está la casilla a la que hemos disparado
            y restarle la vida correspondiente del barco que hemos alcanzado y mostrarlo por pantalla si es tocado o hundido
            """

            for k,subbarcos in enumerate(barcos2):
                for i in range(0,len(subbarcos)):
                        if subbarcos[i][0] == casilla[0] and subbarcos[i][1]==casilla[1]:  # Buscar si en la lista, casilla está dentro
                            quedan1[k]-=1 #Le resto un valor al correspondiente barco
                            if quedan1[k]>0:
                                print("TOCADO!")
                                tablero_aux[casilla[0]][casilla[1]]=":bomb:"
                                tablero_aux_str = '\n'.join([' '.join(fila) for fila in tablero_aux]) 
                                print(emoji.emojize(tablero_aux_str))
                                salir=1
                                break
                            else:
                                print("TOCADO Y HUNDIDO!!")
                                tablero_aux[casilla[0]][casilla[1]]=":bomb:"
                                tablero_aux_str = '\n'.join([' '.join(fila) for fila in tablero_aux]) 
                                print(emoji.emojize(tablero_aux_str))
                                salir=1               
                                break
                if salir==1:
                    break    
                     
        #Comprobamos si está acabado el juego
        if quedan1==[0,0,0,0,0,0]:
            turno1=False
            jugando1=False               


    """ 
    TURNO DE LA MÁQUINA, aquí haremos unos pasos idénticos pero sin mostrar tanto datos por pantalla hasta que no pierda el turno, 
    donde veremos que barcos nuestros ha acertado
    """
        
    while turno2==True: #Este while verifica que se juegue hasta que demos agua y se pierda el turno 
        print("\nTURNO DE LA MÁQUINA")
        while tiro_valido==False: 
            
            disparo_y=rd.randint(0,tablero1.shape[0]-1) #En lugar de tener que introducir las coordenadas, la máquina las elige aletoriamente

            disparo_x=rd.randint(0,tablero1.shape[0]-1)

            if tablero1[disparo_y][disparo_x]==":bomb:" or tablero1[disparo_y][disparo_x]=="🌊":
                tiro_valido=False
            else:
                tiro_valido=True
        
        tiro_valido=False  #La reinicializo por si hay otro tiro acabado el turno      
  

        #Una vez comprobado la posición del tiro, llamamos la función para verificar si ha dado en un barco o en agua:
        casilla=[disparo_y,disparo_x]
        print("(",casilla[0]+1,",",casilla[1]+1,")")
        tablero1,turno2=disparar(casilla,tablero1,barcos1)

        if turno2==False: #Si hemos dado en el agua, perdemos el turno, turno=False, si hemos dado en un barco continuamos jugando
            
            print("Falló la máquina :), tu tablero va así:") #Indicamos que ha fallado la máquina y enseñamos como va tu tablero
            tablero1_str = '\n'.join([' '.join(fila) for fila in tablero1])  
            print(emoji.emojize(tablero1_str))  

            turno1=True
            break
        else:
            salir=0 
            # Restamos la vida correspondiente del barco al que hemos alcanzado:
            for k,subbarcos in enumerate(barcos1):
                for i in range(0,len(subbarcos)):
                        if subbarcos[i][0] == casilla[0] and subbarcos[i][1]==casilla[1]:  # Buscar si en la lista, casilla está dentro
                            quedan2[k]-=1 #Le resto un valor al correspondiente barco
                            if quedan2[k]>0:
                                print("La máquina acertó :(, te ha tocado un barco")
                                salir=1
                                break
                            else:
                                print("La máquina acertó :(, te ha hundido un barco")
                                salir=1               
                                break
                if salir==1:
                    break    
                    
        #Comprobamos si está acabado el juego
        if quedan2==[0,0,0,0,0,0]:
            turno2=False
            jugando2=False               

if jugando1==False:
    print("¡¡¡GANASTE!!!, FIN DEL JUEGO! así quedo su tablero:")
    tablero2_str = '\n'.join([' '.join(fila) for fila in tablero2]) 
    print(emoji.emojize(tablero2_str))
    
else:
    print("GANÓ LA MÁQUINA, lo siento, tu tablero quedó así:")
    tablero1_str = '\n'.join([' '.join(fila) for fila in tablero1])  
    print(emoji.emojize(tablero1_str))  