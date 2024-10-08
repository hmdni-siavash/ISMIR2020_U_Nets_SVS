from argparse import ArgumentParser
from datetime import datetime

from pytorch_lightning import Trainer

from source_separation.data.musdb_wrapper.dataloaders import DataProvider
from source_separation.models.scripts import trainer, evaluator
from source_separation.models.model_definition import get_class_by_name
from source_separation.utils.functions import mkdir_if_not_exists


def main(args):
    pass


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--model', type=str)
    parser.add_argument('--mode', type=str, default='train')
    temp_args, _ = parser.parse_known_args()

    # Model
    model = get_class_by_name(temp_args.model)
    parser = model.add_model_specific_args(parser)

    # Dataset
    parser = DataProvider.add_data_provider_args(parser)

    mode = temp_args.mode

    # Environment Setup
    mkdir_if_not_exists('etc')
    mkdir_if_not_exists('etc/checkpoints')

    parser.add_argument('--ckpt_root_path', type=str, default='etc/checkpoints')
    parser.add_argument('--log', type=str, default=True)
    parser.add_argument('--run_id', type=str, default=str(datetime.today().strftime("%Y%m%d_%H%M")))
    parser.add_argument('--save_weights_only', type=bool, default=False)

    if mode == 'train':
        parser.add_argument('--save_top_k', type=int, default=5)
        parser.add_argument('--patience', type=int, default=40)
        parser.add_argument('--seed', type=int, default=None)

        parser = Trainer.add_argparse_args(parser)
        trainer.train(parser.parse_args())

    elif mode == 'eval':
        parser.add_argument('--ckpt', type=str)
        parser = Trainer.add_argparse_args(parser)
        args = parser.parse_args()
        vargs = vars(args)
        for key in vargs.keys():
            print('{}:{}'.format(key, vargs[key]))
        evaluator.eval(args)
