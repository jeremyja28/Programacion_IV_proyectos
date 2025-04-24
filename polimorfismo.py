class animal:
    def hablar(self):
        return "El animal hace un sonido."

class perro(animal):
    def hablar(self):
        return "Ladra"

class gato(animal):
    def hablar(self):
        return "Maulla"

animales = [animal(), perro(), gato()]
for animal in animales:
    print(animal.hablar())