from dicee.config import Args
from dicee.executer import Execute
# import code;
# code.interact(local=locals())
from dicee.static_funcs import random_prediction
from dicee import KGE
x=KGE('Experiments/2023-07-13 20:46:05.306581')
print(x.predict_topk(head_entity=['alga'],relation=['isa']))
