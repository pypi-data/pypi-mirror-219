# from shutil import move
from os import remove
from os.path import join
import json
import traceback
import numpy as np
from datetime import datetime
from tqdm import tqdm

import maxia_pipedrive.data_handler
import maxia_pipedrive.models
import maxia_pipedrive.api_handler.fields
import maxia_pipedrive.api_handler.utils
import maxia_pipedrive.consts

# GET functions


def get_organization(org_id):
    return maxia_pipedrive.api_handler.utils.get_request(f'{maxia_pipedrive.consts.Endpoints.organizations}/{org_id}')


def get_all_organizations(**query_params_dict):
    print('Loading all organizations...')
    return maxia_pipedrive.api_handler.utils.get_all_request(
        maxia_pipedrive.consts.Endpoints.organizations,
        **query_params_dict
    )


# PUT (update) Functions


def update_organization(org_id, update_dict: dict, org_data_current=None, save=True):
    # Fetch organization current data on variables
    if org_data_current is None:
        org_data_current = get_organization(org_id)
    update_dict = maxia_pipedrive.models.Organization.validate_fields(update_dict.copy())
    org_data_current = maxia_pipedrive.models.Organization.validate_fields(
        org_data_current.copy())
    # Validate update_dict (change each label to the id)
    keys = list(update_dict.keys())
    for field_key in keys:
        if str(update_dict[field_key]) == str(org_data_current[field_key]):
            # no update, remove it for better performance
            del update_dict[field_key]
    # Check if update is required
    if len(update_dict) == 0:
        return {}

    # Mandatory field (name)
    name_api_code = maxia_pipedrive.models.Organization.get_api_code(
        maxia_pipedrive.models.Organization.name)
    update_dict[name_api_code] = update_dict.get(
        name_api_code, org_data_current[name_api_code])
    migration_output = maxia_pipedrive.api_handler.utils.update_request_v2(
        maxia_pipedrive.consts.Endpoints.update_organizations % (org_id),
        maxia_pipedrive.consts.MigrationKind.organization,
        update_dict,
        obj_current_data=org_data_current,
        delete_reversion=False,
        save=save
    )
    return migration_output


def update_multiple_organizations(list_org_id, list_update_dict, all_org_data=None, step_size=500, save=True):
    # get current data on all organizations to be updated
    if all_org_data is None:
        all_org_data = get_all_organizations()
    org_id_org_dict = {
        org_dict['id']: org_dict
        for org_dict in all_org_data
    }
    n_steps = int(np.ceil(len(list_update_dict) / step_size))
    list_migration_fpath = []
    for stp in range(n_steps):
        timestp = datetime.now().strftime(maxia_pipedrive.consts.Consts.date_format)
        migration_fpath = join(
            maxia_pipedrive.consts.Consts.migrations_dir,
            f'update_multiorgid_{timestp}_{stp+1}-{n_steps}.json')
        list_migration_fpath.append(migration_fpath)
        print(
            f'[{stp+1}/{n_steps}] Starting updates... Saving migration file on: {migration_fpath}')
        list_migration_dict = []
        try:
            for org_id, update_dict in tqdm(zip(list_org_id[stp * step_size:(stp + 1) * step_size],
                                                list_update_dict[stp * step_size:(stp + 1) * step_size]),
                                            total=len(list_org_id[stp * step_size:(stp + 1) * step_size])):
                migration_dict = update_organization(
                    int(org_id),  # must be int
                    update_dict,
                    save=False,
                    org_data_current=org_id_org_dict[org_id])
                if len(migration_dict) > 0:
                    list_migration_dict.append(migration_dict)
                    # save current version of migration file
                    with open(migration_fpath, 'w', encoding='utf-8') as f:
                        json.dump(list_migration_dict, f, indent=1)
        except Exception as _:
            print(traceback.print_exc())
            if len(list_migration_dict) > 0:
                print('Got exception while updating... Reverting migration')
                maxia_pipedrive.api_handler.utils.revert_migrations_from_path(
                    migration_fpath)
                list_migration_fpath.remove(migration_fpath)
                return list_migration_fpath

        # Save massive step migration

        print(
            f'Migration step done! Saving step migration file: {migration_fpath}')
        with open(migration_fpath, 'w', encoding='utf-8') as f:
            json.dump(list_migration_dict, f, indent=1)

    # At the end of the loop, with no exception found, we proceed by merging all files into a single file
    all_migration_fpath = join(
        maxia_pipedrive.consts.Consts.migrations_dir,
        f'update_multiorgid_{timestp}.json')
    print(
        f'Saving all migrations into a single file: {all_migration_fpath} ...')
    merged_migration_list_dict = []
    for migration_fpath in list_migration_fpath:
        with open(migration_fpath, 'r', encoding='utf-8') as f:
            merged_migration_list_dict += json.load(f)
        remove(migration_fpath)
    # Save into a single file:
    with open(
        all_migration_fpath,
        'w',
            encoding='utf-8') as f:
        json.dump(merged_migration_list_dict, f, indent=1)

    return all_migration_fpath


# POST (create) Functions


def create_organization(org_dict, save=True):

    # Before creating organization, one must check if it does not already exists... (based on INEP number)
    inep_id_dict = maxia_pipedrive.data_handler.load_relation('orgid_inep')
    inep_api_code = maxia_pipedrive.models.Organization.get_api_code_dict()[maxia_pipedrive.models.Organization.inep_number]

    if org_dict[inep_api_code] not in inep_id_dict.keys(): # must be a new organization
        return maxia_pipedrive.api_handler.utils.create_object(
            maxia_pipedrive.models.Organization,
            maxia_pipedrive.consts.Endpoints.organizations,
            maxia_pipedrive.consts.MigrationKind.organization,
            org_dict,
            save=save
        )
    return {}
    # return create_multiple_organizations([org_dict], save=save)


def create_multiple_organizations(list_org_dict, step_size=500, save=True):
    create_obj_func = create_organization
    obj_migration_kind = maxia_pipedrive.consts.MigrationKind.organization

    return maxia_pipedrive.api_handler.utils.create_multiple_objects(
        create_obj_func, obj_migration_kind,
        list_org_dict,
        step_size=step_size,
        save=save)
    # # First, check if the list of organizations does not exist (based on INEP NUMBER)
    # inep_id_dict = maxia_pipedrive_src.data_handler.load_relation('orgid_inep')

    # # Filter only new organizations
    # inep_api_code = maxia_pipedrive_src.models.Organization.get_api_code_dict()[maxia_pipedrive_src.models.Organization.inep_number]

    # # Validate the org fields
    # list_org_dict = [maxia_pipedrive_src.models.Organization.validate_fields(
    #     org_dict.copy()) for org_dict in list_org_dict]

    # validated_list_org_dict = [
    #     el for el in list_org_dict if el[inep_api_code] not in inep_id_dict.keys()]
    # # Add default owner if
    # for el in validated_list_org_dict:
    #     owner_id_code = maxia_pipedrive_src.models.Organization.get_api_code_dict()[maxia_pipedrive_src.models.Organization.owner_id]
    #     el[owner_id_code] = el.get(owner_id_code, 12127564)

    # if len(list_org_dict) != len(validated_list_org_dict):
    #     print(
    #         f'{len(list_org_dict)-len(validated_list_org_dict)} organization already exist. Skipping...')
    # return maxia_pipedrive_src.api_handler.utils.multiple_post_request(
    #     maxia_pipedrive_src.consts.Endpoints.organizations,
    #     validated_list_org_dict,
    #     maxia_pipedrive_src.consts.MigrationKind.multiple_orgs,
    #     save=save)
