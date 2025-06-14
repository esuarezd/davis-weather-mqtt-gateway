def extract_column_positions(header_line):
    """Detecta los inicios de columnas basado en cambios de espacio a texto."""
    positions = []
    in_column = False
    for i, char in enumerate(header_line):
        if not in_column and char != ' ':
            positions.append(i)
            in_column = True
        elif char == ' ':
            in_column = False
    return positions

def read_weather_data(file_path: str) -> list[dict]:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if len(lines) < 4:
        raise ValueError("El archivo no contiene suficientes líneas.")

    header1 = lines[0].rstrip('\n')
    header2 = lines[1].rstrip('\n')
    data_lines = lines[3:]

    col_positions = extract_column_positions(header2)
    col_positions.append(len(header2))  # Agrega el final para último campo

    # Extrae nombres combinados desde ambas líneas
    column_names = []
    for i in range(len(col_positions) - 1):
        start = col_positions[i]
        end = col_positions[i+1]
        part1 = header1[start:end].strip()
        part2 = header2[start:end].strip()
        combined = f"{part1} {part2}".strip()
        column_names.append(combined)

    results = []
    for line in data_lines:
        record = {}
        for i in range(len(col_positions) - 1):
            start = col_positions[i]
            end = col_positions[i+1]
            key = column_names[i]
            value = line[start:end].strip()
            record[key] = value
        results.append(record)

    return results
