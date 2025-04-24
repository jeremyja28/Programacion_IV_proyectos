class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
        
    def saludar(self):
        return f"Hola, soy {self.nombre} y tengo {self.edad} años."
        

persona1 = Persona("Juan" , 30)
print(persona1.saludar())

class Estudiante(Persona):
    def __init__(self, nombre, edad, carrera):
        super().__init__(nombre, edad)
        self.carrera = carrera
    def saludocompleto(self):
        return f"Hola, soy {self.nombre}, tengo {self.edad} años y estudio {self.carrera}."

est1 = Estudiante("Pedro", 20, "Ingeniería")
print(est1.saludocompleto())