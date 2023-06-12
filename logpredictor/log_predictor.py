import argparse
import os
import subprocess
import sys

sys.path.append(os.path.abspath(''))
sys.path.append(os.path.abspath('') + '/datasets')
sys.path.append(os.path.abspath('') + '/parsers')
sys.path.append(os.path.abspath('') + '/predictor')
sys.path.append(os.path.abspath('') + '/report_generator')
sys.path.append(os.path.abspath('') + '/tmp')
sys.path.append(os.path.abspath('') + '/utils')
sys.path.append(os.path.abspath('') + '/visualizer')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from datasets.log_dataset import LogDataset
from parsers.report_parser import ReportParser
from predictor.recurrent_neural_network import RecurrentNeuralNetwork
from report_generator.report_writer import ReportWriter
from utils.enums import DataProcessTypes


def get_args():
    args_parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    args_parser.add_argument('log_file', help='Log file path')
    args_parser.add_argument('--prediction',
                             help='Includes time series forecasting in the report',
                             action='store_true')
    args_parser.add_argument('--steps',
                             help='Determines what percentage of the number of previous steps must be taken into '
                                  'account when predicting characteristics for subsequent time intervals (by default, '
                                  'it takes into account 10%)',
                             type=int,
                             default=10)
    args_parser.add_argument('--width',
                             help='Determines how many steps to predict (by default, 5% of the number of previous '
                                  'steps is predicted).',
                             type=int,
                             default=5)
    return args_parser.parse_args()


def main():
    args = get_args()
    # pdbadger = PGBadger()
    # subprocess.call('pgbadger /tmp/postgresql-2023-05-21_151700.log -o tmp/pgbadger_out.html', shell=True)
    if args.steps > 100 or args.steps < 1 or args.width > 100 or args.width < 1:
        raise ValueError('Arguments must be between 1 and 100')
    if not args.prediction:
        subprocess.call(f'pgbadger {args.log_file} -o report.html', shell=True)
    else:
        subprocess.call(f'pgbadger {args.log_file} -o tmp/pgbadger_out.html', shell=True)
    report_parser = ReportParser('/tmp/pgbadger_out.html')
    report_parser.parse()
    log_dataset = LogDataset(dataframe_path='/tmp/report_parser_out.csv',
                             preprocess_type=DataProcessTypes.standardization.value,
                             train_set_percent=0.7,
                             valid_set_percent=0.2)
    recurrent_neural_network = RecurrentNeuralNetwork(dataset=log_dataset,
                                                      n_features=log_dataset.dimension,
                                                      n_steps=int(log_dataset.inputs.shape[0] * args.steps // 100),
                                                      n_width=int(log_dataset.inputs.shape[0] * args.width // 100))
    recurrent_neural_network.get_predictions()
    print('Generating html report...')
    report_writer = ReportWriter()
    report_writer.write()
    print('Report created and saved in a file:\n/tmp/logpredictor/report.html')


if __name__ == '__main__':
    main()
