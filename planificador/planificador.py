def presupuesto_familiar(categorias_presupuesto, presupuesto_total, ahorros):
    n = len(categorias_presupuesto)
    dp = [[0] * (int(presupuesto_total) + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        categoria, presupuesto = categorias_presupuesto[i - 1]
        for j in range(int(presupuesto_total) + 1):
            if j >= presupuesto:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - int(presupuesto)] + ahorros[i - 1])           
            else:
                dp[i][j] = dp[i - 1][j]

    # Recuperacion de la solución óptima
    asignacion_presupuesto = [0] * n    
    j = int(presupuesto_total)
    for i in range(n, 0, -1):
        categoria, presupuesto = categorias_presupuesto[i - 1]
        if dp[i][j] != dp[i - 1][j]:
            asignacion_presupuesto[i - 1] = 1
            j -= int(presupuesto)

    return dp[n][int(presupuesto_total)], asignacion_presupuesto

# Ingreso datos del usuario
ingresos_mensuales = float(input("Cuáles son tus ingresos mensuales?: "))
gastos_mensuales = []
categorias_presupuestos = []
for i in range(1, 5):
    categoria = input(f"Ingrese la categoria del gasto {i}: ")
    presupuesto = float(input(f"Cual es el presupuesto mensual para {categoria}: "))
    gastos_mensuales.append(presupuesto)
    categorias_presupuestos.append((categoria, presupuesto))

# Cálculo del presupuesto total disponible
presupuesto_total = int(ingresos_mensuales) - sum(gastos_mensuales)

# Ahorros por categoria (Asumimos un 10% del presupuesto de cada categoría)
ahorros = [0.1 * presupuesto for presupuesto in gastos_mensuales]

# Ejecucion del algoritmo de presupuesto familiar
max_ahorro, asignacion_presupuesto = presupuesto_familiar(categorias_presupuestos, presupuesto_total, ahorros)

# Impresión de los resultados
print(f"Maximo ahorro posible: ${max_ahorro:.2f}")
print(f"Asignacion de presupuesto: ")
for i, (categoria, presupuesto) in enumerate(categorias_presupuestos):
    asignado = "Si" if asignacion_presupuesto[i] else "No"
    print(f" {categoria}: ${presupuesto:.2f} - Asignado: {asignado}")
