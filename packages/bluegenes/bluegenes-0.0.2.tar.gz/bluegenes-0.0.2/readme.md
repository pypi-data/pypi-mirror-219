# Bluegenes

This library is meant to be an easy-to-use library for optimization using
genetic algorithms.

## Status

- [x] Models + tests
- [x] Optimization functions + tests
- [x] Decent documentation

## Overview

The general concept with a genetic algorithm is to evaluate a population for
fitness (an arbitrary metric) and use fitness, recombination, and mutation to
drive evolution toward a more optimal result. In this simple library, the
genetic material is a sequence of ints, floats, or strs, and it is organized
into the following hierarchy:

- `Gene` contains bases (`list[int|float|str]`)
- `Allele` contains `Gene`s
- `Chromosome` contains `Allele`s
- `Genome` contains `Chromosome`s

Each of these classes has a `str name` attribute to identify the genetic
material. These names can be generated as random alphanumeric strs if not
supplied in the relevant instantiation calls.

There are four optimization functions available currently:

- `optimize_gene` - optimizes a Gene
- `optimize_allele` - optimizes an Allele
- `optimize_chromosome` - optimizes a Chromosome
- `optimize_genome` - optimizes a Genome

These optimization functions have largely similar parameters for tuning the
optimization process. See the [Usage](#Usage) section below.

For more detailed documentation, see the
[docs file](https://github.com/k98kurz/bluegenes-python/blob/master/dox.md)
generated automagically by [autodox](https://pypi.org/project/autodox).

## Installation

Installation is with pip.

```bash
pip install bluegenes
```

There are no dependencies.

## Usage

There are are least three ways to use this library: using an included
optimization function, using a custom optimization function, and using the
genetic classes as the basis for an artificial life simulation. Below is a
trivial example of how to do the first of these three.

```python
from bluegenes import Gene, optimize_gene, set_hook
from random import randint, random


# optional functionality: set a hook to be passed every generation as it completes
logs = []

def log_generation(count: int, generation: list[tuple[float], Gene]) -> None:
    logs.append((count, generation))

set_hook(log_generation)


target = 123456
def measure_fitness(gene: Gene) -> float:
    """Produces a fitness score. Passed as parameter to optimize_gene."""
    return 1 / (1 + abs(sum(gene.bases) - target))

def mutate_gene(gene: Gene) -> Gene:
    """Mutates the Gene randomly. Passed as parameter to optimize_gene."""
    for i in range(len(gene.bases)):
        val = random()
        if val <= 0.5:
            gene.bases[i] += randint(0, 100)
        else:
            gene.bases[i] -= randint(0, 100)
    return gene

count, population = optimize_gene(measure_fitness, mutate_gene)
best = population[0]
score = sum(best.bases)

print(f"{count} generations passed")
print(f"the best result had {score=} compared to {target=})")
print(best)
```

Creating custom fitness functions or artificial life simulations is left as an
exercise to the reader.

## Testing

To test, run the following:

```bash
for i in {0..10}; do python tests/test_genes.py; done
for i in {0..10}; do python tests/test_optimization.py; done
```

Note that the randomness may cause some tests to occasionally fail. I halved the
change of a random test failure every time one was encountered, but there are by
definition no guarantees of deterministic behavior when working with random
numbers. In other words, the test suites should each be run a few times, and a
random failure or two should be excused. I have tuned it for <1% chance of a
random test failure (measured), but it will eventually happen if the tests are
run enough times.

## ISC License

ISC License

Copyleft (c) 2023 k98kurz

Permission to use, copy, modify, and/or distribute this software
for any purpose with or without fee is hereby granted, provided
that the above copyleft notice and this permission notice appear in
all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
