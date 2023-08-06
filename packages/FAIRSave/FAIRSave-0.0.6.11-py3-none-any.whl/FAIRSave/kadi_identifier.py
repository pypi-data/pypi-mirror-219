from kadi_apy import KadiManager
from FAIRSave.kadi_search import search_item_id_kadi
from kadi_apy.lib.search import Search
import itertools
from typing import Optional, Union
import os
from pathlib import Path
import itertools
import string
import requests
import re
import math


def title_id_identifier_tuples_kadi(instance: str,
                                        item: str,
                                        collection_id: Optional[int] = None,
                                        collection: Optional[str] = None,
                                        child_collections: Optional[bool] = True,
                                        visibility: Optional[str] = 'private'):
    """Outputs a list of tuples with title, id and identifier for records of a collection.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        item (str): Item whose identifiers should be listed
        collection_id (Optional[int], optional): Id of collection to search in. Defaults to None.
        collection (Optional[str], optional): Title of colleciton to search in. Defaults to None.
        child_collections (Optional[bool], optional): Should child collecitons be included? Defaults to True.
        visibility (Optional[str], optional): Visibility option for records. Defaults to 'private'.
    """
    
    if collection is not None:
        collection_id = search_item_id_kadi(instance,
                                            title=collection,
                                            item='collection')
        
    search_results = (Search(KadiManager(instance)).search_resources(  item=item,
                                        visibility=visibility,
                                        collection=collection_id,
                                        child_collections=child_collections,
                                        per_page=100))
    pages = search_results.json()['_pagination'].get('total_pages')

    item_tuples = []
    for page in range(1, pages+1):
        var = Search(KadiManager(instance)).search_resources(  item=item,
                                visibility=visibility,
                                collection=collection_id,
                                child_collections=child_collections,
                                per_page=100,
                                page=page).json().get('items')
        if item == "record":
            item_tuples += [(x['title'], x['id'], x['identifier'][-11:-6]) for x in var if is_valid_identifier_kadi(x['identifier'])]
        elif item == "collection":
            item_tuples += [(x['title'], x['id'], x['identifier']) for x in var if is_valid_identifier_kadi(x['identifier'])]
        
    item_tuples = sorted(item_tuples, key=lambda x: x[2])
    
    item_tuples_string = ''.join(['\t'.join(str(s) for s in item) + '\n' for item in item_tuples])
    
    manager = KadiManager(instance)
    record = manager.record(id=18224)
    record.upload_string_to_file(item_tuples_string,"Used_identifiers.csv",force=True)

def get_vocpopuli_id(top_level_term: str,
                    Gitlab_PAT: str,
                    project_id: Optional[int] = 41732562):
    """Search in Gitlab for top-level term ID of vocabulary

    Args:
        top_level_term (str): Top-level-term from VocPopuli.
        Gitlab_PAT (str): Access token for Gitlab.
        project_id (Optional[int], optional): Gitlab project id for vocabulary. Defaults to 41732562.

    Returns:
        str: Local id of top-level term in VocPopuli.
    """
    
    issues_ep = f"projects/{project_id}/issues"

    params = {'private_token': Gitlab_PAT,
              'scope': 'all',
              'order_by': 'created_at',
              'sort': 'desc',
              'per_page': 100,
              'search': top_level_term}

    # get all repository issues
    issues_response = requests.get(f"https://gitlab.com/api/v4/{issues_ep}",
                                   params=params)
    issues_dict_list = issues_response.json()

    # handle pagination
    for page in range(2, 1 + int(issues_response.headers.get('X-Total-Pages', 0))):
        params['page'] = page
        next_page = requests.get(f"https://gitlab.com/api/v4/{issues_ep}",
                                 params=params)
        issues_dict_list += next_page.json()

    for issue in issues_dict_list:
        title = issue['title']
        label = title.split(' | ')[0].split('] ')[1]
        if top_level_term == label:
            global_t_id = title.split(' | ')[1]
            break

    repo_tree_ep = f"projects/{project_id}/repository/tree"
    params = {'private_token': Gitlab_PAT,
              'path': 'approved_terms',
              'per_page': 100,
              'ref': 'main'}

    repo_files = []
    repo_files_response = requests.get(f"https://gitlab.com/api/v4/{repo_tree_ep}",
                                       params=params)

    repo_files += repo_files_response.json()

    # handle pagination
    if 'rel="next"' in repo_files_response.headers['Link']:
        more_pages_left = True
    else:
        more_pages_left = False

    while more_pages_left:
        # get all pagination links
        pagination_links = (repo_files_response.headers['Link']
                            .split(', '))
        # get the link to the next page
        next_page_link = [x
                          for x in pagination_links
                          if 'rel="next"' in x][0]
        # strip 'rel="next"'
        next_page_link = next_page_link.split(';')[0]
        # remove leading < and trailing >
        next_page_link = next_page_link[1:-1]
        repo_files_response = requests.get(next_page_link, params=params)
        repo_files += repo_files_response.json()

        # breaking condition
        if any([f'{global_t_id}.json' == x['name'] for x in repo_files]):
            more_pages_left = False
        elif 'rel="next"' in repo_files_response.headers['Link']:
            more_pages_left = True
        else:
            more_pages_left = False

    file_dict = [x
                 for x in repo_files
                 if x['name'] == f'{global_t_id}.json'][0]

    file_path = (file_dict['path']
                 .replace('approved_terms/', 'approved_terms%2F')
                 .replace('.json', '%2Ejson'))

    file_ep = f"projects/{project_id}/repository/files/{file_path}/raw"
    params = {'private_token': Gitlab_PAT,
              'ref': 'main'}
    file = requests.get(f"https://gitlab.com/api/v4/{file_ep}",
                        params=params)
    metadata = file.json().get('metadata')
    id_t_local = metadata.get('id_t_local')
    
    return id_t_local

def new_identifier_kadi(instance: str,
                        top_level_term: str,
                        Gitlab_PAT: str,
                        project_id: Optional[int] = 41732562):
    """Creates a new Kadi4Mat record identifier.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        top_level_term (str): Top-level-term from VocPopuli.
        Gitlab_PAT (str): Access token for Gitlab.
        project_id (Optional[int], optional): Gitlab project id for vocabulary. Defaults to 41732562.

    Returns:
        str: Record identifier
    """
    
    # manager = KadiManager(instance)
    # record = manager.record(id=18224)
    # file_id = record.get_file_id(file_name="Used_identifiers.csv")
    # file = Path(os.path.dirname(os.path.abspath(__file__)),"Used_identifiers.csv")
    # record.download_file(file_id, file)
    # with open(file, "r") as f:
    #     string_of_tuples = f.read()
    
    # list_of_tuples = []
    # # Store string of tuples as list of tuples
    # list_of_strings = string_of_tuples.split('\n')
    # for string in list_of_strings:
    #     list_of_tuples.append(tuple(map(str, string.split('\t'))))
    
    search_results = (Search(KadiManager(instance)).search_resources(  item='record',
                                        visibility='private',
                                        collection=1141,
                                        child_collections=True,
                                        per_page=100))
    pages = search_results.json()['_pagination'].get('total_pages')

    item_tuples = []
    for page in range(1, pages+1):
        var = Search(KadiManager(instance)).search_resources(  item='record',
                                visibility='private',
                                collection=1141,
                                child_collections=True,
                                per_page=100,
                                page=page).json().get('items')
        item_tuples += [(x['title'], x['id'], x['identifier'][-11:-6]) for x in var]
        
    item_tuples = sorted(item_tuples, key=lambda x: x[2])

    ## Search for next higher free idenifier
    list_of_identifiers = [x[2] for x in item_tuples[1:-1]]
    unused = False
    identifier = "aaaaa"
    while unused is False:
        if identifier in list_of_identifiers:
            alphabet = ["a", "b", "c", "d", "e", "f", "g", "h",
                    "i", "j", "k", "l", "m", "n", "o", "p",
                    "q", "r", "s", "t", "u", "v", "w", "x",
                    "y", "z"]
            if identifier[1:5] == "zzzz":
                identifier = alphabet[alphabet.index(identifier[0])+1] + "aaaa"
            elif identifier[2:5] == "zzz":
                identifier = identifier[:1] + alphabet[alphabet.index(identifier[1])+1] + "aaa"
            elif identifier[3:5] == "zz":
                identifier = identifier[:2] + alphabet[alphabet.index(identifier[2])+1] + "aa"
            elif identifier[4] == "z":
                identifier = identifier[:3] + alphabet[alphabet.index(identifier[3])+1] + "a"
            else:
                identifier = identifier[:4] + alphabet[alphabet.index(identifier[4])+1]
        else:
            unused = True
            
    id_t_local = get_vocpopuli_id(top_level_term,Gitlab_PAT,project_id)
    kadi_identifier = id_t_local + '-' + identifier + '-kitmt'
    
    # Update used identifiers list
    title_id_identifier_tuples_kadi(instance,'record')
    
    return kadi_identifier

def unused_identifiers_kadi(instance: str):
    manager = KadiManager(instance)
    record = manager.record(id=18224)
    file_id = record.get_file_id(file_name="Used_identifiers.csv")
    file = Path(os.path.dirname(os.path.abspath(__file__)),"Used_identifiers.csv")
    record.download_file(file_id, file)
    with open(file, "r") as f:
        string_of_tuples = f.read()
    
    list_of_tuples = []
    # Store string of tuples as list of tuples
    list_of_strings = string_of_tuples.split('\n')
    for string_ in list_of_strings:
        list_of_tuples.append(tuple(map(str, string_.split('\t'))))

    ## Search for next higher free idenifier
    list_of_identifiers = [x[2] for x in list_of_tuples[1:-1]]
    used_identifiers = set(list_of_identifiers)

    all_identifiers = set(''.join(identifier) for identifier in itertools.product(string.ascii_uppercase, repeat=5))
    available_identifiers = all_identifiers - used_identifiers
    available_identifiers = sorted(available_identifiers)
    available_identifiers_string = '\n'.join(available_identifiers)
    record.upload_string_to_file(available_identifiers_string,"Unused_identifiers.csv",force=True)

def is_valid_identifier_kadi(identifier_to_test):
    """Checks identifier validation.

    Args:
        identifier_to_test (str): Identifier that should be validated.

    Returns:
        bool: Validation of identifier.
    """
    regex_pattern = "[a-z0-9]{32}-vp-[a-z0-9]{5}-kitmt"  
    prog = re.compile(regex_pattern)
    if prog.match(identifier_to_test):
        return True
    else:
        return False

def Kadi_invalid_identifiers(instance, collection=None, collection_id=None):
    """Returns list of invalid identifiers tuples in Kadi4Mat.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        collection (_type_, optional): Title of colleciton to search in. Defaults to None.
        collection_id (_type_, optional): ID of colleciton to search in. Defaults to None.

    Returns:
        List: List of tuples with titles, invalid identifiers and ids.
    """

    if collection != None:
        collection_id = search_item_id_kadi(instance, collection, 'collection')

    search_results = (Search(KadiManager(instance)).search_resources(item='record',collection=collection_id,child_collections=True,visibility="private",per_page =100))
    total_items = search_results.json()['_pagination'].get('total_items')
    per_page = search_results.json()['_pagination'].get('per_page')
    
    tuples = []
    for n in range(math.ceil(total_items / per_page)):
        var = Search(KadiManager(instance)).search_resources(item='record',collection=collection_id,per_page =100,child_collections=True,visibility="private", page=n+1).json().get('items')
        identifier_id_tuple = [(x['title'], x['identifier'], x['id']) for x in var if not is_valid_identifier_kadi(x['identifier'])]
        tuples.append(identifier_id_tuple)

    list_of_tuples = list(itertools.chain.from_iterable(tuples))
    return list_of_tuples

def Kadi_replace_invalid_identifier(instance: str, Gitlab_PAT: str, collection: Union[int, str] = 1141):
    """Replaces all invalid identifiers in collection

    Args:
        instance (str):  The name of the instance to use in combination with a config file.
        Gitlab_PAT (str): Access token for Gitlab.
        collection (Union[int, str], optional): Title or ID of collection to search in. Defaults to 1141.
    """

    if type(collection) == str:
        collection = search_item_id_kadi(instance, collection, 'collection')
        
    identifier_id_tuples = Kadi_invalid_identifiers('Malte Flachmann', collection_id=collection)
    
    for title, identifier, id in identifier_id_tuples:
        manager = KadiManager(instance)
        
        top_level_term = []
        if 'Tribological Experiment' in title:
            top_level_term = 'Tribological Experiment'
        elif 'Data Processing' in title:
            top_level_term = 'Data Processing'
        elif 'Data Publication' in title:
            top_level_term = "Data Publication"
            pass
        elif 'Preprocessing' in title:
            top_level_term = 'Data Processing'
        elif 'Comparison' in title:
            top_level_term = 'Data Processing'
        elif 'Gwyddion' in title:
            top_level_term = 'Data Processing'
        elif 'Block Specimen' in title:
            top_level_term = 'Block Specimen'
        elif 'Thesis' in title or "Poster" in title:
            top_level_term = 'Publication'
        elif 'Band Saw' in title:
            top_level_term = 'Band Saw'
        elif 'Wire Saw' in title:
            top_level_term = 'Wire Saw'
        elif 'Furnace' in title:
            top_level_term = 'Furnace'
        elif 'Heat Treatment' in title:
            top_level_term = 'Heat Treatment'
        elif 'Electrolyte' in title:
            top_level_term = 'Electrolyte'
        elif 'Optical Surface Profilometer' in title:
            top_level_term = 'Optical Surface Profilometer'
        elif 'MATLAB' in title:
            top_level_term = 'Software'
        elif 'Scanning Electron Microscope' in title:
            top_level_term = 'Scanning Electron Microscope'
        elif 'Light Microscopy' in title:
            top_level_term = 'Light Microscopy'
        elif 'Light Microscope' in title:
            top_level_term = 'Light Microscope'
        elif 'Electron Microscopy' in title:
            top_level_term = 'Electron Microscopy'
        elif 'Optical Surface Profilometry' in title:
            top_level_term = 'Optical Surface Profilometry'
        elif 'Tactile Surface Profilometry' in title:
            top_level_term = 'Tactile Surface Profilometry'
        elif 'Optical Surface Profilometer' in title:
            top_level_term = 'Optical Surface Profilometer'
        elif 'Tactile Surface Profilometer' in title:
            top_level_term = 'Tactile Surface Profilometer'
        elif 'Specimen Cleaning' in title:
            top_level_term = 'Specimen Cleaning'
        elif 'Hardness Measurement' in title:
            top_level_term = 'Hardness Measurement'
        elif 'Demagnitization' in title:
            top_level_term = 'Demagnitization'
        elif 'Commercial Machining' in title:
            top_level_term = 'Commercial Machining'
        elif 'Electrolyte' in title:
            top_level_term = 'Electrolyte'
        elif 'Lubricant for Polishing' in title:
            top_level_term = 'Lubricant for Polishing'
        elif 'Polishing Medium' in title:
            top_level_term = 'Polishing Medium'
        elif 'Grinding Machine' in title:
            top_level_term = 'Grinding Machine'
        elif 'Electropolishing Machine' in title:
            top_level_term = 'Electropolishing Machine'
        elif 'Polishing Machine' in title:
            top_level_term = 'Polishing Machine'
        elif 'Ultrasonic Cleaner' in title:
            top_level_term = 'Ultrasonic Cleaner'
        elif 'Tribometer' in title:
            top_level_term = 'Tribometer'
        elif 'Demagnitizing Plate' in title:
            top_level_term = 'Demagnitizing Plate'
        elif 'Cup Grinding Machine' in title:
            top_level_term = 'Cup Grinding Machine'
        elif 'Metal Sawing' or 'Band Sawing' or 'Wire Sawing' in title:
            top_level_term = 'Metal Sawing'
        elif 'Electropolishing' in title:
            top_level_term = 'Electropolishing'
        elif 'Polishing' in title:
            top_level_term = 'Polishing'
        elif 'Cup Grinding' in title:
            top_level_term = 'Cup Grinding'
        elif 'Grinding' in title:
            top_level_term = 'Grinding'

        if top_level_term != []:
            print(title, top_level_term)

            identifier = new_identifier_kadi(instance,top_level_term,Gitlab_PAT)
            print(identifier)
            print(manager.record(id = id).edit(identifier = identifier))
        