from datetime import datetime
import json
from os import remove
import traceback
import pandas as pd
from os.path import join
import numpy as np
from tqdm import tqdm

import maxia_pipedrive.data_handler
import maxia_pipedrive.models
import maxia_pipedrive.api_handler.fields
import maxia_pipedrive.api_handler.utils
import maxia_pipedrive.api_handler.persons
import maxia_pipedrive.api_handler.followers
import maxia_pipedrive.consts

# All persons from org
all_persons = maxia_pipedrive.api_handler.persons.get_all_persons()
for p in all_persons:
    if p['org_id'] is not None:
        p['owner_id'] = p['owner_id']['value']
        p['org_id'] = p['org_id']['value']
all_persons = pd.DataFrame(all_persons)  # [['id', 'org_id']]
org_people_dict = all_persons.groupby('org_id')['id'].apply(list).to_dict()


def get_all_deals(**query_params_dict):
    print('Get all deals...')
    return maxia_pipedrive.api_handler.utils.get_all_request(
        maxia_pipedrive.consts.Endpoints.deals,
        **query_params_dict
    )


def cascade_following(list_deal_id, save=True, list_output_files=[], all_deals_data=None):
    # Each deal id is associated to an organization and may have an sdr assigned
    if all_deals_data is None:
        all_deals_data = get_all_deals()
    deal_id_deal_dict = {
        org_dict['id']: org_dict
        for org_dict in all_deals_data
    }
    print(json.dumps({k: deal_id_deal_dict[k]
          for k in list_deal_id[:5]}, indent=1))
    deal_id_deal_sdr_id = {
        did: (deal_id_deal_dict[did][maxia_pipedrive.models.Deal.get_api_code(
            maxia_pipedrive.models.Deal.assigned_sdr)] if isinstance(deal_id_deal_dict[did][maxia_pipedrive.models.Deal.get_api_code(
                maxia_pipedrive.models.Deal.assigned_sdr)], int) else deal_id_deal_dict[did][maxia_pipedrive.models.Deal.get_api_code(
                    maxia_pipedrive.models.Deal.assigned_sdr)][maxia_pipedrive.consts.Consts.id])
        for did in list_deal_id
        if deal_id_deal_dict[did][maxia_pipedrive.models.Deal.get_api_code(maxia_pipedrive.models.Deal.assigned_sdr)] is not None
    }

    deal_id_deal_owner_id = {
        did: (deal_id_deal_dict[did][maxia_pipedrive.models.Deal.get_api_code(
            maxia_pipedrive.models.Deal.owner_id)] if isinstance(deal_id_deal_dict[did][maxia_pipedrive.models.Deal.get_api_code(
                maxia_pipedrive.models.Deal.owner_id)], int) else deal_id_deal_dict[did][maxia_pipedrive.models.Deal.get_api_code(
                    maxia_pipedrive.models.Deal.owner_id)][maxia_pipedrive.consts.Consts.id])
        for did in list_deal_id
        if deal_id_deal_dict[did][maxia_pipedrive.models.Deal.get_api_code(maxia_pipedrive.models.Deal.owner_id)] is not None

    }

    deal_id_org_id = {
        did: (deal_id_deal_dict[did][maxia_pipedrive.models.Deal.get_api_code(maxia_pipedrive.models.Deal.organization_id)]
              if isinstance(deal_id_deal_dict[did][maxia_pipedrive.models.Deal.get_api_code(maxia_pipedrive.models.Deal.organization_id)], int)
              else deal_id_deal_dict[did][maxia_pipedrive.models.Deal.get_api_code(maxia_pipedrive.models.Deal.organization_id)]['value']
              )

        for did in list_deal_id
        if deal_id_deal_dict[did][maxia_pipedrive.models.Deal.get_api_code(maxia_pipedrive.models.Deal.organization_id)] is not None
    }

    deal_following_list = [
        {
            maxia_pipedrive.consts.Consts.id: did,
            maxia_pipedrive.consts.Consts.user_id: deal_id_deal_sdr_id.get(did)
        }
        for did in list_deal_id
        if deal_id_deal_sdr_id.get(did) is not None
    ] + \
        [
        {
            maxia_pipedrive.consts.Consts.id: did,
            maxia_pipedrive.consts.Consts.user_id: deal_id_deal_owner_id.get(did)
        }
        for did in list_deal_id
        if deal_id_deal_owner_id.get(did) is not None
    ]

    org_following_list = [
        {
            maxia_pipedrive.consts.Consts.id: deal_id_org_id.get(did),
            maxia_pipedrive.consts.Consts.user_id: deal_id_deal_sdr_id.get(did)
        }
        for did in list_deal_id
        if deal_id_deal_sdr_id.get(did) is not None
        and deal_id_org_id.get(did) is not None
    ] + \
        [
        {
            maxia_pipedrive.consts.Consts.id: deal_id_org_id.get(did),
            maxia_pipedrive.consts.Consts.user_id: deal_id_deal_owner_id.get(did)
        }
        for did in list_deal_id
        if deal_id_deal_owner_id.get(did) is not None
        and deal_id_org_id.get(did) is not None
    ]

    persons_following_list = [
        {
            maxia_pipedrive.consts.Consts.id: pid,
            maxia_pipedrive.consts.Consts.user_id: deal_id_deal_sdr_id.get(did)
        }
        for did in list_deal_id
        for pid in org_people_dict.get(str(deal_id_org_id.get(did)), [])
    ] + \
        [
        {
            maxia_pipedrive.consts.Consts.id: pid,
            maxia_pipedrive.consts.Consts.user_id: deal_id_deal_owner_id.get(did)
        }
        for did in list_deal_id
        for pid in org_people_dict.get(str(deal_id_org_id.get(did)), [])
    ]

# The deal must be followed by the respective SDR
    print('Adding followers to DEALS')
    list_output_files.append(maxia_pipedrive.api_handler.followers.add_follower_to_multiple_deals(
        deal_following_list, save=save
    ))
    print('Adding Followers to ORGANIZATIONS')
    # The organization must be followed by the respective SDR and Consultor
    list_output_files.append(maxia_pipedrive.api_handler.followers.add_follower_to_multiple_organization(
        org_following_list, save=save
    ))
    print('Adding Followers to PERSONS')
    # The persons from each organization must be followed by the respective SDR and Consultor
    list_output_files.append(maxia_pipedrive.api_handler.followers.add_follower_to_multiple_persons(
        persons_following_list, save=save

    ))
    return list_output_files


def create_deal(deal_dict, save=True):
    raise NotImplementedError
    # The migration in this case consists on the outputed id
    # return post_request('deals', deal_dict, 'dealid', save_migration=save_migration)
    return create_multiple_deals([deal_dict], allow_retry=True)


def create_multiple_deals(list_deal_dict, cascade=True, save=True):
    """
    Create multiple deals (no product attached), if cascade = True it will cascade the following after creation
    """
    all_deals = get_all_deals()
    all_deals_titles = [el[maxia_pipedrive.models.Deal.get_api_code(
        maxia_pipedrive.models.Deal.title)] for el in all_deals]

    # TODO: validate deal fields (must have owner_id set, ...)

    # We can't create multiple deals with the same title
    validated_list_deal_dict = [
        el for el in list_deal_dict if el[maxia_pipedrive.models.Deal.get_api_code(maxia_pipedrive.models.Deal.title)] not in all_deals_titles]
    if len(list_deal_dict) != len(validated_list_deal_dict):
        print('maxia_pipedrive_src.models.Organizations IDs already with deal:',  [el[maxia_pipedrive.models.Deal.get_api_code(
            maxia_pipedrive.models.Deal.organization_id)] for el in list_deal_dict if el not in validated_list_deal_dict])
        print(
            f'{len(list_deal_dict)-len(validated_list_deal_dict)} deals already created  (same title). Skipping...')

    # First, create the deals
    list_created_deals = maxia_pipedrive.api_handler.utils.multiple_post_request(
        maxia_pipedrive.consts.Endpoints.deals,
        validated_list_deal_dict,
        maxia_pipedrive.consts.MigrationKind.deal,
        save=False)
    list_output_files = []
    if save:
        list_output_files.append(maxia_pipedrive.api_handler.utils.save_migration(
            maxia_pipedrive.consts.MigrationMethods.create, maxia_pipedrive.consts.MigrationKind.deal, list_created_deals))
    else:
        list_output_files.append(list_created_deals)
    if cascade:
        # Then, cascade the following
        print('Cascading followers')
        with open(list_output_files[0], 'r') as f:
            migration_data = json.load(f)
            list_deal_id = [d[maxia_pipedrive.consts.Consts.details][maxia_pipedrive.consts.Consts.id]
                            for d in migration_data]
            cascade_following(
                list_deal_id,
                save=True,
                list_output_files=list_output_files,
                all_deals_data=None)
    return list_output_files


def build_list_multiple_deals(
        pipeline_name,
        stage_name,
        year,
        list_org_id,
        consultor_alias,
        sdr_alias,
        orgs_info,
        is_keyaccount=True):
    # normal_product_id = 7
    # ka_product_id = 8
    user_id = maxia_pipedrive.data_handler.load_relation(
        maxia_pipedrive.consts.Relations.useralias_userid)[consultor_alias]
    sdr_id = maxia_pipedrive.data_handler.load_relation(
        maxia_pipedrive.consts.Relations.useralias_userid)[sdr_alias]
    product_id = 8 if is_keyaccount else 7
    all_deals = get_all_deals()
    orgs_with_deals = [el['org_id']['value'] for el in all_deals]
    stage_id = maxia_pipedrive.data_handler.load_relation(maxia_pipedrive.consts.Relations.stagealias_stageinfo)[
        pipeline_name + "_" + stage_name]['id']
    deals_list_dict = [
        {
            'title': f"{year} - {orgs_info[org_id]['name']}",
            'quantity': orgs_info[org_id][maxia_pipedrive.models.Organization.get_api_code_dict()[maxia_pipedrive.models.Organization.n_students]],
            'discount_percentage': 0,
            'product_id': product_id,
            'org_id': org_id,
            'user_id': user_id,
            'stage_id': stage_id,
            maxia_pipedrive.models.Deal.get_api_code(maxia_pipedrive.models.Deal.assigned_sdr): sdr_alias
        }
        for org_id in list_org_id
        if org_id not in orgs_with_deals
    ]
    return deals_list_dict


def delete_deals(list_deal_id, save_migration=True):
    raise NotImplementedError
    # endpoint, obj_ids: list, migration_kind, save_migration=True
    return delete_request('deals', list_deal_id, 'dealid', save_migration=save_migration)


def update_deal(deal_id, update_dict, deal_current_data=None, save=True):
    # Validate update_dict
    update_deal_endpoint = maxia_pipedrive.consts.MigrationKind.update_deal % (
        deal_id)
    owner_id_ac = maxia_pipedrive.models.Deal.get_api_code(maxia_pipedrive.models.Deal.owner_id)
    person_id_ac = maxia_pipedrive.models.Deal.get_api_code(maxia_pipedrive.models.Deal.person_id)
    if deal_current_data is None:
        deal_current_data = maxia_pipedrive.api_handler.utils.get_request(
            update_deal_endpoint)

    # if isinstance(deal_current_data[owner_id_ac], dict):
    #     deal_current_data[owner_id_ac] = deal_current_data[owner_id_ac]['id']

    # if isinstance(deal_current_data[person_id_ac], dict):
    #     deal_current_data[person_id_ac] = deal_current_data[person_id_ac]['value']
    update_dict = maxia_pipedrive.models.Deal.validate_fields(update_dict.copy())
    deal_current_data = maxia_pipedrive.models.Deal.validate_fields(
        deal_current_data.copy())
    update_dict_keys = list(update_dict.keys())

    for field_key in update_dict_keys:
        if str(update_dict[field_key]) == str(deal_current_data[field_key]):
            # no update, remove it for better performance
            del update_dict[field_key]
    if len(update_dict) == 0:
        return {}

    return maxia_pipedrive.api_handler.utils.update_request_v2(
        update_deal_endpoint,
        maxia_pipedrive.consts.MigrationKind.deal,
        update_dict,
        obj_current_data=deal_current_data,
        save=save
    )


def update_multiple_deals(list_deal_id, list_update_dict, all_deals_data=None, step_size=500, save=True):
    if all_deals_data is None:
        all_deals_data = get_all_deals()
    deal_id_deal_dict = {
        org_dict['id']: org_dict
        for org_dict in all_deals_data
    }
    n_steps = int(np.ceil(len(list_update_dict) / step_size))
    list_migration_fpath = []
    for stp in range(n_steps):
        timestp = datetime.now().strftime(maxia_pipedrive.consts.Consts.date_format)
        migration_fpath = join(
            maxia_pipedrive.consts.Consts.migrations_dir,
            f'update_multidealid_{timestp}_{stp+1}-{n_steps}.json')
        list_migration_fpath.append(migration_fpath)
        print(
            f'[{stp+1}/{n_steps}] Starting updates... Saving migration file on: {migration_fpath}')
        list_migration_dict = []
        try:
            for deal_id, update_dict in tqdm(zip(list_deal_id[stp * step_size:(stp + 1) * step_size],
                                                 list_update_dict[stp * step_size:(stp + 1) * step_size]),
                                             total=len(list_deal_id[stp * step_size:(stp + 1) * step_size])):
                migration_dict = update_deal(
                    int(deal_id),  # must be int
                    update_dict,
                    save=False,
                    deal_current_data=deal_id_deal_dict[deal_id])
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
        f'update_multidealid_{timestp}.json')
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
