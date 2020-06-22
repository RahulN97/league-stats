import argparse
import pprint
import requests
import threading

from constants import (
    API_KEY,
    ROOT_SUMMONER,
    STRATEGIES
)
from modules import (
    ChampionCombo
)
from resource_manager import (
    FetchStatus,
    ResourceManager,
    RESULTS
)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--strats', nargs='+', default=None,
        help='Choose strategies from the following [{strats}]'.format(
            strats=', '.join(STRATEGIES)
        )
    )
    parser.add_argument(
        '--user', type=str, default=None, help='The root user for running stats'
    )
    parser.add_argument(
        '--size', type=int, default=300,
        help='Number of games in match history to include'
    )
    return parser.parse_args()


def _validate_args(args):
    args.user = args.user if args.user else ROOT_SUMMONER
    #TODO(@rnambiar): validate user

    if not args.strats:
        raise Exception('Must specify at least one strategy to execute')

    args.strats = [s.lower() for s in args.strats]
    for strat in args.strats:
        if strat not in STRATEGIES:
            raise Exception(f'{strat} is not a valid strategy name')
    return args


def display_results():
    rm = ResourceManager()
    pprint.pprint(RESULTS)


def init_shared_resources(args):
    rm = ResourceManager(args)
    rm.init_all_resources()

    if all(status == FetchStatus.SUCCESS for resource,status in rm.statuses.items()):
        return
    failed = [r for r,s in rm.statuses.items() if s == FetchStatus.FAIL]
    raise Exception(f'Resource loading failed for the following resources:\n[{failed}]')


def map_reduce_strats(args):
    threads = [
        threading.Thread(target=produce_strategy(args, strat).execute())
        for strat in args.strats
    ]
    map(lambda t: t.start(), threads)
    map(lambda t: t.join(), threads)


def produce_args():
    return _validate_args(_parse_args())


def produce_strategy(args, strat):
    if strat == 'championcombo':
        return ChampionCombo(args.user, args.size)
    raise Exception(f'Invalid strategy name: {strat}')


if __name__ == "__main__":
    args = produce_args()
    init_shared_resources(args)
    map_reduce_strats(args)
    display_results()
