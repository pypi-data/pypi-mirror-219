import maxia_pipedrive.api_handler.utils
import maxia_pipedrive.models
import maxia_pipedrive.consts


def create_person(person_dict, save=False):
    """
    person_dict keys: Proprietário, Nome, Telefone, Cargo, Codigo INEP
    """
    return maxia_pipedrive.api_handler.utils.create_object(
        maxia_pipedrive.models.Person,
        maxia_pipedrive.consts.Endpoints.persons,
        maxia_pipedrive.consts.MigrationKind.person,
        person_dict,
        save=save
    )

def create_multiple_persons(list_person_dict, step_size=500, save=False):
    create_obj_func = create_person
    obj_migration_kind = maxia_pipedrive.consts.MigrationKind.person

    return maxia_pipedrive.api_handler.utils.create_multiple_objects(
        create_obj_func, obj_migration_kind,
        list_person_dict,
        step_size=step_size, save=save)


def get_all_persons(**query_params_dict):
    return maxia_pipedrive.api_handler.utils.get_all_request(maxia_pipedrive.consts.Endpoints.persons, **query_params_dict)


def update_person(obj_id: int, update_dict: dict, obj_current_data: dict = None, save: bool = True):
    ObjClass = maxia_pipedrive.models.Person
    obj_endpoint = maxia_pipedrive.consts.Endpoints.update_persons
    obj_migration_kind = maxia_pipedrive.consts.MigrationKind.person

    return maxia_pipedrive.api_handler.utils.update_object(
        ObjClass, obj_endpoint, obj_migration_kind,
        obj_id, update_dict, obj_current_data=obj_current_data, save=save
    )


def update_multiple_persons(list_obj_id, list_update_dict, all_obj_data=None, step_size=500, save=True):
    update_obj_func = update_person
    get_all_obj_func = get_all_persons
    obj_migration_kind = maxia_pipedrive.consts.MigrationKind.person

    return maxia_pipedrive.api_handler.utils.update_multiple_object(
        update_obj_func, get_all_obj_func, obj_migration_kind,
        list_obj_id, list_update_dict, all_obj_data=all_obj_data,
        step_size=step_size, save=save)
