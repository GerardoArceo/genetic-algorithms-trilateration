import math
import random
from tkinter import *



################################################################################################################
#Definición de funciones
################################################################################################################

#Pasa de genotipo a fenotipo la subcadena que representa a X, para poder hacer las evaluaciones
gen_to_fen_x = lambda v : ajx + int(v[0:mjx], 2) * ((bjx-ajx)/(2**mjx-1))

#Pasa de genotipo a fenotipo la subcadena que representa a Y, para poder hacer las evaluaciones
gen_to_fen_y = lambda v : ajy + int(v[mjx:len(v)], 2) * ((bjy-ajy)/(2**mjy-1))

#Determina si un vector cumple con respeta las restricciones establecidas
pass_restrictions = lambda x, y : True if (ajx<=x<=bjx and ajy<=y<=bjy) else False

#Calcula la X,Y,Z a partir del vector en cadena binaria
def calculate_vector(v):
  x = gen_to_fen_x(v)
  y = gen_to_fen_y(v)
  z = 0
  for f in functions:
    z += f(x,y) ** 2
  return {'V': v, 'X': x, 'Y': y, 'Z': z}

#Calcular la aptitud de cada uno de los individuos de una generacion
def calculate_generation_aptitude(generation):
  z_sum = 0
  for i in generation:
    z_sum += 1/i['Z']
  for i in generation:
    i['Z%'] = (1/i['Z'])/z_sum

#Escoge los vectores que pasarán a la siguiente generación según sus aptitudes
def select_best_vectors(generation):
  print('\nSELECCIÓN DE LOS VECTORES QUE PASARÁN A LA SIGUIENTE GENERACIÓN')
  index = 1
  new_generation = []
  for i in range(0, num_i):#Seleccionará num_i vectores para la siguiente generación, aunque se pueden repetir
    r = random.random() #Calcula un número random
    z_acum = 0 #Calcula el acumulado de Z%
    for v in generation:#Recorre todos los vectores de la generación
      z_acum += v['Z%'] #Se actualiza el acumulado de Z%
      if (r<z_acum):#Si el numero aleatorio calculado cayó en el intervalo de Z% del vector v...
        if(v['V'] not in new_generation):
          print('Vector ' + str(v['ID']) + ' escogido' + ' -> Nuevo V' + str(index))
          new_generation.append(v['V'])#Seleccionar vector para la siguiente generación
          index+=1
        else:
          print('Vector ' + str(v['ID']) + ' escogido, valor repetido')
        break
  return new_generation

#Genera un vector binario completamente aleatorio de tamaño size
def generate_random_vector():
  while True:
    v = ''
    for _ in range(size):
      v += str(random.randint(0,1))
    if pass_restrictions(gen_to_fen_x(v), gen_to_fen_y(v)):
      return calculate_vector(v)
    else:
      print('El vector no cumple las condiciones, se generará otro...')

#Genera un nuevo vector, decide aleatoriamente que método utilizar para su generación
def generate_new_vector(new_generation):
  while True:
    opc = random.randint(0,1)
    if len(new_generation)==1 or opc==0:
      new_vector = generate_mutation(new_generation)
    elif opc==1:
      new_vector = generate_crossover(new_generation)
    if pass_restrictions(gen_to_fen_x(new_vector), gen_to_fen_y(new_vector)):
      return new_vector
    else:
      print('El vector no cumple las condiciones, se generará otro...')

#Genera un nuevo vector al mutar un gen aleatorio de un individuo aleatorio de la nueva generación
def generate_mutation(new_generation):
  r = random.randint(0,len(new_generation)-1)
  v = new_generation[r] #Vector que se mutará
  p = random.randint(0,size-1) #Posición que se mutará
  l = list(v)
  l[p] = str(int(not bool(int(l[p]))))
  new_vector = "".join(l)
  print('Vector ' + new_vector + ' creado a partir de la mutación de NV' + str(r+1) + ' en la posición ' + str(p+1))
  return new_vector

#Genera un nuevo vector al cruzar 2 individuos aleatorios de la nueva generación
def generate_crossover(new_generation):
  r1 = random.randint(0,len(new_generation)-1)
  r2 = r1
  while r2==r1:
    r2 = random.randint(0,len(new_generation)-1)
  v1 = new_generation[r1] #Vector que se apareará 7u7
  v2 = new_generation[r1] #Vector que se apareará 7u7
  p = random.randint(0,size-1) #Posición que se mutará
  new_vector = v1[0:p] + v2[p:len(v2)]
  print('Vector ' + new_vector + ' creado a partir de la cruza de NV' + str(r1+1) + ' y NV' + str(r2+1) + ' en la posición ' + str(p+1))
  return new_vector

#Imprime una generación determinada
def print_generation(generation, i):
  print('\n\n\n\n*******************************************************************************\n\n\n\n')
  print('GENERACIÓN ' + str(i))
  sum_z = 0
  index = 1
  print("{:<2} {:<100} {:<20} {:<20} {:<20} {:<20}".format('ID','VECTOR','X','Y','Z','Z%'))
  for i in generation:
    i['ID'] = index
    print("{:<2} {:<100} {:<20} {:<20} {:<20} {:<20}".format(i['ID'], i['V'], i['X'], i['Y'], i['Z'], i['Z%']))
    index+=1
    sum_z+=i['Z']
  print('Sumatoria de Z: ' + str(sum_z))





################################################################################################################
#FUNCIÓN PRINCIPAL
################################################################################################################
def main():
  global mjx, mjy, size, ajx, bjx, ajy, bjy, num_g, num_i, bits, functions
  mjx, mjy, size, ajx, bjx, ajy, bjy = 0, 0, 0, 0, 0, 0, 0 #Intervalos de X,Y
  num_g, num_i, bits = int(e1.get()), int(e2.get()), int(e3.get())
  functions = [] #Lista para almacenar las funciones que conforman a la F.O. 

  references = []
  for r in er:
    if len(r[0].get())>0 and len(r[1].get())>0 and len(r[2].get())>0:
      references.append({'X': float(r[0].get()), 'Y': float(r[1].get()), 'R': float(r[2].get())})

  for ref in references:
    functions.append(lambda x, y, x1=ref['X'], y1=ref['Y'], r=ref['R']: ((x-x1)**2 + (y-y1)**2) - r**2)
    #Cálculo del dominio de X
    if(ref['X']-ref['R'] < ajx):
      ajx = ref['X']-ref['R']
    if(ref['X']+ref['R'] > bjx):
      bjx = ref['X']+ref['R']
    #Cálculo del dominio de Y
    if(ref['Y']+ref['R'] > bjy):
      bjy = ref['Y']+ref['R']
    if(ref['Y']-ref['R'] < ajy):
      ajy = ref['Y']-ref['R']

  #Cálculo del tamaño de la cadena de cromosomas
  mjx = math.ceil((math.log10(bjx-ajx)*(10**bits))/(math.log10(2)))
  mjy = math.ceil((math.log10(bjy-ajy)*(10**bits))/(math.log10(2)))
  size = mjx + mjy

  Label(master, text="Información sobre última ejecución").grid(row=13)

  Label(master, text="Intervalo de valores para X: ").grid(row=14)
  Label(master, text=str(ajx) + '<=x<=' + str(bjx)).grid(row=14, column=1)

  Label(master, text="Tamaño de la cadena de X: ").grid(row=14, column=2)
  Label(master, text=str(mjx)).grid(row=14, column=3)

  Label(master, text="Intervalo de valores para Y: ").grid(row=15)
  Label(master, text=str(ajy) + '<=y<=' + str(bjy)).grid(row=15, column=1)

  Label(master, text="Tamaño de la cadena de Y: ").grid(row=15, column=2)
  Label(master, text=str(mjy)).grid(row=15, column=3)

  Label(master, text="Tamaño de la cadena de cromosomas: ").grid(row=16)
  Label(master, text=str(size)).grid(row=16, column=1)

  generations = [] #Lista que almacena todas las generaciones

  #Creación aleatoria de la 1ra generación
  generation = []
  for _ in range(num_i):
    generation.append(generate_random_vector())
  calculate_generation_aptitude(generation)
  generations.append(generation)
  print_generation(generation, 1)

  #Se crean todas las demás generaciones
  for g in range(1, num_g+1):
    #Selección de los vectores que pasarán a la siguiente generación
    new_generation = select_best_vectors(generations[g-1]) #Mejores vectores de la generación anterior
    vectors_left = num_i-len(new_generation) #Vectores que faltan para completar la población
    if vectors_left>0: #Si la población quedó incompleta
      print('Se generarán ' + str(vectors_left) + ' nuevos vectores para completar la población')
      new_vectors = []#Lista que almacena los nuevos vectores generados
      for _ in range(vectors_left):#Se crean los nuevos vectores para recompletar la población
        new_vectors.append(generate_new_vector(new_generation))      
      new_generation += new_vectors

    #Creación de la nueva generación
    generation = []
    for v in new_generation: #Se calculan los datos de cada vector
      generation.append(calculate_vector(v))
    calculate_generation_aptitude(generation)
    generations.append(generation) #Se agrega la nueva generación al historial
    print_generation(generation, g+1)

  #Resultado final
  max_v = generations[-1][0] #Mejor vector de la última generación
  for v in generations[-1]: #Itera a través de la última generación
    if v['Z%'] > max_v['Z%']:
      max_v = v
  
  Label(master, text="").grid(row=17)

  Label(master, text="Mejor vector de la última generación").grid(row=18)
  Label(master, text='V' + str(max_v['ID'])).grid(row=19)

  Label(master, text="Z Mín").grid(row=18, column=1)
  Label(master, text="{:.4f}".format(max_v['Z'])).grid(row=19, column=1)
  
  Label(master, text="Coordenada X").grid(row=18, column=2)
  Label(master, text="{:.2f}".format(max_v['X'])).grid(row=19, column=2)

  Label(master, text="Coordenada Y").grid(row=18, column=3)
  Label(master, text="{:.2f}".format(max_v['Y'])).grid(row=19, column=3)





################################################################################################################
#INICIO DEL PROGRAMA
################################################################################################################

master = Tk()
master.title("Programa que resuelve el problema de trilateración con algoritmos genéticos")

Label(master, text="Número de generaciones").grid(row=1)
e1 = Entry(master)
e1.insert(0, 100)
e1.grid(row=1, column=1)

Label(master, text="Número de individuos por generación").grid(row=2)
e2 = Entry(master)
e2.insert(0, 10)
e2.grid(row=2, column=1)

Label(master, text="Número de bits de precisión").grid(row=3)
e3 = Entry(master)
e3.insert(0, 1)
e3.grid(row=3, column=1)

Label(master, text="").grid(row=4)
Label(master, text="X").grid(row=5, column=1)
Label(master, text="Y").grid(row=5, column=2)
Label(master, text="Distancia").grid(row=5, column=3)

initial_data = [[-0.85,  2.45,  2.25], [2.6, 4.45,  2.85], [6.15,  0, 5.2], [-0.85,  -0.5,  3.2]]
er = []
i = 0
for data in initial_data:
  Label(master, text="Referencia " + str(i+1)).grid(row=6+i)
  ex = Entry(master)
  ex.delete(0, END)
  ex.insert(0, data[0])
  ex.grid(row=6+i, column=1)

  ey = Entry(master)
  ey.delete(0, END)
  ey.insert(0, data[1])
  ey.grid(row=6+i, column=2)

  ed = Entry(master)
  ed.delete(0, END)
  ed.insert(0, data[2])
  ed.grid(row=6+i, column=3)

  er.append([ex, ey, ed])
  i+=1

Label(master, text="").grid(row=10)
Button(master, text='Calcular coordenadas', command=main,highlightbackground="blue").grid(row=11, column=1)
mainloop( )

