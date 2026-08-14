# Ventanilla de atención bancaria

Un banco cuenta con una ventanilla de atención para sus clientes. Los clientes llegan y deben esperar su turno para ser atendidos. Sin embargo, el banco maneja diferentes niveles de prioridad para organizar la atención.

Existen tres tipos de clientes:

1. **Público general:** clientes que no tienen ninguna prioridad especial.
2. **Clientes VIP:** clientes que cuentan con un servicio preferencial.
3. **Atención prioritaria:** personas con discapacidad, adultos mayores o mujeres embarazadas.

La ventanilla siempre debe atender primero a los clientes con mayor prioridad. Dentro de un mismo nivel de prioridad, los clientes deben ser atendidos en el mismo orden en que llegaron.

El orden de prioridad es el siguiente:

1. Atención prioritaria.
2. Clientes VIP.
3. Público general.

Por ejemplo, si llegan los siguientes clientes:

* Ana, público general
* Luis,  VIP
* María, público general
* Carlos, atención prioritaria

El orden de atención debe ser:

**Carlos -> Luis -> Ana -> María**

### Problema

Completa la implementación de `bank.py` para que la simulación de este proceso funcione adecuadamente.

El programa recibirá la ruta a un archivo en formato CSV, con la primer columna representando el nombre del cliente y la segunda representando el tipo de cliente (`General`, `VIP`, `Special`):

```
Ana, General
Luis, VIP
María, General
Carlos, Special
```

El orden en que llegan los clientes está definido por el orden en que aparecen en la entrada; es decir, en el ejemplo anterior, el orden de llegada fue `Ana -> Luis -> María -> Carlos`.

Internamente, la lógica de negocios se implementa en la función `dispatch_customers`, que recibe una lista de clientes y su tipo en el orden en que llegaron al banco. La salida de esta función es una lista con los nombres de los clientes en el orden en que fueron atendidos.

No es necesario realizar validación de entrada, asume que siempre será correcta y habrá por lo menos 1 cliente.

### Casos de prueba

En el directorio `inputs/` se incluyen 10 archivos de entrada de ejemplo (`input1.csv` a `input10.csv`), y en el directorio `outputs/` su salida esperada correspondiente (`expected1.txt` a `expected10.txt`).

Para verificar tu implementación de `bank.py` contra un solo caso (por ejemplo `input1.csv`), ejecuta desde este directorio:

```bash
diff <(python bank.py inputs/input1.csv) outputs/expected1.txt && echo OK || echo FAIL
```

Si no se imprime nada además de `OK`, la salida de tu programa coincide exactamente con la esperada.

### Pruebas con pytest

También se incluye `test_bank.py`, que prueba directamente la función `dispatch_customers` de `bank.py` (importándola) contra los mismos 10 casos de entrada/salida esperada.

Para ejecutar las pruebas usando `pytest`:

```bash
pytest -v
```