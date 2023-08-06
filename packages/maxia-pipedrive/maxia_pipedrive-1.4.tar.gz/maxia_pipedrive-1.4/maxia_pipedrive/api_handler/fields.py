import maxia_pipedrive.data_handler
import maxia_pipedrive.api_handler.utils
import maxia_pipedrive.consts

# ORGANIZATIONS FIELD INFO


def get_all_org_field_info():
    return maxia_pipedrive.api_handler.utils.get_all_request(maxia_pipedrive.consts.Endpoints.organization_fields)


def get_org_field_info(field_key):
    return maxia_pipedrive.data_handler.load_relation(maxia_pipedrive.consts.Relations.orgfieldinfo).get(field_key, None)


# DEAL FIELD INFO

def get_all_deal_field_info():
    return maxia_pipedrive.api_handler.utils.get_all_request(maxia_pipedrive.consts.Endpoints.deal_fields)


def get_deal_field_info(field_key):
    return maxia_pipedrive.data_handler.load_relation(maxia_pipedrive.consts.Relations.dealfieldinfo).get(field_key, None)

# PERSONS FIELD INFO


def get_all_person_field_info():
    return maxia_pipedrive.api_handler.utils.get_all_request(maxia_pipedrive.consts.Endpoints.person_fields)


def get_person_field_info(field_key):
    return maxia_pipedrive.data_handler.load_relation(maxia_pipedrive.consts.Relations.personfieldinfo).get(field_key, None)
