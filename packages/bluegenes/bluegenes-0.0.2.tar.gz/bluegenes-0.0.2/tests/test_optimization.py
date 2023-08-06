from context import genes, optimization
from random import randint, random
import unittest


class TestOptimizationForGenes(unittest.TestCase):
    def population(self) -> list[genes.Gene]:
        return [
            genes.Gene("test", [1.0, 2.0, 3.0, 4.0]),
            genes.Gene("test", [2.1, 1.1, 4.1, 3.1]),
            genes.Gene("test", [0.2, 3.2, 2.2, 1.2]),
            genes.Gene("test", [3.3, 4.3, 1.3, 2.3]),
        ]

    def setUp(self) -> None:
        self.parents = self.population()
        return super().setUp()

    def test_child_from_parents_returns_recombination_of_two_random_parents(self):
        child = optimization.child_from_parents(self.parents)

        parent_bases = {
            i: self.parents[i].bases
            for i in range(len(self.parents))
        }
        parents = set()
        for base in child.bases:
            for k, v in parent_bases.items():
                if base in v:
                    parents.add(k)
        assert len(parents) <= 2

    def test_optimize_gene_exits_after_max_iterations_or_achieving_fitness_target(self):
        target = 123.456

        def measure_fitness(gene: genes.Gene) -> float:
            return 1 / abs(sum(gene.bases) - target)

        def mutate_gene(gene: genes.Gene) -> genes.Gene:
            for i in range(len(gene.bases)):
                val = random()
                if val <= 0.1:
                    gene.bases[i] *= random()
                elif val <= 0.2:
                    gene.bases[i] /= random()
                elif val <= 0.6:
                    gene.bases[i] += random()
                else:
                    gene.bases[i] -= random()
            return gene

        count, population = optimization.optimize_gene(
            measure_fitness=measure_fitness,
            mutate_gene=mutate_gene,
            initial_population=self.population(),
            max_iterations=100,
            population_size=100
        )

        assert type(count) is int and count <= 100
        assert type(population) is list
        assert all(type(p) is genes.Gene for p in population)
        assert len(population) == 100
        best = (sum(population[0].bases), population[0])

        assert count < 100 or (best[0] - target)/target < 0.01


class TestOptimizationForAlleles(unittest.TestCase):
    def population(self) -> list[genes.Allele]:
        return [
            genes.Allele("test", [
                genes.Gene("gn1", [1.0, 2.0, 3.0, 4.0]),
                genes.Gene("gn2", [2.1, 1.1, 4.1, 3.1]),
            ]),
            genes.Allele("test", [
                genes.Gene("gn1", [1.2, 2.2, 3.2, 4.2]),
                genes.Gene("gn2", [2.3, 1.3, 4.3, 3.3]),
            ]),
            genes.Allele("test", [
                genes.Gene("gn1", [1.4, 2.4, 3.4, 4.4]),
                genes.Gene("gn2", [2.5, 1.5, 4.5, 3.5]),
            ]),
            genes.Allele("test", [
                genes.Gene("gn1", [1.6, 2.6, 3.6, 4.6]),
                genes.Gene("gn2", [2.7, 1.7, 4.7, 3.7]),
            ]),
        ]

    def setUp(self) -> None:
        self.parents = self.population()
        return super().setUp()

    def test_child_from_parents_returns_recombination_of_two_random_parents(self):
        child = optimization.child_from_parents(self.parents)

        parent_genes = {
            i: self.parents[i].genes
            for i in range(len(self.parents))
        }
        parent_bases = {
            i: [b for g in pg for b in g.bases]
            for i, pg in parent_genes.items()
        }
        parents = set()
        for gene in child.genes:
            for base in gene.bases:
                for k, v in parent_bases.items():
                    if base in v:
                        parents.add(k)
        assert len(parents) <= 2

    def test_optimize_allele_exits_after_max_iterations_or_achieving_fitness_target(self):
        target = 123.456

        def measure_fitness(allele: genes.Allele) -> float:
            sums = [sum(g.bases) for g in allele.genes]
            return 1 / (1 + abs(sum(sums) - target))

        def mutate_gene(gene: genes.Gene) -> genes.Gene:
            for i in range(len(gene.bases)):
                val = random()
                if val <= 0.1:
                    gene.bases[i] *= random()
                elif val <= 0.2:
                    gene.bases[i] /= random()
                elif val <= 0.6:
                    gene.bases[i] += random()
                else:
                    gene.bases[i] -= random()
            return gene

        def mutate_allele(allele: genes.Allele) -> genes.Allele:
            allele.genes = [mutate_gene(g) for g in allele.genes]
            return allele

        count, population = optimization.optimize_allele(
            measure_fitness=measure_fitness,
            mutate_allele=mutate_allele,
            initial_population=self.population(),
            max_iterations=100,
            population_size=100
        )

        assert type(count) is int and count <= 100
        assert type(population) is list
        assert all(type(p) is genes.Allele for p in population)
        assert len(population) == 100
        sums = [sum(g.bases) for g in population[0].genes]
        best = (sum(sums), population[0])

        assert count < 100 or (best[0] - target)/target < 0.01


class TestOptimizationForChromosomes(unittest.TestCase):
    def population(self) -> list[genes.Chromosome]:
        return [
            genes.Chromosome("test", [
                genes.Allele("al1", [
                    genes.Gene("gn1", [1.0, 2.0, 3.0, 4.0]),
                    genes.Gene("gn2", [2.1, 1.1, 4.1, 3.1]),
                ]),
                genes.Allele("al2", [
                    genes.Gene("gn1", [11.0, 12.0, 13.0, 14.0]),
                    genes.Gene("gn2", [12.1, 11.1, 14.1, 13.1]),
                ]),
            ]),
            genes.Chromosome("test", [
                genes.Allele("al1", [
                    genes.Gene("gn1", [1.2, 2.2, 3.2, 4.2]),
                    genes.Gene("gn2", [2.3, 1.3, 4.3, 3.3]),
                ]),
                genes.Allele("al2", [
                    genes.Gene("gn1", [11.2, 12.2, 13.2, 14.2]),
                    genes.Gene("gn2", [12.3, 11.3, 14.3, 13.3]),
                ]),
            ]),
            genes.Chromosome("test", [
                genes.Allele("al1", [
                    genes.Gene("gn1", [1.4, 2.4, 3.4, 4.4]),
                    genes.Gene("gn2", [2.5, 1.5, 4.5, 3.5]),
                ]),
                genes.Allele("al2", [
                    genes.Gene("gn1", [11.4, 12.4, 13.4, 14.4]),
                    genes.Gene("gn2", [12.5, 11.5, 14.5, 13.5]),
                ]),
            ]),
            genes.Chromosome("test", [
                genes.Allele("al1", [
                    genes.Gene("gn1", [1.6, 2.6, 3.6, 4.6]),
                    genes.Gene("gn2", [2.7, 1.7, 4.7, 3.7]),
                ]),
                genes.Allele("al2", [
                    genes.Gene("gn1", [11.6, 12.6, 13.6, 14.6]),
                    genes.Gene("gn2", [12.7, 11.7, 14.7, 13.7]),
                ]),
            ]),
        ]

    def setUp(self) -> None:
        self.parents = self.population()
        return super().setUp()

    def test_child_from_parents_returns_recombination_of_two_random_parents(self):
        child = optimization.child_from_parents(self.parents)

        parent_alleles = {
            i: self.parents[i].alleles
            for i in range(len(self.parents))
        }
        parent_genes = {
            i: [g for a in pa for g in a.genes]
            for i, pa in parent_alleles.items()
        }
        parent_bases = {
            i: [b for g in pg for b in g.bases]
            for i, pg in parent_genes.items()
        }
        parents = set()
        for allele in child.alleles:
            for gene in allele.genes:
                for base in gene.bases:
                    for k, v in parent_bases.items():
                        if base in v:
                            parents.add(k)
        assert len(parents) <= 2

    def test_optimize_chromosome_exits_after_max_iterations_or_achieving_fitness_target(self):
        target = 123.456

        def measure_fitness(chromosome: genes.Chromosome) -> float:
            sums = [sum(g.bases) for a in chromosome.alleles for g in a.genes]
            return 1 / (1 + abs(sum(sums) - target))

        def mutate_gene(gene: genes.Gene) -> genes.Gene:
            for i in range(len(gene.bases)):
                val = random()
                if val <= 0.1:
                    gene.bases[i] *= random()
                elif val <= 0.2:
                    gene.bases[i] /= random()
                elif val <= 0.6:
                    gene.bases[i] += random()
                else:
                    gene.bases[i] -= random()
            return gene

        def mutate_allele(allele: genes.Allele) -> genes.Allele:
            allele.genes = [mutate_gene(g) for g in allele.genes]
            return allele

        def mutate_chromosome(chromosome: genes.Chromosome) -> genes.Chromosome:
            chromosome.alleles = [mutate_allele(a) for a in chromosome.alleles]
            return chromosome

        count, population = optimization.optimize_chromosome(
            measure_fitness=measure_fitness,
            mutate_chromosome=mutate_chromosome,
            initial_population=self.population(),
            max_iterations=100,
            population_size=100
        )

        assert type(count) is int and count <= 100
        assert type(population) is list
        assert all(type(p) is genes.Chromosome for p in population)
        assert len(population) == 100
        sums = [sum(g.bases) for a in population[0].alleles for g in a.genes]
        best = (sum(sums), population[0])

        assert count < 100 or (best[0] - target)/target < 0.01


class TestOptimizationForGenomes(unittest.TestCase):
    def population(self) -> list[genes.Genome]:
        return [
            genes.Genome("test", [
                genes.Chromosome("chr1", [
                    genes.Allele("al1", [
                        genes.Gene("gn1", [1.0, 2.0, 3.0, 4.0]),
                        genes.Gene("gn2", [2.1, 1.1, 4.1, 3.1]),
                    ]),
                    genes.Allele("al2", [
                        genes.Gene("gn1", [11.0, 12.0, 13.0, 14.0]),
                        genes.Gene("gn2", [12.1, 11.1, 14.1, 13.1]),
                    ]),
                ])
            ]),
            genes.Genome("test", [
                genes.Chromosome("chr1", [
                    genes.Allele("al1", [
                        genes.Gene("gn1", [1.2, 2.2, 3.2, 4.2]),
                        genes.Gene("gn2", [2.3, 1.3, 4.3, 3.3]),
                    ]),
                    genes.Allele("al2", [
                        genes.Gene("gn1", [11.2, 12.2, 13.2, 14.2]),
                        genes.Gene("gn2", [12.3, 11.3, 14.3, 13.3]),
                    ]),
                ])
            ]),
            genes.Genome("test", [
                genes.Chromosome("chr1", [
                    genes.Allele("al1", [
                        genes.Gene("gn1", [1.4, 2.4, 3.4, 4.4]),
                        genes.Gene("gn2", [2.5, 1.5, 4.5, 3.5]),
                    ]),
                    genes.Allele("al2", [
                        genes.Gene("gn1", [11.4, 12.4, 13.4, 14.4]),
                        genes.Gene("gn2", [12.5, 11.5, 14.5, 13.5]),
                    ]),
                ])
            ]),
            genes.Genome("test", [
                genes.Chromosome("chr1", [
                    genes.Allele("al1", [
                        genes.Gene("gn1", [1.6, 2.6, 3.6, 4.6]),
                        genes.Gene("gn2", [2.7, 1.7, 4.7, 3.7]),
                    ]),
                    genes.Allele("al2", [
                        genes.Gene("gn1", [11.6, 12.6, 13.6, 14.6]),
                        genes.Gene("gn2", [12.7, 11.7, 14.7, 13.7]),
                    ]),
                ])
            ]),
        ]

    def setUp(self) -> None:
        self.parents = self.population()
        return super().setUp()

    def test_child_from_parents_returns_recombination_of_two_random_parents(self):
        child = optimization.child_from_parents(self.parents)

        parent_chromosomes = {
            i: self.parents[i].chromosomes
            for i in range(len(self.parents))
        }
        parent_alleles = {
            i: [a for c in pc for a in c.alleles]
            for i, pc in parent_chromosomes.items()
        }
        parent_genes = {
            i: [g for a in pa for g in a.genes]
            for i, pa in parent_alleles.items()
        }
        parent_bases = {
            i: [b for g in pg for b in g.bases]
            for i, pg in parent_genes.items()
        }
        parents = set()
        for chromosome in child.chromosomes:
            for allele in chromosome.alleles:
                for gene in allele.genes:
                    for base in gene.bases:
                        for k, v in parent_bases.items():
                            if base in v:
                                parents.add(k)
        assert len(parents) <= 2

    def test_optimize_genome_exits_after_max_iterations_or_achieving_fitness_target(self):
        target = 123.456

        def measure_fitness(genome: genes.Genome) -> float:
            sums = [
                sum(g.bases)
                for c in genome.chromosomes
                for a in c.alleles
                for g in a.genes
            ]
            return 1 / (1 + abs(sum(sums) - target))

        def mutate_gene(gene: genes.Gene) -> genes.Gene:
            for i in range(len(gene.bases)):
                val = random()
                if val <= 0.1:
                    gene.bases[i] *= random()
                elif val <= 0.2:
                    gene.bases[i] /= random()
                elif val <= 0.6:
                    gene.bases[i] += random()
                else:
                    gene.bases[i] -= random()
            return gene

        def mutate_allele(allele: genes.Allele) -> genes.Allele:
            allele.genes = [mutate_gene(g) for g in allele.genes]
            return allele

        def mutate_chromosome(chromosome: genes.Chromosome) -> genes.Chromosome:
            chromosome.alleles = [mutate_allele(a) for a in chromosome.alleles]
            return chromosome

        def mutate_genome(genome: genes.Genome) -> genes.Genome:
            genome.chromosomes = [mutate_chromosome(c) for c in genome.chromosomes]
            return genome

        count, population = optimization.optimize_genome(
            measure_fitness=measure_fitness,
            mutate_genome=mutate_genome,
            initial_population=self.population(),
            max_iterations=100,
            population_size=100
        )

        assert type(count) is int and count <= 100
        assert type(population) is list
        assert all(type(p) is genes.Genome for p in population)
        assert len(population) == 100
        sums = [
            sum(g.bases)
            for c in population[0].chromosomes
            for a in c.alleles
            for g in a.genes
        ]
        best = (sum(sums), population[0])

        assert count < 100 or (best[0] - target)/target < 0.01


class TestOptimizationHookForGenes(unittest.TestCase):
    def setUp(self) -> None:
        self.original_hook = optimization._hook
        return super().setUp()

    def tearDown(self) -> None:
        optimization._hook = self.original_hook
        return super().tearDown()

    def test_set_hook_sets__hook(self):
        def hook (count: int, population: list[tuple[int, genes.Gene]]) -> None:
            print((count, population))

        assert optimization._hook is None
        optimization.set_hook(hook)
        assert optimization._hook is hook

    def test_unset_hook_unsets__hook(self):
        def hook (count: int, population: list[tuple[int, genes.Gene]]) -> None:
            print((count, population))

        assert optimization._hook is None
        optimization.set_hook(hook)
        assert optimization._hook is hook
        optimization.unset_hook()
        assert optimization._hook is None

    def test_hook_is_called_on_each_generation(self):
        logs = []
        def hook (count: int, population: list[tuple[int, genes.Gene]]) -> None:
            logs.append((count, population))

        target = 123
        def measure_fitness(gene: genes.Gene):
            return 1 / (1 + abs(sum(gene.bases) - target))

        def mutate_gene(gene: genes.Gene) -> genes.Gene:
            for i in range(len(gene.bases)):
                val = random()
                if val <= 0.5:
                    gene.bases[i] += randint(0, 10)
                else:
                    gene.bases[i] -= randint(0, 10)
            return gene

        optimization.set_hook(hook)
        count, _ = optimization.optimize_gene(
            measure_fitness, mutate_gene, max_iterations=100
        )

        assert len(logs) == count
        assert all([type(l) is tuple for l in logs])
        assert all([type(l[0]) is int for l in logs])
        assert all([type(l[1]) is list for l in logs])
        assert all([type(fs[0]) is float for l in logs for fs in l[1]])
        assert all([type(fs[1]) is genes.Gene for l in logs for fs in l[1]])


if __name__ == '__main__':
    unittest.main()
