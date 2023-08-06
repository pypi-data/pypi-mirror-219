import os
from os.path import join
class Consts:
    date_format = '%Y-%m-%d_%H%M%S'
    data_dir = './data'
    migrations_dir = './migrations'
    reversed_migrations = './reversed_migrations'
    relations_dir = join(data_dir, 'relations')
    microdados_dir = join(data_dir, 'microdados')
    microdados_treated_dir = join(data_dir, 'microdados_treated')
    API_TOKEN = {
        'api_token': os.environ.get('PIPEDRIVE_API_TOKEN')
    }
    API_URL = 'https://maxia.pipedrive.com/api/v1/'

    # Keywords
    id = 'id'
    user_id = 'user_id'
    migration_kind = 'kind'
    endpoint = 'endpoint'
    method = 'method'
    details = 'details'
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(relations_dir, exist_ok=True)
    os.makedirs(migrations_dir, exist_ok=True)
    os.makedirs(reversed_migrations, exist_ok=True)
    os.makedirs(microdados_dir, exist_ok=True)
    os.makedirs(microdados_treated_dir, exist_ok=True)

class MigrationKind:
    person = 'personid'
    organization = 'orgid'
    deal = 'dealid'
    product_to_deal = 'productdealid'
    multiproduct_to_deal = 'multiproductdealid'
    multiple_orgs = 'multiorgid'
    follower_to_deal = 'followerdealid'
    follower_to_person = 'followerpersonid'
    follower_to_org = 'followerorgid'

class Endpoints:
    # Base
    persons = 'persons'
    organizations = 'organizations'
    deals = 'deals'
    users = 'users'
    stages = 'stages'
    products = 'products'
    # Composed
    organization_fields = 'organizationFields'
    deal_fields = 'dealFields'
    person_fields = 'personFields'
    deal_followers = f'{deals}/%s/followers'
    person_followers = f'{persons}/%s/followers'
    organization_followers = f'{organizations}/%s/followers'
    product_to_deal = f'{deals}/%s/products'
    product_from_deal = f'{deals}/%s/products/%s'
    # update deal
    update_deal = f'{deals}/%s'

    # update persons
    update_persons = f'{persons}/%s'

    # update organizations
    update_organizations = f'{organizations}/%s'


class Relations:
    orgid_inep = 'orgid_inep'
    orgfieldinfo = 'orgfieldinfo'
    dealfieldinfo = 'dealfieldinfo'
    personfieldinfo = 'personfieldinfo'
    useralias_userid = 'useralias_userid'
    stagealias_stageinfo = 'stagealias_stageinfo'
    products_info = 'products_info'

    @classmethod
    def get_available_relations(cls):
        return [el for k, el in cls.__dict__.items() if '__' not in k and not isinstance(el, classmethod)]


class MigrationMethods:
    update = 'update'
    create = 'create'
    delete = 'delete'
