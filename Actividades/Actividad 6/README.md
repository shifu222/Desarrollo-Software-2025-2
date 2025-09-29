
# Actividad 6: Introducción a Git conceptos básicos y operaciones esenciales

## Ejercicio 1: Manejo avanzado de ramas y resolución de conflictos

Creé una nueva rama para trabajar separado:

![Creación de rama](image.png)

Cambié cosas en main.py desde la nueva rama:

![Cambios en feature](image-1.png)

También modifiqué el mismo archivo desde main para que haya conflicto:

![Cambios en main](image-2.png)

Al hacer merge salieron conflictos, los resolví editando el archivo:

![Merge completado](image-3.png)

Borré la rama cuando ya no la necesitaba:

![Eliminación de rama](image-4.png)

## Ejercicio 2: Exploración y manipulación del historial de commits

Aquí revisé el historial de commits. Los principales cambios fueron:

- Arreglé el conflicto entre main y feature/advanced-feature
- Cambié el mensaje en main.py
- Agregué la función greet() y arreglé un error (Print estaba mal escrito)

Para ver solo mis commits:

![Filtrado por autor](image-5.png)

Hice rebase para limpiar el historial:

![Inicio de rebase](image-6.png)

Usé squash para juntar varios commits en uno:

![Después del squash](image-7.png)

![Historial limpio](image-8.png)

## Ejercicio 3: Creación y gestión de ramas desde commits específicos

Tenía un bug en la función greet(), lo arreglé:

![Corrección de bug](image-9.png)

Hice commit del arreglo:

![Commit de hotfix](image-10.png)

El merge fue automático (fast-forward):

![Merge fast-forward](image-11.png)

Para ver mejor cómo quedó el historial:

![Grafo de commits](image-12.png)

## Ejercicio 4: Manipulación y restauración de commits con git reset y git restore

Cambié main.py pero después me arrepentí:

![Modificación accidental](image-13.png)

Deshice los cambios con git checkout:

![Cambios revertidos](image-14.png)

## Ejercicio 5: Trabajo colaborativo y manejo de Pull Requests

Subí mi código para hacer pull request:

![Push para PR](image-18.png)

![PR creado](image-19.png)

Me aceptaron el pull request:

![PR aprobado](image-20.png)

## Ejercicio 6: Cherry-Picking y Git Stash

Agregué una línea para probar cherry pick:

![Línea para cherry pick](image-15.png)

Hice una nueva rama para el cherry pick:

![Rama para cherry pick](image-16.png)

Guardé cambios en stash sin hacer commit:

![Git stash](image-17.png)

## Conclusiones

- Las ramas sirven para trabajar en paralelo
- Los conflictos se arreglan editando manualmente
- Rebase ayuda a mantener un historial limpio  
- Squash junta commits relacionados
- Cherry pick sirve para traer commits específicos
- Stash guarda cambios temporalmente
