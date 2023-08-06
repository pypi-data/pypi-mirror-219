from datetime import datetime
import json
import os
from os.path import join
from shutil import move
import traceback
import numpy as np
import requests
from tqdm import tqdm
from typing import Callable
import maxia_pipedrive.consts


API_TOKEN = {
    'api_token': os.environ.get('PIPEDRIVE_API_TOKEN')
}

API_URL = 'https://maxia.pipedrive.com/api/v1/'

# UTILITARY FUNCTIONS


def get_query_params(query_params_dict):
    return '&'.join([f'{k}={v}' for k, v in query_params_dict.items()])


def save_migration(method_, migration_kind, migration_dict, obj_id=None):
    timestp = datetime.now().strftime(maxia_pipedrive.consts.Consts.date_format)
    if obj_id is not None:
        filename = f'{method_}_{migration_kind}_{obj_id}_{timestp}.json'
    else:
        filename = f'{method_}_{migration_kind}_{timestp}.json'
    migration_fpath = join(
        maxia_pipedrive.consts.Consts.migrations_dir, filename)
    print(f'Updated! Saving migration file: {migration_fpath}')
    with open(migration_fpath, 'w', encoding='utf-8') as f:
        json.dump(migration_dict, f, indent=1)
    return migration_fpath


def prepare_batch_multiple_post(list_json_data, step_size=100):
    n_steps = int(np.ceil(len(list_json_data)/step_size))
    # list_migration_fpath = []
    return [
        list_json_data[step * step_size:(step + 1) * step_size]
        for step in range(n_steps)
    ]


def revert_migrations(migrations: list):
    any_failed = False
    list_reverse_migration = []
    for migration_dict in migrations[::-1]:
        endpoint = migration_dict['endpoint']
        migration_kind = migration_dict.get('kind')
        method = migration_dict['method']
        migration_details = migration_dict['details']
        if method == 'put':
            obj_ids = migration_dict['id']
            obj_current = {
                k: tv[1]
                for k, tv in migration_details.items()
            }
            reverse_update_dict = {
                k: tv[0]
                for k, tv in migration_details.items()
            }

            # Revert migration
            rev_mig = update_request(
                endpoint, obj_ids, migration_kind, reverse_update_dict,
                obj_current_data=obj_current
            )
            if len(rev_mig) > 0:
                list_reverse_migration.append(
                    rev_mig
                )
            else:
                any_failed = True
        elif method == 'post':
            # The reverse of POST is DELETE
            rev_mig = delete_request(
                endpoint, [migration_details['id']], migration_kind)
            if len(rev_mig) > 0:
                list_reverse_migration.append(
                    rev_mig
                )
            else:
                any_failed = True
        elif method == 'delete':
            obj_ids = migration_details['id']
            if not isinstance(obj_ids, list):
                obj_ids = [obj_ids]
            if 'organization' in endpoint or 'person' in endpoint:
                reverse_update_dict = {
                    'active_flag': True
                }
            elif 'deal' in endpoint:
                reverse_update_dict = {
                    'status': 'open'
                }
            else:
                raise NotImplementedError(
                    f'Delete reversion for {endpoint} not implemented yet.')

            for obj_id in obj_ids:
                rev_mig = update_request(
                    endpoint, obj_id, migration_kind, reverse_update_dict,
                    obj_current_data=None,
                    delete_reversion=True
                )
                if len(rev_mig) > 0:
                    list_reverse_migration.append(
                        rev_mig
                    )
                else:
                    any_failed = True
    if any_failed:
        print('Failed to undo some migrations!')
    return list_reverse_migration, any_failed


def revert_migrations_from_path(migration_fpath, save=False):
    with open(migration_fpath, 'r', encoding='utf-8') as f:
        migrations = json.load(f)
        if isinstance(migrations, dict):
            migrations = [migrations]

    list_reverse_migration, any_error = revert_migrations(migrations)
    if any_error:
        print('Check the moved file for more details about the error!')
    filename = migration_fpath.split('/')[1]
    moved_migration_fpath = join(
        maxia_pipedrive.consts.Consts.reversed_migrations,
        filename
    )
    print(
        f'Moving reversed migration file from {migration_fpath} to {moved_migration_fpath}')
    move(
        migration_fpath,
        moved_migration_fpath
    )
    if save:
        # output_fpath = ".".join(moved_migration_fpath.split('.')[:-1]) + "_reversion.json"
        output_fpath = join(
            maxia_pipedrive.consts.Consts.reversed_migrations, "reversion_"+filename)
        print(f'Reversed! Saving reversion file: {output_fpath}')
        with open(output_fpath, 'w', encoding='utf-8') as f:
            json.dump(list_reverse_migration, f, indent=1)
        return output_fpath
    return list_reverse_migration

# SINGLE


def get_request(endpoint):
    req = requests.get(join(API_URL, endpoint), params=API_TOKEN)
    if req.status_code == 200 and req.json()['success']:
        return req.json()['data']
    else:
        print(join(API_URL, endpoint), req.status_code)
        return []


def post_request(endpoint, json_data, migration_kind, save=False):
    migration_dict = {
        'endpoint': endpoint,
        'method': 'post',
        'kind': migration_kind,
        'details': json_data
    }
    req = requests.post(
        join(API_URL, endpoint),
        params=API_TOKEN,
        json=json_data
    )
    if not (200 <= req.status_code < 300):
        print(f'Request failed! status={req.status_code}')
        print(req.content)
        print('input:', migration_dict)
        return {}
    req = req.json()

    if req['success'] is True:
        obj_id = req['data']['id']
        json_data['id'] = obj_id
        if save:
            return save_migration(maxia_pipedrive.consts.MigrationMethods.create, migration_kind, migration_dict, obj_id=obj_id)
        return migration_dict
    return {}


def update_request(endpoint, obj_id, migration_kind, validated_update_dict, obj_current_data=None, delete_reversion=False):
    # Fetch organization current data on variables
    if obj_current_data is None and delete_reversion is False:
        obj_current_data = get_request(
            join(endpoint, str(obj_id)))  # get_organization(org_id)
    if delete_reversion is False:
        migration_dict = {
            k: (v1, validated_update_dict.get(k, v1))
            for k, v1 in obj_current_data.items() if k in validated_update_dict
        }
        # Apply changes
        migration_dict = {
            'endpoint': endpoint,
            'method': 'put',
            'kind': migration_kind,
            'id': obj_id,
            'details': migration_dict
        }
    else:
        migration_dict = {
            'endpoint': endpoint,
            'method': 'put',
            'kind': migration_kind,
            'id': obj_id,
            'details': validated_update_dict
        }
    req = requests.put(
        join(API_URL, endpoint, str(obj_id)),
        params=API_TOKEN,
        json=validated_update_dict
    )
    if req.status_code != 200:
        print('Request failed!')
        print(req.content)
        return {}
    req = req.json()
    if req['success'] is True:
        return migration_dict
    return {}


def update_request_v2(
        endpoint,
        migration_kind,
        validated_update_dict,
        obj_current_data=None,
        delete_reversion=False,
        save=False):

    if obj_current_data is None and delete_reversion is False:
        obj_current_data = get_request(endpoint)
    if delete_reversion is False:
        migration_dict = {
            k: (v1, validated_update_dict.get(k, v1))
            for k, v1 in obj_current_data.items() if k in validated_update_dict
        }
        # Apply changes
        migration_dict = {
            maxia_pipedrive.consts.Consts.endpoint: endpoint,
            maxia_pipedrive.consts.Consts.method: 'put',
            maxia_pipedrive.consts.Consts.migration_kind: migration_kind,
            maxia_pipedrive.consts.Consts.details: migration_dict
        }
    else:
        migration_dict = {
            maxia_pipedrive.consts.Consts.endpoint: endpoint,
            maxia_pipedrive.consts.Consts.method: 'put',
            maxia_pipedrive.consts.Consts.migration_kind: migration_kind,
            maxia_pipedrive.consts.Consts.details: validated_update_dict
        }
        print(migration_dict)
    req = requests.put(
        join(API_URL, endpoint),
        params=API_TOKEN,
        json=validated_update_dict
    )
    if req.status_code != 200:
        print('Request failed!')
        print(req.content)
        return {}
    req = req.json()
    if req['success'] is True:
        if save:
            return save_migration(maxia_pipedrive.consts.MigrationMethods.update, migration_kind, migration_dict, obj_id=None)
        return migration_dict
    return {}


def single_delete_request(endpoint):
    req = requests.delete(
        join(API_URL, endpoint),
        params=API_TOKEN
    )
    if not (200 <= req.status_code < 300):
        print(f'Request failed! status={req.status_code}')
        print(req.content)
        return {}
    req = req.json()

    if req['success'] is True:
        return {
            'method': 'delete',
            'endpoint': endpoint,
            'kind': 'single_delete',
            'details': req['data']
        }
    return {}

# MULTIPLE

# def multiple_update_request(list_endpoint, list_json_data, migration_kind)


def get_all_request(endpoint, verbose=False, **query_params_dict):
    query_params_str = get_query_params(query_params_dict)
    list_data = []
    next_start = 0
    while next_start is not None:
        req = requests.get(
            join(API_URL, endpoint +
                 f"?{query_params_str}&limit=5000&start={next_start}"),
            params=API_TOKEN
        )
        if req.status_code == 200:
            if req.json()['data'] is not None:
                list_data += req.json()['data']
            next_start = req.json()['additional_data']['pagination'].get(
                'next_start', None)
        else:
            next_start = None
            print(req.text)
        if verbose:
            print(f'\tFetched {len(list_data)} from {endpoint}...')
    return list_data


def multiple_post_request(endpoint, list_json_data, migration_kind, save=True):
    list_migration_dict = []
    try:
        for json_data in tqdm(list_json_data):
            # From json_data we must extract the composed_post_endpoint
            id_replace = ()
            if maxia_pipedrive.consts.Consts.id in json_data:
                id_replace = (json_data[maxia_pipedrive.consts.Consts.id],)
                del json_data[maxia_pipedrive.consts.Consts.id]
            migration_dict = post_request(
                endpoint % id_replace,
                json_data,
                migration_kind
            )
            if len(migration_dict) > 0:
                list_migration_dict.append(migration_dict)
    except Exception as _:
        print(traceback.print_exc())
        print('Got exception while updating... Reverting migration')
        return revert_migrations(list_migration_dict)
    if save:
        return save_migration(maxia_pipedrive.consts.MigrationMethods.create, migration_kind, list_migration_dict, obj_id=None)
    return list_migration_dict


def delete_request(endpoint, obj_ids: list, migration_kind):
    req = requests.delete(
        join(API_URL, endpoint) + '?ids=' + ','.join(str(el)
                                                     for el in obj_ids),
        params=API_TOKEN
    )
    if not (200 <= req.status_code < 300):
        print(f'Request failed! status={req.status_code}')
        print(req.content)
        return {}
    req = req.json()
    if req['success'] is True:
        migration_dict = {
            'method': 'delete',
            'endpoint': endpoint,
            'kind': migration_kind,
            'id': obj_ids,
            'details': req['data']
        }
        return migration_dict
    return {}


def composed_delete_request(composed_endpoint, migration_kind):
    req = requests.delete(
        join(API_URL, composed_endpoint),
        params=API_TOKEN
    )
    if not (200 <= req.status_code < 300):
        print(f'Request failed! status={req.status_code}')
        print(req.content)
        return {}
    req = req.json()
    if req['success'] is True:
        migration_dict = {
            'method': 'delete',
            'endpoint': composed_endpoint,
            'kind': migration_kind,
            'details': req['data']
        }
        return migration_dict
    return {}


# GENERIC OBJECT FUNCTIONS

def update_object(
        ObjClass: object, obj_endpoint: str, obj_migration_kind: str,
        obj_id: int, update_dict: dict, obj_current_data: dict = None,
        save: bool = True):
    # Validate update_dict
    update_obj_endpoint = obj_endpoint % obj_id
    if obj_current_data is None:
        obj_current_data = get_request(
            update_obj_endpoint)

    update_dict = ObjClass.validate_fields(update_dict.copy())
    obj_current_data = ObjClass.validate_fields(obj_current_data.copy())
    update_dict_keys = list(update_dict.keys())

    for field_key in update_dict_keys:
        if str(update_dict[field_key]) == str(obj_current_data[field_key]):
            # no update, remove it for better performance
            del update_dict[field_key]
    if len(update_dict) == 0:
        return {}

    return update_request_v2(
        update_obj_endpoint,
        obj_migration_kind,
        update_dict,
        obj_current_data=obj_current_data,
        save=save
    )


def update_multiple_object(
        update_obj_func: Callable, get_all_obj_func: Callable, obj_migration_kind,
        list_obj_id, list_update_dict, all_obj_data=None,
        step_size=500, save=True):
    # ObjClass = maxia_pipedrive_src.models.Person
    # obj_endpoint = maxia_pipedrive_src.consts.Endpoints.update_persons
    # obj_migration_kind = maxia_pipedrive_src.consts.MigrationKind.person

    # update_obj_func = update_person
    # get_all_obj_func = get_all_persons

    if all_obj_data is None:
        all_obj_data = get_all_obj_func()

    obj_id_obj_dict = {
        obj_dict['id']: obj_dict
        for obj_dict in all_obj_data
    }
    n_steps = int(np.ceil(len(list_update_dict) / step_size))
    list_migration_fpath = []
    for stp in range(n_steps):
        timestp = datetime.now().strftime(maxia_pipedrive.consts.Consts.date_format)
        migration_fpath = os.path.join(
            maxia_pipedrive.consts.Consts.migrations_dir,
            f'update_{obj_migration_kind}_{timestp}_{stp+1}-{n_steps}.json')
        list_migration_fpath.append(migration_fpath)
        print(
            f'[{stp+1}/{n_steps}] Starting updates... Saving migration file on: {migration_fpath}')
        list_migration_dict = []
        try:
            for obj_id, update_dict in tqdm(zip(list_obj_id[stp * step_size:(stp + 1) * step_size],
                                                list_update_dict[stp * step_size:(stp + 1) * step_size]),
                                            total=len(list_obj_id[stp * step_size:(stp + 1) * step_size])):
                migration_dict = update_obj_func(
                    int(obj_id),  # must be int
                    update_dict,
                    save=False,
                    obj_current_data=obj_id_obj_dict[obj_id])
                if len(migration_dict) > 0:
                    list_migration_dict.append(migration_dict)
                    # save current version of migration file
                    with open(migration_fpath, 'w', encoding='utf-8') as f:
                        json.dump(list_migration_dict, f, indent=1)
        except Exception as _:
            print(traceback.print_exc())
            if len(list_migration_dict) > 0:
                print('Got exception while updating... Reverting migration')
                revert_migrations_from_path(migration_fpath)
                list_migration_fpath.remove(migration_fpath)
                return list_migration_fpath

        # Save massive step migration

        print(
            f'Migration step done! Saving step migration file: {migration_fpath}')
        with open(migration_fpath, 'w', encoding='utf-8') as f:
            json.dump(list_migration_dict, f, indent=1)

    # At the end of the loop, with no exception found, we proceed by merging all files into a single file
    if save:
        all_migration_fpath = join(
            maxia_pipedrive.consts.Consts.migrations_dir,
            f'update_{obj_migration_kind}_{timestp}.json')
        print(
            f'Saving all migrations into a single file: {all_migration_fpath} ...')
    merged_migration_list_dict = []
    for migration_fpath in list_migration_fpath:
        with open(migration_fpath, 'r', encoding='utf-8') as f:
            merged_migration_list_dict += json.load(f)
        os.remove(migration_fpath)
    if save:
        # Save into a single file:
        with open(
            all_migration_fpath,
            'w',
                encoding='utf-8') as f:
            json.dump(merged_migration_list_dict, f, indent=1)

        return all_migration_fpath
    return merged_migration_list_dict


def create_object(
        ObjClass: object, obj_endpoint: str, obj_migration_kind: str,
        obj_creation_dict: dict, save: bool = True):

    # validate fields
    obj_creation_dict = ObjClass.validate_fields(obj_creation_dict.copy())

    # Create
    return post_request(
        obj_endpoint,
        obj_creation_dict,
        obj_migration_kind,
        save=save
    )


def create_multiple_objects(
        create_obj_func: Callable,
        obj_migration_kind,
        list_obj_dict,
        step_size=500, save=True):

    n_steps = int(np.ceil(len(list_obj_dict) / step_size))
    list_migration_fpath = []
    for stp in range(n_steps):
        timestp = datetime.now().strftime(maxia_pipedrive.consts.Consts.date_format)
        migration_fpath = os.path.join(
            maxia_pipedrive.consts.Consts.migrations_dir,
            f'create_{obj_migration_kind}_{timestp}_{stp+1}-{n_steps}.json')
        list_migration_fpath.append(migration_fpath)
        print(
            f'[{stp+1}/{n_steps}] Starting updates... Saving migration file on: {migration_fpath}')
        list_migration_dict = []
        try:
            for create_obj_dict in tqdm(list_obj_dict[stp * step_size:(stp + 1) * step_size],
                                        total=len(list_obj_dict[stp * step_size:(stp + 1) * step_size])):
                migration_dict = create_obj_func(
                    create_obj_dict,
                    save=False)
                if len(migration_dict) > 0:
                    list_migration_dict.append(migration_dict)
                    # save current version of migration file
                    with open(migration_fpath, 'w', encoding='utf-8') as f:
                        json.dump(list_migration_dict, f, indent=1)
        except Exception as _:
            print(traceback.print_exc())
            if len(list_migration_dict) > 0:
                print('Got exception while updating... Reverting migration')
                revert_migrations_from_path(migration_fpath)
                list_migration_fpath.remove(migration_fpath)
                return list_migration_fpath

        # Save massive step migration

        print(
            f'Migration step done! Saving step migration file: {migration_fpath}')
        with open(migration_fpath, 'w', encoding='utf-8') as f:
            json.dump(list_migration_dict, f, indent=1)

    # At the end of the loop, with no exception found, we proceed by merging all files into a single file
    if save:
        all_migration_fpath = join(
            maxia_pipedrive.consts.Consts.migrations_dir,
            f'create_{obj_migration_kind}_{timestp}.json')
        print(
            f'Saving all migrations into a single file: {all_migration_fpath} ...')
    merged_migration_list_dict = []
    for migration_fpath in list_migration_fpath:
        with open(migration_fpath, 'r', encoding='utf-8') as f:
            merged_migration_list_dict += json.load(f)
        os.remove(migration_fpath)
    if save:
        # Save into a single file:
        with open(
            all_migration_fpath,
            'w',
                encoding='utf-8') as f:
            json.dump(merged_migration_list_dict, f, indent=1)

        return all_migration_fpath
    return merged_migration_list_dict
