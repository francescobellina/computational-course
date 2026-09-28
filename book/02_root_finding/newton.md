# Metodo di Newton

Il metodo di Newton risolve numericamente un'equazione non lineare

$$
f(x)=0
$$

costruendo una successione di approssimazioni. Data un'approssimazione iniziale $x_0$,
la tangente a $f$ in $x_n$ produce l'iterazione

$$
x_{n+1}
=
x_n-\frac{f(x_n)}{f'(x_n)}.
$$

Se $f$ è sufficientemente regolare, $f'(x^*) \neq 0$ e il punto iniziale è abbastanza
vicino a una radice semplice $x^*$, la convergenza è localmente quadratica; questo è il
comportamento classico discusso nei testi di analisi numerica [@burden2015].

## Implementazione

L'algoritmo non è duplicato nel Book: è implementato in
`src/computational_course/root_finding.py` e importato dagli esperimenti.

```python
from computational_course.root_finding import newton
```

## Esperimento

Nel [notebook eseguibile](../../notebooks/02_root_finding/newton_experiment.ipynb)
applichiamo Newton a

$$
f(x)=\cos(x)-x,
$$

partendo da $x_0=1$. Il notebook costruisce la sequenza degli iterati, calcola i residui
e produce un grafico in scala logaritmica.

## Interpretazione

La radice è circa $0.7390851332$. Quando l'iterazione entra nel regime locale, il residuo
crolla rapidamente. Il grafico del notebook rende visibile questo comportamento e mostra
anche perché è utile mantenere separati algoritmo (`src/`) ed esperimento (`notebooks/`).
