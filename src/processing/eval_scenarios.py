import os
import argparse
import pandas as pd

from structure.usecase import UseCase

from structure.usecase import UseCase
from structure.entity import Entity
from structure.step import Step

from util.sequencediagramparser import parse_sequence_diagram as psd

datapath = '../../data/'

def read_mermaid_diagram(path: str) -> list[str]:
    with open(path, 'r') as file:
        return [line for line in file]
    
def parse_use_case(req: str, ucid: str, lines: list[str]) -> UseCase:
    # discard the first two and last lines which contain the ``` syntax
    lines = lines[2:-1]

    # remove the trailing \n from all lines
    lines = [(line[:-1] if line.endswith('\n') else line) for line in lines]

    # remove all empty lines
    lines = [line for line in lines if line.strip()!=""]

    # parse the actors and participants
    entities: list[Entity] = []
    i = 0
    currentline: str = lines[i]
    while currentline.startswith('actor') or currentline.startswith('participant'):
        entities.append(Entity(currentline))

        i = i + 1
        currentline = lines[i]

    # parse the sequence
    firststep: Step = psd(lines[i:], entities)

    return UseCase(req, ucid, entities, firststep)

def parse_use_cases(path: str) -> list[UseCase]:
    result: list[UseCase] = []

    # find all the reqs in the path
    reqs = [ f.name for f in os.scandir(path) if f.is_dir() ]
    for req in reqs:
        req_path = os.path.join(path, req)

        # find all the use cases from that req
        ucs = [ f.name for f in os.scandir(req_path) if f.is_file() ]
        for ucfile in ucs:
            uc_path = os.path.join(req_path, ucfile)
            ucid = ucfile.split('.')[0]

            mermaid_diagram = read_mermaid_diagram(uc_path)
            uc: UseCase = parse_use_case(req=req, ucid=ucid, lines=mermaid_diagram)
            result.append(uc)

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Specify both a Requirement and Use Case ID to inspect a specific requirement instead of parsing all requirements')
    parser.add_argument('--req', type=str, default=None, help='Identifier of the requirement (in REQ-XXXX format), defaults to None')
    parser.add_argument('--ucid', type=str, default=None, help='Identifier of the use case (e.g., uc1, uc2), defaults to None')
    args=parser.parse_args()

    if args.req != None and args.ucid != None:
        filename: str = os.path.join(datapath, f'transformation/{args.req}/{args.ucid}.md')
        try:
            # parse one specific req
            md = read_mermaid_diagram(filename)
            uc = parse_use_case(req=args.req, ucid=args.ucid, lines=md)

            # print the use case
            print(f'{args.req}/{args.ucid}')
            print(f' - {uc.get_number_of_entities()} entities ({uc.get_number_of_entities(only_actors=True)} actors, {uc.get_number_of_entities(only_explicit=True)} explicit)')
            print(f' - {uc.get_number_of_interactions(only_userlevel=False)} interactions ({uc.get_number_of_interactions(only_userlevel=True)} user-system level, {uc.get_number_of_consecutive_interactions()} consecutive)')
            print()
            uc.print()
        except FileNotFoundError as e:
            print(f'No file found at {filename}')
    else:
        # parse all use cases
        ucs = parse_use_cases(os.path.join(datapath, 'transformation/'))
        print(f'Parsed {len(ucs)} use case descriptions in sequence diagram format.')

        # create an empty data frame for all the metrics
        df: pd.DataFrame = pd.DataFrame(columns=[
            'req', 'ucid', # index
            'entities', 'actors', 'actors_explicit', # information about the entities
            'interactions', 'pureinteractions', 'consecutive' # information about the interactions
            ])
        df = df.set_index(['req', 'ucid'])
        
        # calculate the metrics of interest and store them rowwise into the data frame
        for uc in ucs:
            df.loc[(uc.req, uc.ucid),:] = pd.Series({
                'entities': uc.get_number_of_entities(),
                'actors': uc.get_number_of_entities(only_actors=True),
                'actors_explicit': uc.get_number_of_entities(only_actors=True, only_explicit=True),
                'interactions': uc.get_number_of_interactions(),
                'pureinteractions': uc.get_number_of_interactions(only_userlevel=True),
                'consecutive': uc.get_number_of_consecutive_interactions()
            })

        # save the data frame as a file
        df.to_csv(os.path.join(datapath, 'extraction/uca-automatic.csv'))