from kadi_apy import KadiManager
from datetime import datetime
import os
from genericpath import isdir, isfile
import shutil
from FAIRSave.kadi_search import search_item_id_kadi
import time
from typing import Optional, Union, Dict
from FAIRSave.kadi_instances import read_operator_config
from FAIRSave.kadi_identifier import new_identifier_kadi


def Record_Create(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Record_Create" will be renamed to '
                  '"create_record_kadi" in a future release!',
                  DeprecationWarning)
    return create_record_kadi(*args, **kwargs)


def create_record_kadi(instance: str,
                       record_name: str,
                       top_level_term: str,
                       Gitlab_PAT: str,
                       project_id: Optional[int] = 41732562):

    """Create a record in Kadi4Mat.

    Args:
        instance: The name of the instance to use in combination with a config file.
        record_name: Name of the record.
        top_level_term: Top Level term of the vocabulary.
        GITLAB_PAT: Personal access token to Gitlab.

    Returns:
    tuple: Tuple of id and identifier of newly crated record.
    """

    # Access Manager with Configuration Instance
    manager = KadiManager(instance=instance)

    # Create identifier from local_id and unique identifier for external applications
    identifier = new_identifier_kadi(instance,top_level_term,Gitlab_PAT,project_id)

    # This creates a new record if none with the given identifier exists yet.
    # If one exists, but we cannot access it, an exception will be raised.
    record = manager.record(identifier=identifier, title=record_name, create=True)
    return (record.id, identifier)

def Record_Add_Links_and_Edit(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Record_Add_Links_and_Edit" will be renamed to '
                  '"record_add_links_and_edit_kadi" in a future release!',
                  DeprecationWarning)
    return record_add_links_and_edit_kadi(*args, **kwargs)


def record_add_links_and_edit_kadi(instance: str,
                                   link_to: Union[int, str],
                                   link_name: str,
                                   record_type: Optional[str] = None,
                                   record: Optional[str] = None,
                                   record_id: Optional[int] = None,
                                   description: Optional[str] = None):
    """Add links to a record and edit the metadata of the record.

    Args:
        instance: The name of the instance to use in combination with a config file.
        link_to (any): Name of the raw data record which the new record should be linked to.
        link_name: Name of the link.
        record: Name of the record. Defaults to None.
        record_id: ID of the record to edit. Defaults to None.
    """

    manager = KadiManager(instance=instance)
    # Get record ID if only name is given
    if record is not None:
        record_id = search_item_id_kadi(instance=instance,
                                        title=record,
                                        item='record')
    record = manager.record(id=record_id)

    # Get record ID from record to be linked
    if type(link_to) == 'int':
        linked_record_id = link_to
    else:
        linked_record_id = search_item_id_kadi(instance=instance,
                                               title=link_to,
                                               item='record')
    rd_record = manager.record(id=linked_record_id)

    # Add record link to other record
    record.link_record(linked_record_id, link_name)
    # Add the type of record
    record.edit(type=record_type)
    record.edit(visibilty=rd_record.meta.get('visibility'))
    record.edit(license="CC-BY-4.0")
    record.edit(description=description)

    # Add permissions to record
    for x in rd_record.get_groups().json().get('items'):
        group_id = x.get('group').get('id')
        group_role = x.get('role').get('name')
        record.add_group_role(group_id=group_id, role_name=group_role)


def record_link_collection_kadi(instance: str,
                                record: Union[int, str],
                                collection: Union[int, str]):
    """Add a record to a collection.

    Args:
        instance (str): The name of the instance o use in combination with a config file.
        record (Union[int, str]): Name or ID of the record that should be linked to a collection.
        collection (Union[int, str]): Name or ID of the collection the record should be linked to.
    """
    manager = KadiManager(instance=instance)
    
    if type(record) == 'int':
        record_id = record
    else:
        record_id = search_item_id_kadi(instance=instance,
                                        title=record,
                                        item='record')
    
    if type(collection) == 'int':
        collection_id = collection
    else:
        collection_id = search_item_id_kadi(instance=instance,
                                        title=collection,
                                        item='collection')
    collection = manager.collection(id=collection_id)
    
    collection.add_record_link(record_id=record_id)

def Record_Add_Tags(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Record_Add_Tags" will be renamed to '
                  '"record_add_tags_kadi" in a future release!',
                  DeprecationWarning)
    return record_add_tags_kadi(*args, **kwargs)


def record_add_tags_kadi(instance: str, tags: str,
                         record: Optional[str] = None,
                         record_id: Optional[int] = None):
    """Add tags to a record.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        tags (str): Comma-separated tags to add to a record.
        record(str, optional): Name of the record. Defaults to None.
        record_id (int, optional): ID of the record to edit. Defaults to None.
    """

    manager = KadiManager(instance=instance)
    if record is not None:
        record_id = search_item_id_kadi(instance=instance,
                                        title=record,
                                        item='record')
    record = manager.record(id=record_id)

    # Add tags to record
    tags = tags.replace(' ', '').split(",")
    for tag in tags:
        record.add_tag(tag)


def Record_Add_Metadata(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Record_Add_Metadata" will be renamed to '
                  '"record_add_metadata_kadi" in a future release!',
                  DeprecationWarning)
    return record_add_metadata_kadi(*args, **kwargs)


def record_add_metadata_kadi(instance: str,
                             operator: str,
                             record: Optional[str] = None,
                             record_id: Optional[int] = None,
                             sofware_info: Optional[Dict] = None):
    """Add metadata to a record.

    Args:
        instance: The name of the instance to use in combination with a config file.
        record: Name of the record. Defaults to None.
        record_id (int, optional): ID of the record to edit. Defaults to None.
    """
    manager = KadiManager(instance=instance)
    if record is not None:
        record_id = search_item_id_kadi(instance=instance,
                                        title=record,
                                        item='record')
    record = manager.record(id=record_id)

    # Read the operator config
    (first_name, last_name, institution_name, 
     institute, user_role, user_token, building,
     floor, room_number, institution_location,
     tags, description) = read_operator_config(instance=operator)

    # Time: dalight saings time
    if time.daylight == 1:
        time_plus = 0
    else:
        time_plus = 1
    time_zone = 1
    time_shift = time_zone + time_plus
    time_shift = '+0' + str(time_shift) + ':00'

    # Add metadata to the record
    list_of_dict = [{'key': 'General Info (Process)', 'type': 'dict', 'value': [
                        {'key': 'Location Information', 'type': 'dict', 'value': [
                            {'key': 'Building', 'type': 'str', 'value': building.replace("Â", "")},
                            {'key': 'Floor', 'type': 'int', 'value': floor},
                            {'key': 'Room Number', 'type': 'str', 'value': room_number},
                            {'key': 'Institution (Location)', 'type': 'str', 'value': institution_location}
                            ]},
                        {'key': 'Operator(s) in Charge', 'type': 'dict', 'value': [
                            {"key": "Last Name", "type": "str", "value": last_name},
                            {"key": "First Name", "type": "str", "value": first_name},
                            {'key': 'Institution Name', 'type': 'str', 'value': institution_name},
                            {'key': 'Institute', 'type': 'str', 'value': institute},
                            {'key': 'User Role', 'type': 'str', 'value': user_role},
                            {'key': 'User Token', 'type': 'str', 'value': user_token}]},
                        {'key': 'Timestamp', 'type': 'date', 'value': str(datetime.now()).replace(' ', 'T') + time_shift}
                        ]}
                    ]
    if sofware_info:
        list_of_dict.append(sofware_info)
    else:
        list_of_dict.append({'key': 'Array of Software Used', 'type': 'list', 'value': [
            {'type': 'dict', 'value': [
                {'key': 'Software Name', 'type': 'str', 'value': 'MATLAB'},
                {'key': 'Software Version', 'type': 'str', 'value': 'R2022b'}
                ]}
            ]})
    record.add_metadata(list_of_dict, force=False)


def Record_Add_Files(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Record_Add_Files" will be renamed to '
                  '"record_add_files_kadi" in a future release!',
                  DeprecationWarning)
    return record_add_files_kadi(*args, **kwargs)


def record_add_files_kadi(instance: str,
                          files_path: str,
                          file_purpose: str,
                          record: Optional[str] = None,
                          record_id: Optional[int] = None,
                          file_list=None):
    """Add Files to a record and add the metadata of the files to record extras.

    Args:
        instance: The name of the instance to use in combination with a config file.
        files_path: Path where the files to upload are stored.
        files_purpose: Purpose of the files that are uploaded.
        record: Name of the record. Defaults to None.
        record_id: ID of the record to edit. Defaults to None.
        file_list
    """
    manager = KadiManager(instance=instance)
    if record is not None:
        record_id = search_item_id_kadi(instance=instance,
                                        title=record,
                                        item='record')
    record = manager.record(id=record_id)

    if file_list is not None and file_list == str:
        file_list = file_list.replace(' ', '').split(",")
    elif file_list is None:
        file_list = os.listdir(files_path)

    if files_path is not None:
        # Add metadata from files
        for file in file_list:
            file_id = []
            if isfile(files_path + '\\' + file):
                record.upload_file(files_path + '\\' + file, force=True)
                file_id = record.get_file_id(file)
                file_info = record.get_file_info(file_id).json()
                file_size = file_info.get('size')
                file_name = file_info.get('name')
                file_MD = {"type": "dict","value":[
                                {"key": "File Name", "type": "str", "value": file_name},
                                {"key": "File Persistent ID", "type": "str", "value": file_id},
                                {"key": "File Size", "type": "float", "unit": "kB", "value": file_size},
                                {"key": "File(s) Purpose", "type": "str", "value": file_purpose}]}
            elif isdir(files_path + '\\' + file):
                zip_file = shutil.make_archive(files_path + '/' + file,
                                               'zip',
                                               files_path + '/' + file,
                                               files_path)
                record.upload_file(zip_file, force=True)
                file_id = record.get_file_id(file + '.zip')
                file_info = record.get_file_info(file_id).json()
                file_size = file_info.get('size')
                file_name = file_info.get('name')
                file_MD = {"type": "dict","value":[
                                {"key": "File Name", "type": "str", "value": file_name},
                                {"key": "File Persistent ID", "type": "str", "value": file_id},
                                {"key": "File Size", "type": "float", "unit": "kB", "value": file_size},
                                {"key": "File(s) Purpose", "type": "str", "value": file_purpose}]}

            record_MD = record.meta.get('extras')
            if record_MD[-1].get('key') == "Array Produced File Metadata":
                # record.remove_metadatum("Array Produced File Metadata")
                file_MD_array = record_MD[-1]
                file_MD_array['value'].append(file_MD)
            else:
                file_metadata = {"key": "Array Produced File Metadata", "type": "list", "value": []}
                file_metadata['value'].append(file_MD)
                file_MD_array = file_metadata
            record.add_metadata(file_MD_array, force=True)
