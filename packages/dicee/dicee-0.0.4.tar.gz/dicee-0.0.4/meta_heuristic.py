from main import get_default_arguments
from dicee.executer import Execute, ContinuousExecute


def find_valid_p_q(dim):
    results = set()
    p = 0
    q = 0
    denom = p + q + 1
    while True:
        if denom == dim:
            break

        r = dim / denom
        if r.is_integer():
            results.add((p, q))
            assert (dim / (p + q + 1)).is_integer()
        else:
            for i in range(denom):
                if (dim / (i + denom - i + 1)).is_integer():
                    results.add((i, denom - i))

        denom += 1

    return results


def initialize_population(dim):
    result = []
    for (p, q) in find_valid_p_q(dim):
        result.append({'p': p, 'q': q, 'num_epochs': 10})
    return result


# Initialize the population
population = initialize_population(dim=2)
for i in population:
    args = get_default_arguments()
    args.p = i['p']
    args.q = i['q']
    args.num_epochs = i['num_epochs']
    report = Execute(args).start()

    i['Train'] = report['Train']
    i['Val'] = report['Val']
    i['Test'] = report['Test']
    i['path_experiment_folder'] = report['path_experiment_folder']

# Sort the population.
population.sort(key=lambda x: x['Train']['MRR'], reverse=True)
# Take the best 50%.
population = population[:len(population) // 2]

print('Population:', len(population))
while len(population) >0:
    for i in population:
        args = get_default_arguments()
        args.p = i['p']
        args.q = i['q']
        args.num_epochs = i['num_epochs'] + i['num_epochs']
        args.path_experiment_folder = i['path_experiment_folder']
        report = ContinuousExecute(args).continual_start()

        i['Train'] = report['Train']
        i['Val'] = report['Val']
        i['Test'] = report['Test']

# Sort the population.
population.sort(key=lambda x: x['Train']['MRR'], reverse=True)
# Take the best 50%.
population = population[:len(population) // 2]

for i in population:
    print(i)
