# EstrategiasInversion_Clase01_MatApl# Actividad 6: Estrategias de inversión

### Operaciones con vectores y matrices — Álgebra Lineal

Comparación de la evolución de un capital inicial $C$ invertido en 6 compañías bajo dos estrategias distintas — **Buy and Hold** y **Rebalanceo Diario** — contrastadas contra el rendimiento del **S&P500**, usando operaciones matriciales y vectoriales con NumPy.

## Escenario

Un inversor desea comparar la evolución de un capital inicial `C` invertido en 6 compañías (Apple, Amazon, etc.) desde el 01/01/2024 hasta el 18/02/2025.

**Datos de entrada:**

- `P ∈ ℝ^(T×6)`: matriz de precios diarios, con `T` días y 6 compañías.
- Vector de precios del S&P500 para el mismo período.
- Capital inicial `C` (valor del S&P500 el primer día).

**Compañías utilizadas:** Apple (AAPL), Amazon (AMZN), Microsoft (MSFT), Google (GOOGL), Meta (META), Nvidia (NVDA)

## Estrategias comparadas

1. **Buy and Hold**: invertir `C/6` en cada acción el primer día y no volver a operar.
2. **Rebalanceo Diario**: reajustar la cartera cada día para que el valor invertido en cada acción sea siempre 1/6 del total.

## Objetivo

Usando operaciones de álgebra lineal, calcular y graficar la riqueza acumulada diaria de ambas estrategias y compararla con el S&P500.

## Fundamento matemático

**Retornos diarios** (matriz `(T-1)×6`):

$$R[t] = \frac{P[t]}{P[t-1]} - 1$$

**Buy and Hold:** las unidades compradas el día 0 se mantienen fijas. La riqueza en cualquier día es el producto (broadcasting) entre la matriz de precios `P` y el vector de unidades compradas, sumado por fila:

$$\text{wealth}_{BH}[t] = \sum_{i=1}^{6} P[t, i] \cdot n_i$$

**Rebalanceo Diario:** si cada día se reparte el capital en partes iguales, el retorno del portafolio es el promedio simple de los 6 retornos individuales — un producto matriz-vector:

$$\text{retorno\_portafolio} = R \cdot w \quad \text{con} \quad w = \left[\tfrac{1}{6}, \dots, \tfrac{1}{6}\right]$$

$$\text{wealth}_{Rebal}[t] = \text{wealth}_{Rebal}[t-1] \cdot (1 + \text{retorno\_portafolio}[t-1])$$

**S&P500 (referencia):**

$$\text{wealth}_{SP500}[t] = C \cdot \frac{P_{sp500}[t]}{P_{sp500}[0]}$$

## Requisitos

```bash
pip install yfinance numpy pandas matplotlib
```

## Uso

Abrir y ejecutar `Actividad6_Estrategias_Inversion.ipynb` en Jupyter o Google Colab, corriendo las celdas en orden.

## Resultados (periodo 01/01/2024 – 18/02/2025)

| Estrategia | Riqueza final | Retorno total |
|---|---|---|
| Buy and Hold | $8,161.31 | 72.08% |
| Rebalanceo Diario | $7,989.32 | 68.45% |
| S&P500 | $6,114.63 | 28.92% |

## Conclusiones

- Ambas estrategias superan ampliamente al S&P500 en este período, ya que las 6 compañías tecnológicas seleccionadas tuvieron un desempeño excepcional frente al mercado general.
- Buy and Hold rinde ligeramente más que el Rebalanceo Diario en este caso, porque al no rebalancear se deja correr sin recortar a la acción que más subió (Nvidia), mientras que el rebalanceo diario "vende ganadores" constantemente para mantener los pesos iguales.
- Esto ilustra un principio conocido en finanzas: el rebalanceo diario reduce la concentración de riesgo y suaviza la dependencia de un solo activo, pero puede sacrificar algo de rendimiento cuando un activo individual tiene un rally muy fuerte y sostenido.