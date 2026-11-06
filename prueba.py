class SimuladorReemplazoPaginas:

    def __init__(self, secuencia):
        self.secuencia = secuencia

    def fifo(self, num_marcos):
        marcos = []
        fallos = 0
        historial = []

        for pag in self.secuencia:
            if pag in marcos:
                historial.append((pag, list(marcos), "Acierto"))
            else:
                fallos += 1
                if len(marcos) < num_marcos:
                    marcos.append(pag)
                else:
                    marcos.pop(0)  # Elimina el más antiguo
                    marcos.append(pag)
                historial.append((pag, list(marcos), "Fallo"))
        return fallos, historial

    def lru(self, num_marcos):
        marcos = []
        fallos = 0
        historial = []

        for pag in self.secuencia:
            if pag in marcos:
                # Se mueve la página accedida al final para marcarla como la más recientemente usada
                marcos.remove(pag)
                marcos.append(pag)
                historial.append((pag, list(marcos), "Acierto"))
            else:
                fallos += 1
                if len(marcos) < num_marcos:
                    marcos.append(pag)
                else:
                    marcos.pop(0)  # Elimina la menos recientemente usada
                    marcos.append(pag)
                historial.append((pag, list(marcos), "Fallo"))
        return fallos, historial

    def clock(self, num_marcos):
        marcos = [None] * num_marcos
        bits_uso = [0] * num_marcos
        puntero = 0
        fallos = 0
        historial = []

        for pag in self.secuencia:
            if pag in marcos:
                idx = marcos.index(pag)
                bits_uso[idx] = 1  # Marcar bit de uso
                estado_marcos = [m for m in marcos if m is not None]
                historial.append((pag, estado_marcos, "Acierto"))
            else:
                fallos += 1
                inserted = False
                # Primero, intentar insertar en un espacio vacío si existe
                for i in range(num_marcos):
                    idx = (puntero + i) % num_marcos
                    if marcos[idx] is None:
                        marcos[idx] = pag
                        bits_uso[idx] = 1
                        puntero = (idx + 1) % num_marcos
                        inserted = True
                        break

                if not inserted:
                    # Aplicar algoritmo Clock para reemplazar
                    while True:
                        if bits_uso[puntero] == 0:
                            marcos[puntero] = pag
                            bits_uso[puntero] = 1
                            puntero = (puntero + 1) % num_marcos
                            break
                        else:
                            bits_uso[puntero] = 0
                            puntero = (puntero + 1) % num_marcos

                estado_marcos = [m for m in marcos if m is not None]
                historial.append((pag, estado_marcos, "Fallo"))

        return fallos, historial


# --- Ejecución de prueba ---
secuencia = [
    7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1,5,8,
]
simulador = SimuladorReemplazoPaginas(secuencia)

print(f"{'Marcos':<8} | {'FIFO':<8} | {'LRU':<8} | {'Clock':<8}")
print("-" * 35)
for m in [3, 4, 5]:
    f_fifo, _ = simulador.fifo(m)
    f_lru, _ = simulador.lru(m)
    f_clock, _ = simulador.clock(m)
    print(f"{m:<8} | {f_fifo:<8} | {f_lru:<8} | {f_clock:<8}")