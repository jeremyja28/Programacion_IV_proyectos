opcion = int(input("Elige una opción:\n1. Sumar\n2. Restar\n3. Multiplicar\n4. Dividir\n"))
if opcion >= 1 and opcion <= 4:
    num1 = float(input("Introduce el primer número: "))
    num2 = float(input("Introduce el segundo número (mayor a cero): "))
    if opcion == 1:
        resultado = num1 + num2
        print(f"La suma de {num1} y {num2} es: {resultado}")
    elif opcion == 2:
        resultado = num1 - num2
        print(f"La resta de {num1} y {num2} es: {resultado}")
    elif opcion == 3:
        resultado = num1 * num2
        print(f"La multiplicacion entre {num1} y {num2} es: {resultado}")
    else:
        if num2 != 0:
            resultado = num1 / num2
            print(f"La division entre {num1} y {num2} es: {resultado}")
        else:
            print("Error no se puede dividir para 0!")
else:
    print("Opción no válida")