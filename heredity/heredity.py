import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Initialize
    joint_prob = 1

    # Independent probabilities
    for person in people.keys():
        people[person]['Probabilities'] = dict()
        if people[person]['father'] == None and people[person]['mother'] == None: # Se asume que están los dos
            # Number of genes
            if person not in one_gene.union(two_genes):
                people[person]['Probabilities']['no_genes'] = PROBS["gene"][0]               # 0.96
                if person in have_trait:
                    people[person]['Probabilities']['have_trait'] = PROBS['trait'][0][True]      # 0.01
                else:
                    people[person]['Probabilities']['no_trait'] = PROBS['trait'][0][False]     # 0.99
            if person in one_gene:
                people[person]['Probabilities']['one_gene'] = PROBS["gene"][1]               # 0.03
                if person in have_trait:
                    people[person]['Probabilities']['have_trait'] = PROBS['trait'][1][True]      # 0.56
                else:
                    people[person]['Probabilities']['no_trait'] = PROBS['trait'][1][False]     # 0.44
            if person in two_genes:
                people[person]['Probabilities']['two_genes'] = PROBS["gene"][2]              # 0.01
                if person in have_trait:
                    people[person]['Probabilities']['have_trait'] = PROBS['trait'][2][True]      # 0.65
                else:
                    people[person]['Probabilities']['no_trait'] = PROBS['trait'][2][False]     # 0.35
        
        else:
            if person not in one_gene.union(two_genes):
                if person in have_trait:
                    people[person]['Probabilities']['have_trait'] = PROBS['trait'][0][True]      # 0.01
                else:
                    people[person]['Probabilities']['no_trait'] = PROBS['trait'][0][False]     # 0.99
            if person in one_gene:
                if person in have_trait:
                    people[person]['Probabilities']['have_trait'] = PROBS['trait'][1][True]      # 0.56
                else:
                    people[person]['Probabilities']['no_trait'] = PROBS['trait'][1][False]     # 0.44
            if person in two_genes:
                if person in have_trait:
                    people[person]['Probabilities']['have_trait'] = PROBS['trait'][2][True]      # 0.65
                else:
                    people[person]['Probabilities']['no_trait'] = PROBS['trait'][2][False]     # 0.35
            

    # Dependent probabilities - inherited genes before mutation
    for person in people.keys():
        father = people[person]['father']
        mother = people[person]['mother']
        if father != None and mother != None:
            if father in two_genes and mother in two_genes:
                people[person]['Probabilities']['inherit_two_genes'] = 1
            
            if father in two_genes and mother in one_gene:
                people[person]['Probabilities']['inherit_one_gene'] = 0.5
                people[person]['Probabilities']['inherit_two_genes'] = 0.5
            if mother in two_genes and father in one_gene:
                people[person]['Probabilities']['inherit_one_gene'] = 0.5
                people[person]['Probabilities']['inherit_two_genes'] = 0.5
            
            if father in two_genes and mother not in one_gene.union(two_genes):
                people[person]['Probabilities']['inherit_one_gene'] = 1
            if mother in two_genes and father not in one_gene.union(two_genes):
                people[person]['Probabilities']['inherit_one_gene'] = 1

            if mother in one_gene and father in one_gene:
                people[person]['Probabilities']['inherit_no_genes'] = 0.25
                people[person]['Probabilities']['inherit_one_gene'] = 0.5
                people[person]['Probabilities']['inherit_two_genes'] = 0.25

            if father in one_gene and mother not in one_gene.union(two_genes):
                people[person]['Probabilities']['inherit_no_genes'] = 0.5
                people[person]['Probabilities']['inherit_one_gene'] = 0.5
            if mother in one_gene and father not in one_gene.union(two_genes):
                people[person]['Probabilities']['inherit_no_genes'] = 0.5
                people[person]['Probabilities']['inherit_one_gene'] = 0.5

            if mother not in one_gene.union(two_genes) and father not in one_gene.union(two_genes):
                people[person]['Probabilities']['inherit_no_genes'] = 1

            # Dependent probabilities - child genes after mutation

            if 'inherit_two_genes' in people[person]['Probabilities'].keys():
                if person not in one_gene.union(two_genes):
                    people[person]['Probabilities']['2-0 mutation'] = PROBS['mutation']**2
                if person in one_gene:
                    people[person]['Probabilities']['2-1 mutation'] = 2*(PROBS['mutation']*(1-PROBS['mutation']))              
                if person in two_genes:
                    people[person]['Probabilities']['2-2 mutation'] = (1-PROBS['mutation'])**2

            if 'inherit_one_gene' in people[person]['Probabilities'].keys():
                if person not in one_gene.union(two_genes):
                    people[person]['Probabilities']['1-0 mutation'] = PROBS['mutation']*(1-PROBS['mutation'])
                if person in one_gene:    
                    people[person]['Probabilities']['1-1 mutation'] = (1-PROBS['mutation'])**2 + PROBS['mutation']**2        
                if person in two_genes:    
                    people[person]['Probabilities']['1-2 mutation'] = PROBS['mutation']*(1-PROBS['mutation'])           

            if 'inherit_no_genes'in people[person]['Probabilities'].keys():
                if person not in one_gene.union(two_genes):
                    people[person]['Probabilities']['0-0 mutation'] = (1-PROBS['mutation'])**2  
                if person in one_gene:    
                    people[person]['Probabilities']['0-1 mutation'] = 2*(PROBS['mutation']*(1-PROBS['mutation']))              
                if person in two_genes:
                    people[person]['Probabilities']['0-2 mutation'] = PROBS['mutation']**2

    # Calculate joint probability
    for person in people.keys():
        if people[person]['father'] != None and people[person]['mother'] != None:
            
            prob_child = 0
            
            if person not in one_gene.union(two_genes):
                if 'inherit_no_genes' in people[person]['Probabilities'].keys():
                    prob_child += people[person]['Probabilities']['inherit_no_genes'] * people[person]['Probabilities']['0-0 mutation']
                if 'inherit_one_gene' in people[person]['Probabilities'].keys():
                    prob_child += people[person]['Probabilities']['inherit_one_gene'] * people[person]['Probabilities']['1-0 mutation']
                if 'inherit_two_genes' in people[person]['Probabilities'].keys():
                    prob_child += people[person]['Probabilities']['inherit_two_genes'] * people[person]['Probabilities']['2-0 mutation']

            if person in one_gene:
                if 'inherit_no_genes' in people[person]['Probabilities'].keys():
                    prob_child += people[person]['Probabilities']['inherit_no_genes'] * people[person]['Probabilities']['0-1 mutation']
                if 'inherit_one_gene' in people[person]['Probabilities'].keys():
                    prob_child += people[person]['Probabilities']['inherit_one_gene'] * people[person]['Probabilities']['1-1 mutation']
                if 'inherit_two_genes' in people[person]['Probabilities'].keys():
                    prob_child += people[person]['Probabilities']['inherit_two_genes'] * people[person]['Probabilities']['2-1 mutation']
            
            if person in two_genes:
                if 'inherit_no_genes' in people[person]['Probabilities'].keys():
                    prob_child += people[person]['Probabilities']['inherit_no_genes'] * people[person]['Probabilities']['0-2 mutation']
                if 'inherit_one_gene' in people[person]['Probabilities'].keys():
                    prob_child += people[person]['Probabilities']['inherit_one_gene'] * people[person]['Probabilities']['1-2 mutation']
                if 'inherit_two_genes' in people[person]['Probabilities'].keys():
                    prob_child += people[person]['Probabilities']['inherit_two_genes'] * people[person]['Probabilities']['2-2 mutation']

            ###########
            # people[person]['Probabilities_2'] = people[person]['Probabilities'].copy()
            ##########


            if 'have_trait' in people[person]['Probabilities'].keys():
                people[person]['Probabilities'] ={'prob_child':prob_child,'have_trait':people[person]['Probabilities']['have_trait']}
            if 'no_trait' in people[person]['Probabilities'].keys():
                people[person]['Probabilities'] ={'prob_child':prob_child,'no_trait':people[person]['Probabilities']['no_trait']}

        for value in people[person]['Probabilities'].values():
            joint_prob *= value


    return joint_prob
    # raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person not in one_gene.union(two_genes):
            probabilities[person]["gene"][0]        +=  p
        if person in one_gene:
            probabilities[person]["gene"][1]        +=  p
        if person in two_genes:
            probabilities[person]["gene"][2]        +=  p
        if person in have_trait:
            probabilities[person]["trait"][True]    +=  p
        if person not in have_trait:
            probabilities[person]["trait"][False]   +=  p

    # raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:

        genesNormFactor = (probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2])
        for numGenes in probabilities[person]["gene"]:
            probabilities[person]["gene"][numGenes] = probabilities[person]["gene"][numGenes] / genesNormFactor
        
        traitNormFactor = (probabilities[person]["trait"][True] + probabilities[person]["trait"][False])
        for value in probabilities[person]["trait"]:
            probabilities[person]["trait"][value] = probabilities[person]["trait"][value] / traitNormFactor
    # raise NotImplementedError


if __name__ == "__main__":
    main()
########################     Pruebas       ############################

# people = load_data("data\\family0.csv")

# one_gene = set()
# one_gene.add( 'Harry' )
# # one_gene.add('Lily')
# # one_gene.add('James')
# two_genes = {'James',}
# # two_genes = set()
# # two_genes = {'Lily','James','Harry'}
# trait = set()
# trait.add('James')
# # trait = {'Lily',}
# # trait = {"Harry", "James",'Lily'}

# joint_probability( people, one_gene, two_genes, trait)