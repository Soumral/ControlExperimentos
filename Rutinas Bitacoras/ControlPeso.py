import csv

def actualizarBitacora(nuevosRegistros, archivoPrincipal):
    probetas = {}

    try:
        with open(archivoPrincipal, mode='r', encoding='utf-8') as f_maestro:
            lector_maestro = csv.DictReader(f_maestro)

            for fila in lector_maestro:
                id_probeta = fila['ID Probeta']
                probetas[id_probeta] = []

                for i in range(1, 4):
                    if fila.get(f'Peso {i}', '').strip() != '':
                        probetas[id_probeta].append({
                            'peso': fila[f'Peso {i}'],
                            'fecha': fila[f'Fecha {i}'],
                            'hora': fila[f'Hora {i}'],
                            'tecnico': fila[f'Tecnico {i}']
                        })
    except FileNotFoundError:
        print(f"Nota: No se encontró un archivo maestro previo '{archivoPrincipal}'. Se creará uno nuevo.")

    try:
        with open(nuevosRegistros, mode='r', encoding='utf-8') as f_nuevos:
            lector_csv = csv.reader(f_nuevos)

            for fila in lector_csv:
                if not fila:
                    continue
                id_probeta = fila[0].strip()

                if id_probeta not in probetas:
                    probetas[id_probeta] = []

                probetas[id_probeta].append({
                    'peso': fila[1].strip(),
                    'fecha': fila[2].strip(),
                    'hora': fila[3].strip(),
                    'tecnico': fila[4].strip()
                })

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de registros nuevos '{nuevosRegistros}'.")
        return

    # 3. Sobrescribir el archivo maestro con los datos combinados
    encabezados_salida = [
        'ID Probeta',
        'Peso 1', 'Fecha 1', 'Hora 1', 'Tecnico 1',
        'Peso 2', 'Fecha 2', 'Hora 2', 'Tecnico 2',
        'Peso 3', 'Fecha 3', 'Hora 3', 'Tecnico 3'
    ]

    with open(archivoPrincipal, mode='w', encoding='utf-8', newline='') as f_out:
        escritor_csv = csv.DictWriter(f_out, fieldnames=encabezados_salida)
        escritor_csv.writeheader()

        for id_probeta, registros in probetas.items():
            fila_salida = {'ID Probeta': id_probeta}

            for i in range(1, 4):
                if i <= len(registros):
                    registro_actual = registros[i - 1]
                    fila_salida[f'Peso {i}'] = registro_actual['peso']
                    fila_salida[f'Fecha {i}'] = registro_actual['fecha']
                    fila_salida[f'Hora {i}'] = registro_actual['hora']
                    fila_salida[f'Tecnico {i}'] = registro_actual['tecnico']
                else:
                    fila_salida[f'Peso {i}'] = ''
                    fila_salida[f'Fecha {i}'] = ''
                    fila_salida[f'Hora {i}'] = ''
                    fila_salida[f'Tecnico {i}'] = ''

            escritor_csv.writerow(fila_salida)

    print(f"Actualización completada. Archivo maestro guardado en '{archivoPrincipal}'.'")


archivoNuevos = 'nuevos_pesos.csv'

archivoConsolidado = 'probetas_maestro.csv'

actualizarBitacora(archivoNuevos, archivoConsolidado)