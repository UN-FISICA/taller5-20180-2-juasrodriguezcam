from PIL import Image as I, ImageFilter as IF, ImageStat as IS
import matplotlib.pyplot as plt
from scipy import ndimage as nd
from scipy.optimize import least_squares
import numpy as np

def calc(image, hz, dx):
    imagen=I.fromarray(np.uint8(image), 'RGB')
    imagen.save('imagen1.png')
    t=1/hz
    img=I.open('imagen1.png') #Abre la imagen
    imgg=I.open('imagen1.png').convert('L') #La pasa a escala de grises
    imgg=imgg.filter(IF.GaussianBlur) #Filtra promediando los valores en la imagen 'difumina'
    imgg=imgg.filter(IF.MinFilter) #Filtra tomando los valores mínimos en cada cuadro
    imggp=imgg.load() #Para poder modificar la imagen
    
    ancho, alto=img.size 
    
    #img.show()
    
    stat=IS.Stat(imgg) #Guarda las estadísitcas de la imagen
    mean=int(stat.mean[0]) #De todas las estadísticas da el valor medio
    for i in range(alto): #Ciclo para binarizar respecto al promedio
        for j in range(ancho):
            if imggp[j,i]<mean:
                imggp[j,i]=0
            else:
                imggp[j,i]=255
            
    filtro=imgg.filter(IF.FIND_EDGES) #Filtro que reconoce los bordes en la imagen
    filtro.save('filtrada.png')
    
    filtroplt=plt.imread('filtrada.png') #La imagen filtrada se usa con matplotlib
    for i in range(ancho):
        filtroplt[0][i]=0 #La primera fila la manda a negro
    #plt.imshow(filtroplt)
    #plt.show()
    
    label,obj=nd.label(filtroplt) #Python encuentra objetos con cierta estructura
    com=nd.center_of_mass(filtroplt,label,range(3,obj+1)) #Centro de masa para label mayor que 3
    
    for j in range(3): #Revisa tres veces si hay que quitar algún objeto exterior a la pelota
        for i in range(len(com)):
            if i>=len(com):
                break
            if com[i][1]<249:
                com.pop(i)
            elif com[i][1]>250:
                com.pop(i)
    
    T=[]
    y=[]
    #Falta saber el tiempo
    for i in range(len(com)):
        T.append(t*i)
        y.append(com[i][0])
        
    def fun(x,t,y):
        return x[0]+x[1]*t+x[2]*(t**2)/2-y
    
    tnp=np.array(T)
    ynp=np.array(y)
    x0=np.array([0.0,0.0,17.6])
    
    sol=least_squares(fun,x0,args=(tnp,ynp))
    acel=round(sol.x[2]*dx)
    return acel
