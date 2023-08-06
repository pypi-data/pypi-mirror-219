from .errors import tert
from .genes import Gene, Allele, Chromosome, Genome
from random import choices
from typing import Any, Callable


T = Genome | Chromosome | Allele | Gene

_hook = None


def set_hook(func: Callable[[int, list[tuple[int|float, T]]], None]) -> None:
    """Set a hook that will be called after every generation and passed
        the current generation count and the population with fitness
        scores.
    """
    tert(callable(func), "func must be Callable")
    global _hook
    _hook = func


def unset_hook() -> None:
    """Unsets the hook."""
    global _hook
    _hook = None


def _optimize(
        opt_type: type,
        measure_fitness: Callable[[T, int|float], int|float],
        mutate_func: Callable[[T], T],
        initial_population: list[Chromosome] = None, population_size: int = 100,
        genome_size: int = 2, chromosome_size: int = 2, allele_size: int = 3,
        gene_size: int = 10, fitness_target: int|float = 1.0,
        max_iterations: int = 1000,
        base_factory: Callable[[Any], int|float|str] = None,
        factory_args: list[Any] = None,
        factory_kwargs: dict[str, Any] = None,
        T_name: str = None, parents_per_generation: int = 10,
    ) -> tuple[int, list[T]]:
    """Internal function for abstracting optimization code."""
    tert(opt_type in (Genome, Chromosome, Allele, Gene),
         "opt_type must be one of Genome, Chromosome, Allele, or Gene")
    tert(initial_population is None or all(type(p) is opt_type for p in initial_population),
         f"initial_population must be None or list[{opt_type.__name__}]")
    population = initial_population
    if population is None:
        if opt_type is Genome:
            population = [
                Genome.make(
                    genome_size, chromosome_size, allele_size, gene_size, T_name,
                    base_factory=base_factory, factory_args=factory_args,
                    factory_kwargs=factory_kwargs
                )
                for _ in range(population_size)
            ]
        elif opt_type is Chromosome:
            population = [
                Chromosome.make(
                    chromosome_size, allele_size, gene_size, T_name,
                    base_factory=base_factory, factory_args=factory_args,
                    factory_kwargs=factory_kwargs
                )
                for _ in range(population_size)
            ]
        elif opt_type is Allele:
            population = [
                Allele.make(
                    allele_size, gene_size, T_name, base_factory=base_factory,
                    factory_args=factory_args, factory_kwargs=factory_kwargs
                )
                for _ in range(population_size)
            ]
        else:
            population = [
                Gene.make(
                    gene_size, T_name, base_factory=base_factory,
                    factory_args=factory_args, factory_kwargs=factory_kwargs
                )
                for _ in range(population_size)
            ]

    count = 0
    fitness_scores: list[tuple[int|float, T]] = [
        (measure_fitness(g), g)
        for g in population
    ]
    fitness_scores.sort(key=lambda fs: fs[0])
    fitness_scores.reverse()
    best_fitness = fitness_scores[0][0]

    while count < max_iterations and best_fitness < fitness_target:
        # breed parents at random proportional to their order by score
        parents = [fs[1] for fs in fitness_scores[:parents_per_generation]]
        children = [
            child_from_parents(parents)
            for _ in range(population_size-len(parents))
        ]

        children = [mutate_func(child) for child in children]
        population = [*children, *parents]
        fitness_scores: list[tuple[int|float, T]] = [
            (measure_fitness(g), g)
            for g in population
        ]
        fitness_scores.sort(key=lambda fs: fs[0])
        fitness_scores.reverse()
        best_fitness = fitness_scores[0][0]
        count += 1

        if _hook:
            _hook(count, fitness_scores)

    population = [fs[1] for fs in fitness_scores]
    return (count, population)


def optimize_gene(
        measure_fitness: Callable[[Gene, int|float], int|float],
        mutate_gene: Callable[[Gene], Gene],
        initial_population: list[Gene] = None, population_size: int = 100,
        gene_size: int = 10, fitness_target: int|float = 1.0,
        max_iterations: int = 1000,
        base_factory: Callable[[Any], int|float|str] = None,
        factory_args: list[Any] = None,
        factory_kwargs: dict[str, Any] = None, gene_name: str = None,
        parents_per_generation: int = 10) -> tuple[int, list[Gene]]:
    """Optimize a Gene given a measure_fitness function, a mutate_gene
        function, a population_size int, a gene_size int, a
        fitness_target float, and a max_iterations int. Supply
        base_factory to produce Gene bases other than random ints
        between 0 and 10, with optional factory_args and factory_kwargs
        which will be passed to each call of base_factory. Supply
        gene_name to assign the name to each Gene in the population.
        Returns the number of iterations and the final population.
    """
    return _optimize(
        Gene, measure_fitness, mutate_gene, initial_population,
        population_size, None, None, None, gene_size, fitness_target,
        max_iterations, base_factory, factory_args, factory_kwargs, gene_name,
        parents_per_generation
    )


def optimize_allele(
        measure_fitness: Callable[[Allele, int|float], int|float],
        mutate_allele: Callable[[Allele], Allele],
        initial_population: list[Allele] = None, population_size: int = 100,
        allele_size: int = 2, gene_size: int = 10,
        fitness_target: int|float = 1.0, max_iterations: int = 1000,
        base_factory: Callable[[Any], int|float|str] = None,
        factory_args: list[Any] = None, factory_kwargs: dict[str, Any] = None,
        allele_name: str = None, parents_per_generation: int = 10
        ) -> tuple[int, list[Allele]]:
    """Optimize an Allele given a measure_fitness function, a
        mutate_allele function, a population_size int, a fitness_target
        float, and a max_iterations int. Supply base_factory to produce
        Gene bases other than random ints between 0 and 10,
        with optional factory_args and factory_kwargs which will be
        passed to each call of base_factory. Supply allele_name to
        assign the name to each generated Allele in the population.
        Supply an allele_size int and a gene_size int to customize
        generation of a random initial population, or supply
        initial_population list[Allele] to specify the initial
        population. Returns the number of iterations and the final
        population.
    """
    return _optimize(
        Allele, measure_fitness, mutate_allele, initial_population,
        population_size, None, None, allele_size, gene_size,
        fitness_target, max_iterations, base_factory, factory_args,
        factory_kwargs, allele_name, parents_per_generation
    )


def optimize_chromosome(
        measure_fitness: Callable[[Chromosome, int|float], int|float],
        mutate_chromosome: Callable[[Chromosome], Chromosome],
        initial_population: list[Chromosome] = None, population_size: int = 100,
        chromosome_size: int = 2, allele_size: int = 3, gene_size: int = 10,
        fitness_target: int|float = 1.0, max_iterations: int = 1000,
        base_factory: Callable[[Any], int|float|str] = None,
        factory_args: list[Any] = None,
        factory_kwargs: dict[str, Any] = None,
        chromosome_name: str = None, parents_per_generation: int = 10,
    ) -> tuple[int, list[Chromosome]]:
    """Optimize an Chromosome given a measure_fitness function, a
        mutate_chromosome function, a population_size int, a fitness_target
        float, and a max_iterations int. Supply base_factory to produce
        Gene bases other than random ints between 0 and 10,
        with optional factory_args and factory_kwargs which will be
        passed to each call of base_factory. Supply chromosome_name to
        assign the name to each generated Chromosome in the population.
        Supply an allele_size int and a gene_size int to customize
        generation of a random initial population, or supply
        initial_population list[Chromosome] to specify the initial
        population. Returns the number of iterations and the final
        population.
    """
    return _optimize(
        Chromosome, measure_fitness, mutate_chromosome, initial_population,
        population_size, None, chromosome_size, allele_size, gene_size,
        fitness_target, max_iterations, base_factory, factory_args,
        factory_kwargs, chromosome_name, parents_per_generation
    )


def optimize_genome(
        measure_fitness: Callable[[Genome, int|float], int|float],
        mutate_genome: Callable[[Genome], Genome],
        initial_population: list[Genome] = None, population_size: int = 100,
        genome_size: int = 1, chromosome_size: int = 2, allele_size: int = 3,
        gene_size: int = 10, fitness_target: int|float = 1.0,
        max_iterations: int = 1000,
        base_factory: Callable[[Any], int|float|str] = None,
        factory_args: list[Any] = None,
        factory_kwargs: dict[str, Any] = None,
        genome_name: str = None, parents_per_generation: int = 10,
    ) -> tuple[int, list[Genome]]:
    """Optimize a Genome given a measure_fitness function, a
        mutate_chromosome function, a population_size int, a fitness_target
        float, and a max_iterations int. Supply base_factory to produce
        Gene bases other than random ints between 0 and 10,
        with optional factory_args and factory_kwargs which will be
        passed to each call of base_factory. Supply genome_name to
        assign the name to each generated Genome in the population.
        Supply an allele_size int and a gene_size int to customize
        generation of a random initial population, or supply
        initial_population list[Genome] to specify the initial
        population. Returns the number of iterations and the final
        population.
    """
    return _optimize(
        Genome, measure_fitness, mutate_genome, initial_population,
        population_size, genome_size, chromosome_size, allele_size, gene_size,
        fitness_target, max_iterations, base_factory, factory_args,
        factory_kwargs, genome_name, parents_per_generation
    )


def child_from_parents(parents: list[Genome]) -> Genome:
    """Select two parents at random semi-proportional to their order in
        the list. Recombine the two chosen parent Genes, and return the
        result.
    """
    weights = [len(parents[i:])/len(parents) for i in range(len(parents))]
    dad, mom = choices(parents, weights, k=2)
    return dad.recombine(mom)
