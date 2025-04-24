for i in range(5,10):
    print(i)
    
for i in range(1,6):
    print("Tabla de multiplicar de " ,i)
    for j in range(1,6):
        print(i, "x", j, "=", i*j)

#Lista desde el -10 hasta el +10 identificando los pares e impares
#CNTRL+K+C para poner comentario todo el bloque de texto
#CNTRL+K+U para quitar el comentario a todo el bloque de texto
i = -10
while i <=10:
    if i % 2 == 0:
        print(i, "es par")
    else:
        print(i, "es impar")
    i += 1
