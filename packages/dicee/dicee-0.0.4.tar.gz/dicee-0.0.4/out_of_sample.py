from py2puml.py2puml import py2puml

if __name__ == '__main__':
    # outputs the PlantUML content in the terminal
    print(''.join(py2puml('py2puml/domain', 'py2puml.domain')))

    exit(1)
    # writes the PlantUML content in a file
    with open('py2puml/domain.puml', 'w') as puml_file:
        puml_file.writelines(py2puml('py2puml/domain', 'py2puml.domain'))


exit(1)
import torch.nn

from dicee import KGE

model = KGE(path='Experiments/2023-02-27 11:18:18.836545')
# triples with france as subject
selected_idx_triples = model.train_set[model.train_set[:, 0] == model.entity_to_idx['france']]

heads = ['france' for i in range(len(selected_idx_triples))]
relations = [model.idx_to_relations[int(i)] for i in selected_idx_triples[:, 1]]
tails = [model.idx_to_entity[int(i)] for i in selected_idx_triples[:, -1]]


def distmult_scoring_func(head_ent_emb, rel_ent_emb, tail_ent_emb):
    # return torch.sum(head_ent_emb*rel_ent_emb*tail_ent_emb,dim=1)
    return torch.einsum('bd, bd, bd ->b', head_ent_emb, rel_ent_emb, tail_ent_emb)


print(torch.sigmoid(
    distmult_scoring_func(model.get_entity_embeddings(['france']), model.get_relation_embeddings(['locatedin']),
                          model.get_entity_embeddings(['western_europe']))))

emb_rel, emb_tail = model.get_relation_embeddings(relations), model.get_entity_embeddings(tails)
y = torch.ones(len(emb_tail))
x = torch.cat((emb_rel, emb_tail), dim=1)
out_of_vocab_emb = torch.zeros(32, requires_grad=True)
# print(out_of_vocab_emb.grad)
# Firs iteration
for i in range(1, 100):
    out_of_vocab_emb.grad = None
    yhat = torch.sigmoid(torch.sum((out_of_vocab_emb * emb_rel) * emb_tail, dim=1))
    loss = torch.mean((y - yhat) ** 2)
    loss.backward()
    out_of_vocab_emb.data -= out_of_vocab_emb.grad * 0.01



print(torch.sigmoid(
    distmult_scoring_func(out_of_vocab_emb.data.view(1,32), model.get_relation_embeddings(['locatedin']),
                          model.get_entity_embeddings(['western_europe']))))


exit(1)

# print(model.entity_to_idx)
print(model.relation_to_idx)
# spain, belguim, germany
for s, ent in zip(*model.topk(head_entity='france', relation='neighbor', k=12)):
    print(s, ent)

print('aou')
# an entity representing spain_and_germany (i.e. two entities) can be seen as out-of-vocab entity
avg_emb = model.get_entity_embeddings(items=['germany', 'spain', 'belgium']).mean(dim=0)
model.add_new_entity_embeddings(entity_name='spain_belgium', embeddings=avg_emb)

for s, ent in zip(*model.topk(head_entity='france', relation='neighbor', k=12)):
    print(s, ent)
