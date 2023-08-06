# bluegenes

## Classes

### `Gene(object)`

#### Annotations

- name: str
- bases: list[int | float | str]

#### Methods

##### `copy() -> Gene:` 

Returns an exact copy of the Gene.

##### `insert(index: int = None, base: int | float | str = None) -> Gene:` 

Inserts the base at the index. If index is None, the base is inserted at a
random index. If base is None, adds a random int base. Returns self for chaining
operations.

##### `append(base: int | float | str = None) -> Gene:` 

Adds a base to the end of the gene. If base is None, adds a random int base.
Returns self for chaining operations.

##### `insert_sequence(index: int = None, sequence: list[int | float | str] = None) -> Gene:` 

Inserts the sequence at the index. If index is None, the sequence is inserted at
a random index. If sequence is None, a random sequence in size between 1 and the
current len of the gene bases will be inserted.

##### `delete(index: int = None) -> Gene:` 

Deletes the base at the index. If index is None, a random base is deleted.
Returns self for chaining operations.

##### `delete_sequence(index: int = None, size: int = None) -> Gene:` 

Deletes size bases beggining at the index. If index is None, a random index is
used. If size is None, a random size is used. Returns self for chaining
operations.

##### `substitute(index: int = None, base: int | float | str = None) -> Gene:` 

Substitutes the base at the index with the given base. If index is None, a
random index will be used. If base is None, a random int base will be used.
Returns self for chaining operations.

##### `recombine(other: Gene, indices: list[int] = None) -> Gene:` 

Recombines with another gene at the given indexes. If indices is None, between 1
and ceil(log(len(self.bases))) random indices will be chosen. Returns the
resultant Gene.

##### `@classmethod make(n_bases: int, name: str, max_base_size: int, base_factory: Callable[[None], int | float | str], factory_args: list, factory_kwargs: dict) -> Gene:` 

Makes and returns a randomized Gene.

##### `to_dict() -> dict:` 

Serialize the Gene to a dict.

##### `@classmethod from_dict(data: dict) -> Gene:` 

Deserialize a Gene from a dict.

### `Allele(object)`

#### Annotations

- name: str
- genes: list[Gene]

#### Methods

##### `copy() -> Allele:` 

Returns an exact copy of the Allele, copying the underlying Genes as well.

##### `insert(index: int, gene: Gene, n_bases: int, max_base_size: int, base_factory: Callable[[None], int | float | str], factory_args: list = None, factory_kwargs: dict = None) -> Allele:` 

Inserts the gene at the index. If index is None, the gene is inserted at a
random index. If gene is None, adds a random gene using Gene.make, passing the
kwargs. Returns self for chaining operations.

##### `append(gene: Gene, n_bases: int, max_base_size: int, base_factory: Callable[[None], int | float | str], factory_args: list, factory_kwargs: dict = None) -> Allele:` 

Adds a gene to the end of the allele. If gene is None, adds a random Gene using
Gene.make and passing kwargs. Returns self for chaining operations.

##### `duplicate(index: int = None) -> Allele:` 

Duplicates the Gene at the index. If index is None, the Gene at a random index
is duplicated. Returns self for chaining operations.

##### `delete(index: int = None) -> Allele:` 

Deletes the Gene at the index. If index is None, a Gene is deleted at a random
index. Returns self for chaining operations.

##### `substitute(index: int, gene: Gene, n_bases: int, max_base_size: int, base_factory: Callable[[None], int | float | str], factory_args: list = None, factory_kwargs: dict = None) -> Allele:` 

Substitutes the Gene at the index with the given gene. If index is None, a
random index will be used. If gene is None, adds a random gene using Gene.make,
passing the kwargs. Returns self for chaining operations.

##### `recombine(other: Allele, indices: list[int] = None, recombine_genes: bool = True, match_genes: bool = True) -> Allele:` 

Recombines with the other Allele, swapping at the given indices. If indices is
None, between 1 and ceil(log(len(self.genes))) random indices will be chosen.
Recombines individual Genes if recombine_genes is True. Recombines only Genes
with matching names if match_genes is True. Returns the new Allele.

##### `@classmethod make(n_genes: int, n_bases: int, name: str, max_base_size: int, base_factory: Callable[[None], int | float | str], factory_args: list, factory_kwargs: dict) -> Allele:` 

Makes and returns an Allele of randomized Genes.

##### `to_dict() -> dict:` 

Serialize the Allele to a dict.

##### `@classmethod from_dict(data: dict) -> Allele:` 

Deserialize an Allele from a dict.

### `Chromosome(object)`

#### Annotations

- name: str
- alleles: list[Allele]

#### Methods

##### `copy() -> Chromosome:` 

Returns an exact copy of the Chromosome, copying the underlying Alleles as well.

##### `insert(index: int, allele: Allele, n_genes: int, n_bases: int, max_base_size: int, base_factory: Callable[[None], int | float | str], factory_args: list = None, factory_kwargs: dict = None) -> Chromosome:` 

Inserts the allele at the index. If index is None, the allele is inserted at a
random index. If allele is None, adds a random allele using Allele.make, passing
the kwargs. Returns self for chaining operations.

##### `append(allele: Allele, n_genes: int, n_bases: int, max_base_size: int, base_factory: Callable[[None], int | float | str], factory_args: list, factory_kwargs: dict = None) -> Chromosome:` 

Adds a allele to the end of the chromosome. If allele is None, adds a random
Allele using Allele.make and passing kwargs. Returns self for chaining
operations.

##### `duplicate(index: int = None) -> Chromosome:` 

Duplicates the Allele at the index. If index is None, the Allele at a random
index is duplicated. Returns self for chaining operations.

##### `delete(index: int = None) -> Chromosome:` 

Deletes the Allele at the index. If index is None, an Allele is deleted at a
random index. Returns self for chaining operations.

##### `substitute(index: int, allele: Allele, n_genes: int, n_bases: int, max_base_size: int, base_factory: Callable[[None], int | float | str], factory_args: list = None, factory_kwargs: dict = None) -> Chromosome:` 

Substitutes the Allele at the index with the given allele. If index is None, a
random index will be used. If allele is None, adds a random allele using
Allele.make, passing the kwargs. Returns self for chaining operations.

##### `recombine(other: Chromosome, indices: list[int] = None, recombine_alleles: bool = True, match_alleles: bool = True, recombine_genes: bool = True, match_genes: bool = True) -> Chromosome:` 

Recombines with the other Chromosome, swapping at the given indices. If indices
is None, between 1 and ceil(log(len(self.alleles))) random indices will be
chosen. Recombines individual Alleles if recombine_allels is True. Recombines
only Alleles with matching names if match_alleles is True. Recombines individual
Genes if recombine_genes is True. Recombines only Genes with matching names if
match_genes is True. Returns the new Chromosome.

##### `@classmethod make(n_alleles: int, n_genes: int, n_bases: int, name: str, max_base_size: int, base_factory: Callable[[None], int | float | str], factory_args: list, factory_kwargs: dict) -> Chromosome:` 

Makes and returns a Chromosome of randomized Alleles.

##### `to_dict() -> dict:` 

Serialize the Chromosome to a dict.

##### `@classmethod from_dict(data: dict) -> Chromosome:` 

Deserialize a Chromosome from a dict.

### `Genome(object)`

#### Annotations

- name: str
- chromosomes: list[Chromosome]

#### Methods

##### `copy() -> Genome:` 

Returns an exact copy of the Genome, copying the underlying Chromosome as well.

##### `insert(index: int, chromosome: Chromosome, n_alleles: int, n_genes: int, n_bases: int, max_base_size: int, base_factory: Callable[[None], int | float | str], factory_args: list = None, factory_kwargs: dict = None) -> Chromosome:` 

Inserts the chromosome at the index. If index is None, the chromosome is
inserted at a random index. If chromosome is None, adds a random chromosome
using Chromosome.make, passing the kwargs. Returns self for chaining operations.

##### `append(chromosome: Chromosome, n_alleles: int, n_genes: int, n_bases: int, max_base_size: int, base_factory: Callable[[None], int | float | str], factory_args: list, factory_kwargs: dict = None) -> Genome:` 

Adds a chromosome to the end of the genome. If chromosome is None, adds a random
Chromosome using Chromosome.make and passing kwargs. Returns self for chaining
operations.

##### `duplicate(index: int = None) -> Genome:` 

Duplicates the Chromosome at the index. If index is None, the Chromosome at a
random index is duplicated. Returns self for chaining operations.

##### `delete(index: int = None) -> Genome:` 

Deletes the Chromosome at the index. If index is None, a Chromosome is deleted
at a random index. Returns self for chaining operations.

##### `substitute(index: int, chromosome: Chromosome, n_alleles: int, n_genes: int, n_bases: int, max_base_size: int, base_factory: Callable[[None], int | float | str], factory_args: list = None, factory_kwargs: dict = None) -> Genome:` 

Substitutes the Chromosome at the index with the given chromosome. If index is
None, a random index will be used. If chromosome is None, adds a random
chromosome using Chromosome.make, passing the kwargs. Returns self for chaining
operations.

##### `recombine(other: Genome, indices: list[int] = None, recombine_chromosomes: bool = True, match_chromosomes: bool = True, recombine_alleles: bool = True, match_alleles: bool = True, recombine_genes: bool = True, match_genes: bool = True) -> Genome:` 

Recombines with the other Genome, swapping at the given indices. If indices is
None, between 1 and ceil(log(len(self.chromosomes))) random indices will be
chosen. Recombines individual Chromosomes if recombine_chromosomes is True.
Recombines only Chromosomes with matching names if match_chromosomes is True.
Recombines individual Alleles if recombine_alleles is True. Recombines only
Alleles with matching names if match_alleles is True. Recombines individual
Genes if recombine_genes is True. Recombines only Genes with matching names if
match_genes is True. Returns the new Genome.

##### `@classmethod make(n_chromosomes: int, n_alleles: int, n_genes: int, n_bases: int, name: str, max_base_size: int, base_factory: Callable[[None], int | float | str], factory_args: list, factory_kwargs: dict) -> Genome:` 

Makes and returns a Genome of randomized Chromosomes.

##### `to_dict() -> dict:` 

Serialize the Genome to a dict.

##### `@classmethod from_dict(data: dict) -> Genome:` 

Deserialize a Genome from a dict.

## Functions

### `optimize_gene(measure_fitness: Callable, mutate_gene: Callable, initial_population: list = None, population_size: int = 100, gene_size: int = 10, fitness_target: int | float = 1.0, max_iterations: int = 1000, base_factory: Callable = None, factory_args: list = None, factory_kwargs: dict = None, gene_name: str = None, parents_per_generation: int = 10) -> tuple[int, list[bluegenes.genes.Gene]]:` 

Optimize a Gene given a measure_fitness function, a mutate_gene function, a
population_size int, a gene_size int, a fitness_target float, and a
max_iterations int. Supply base_factory to produce Gene bases other than random
ints between 0 and 10, with optional factory_args and factory_kwargs which will
be passed to each call of base_factory. Supply gene_name to assign the name to
each Gene in the population. Returns the number of iterations and the final
population.

### `optimize_allele(measure_fitness: Callable, mutate_allele: Callable, initial_population: list = None, population_size: int = 100, allele_size: int = 2, gene_size: int = 10, fitness_target: int | float = 1.0, max_iterations: int = 1000, base_factory: Callable = None, factory_args: list = None, factory_kwargs: dict = None, allele_name: str = None, parents_per_generation: int = 10) -> tuple[int, list[bluegenes.genes.Allele]]:` 

Optimize an Allele given a measure_fitness function, a mutate_allele function, a
population_size int, a fitness_target float, and a max_iterations int. Supply
base_factory to produce Gene bases other than random ints between 0 and 10, with
optional factory_args and factory_kwargs which will be passed to each call of
base_factory. Supply allele_name to assign the name to each generated Allele in
the population. Supply an allele_size int and a gene_size int to customize
generation of a random initial population, or supply initial_population
list[Allele] to specify the initial population. Returns the number of iterations
and the final population.

### `optimize_chromosome(measure_fitness: Callable, mutate_chromosome: Callable, initial_population: list = None, population_size: int = 100, chromosome_size: int = 2, allele_size: int = 3, gene_size: int = 10, fitness_target: int | float = 1.0, max_iterations: int = 1000, base_factory: Callable = None, factory_args: list = None, factory_kwargs: dict = None, chromosome_name: str = None, parents_per_generation: int = 10) -> tuple[int, list[bluegenes.genes.Chromosome]]:` 

Optimize an Chromosome given a measure_fitness function, a mutate_chromosome
function, a population_size int, a fitness_target float, and a max_iterations
int. Supply base_factory to produce Gene bases other than random ints between 0
and 10, with optional factory_args and factory_kwargs which will be passed to
each call of base_factory. Supply chromosome_name to assign the name to each
generated Chromosome in the population. Supply an allele_size int and a
gene_size int to customize generation of a random initial population, or supply
initial_population list[Chromosome] to specify the initial population. Returns
the number of iterations and the final population.

### `optimize_genome(measure_fitness: Callable, mutate_genome: Callable, initial_population: list = None, population_size: int = 100, genome_size: int = 1, chromosome_size: int = 2, allele_size: int = 3, gene_size: int = 10, fitness_target: int | float = 1.0, max_iterations: int = 1000, base_factory: Callable = None, factory_args: list = None, factory_kwargs: dict = None, genome_name: str = None, parents_per_generation: int = 10) -> tuple[int, list[bluegenes.genes.Genome]]:` 

Optimize a Genome given a measure_fitness function, a mutate_chromosome
function, a population_size int, a fitness_target float, and a max_iterations
int. Supply base_factory to produce Gene bases other than random ints between 0
and 10, with optional factory_args and factory_kwargs which will be passed to
each call of base_factory. Supply genome_name to assign the name to each
generated Genome in the population. Supply an allele_size int and a gene_size
int to customize generation of a random initial population, or supply
initial_population list[Genome] to specify the initial population. Returns the
number of iterations and the final population.

### `set_hook(func: Callable):` 

Set a hook that will be called after every generation and passed the current
generation count and the population with fitness scores.

### `unset_hook():` 

Unsets the hook.


