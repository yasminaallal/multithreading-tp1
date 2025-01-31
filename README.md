# TP Réalisé par Allal Yasmine et Grandisson Mahé

## Résultats de la résolution d'équations

| Langage & Solver       | Tâches traitées    | Temps d'exécution (s) |
|------------------------|--------------------|------------------------|
| **C++ - ldlt**        | Task 1 à Task 4    | 0.0444                 |
| **C++ - llt**         | Task 2 à Task 5    | 0.0059                 |
| **Python - Minion-1** | Task 1 à Task 4    | 0.0261                 |

Les deux premières lignes correspondent aux calculs effectués en **C++**, en utilisant respectivement les solveurs `ldlt` et `llt`.  
La troisième ligne représente une exécution réalisée avec **NumPy** en **Python**.

Nous constatons que le code Python est plus rapide que le solveur `ldlt` en C++, bien que **C++ soit généralement plus performant** que Python.  
Cela s'explique par le fait que **NumPy** n'est pas directement écrit en Python, mais implémente des optimisations en **langage bas niveau** comme **C** ou **Fortran**, ce qui améliore considérablement ses performances.
