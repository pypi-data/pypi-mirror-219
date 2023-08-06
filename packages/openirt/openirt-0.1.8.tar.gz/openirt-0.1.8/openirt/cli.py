import argparse
from irt_instance import IRTInstance

parser = argparse.ArgumentParser(prog='openirt',
                                 description='Item Response Theory package CLI')

parser.add_argument('action', type=str, choices=['train', 'est-item', 'est-ability'], help='The action to perform')
parser.add_argument('results', type=str, help='The path to the results file')
parser.add_argument('--item_params', type=str, help='The path to the item parameters file')
parser.add_argument('--ability', type=str, help='The path to the ability parameters file')
parser.add_argument('--model', type=str, choices=['1pl', '2pl', '3pl', 'norm'],
                    help='The IRT model to use', default='2pl')
parser.add_argument('--row', type=str, default='None', choices=['item', 'subject'], help='The attribute associated with the rows')
parser.add_argument('--col', type=str, default='None', choices=['item', 'subject'] , help='The attribute associated with the columns')
parser.add_argument('--labeled', default=False, action='store_true', help='Specify if the items or subjects are labeled')
parser.add_argument('--saveICC', default=False, action='store_true', help='Save the ICC values to a file')

# Parse the command line arguments
args = parser.parse_args()
if args.row == args.col and args.row != 'None':
    parser.error('Rows and columns must be different dimensions.')

irt_model = IRTInstance(results_file = args.results, 
                        model=args.model, 
                        labeled=args.labeled, 
                        item_params_file=args.item_params, 
                        ability_file=args.ability,
                        row=args.row,
                        col=args.col)

if args.action == 'train':
    irt_model.train_model()
    irt_model.save_item_params()
    irt_model.save_abilities()

if args.action == 'est-item':
    irt_model.estimate_item_params()
    irt_model.save_item_params()
    
if args.action == 'est-ability':
    irt_model.estimate_abilities()
    irt_model.save_abilities()
    
if args.saveICC:
    irt_model.saveICC()