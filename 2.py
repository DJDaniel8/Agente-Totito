import random #importamos la libreria de random para toma de deciones aleatorias
class AgenteCompra:
    def __init__(self, presupuesto):#metodo constructor
        self.presupuesto = presupuesto#establece el presupuesto
    def tomar_decision(self, productos):#funcion toma de decisiones
    # Simulamos la toma de decisiones basada en cambios de precios
        for producto in productos:#for para iterar toda la lista de productos
            cambio_precio = random.uniform(-0.1, 0.1) # Simula cambios de precio
            precio_actualizado = producto['precio'] * (1 + cambio_precio) #acutaliza el precio del poroducto
            
        if precio_actualizado <= self.presupuesto:#si el presupuesto es mayor entra 
            print(f"Compra de {producto['nombre']} por ${precio_actualizado:.2f}")#imprime que compro el producto
            self.presupuesto -= precio_actualizado#se resta el precio del producto del presupuesto
        else:#si no alcanza el presupusto
            print(f"No hay presupuesto suficiente para {producto['nombre']}") #imprime que no hay presupuesto
            
# Ejemplo de uso
presupuesto_inicial = 100.0#presupuesto para el ejemplo
agente = AgenteCompra(presupuesto_inicial)#creamos el agente con el presupuesto
productos_en_venta = [#creamos un array de productos.
 {'nombre': 'Producto A', 'precio': 20.0},
 {'nombre': 'Producto B', 'precio': 30.0},
 {'nombre': 'Producto C', 'precio': 15.0},
]

# Simulamos varias iteraciones para mostrar cómo el agente ajusta sus decisiones
for _ in range(3):
    print("\nIteración:")
    agente.tomar_decision(productos_en_venta)
    print(f"Presupuesto restante: ${agente.presupuesto:.2f}")