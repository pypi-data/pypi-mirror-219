import maxia_pipedrive.data_handler
import maxia_pipedrive.models
import maxia_pipedrive.api_handler.fields
import maxia_pipedrive.api_handler.utils
import maxia_pipedrive.consts


def add_follower_to_person(person_id, user_id, save=True):
    return add_follower_to_multiple_persons([{
        maxia_pipedrive.consts.Consts.id: person_id,
        maxia_pipedrive.consts.Consts.user_id: user_id
    }], save=save)

def add_follower_to_multiple_persons(list_followers_person_dict, save=True):
    return maxia_pipedrive.api_handler.utils.multiple_post_request(
        maxia_pipedrive.consts.Endpoints.person_followers,
        list_followers_person_dict,
        maxia_pipedrive.consts.MigrationKind.follower_to_person,
        save=save
    )

def add_follower_to_deal(deal_id, user_id, save=True):
    return add_follower_to_multiple_deals([{
        maxia_pipedrive.consts.Consts.id: deal_id,
        maxia_pipedrive.consts.Consts.user_id: user_id
    }], save=save)

def add_follower_to_multiple_deals(list_follower_deal_dict, save=True):
    return maxia_pipedrive.api_handler.utils.multiple_post_request(
        maxia_pipedrive.consts.Endpoints.deal_followers,
        list_follower_deal_dict,
        maxia_pipedrive.consts.MigrationKind.follower_to_deal,
        save=save
    )

def add_follower_to_organization(org_id, follower_id, save=True):
    return add_follower_to_multiple_organization([{
        maxia_pipedrive.consts.Consts.id: org_id,
        maxia_pipedrive.consts.Consts.user_id: follower_id
    }], save=save)

def add_follower_to_multiple_organization(list_follower_organization_dict, save=True):
    return maxia_pipedrive.api_handler.utils.multiple_post_request(
        maxia_pipedrive.consts.Endpoints.organization_followers,
        list_follower_organization_dict,
        maxia_pipedrive.consts.MigrationKind.follower_to_org,
        save=save
    )


def get_followers_from_deal(deal_id):
    return maxia_pipedrive.api_handler.utils.get_all_request(maxia_pipedrive.consts.Endpoints.deal_followers % (deal_id))

def get_followers_from_person(person_id):
    return maxia_pipedrive.api_handler.utils.get_all_request(maxia_pipedrive.consts.Endpoints.person_followers % (person_id))

def get_followers_from_organization(org_id):
    return maxia_pipedrive.api_handler.utils.get_all_request(maxia_pipedrive.consts.Endpoints.organization_followers % (org_id))