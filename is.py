import simpy
import random

# Configuración inicial
RANDOM_SEED = 42
MEMORIA_RAM = 100
VELOCIDAD_CPU = 1
INTERVALO_LLEGADA = 10
TIEMPO_TOTAL = 0

random.seed(RANDOM_SEED)  # Fijar la semilla del generador de números aleatorios

def proceso(env, nombre, cpu, ram, memoria_requerida, instrucciones, velocidad_cpu):
    global TIEMPO_TOTAL
    tiempo_llegada = env.now
    print(f'{nombre} creado, requiere {memoria_requerida} de memoria RAM y {instrucciones} instrucciones')

    # Solicitar RAM (Estado NEW a READY)
    with ram.get(memoria_requerida) as req_ram:
        yield req_ram
        print(f'{nombre} en estado READY')

        # Solicitar CPU (Estado READY a RUNNING)
        while instrucciones > 0:
            with cpu.request() as req_cpu:
                yield req_cpu
                # Ejecutar instrucciones (Simulación de ejecución)
                tiempo_ejecucion = min(instrucciones, VELOCIDAD_CPU) / VELOCIDAD_CPU
                yield env.timeout(tiempo_ejecucion)
                instrucciones -= VELOCIDAD_CPU
                if instrucciones > 0:
                    # Simular I/O (Estado RUNNING a WAITING)
                    yield env.timeout(random.expovariate(1.0 / INTERVALO_LLEGADA))

    # Liberar RAM y marcar como TERMINATED
    yield ram.put(memoria_requerida)
    print(f'{nombre} TERMINATED. Tiempo total: {env.now - tiempo_llegada}')
    TIEMPO_TOTAL += env.now - tiempo_llegada

# Ambiente y recursos
env = simpy.Environment()
ram = simpy.Container(env, init=MEMORIA_RAM, capacity=MEMORIA_RAM)
cpu = simpy.Resource(env, capacity=1)

# Solicitar al usuario el número de procesos
NUM_PROCESOS = int(input("Ingrese el número de procesos a simular: "))

# Crear y ejecutar procesos
for i in range(NUM_PROCESOS):
    memoria_requerida = random.randint(1, 10)
    instrucciones = random.randint(1, 10) * 10
    env.process(proceso(env, f'Proceso {i}', cpu, ram, memoria_requerida, instrucciones, VELOCIDAD_CPU))

# Iniciar simulación
env.run()

# Estadísticas finales
print(f"Tiempo total de ejecución: {TIEMPO_TOTAL}")
print(f"Tiempo promedio por proceso: {TIEMPO_TOTAL / NUM_PROCESOS}")