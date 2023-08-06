from datetime import datetime
import json
import maxia_pipedrive.api_handler.organizations
import maxia_pipedrive.api_handler.stages
import maxia_pipedrive.api_handler.fields
import maxia_pipedrive.api_handler.users
import maxia_pipedrive.api_handler.products
import maxia_pipedrive.models
import maxia_pipedrive.consts

dateformat = '%Y-%m-%d_%H%M%S'


def fetch_id_inep_reference(org_id=None, save=True):
    """ This module will fetch the reference id/INEP"""
    id_inep_dict = None
    if org_id is None:
        data = maxia_pipedrive.api_handler.organizations.get_all_organizations()
        id_inep_dict = {
            org_dict[maxia_pipedrive.models.Organization.get_api_code_dict(
            )[maxia_pipedrive.models.Organization.inep_number]]: org_dict['id']
            for org_dict in data
        }

    else:
        org_dict = maxia_pipedrive.api_handler.organizations.get_organization(org_id)
        id_inep_dict = {
            org_dict[maxia_pipedrive.models.Organization.get_api_code_dict(
            )[maxia_pipedrive.models.Organization.inep_number]]: org_dict['id']
        }
    if save:
        timestp = datetime.now().strftime(dateformat)
        print(len(id_inep_dict))
        with open(f'data/relations/orgid_inep_{timestp}.json', 'w', encoding='utf-8') as f:
            json.dump(id_inep_dict, f, indent=1)
    return id_inep_dict


def fetch_orgfieldinfo_reference(save=True):
    data = None
    if data is None:
        data = maxia_pipedrive.api_handler.fields.get_all_org_field_info()
    key_id_dict = {
        field_dict['key']: field_dict
        for field_dict in data
    }
    if save:
        timestp = datetime.now().strftime(dateformat)
        print(len(key_id_dict))
        with open(f'data/relations/{maxia_pipedrive.consts.Relations.orgfieldinfo}_{timestp}.json', 'w', encoding='utf-8') as f:
            json.dump(key_id_dict, f, indent=1)


def fetch_dealfieldinfo_reference(save=True):
    data = None
    if data is None:
        data = maxia_pipedrive.api_handler.fields.get_all_deal_field_info()
    key_id_dict = {
        field_dict['key']: field_dict
        for field_dict in data
    }
    if save:
        timestp = datetime.now().strftime(dateformat)
        print(len(key_id_dict))
        with open(f'data/relations/{maxia_pipedrive.consts.Relations.dealfieldinfo}_{timestp}.json', 'w', encoding='utf-8') as f:
            json.dump(key_id_dict, f, indent=1)


def fetch_personfieldinfo_reference(save=True):
    data = None
    if data is None:
        data = maxia_pipedrive.api_handler.fields.get_all_person_field_info()
    key_id_dict = {
        field_dict['key']: field_dict
        for field_dict in data
    }
    if save:
        timestp = datetime.now().strftime(dateformat)
        print(len(key_id_dict))
        with open(f'data/relations/{maxia_pipedrive.consts.Relations.personfieldinfo}_{timestp}.json', 'w', encoding='utf-8') as f:
            json.dump(key_id_dict, f, indent=1)


def fetch_useralias_userid_reference(save=True):
    data = maxia_pipedrive.api_handler.users.get_all_users()
    name_email_id_dict = [
        {
            user['name']: user['id'],
            user['email']: user['id']
        }
        for user in data
    ]
    name_email_id_dict = {
        k: v for d in name_email_id_dict for k, v in d.items()}
    if save:
        timestp = datetime.now().strftime(dateformat)
        print(len(name_email_id_dict))
        with open(f'data/relations/useralias_userid_{timestp}.json', 'w', encoding='utf-8') as f:
            json.dump(name_email_id_dict, f, indent=1)


def fetch_stagealias_stageinfo_reference(save=True):
    data = maxia_pipedrive.api_handler.stages.get_all_stages()
    stagealias_stagedata = {
        stage['pipeline_name'] + "_" + stage['name']: stage
        for stage in data
    }
    if save:
        timestp = datetime.now().strftime(dateformat)
        print(len(stagealias_stagedata))
        with open(f'data/relations/stagealias_stageinfo_{timestp}.json', 'w', encoding='utf-8') as f:
            json.dump(stagealias_stagedata, f, indent=1)


def fetch_products_info(save=True):
    data = maxia_pipedrive.api_handler.products.get_all_products()
    product_info = {
        prod['id']: prod['prices'][0]['price']
        for prod in data
    }
    if save:
        timestp = datetime.now().strftime(dateformat)
        print(len(product_info))
        with open(f'data/relations/products_info_{timestp}.json', 'w', encoding='utf-8') as f:
            json.dump(product_info, f, indent=1)


if __name__ == '__main__':
    # fetch_id_inep_reference()
    # fetch_orgfieldinfo_reference(save=True)
    # fetch_useralias_userid_reference(save=True)
    # fetch_stagealias_stageinfo_reference(save=True)
    # fetch_products_info(save=True)
    fetch_personfieldinfo_reference(save=True)
