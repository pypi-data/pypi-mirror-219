from faknow.run import run, run_from_yaml
from faknow.model.content_based.multi_modal.eann import EANN
from faknow.run.content_based.multimodal.run_eann import run_eann, run_eann_from_yaml


if __name__ == '__main__':
    model = 'eann'
    run_from_yaml(model, r'..\properties\eann.yaml')
    # model = 'mdfend'
    # run(model, train_path=r'F:\dataset\weibo21-mdfend\all.json')
