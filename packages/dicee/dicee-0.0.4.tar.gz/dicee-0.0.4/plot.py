from dicee import KGE

KGE('Experiments/2023-05-12 10:27:13.950047')

exit(1)
import os
import json
import pandas as pd
import pickle
import matplotlib.pyplot as plt

paths = ['UMLS/', 'KINSHIP/']
fig, axes = plt.subplots(2, 2, figsize=(9, 7))


def load_pickle(*, file_path=str):
    with open(file_path, 'rb') as f:
        return pickle.load(f)


data_for_plots = []
for ith, input_str_path in enumerate(paths):
    sub_folder_str_paths = os.listdir(input_str_path)
    results = dict()

    experiments = []
    have_seen = set()
    for path in sub_folder_str_paths:
        try:
            with open(input_str_path + path + '/configuration.json', 'r') as f:
                config = json.load(f)
                config = {i: config[i] for i in
                          ['model', 'embedding_dim', 'callbacks', 'path_dataset_folder', 'p', 'q']}

                config['results'] = load_pickle(file_path=input_str_path + path + '/evals_per_epoch')
                experiments.append(config)

        except:
            print('Exception occured at reading config', path)
            continue

    labels = []
    for i in experiments:
        data_for_plots.append((input_str_path, f'{i["p"]},{i["q"]}', [i['Train']['MRR'] for i in i['results']],
                               [i['Val']['MRR'] for i in i['results']]))

color_mapping = {'0,0': 'pink',
                 '1,0': 'orange',
                 '0,1': 'green',
                 '3,0': 'red',
                 '0,3': 'purple',
                 '3,4': 'brown',
                 '4,3': 'blue'}

data_for_plots.sort(key=lambda x: x[1])

for input_str_path, label, train_mrr, val_mrr in data_for_plots:

    if label in ['0,0', '1,0', '0,1', '3,0', '0,3', '3,4', '4,3']:
        if input_str_path == 'UMLS/':
            axes[0][0].plot(train_mrr, label=label, c=color_mapping[label])
            axes[1][0].plot(val_mrr, label=label, c=color_mapping[label])
        else:
            axes[0][1].plot(train_mrr, label=label, c=color_mapping[label])
            axes[1][1].plot(val_mrr, label=label, c=color_mapping[label])

axes[0][0].set_ylim([0, 1.1])
axes[0][1].set_ylim([0, 1.1])
axes[1][0].set_ylim([0, 1.1])
axes[1][1].set_ylim([0, 1.1])

axes[0][0].set_title('UMLS')
axes[0][1].set_title('KINSHIP')

axes[0][0].set_ylabel('Train MRR')
axes[1][0].set_ylabel('Val MRR')

axes[1][0].set_xlabel('Epochs')
axes[1][1].set_xlabel('Epochs')

axes[0][0].grid(True)
axes[0][1].grid(True)
axes[1][0].grid(True)
axes[1][1].grid(True)

axes[0][0].legend()
axes[0][1].legend(loc=(1.02, -.3))
# axes[1][0].legend()
# axes[1][1].legend()
plt.savefig('CMult.pdf')

plt.show()
