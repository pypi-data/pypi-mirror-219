import maxia_pipedrive.api_handler.utils
import maxia_pipedrive.consts


def get_all_stages():
    return maxia_pipedrive.api_handler.utils.get_request(maxia_pipedrive.consts.Endpoints.stages)
