from kadi_apy import KadiManager
from FAIRSave.kadi_search import *
import os
from pathlib import Path
import itertools
import string


def get_title_id_identifier_tuples_kadi(instance: str,
                                        item: str,
                                        collection_id: Optional[int] = None,
                                        collection: Optional[str] = None,
                                        child_collections: Optional[bool] = True,
                                        visibility: Optional[str] = 'private'):
    
    if collection is not None:
        collection_id = search_item_id_kadi(instance,
                                            title=collection,
                                            item='collection')
        
    sr = KadiManager(instance).search_resource()
    search_results = (sr.search_items(  item=item,
                                        visibility=visibility,
                                        collection=collection_id,
                                        child_collections=child_collections,
                                        per_page=100))
    pages = search_results.json()['_pagination'].get('total_pages')

    item_tuples = []
    for page in range(1, pages+1):
        var = sr.search_items(  item=item,
                                visibility=visibility,
                                collection=collection_id,
                                child_collections=child_collections,
                                per_page=100,
                                page=page).json().get('items')
        if item == "record":
            item_tuples += [(x['title'], x['id'], x['identifier'][-11:-6]) for x in var]
        elif item == "collection":
            item_tuples += [(x['title'], x['id'], x['identifier']) for x in var]
        
    item_tuples = sorted(item_tuples, key=lambda x: x[2])
    
    item_tuples_string = ''.join(['\t'.join(str(s) for s in item) + '\n' for item in item_tuples])
    
    manager = KadiManager(instance)
    record = manager.record(id=18224)
    record.upload_string_to_file(item_tuples_string,"Used_identifiers.csv",force=True)

def new_identifier_kadi(instance: str):
    
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
    for string in list_of_strings:
        list_of_tuples.append(tuple(map(str, string.split('\t'))))

    ## Search for next higher free idenifier
    list_of_identifiers = [x[2] for x in list_of_tuples[1:-1]]
    used = True
    identifier = "aaaaa"
    while used is True:
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
            used = False
    
    return identifier

# print(new_identifier_kadi('Malte Flachmann'))

# item_tuples = get_title_id_identifier_tuples_kadi("Malte Flachmann", "record",1141)


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
    
# unused_identifiers_kadi("Malte Flachmann")
