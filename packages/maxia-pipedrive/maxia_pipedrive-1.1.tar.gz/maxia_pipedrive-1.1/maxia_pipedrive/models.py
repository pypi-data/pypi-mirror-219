"""
This script is used for Organizations.

One of its purpose is to generate integration files for update and setup organizations
"""
import maxia_pipedrive.consts
import maxia_pipedrive.api_handler.fields
import maxia_pipedrive.data_handler

class Model:
    @classmethod
    def get_api_code_dict(cls):
        raise NotImplementedError

    @classmethod
    def get_api_code(cls, feat):
        return cls.get_api_code_dict()[feat]

    @classmethod
    def validate_fields(cls, object_dict):
        return object_dict


class Organization(Model):
    organization_id = 'ID'
    # Default fields
    owner_id = 'Proprietário'
    name = 'Nome'
    full_address = 'Endereço'

    # Custom fields
    inep_number = 'Codigo INEP'
    cnpj = 'CNPJ'
    cnpj_mantenedora = 'CNPJ Mantenedora'
    inep_number_sede = 'Codigo INEP Sede'
    school_group = 'Grupo'
    school_network = 'Rede'
    n_students = 'Quantidade de Alunos'
    average_price = 'Ticket Médio'
    phone_number = 'Telefone'
    relationship = 'Relacionamento'
    segmentos = 'Segmentos'  # Multiple-choice
    segmentos_n_inf = 'Quantidade Infantil'
    segmentos_n_fund_1 = 'Quantidade Fund I'
    segmentos_n_fund_2 = 'Quantidade Fund II'
    segmentos_n_medio = 'Quantidade Ens Médio'
    segmentos_n_prof = 'Quantidade Ens Prof'
    segmentos_n_eja = 'Quantidade EJA'
    segmentos_n_esp = 'Quantidade Especial'
    # has_internet = 'Internet'  # students

    which_events = 'Participou de evento?'

    custom_address_region = 'Região'
    custom_address_uf = 'UF'
    custom_address_city = 'Cidade'
    custom_address_neigh = 'Bairro'
    custom_address_cep = 'CEP'

    # Intra-analysis features (they are not imported to pipedrive)
    n_rooms = 'Qtd Salas Internas'
    n_rooms_clim = 'Qtd Salas Climatizadas'
    n_desktop = 'Qtd Desktops'  # students
    n_notebook = 'Qtd Notebook'  # students
    n_tablets = 'Qtd Tablets'  # students
    has_banda_larga = 'Fast Internet'

    @classmethod
    def get_api_code_dict(cls):
        return {
            cls.organization_id: 'id',
            cls.owner_id: 'owner_id',
            cls.name: 'name',
            cls.inep_number: '0a490011985fd28d5682ee71546d97670cc0dfbf',
            cls.cnpj: 'ff69de8bea301facdf0cee133c2a9c582744a623',
            cls.cnpj_mantenedora: '005fcfd3ab98ed8d98b1652d00460ed657a76350',
            cls.custom_address_cep: '3fd544da0cb20c8219b02bf52075a90b509c5ea3',
            cls.custom_address_city: 'abade4dfc58a50fa7271f42c3b52f8ff1761cd8a',
            cls.custom_address_uf: '94478254cf891a222b76ba61bd7c0244def265d7',
            cls.custom_address_region: '2cc32b1aa9288ae2eae32450a28c0a0f44159152',
            cls.custom_address_neigh: '204a857a68d70f3de93f88a505585d59bb4acd66',
            cls.phone_number: '67ae8926ef9c252fb13d0f9ee412d4aefdca4747',
            cls.n_students: '97089acf46628b3a90da40f90f0087f3d1d37d7f',
            cls.average_price: '469fba0ae19834f92ee283ca82a4f944d84c0ce1',
            cls.segmentos: '6a186c0ee7c565b5016accd549186025a27c3f5d',  # Multiple-choice
            cls.segmentos_n_inf: '62ab910af9ceffbd4d1cc7ce66a51aa7eeaf50f9',
            cls.segmentos_n_fund_1: '52cfcf541010b82f9b7172854965b667152d0a1f',
            cls.segmentos_n_fund_2: '4544f9777fa789239bd48fce363d1329838550c4',
            cls.segmentos_n_medio: '396abbbdc276d4a5759087c23a145ee14190c634',
            cls.relationship: '15087ac8ef38b935addeb068624d24f0dc7ce229',
            cls.school_group: '03885ba828d6b10d377a154aca8c4b7755dde310',
            cls.school_network: '419a3c286ad0a9198ef258999d1abf06b811dcec',
            cls.full_address: 'address',
            cls.which_events: '49ccc11a76f28804c14982f65c68baf20187bdde'
        }

    @classmethod
    def validate_fields(cls, organization_dict):
        # Validate update_dict (change each label to the id)
        validated_organization_dict = {}
        for field_key, field_value in organization_dict.items():
            
            field_info = maxia_pipedrive.api_handler.fields.get_org_field_info(field_key)
            
            if field_info is None:
                continue
            if field_info['field_type'] in ['enum', 'set', 'visible_to']:
                if field_value != '' and field_value is not None:
                    field_options_ids = {
                        el['label']: str(el['id'])
                        for el in field_info['options']
                    }
                    field_values = str(field_value).split(',')
                    # Check if the labels are ids or actually labels

                    field_values = [
                        field_options_ids.get(str(label))
                        if str(label) in field_options_ids.keys() and str(label) not in field_options_ids.values()
                        else str(label)
                        for label in field_values]
                    validated_organization_dict[field_key] = ','.join(
                        field_values)
                else:
                    validated_organization_dict[field_key] = None
            elif field_info['field_type'] in ['double', 'address', 'varchar']:
                validated_organization_dict[field_key] = field_value
            elif field_info['field_type'] in ['user']:
                # Get user ID
                # Check if the user_id was sent
                if isinstance(field_value, dict):
                    organization_dict[field_key] = organization_dict[field_key]['id']
                    field_value = organization_dict[field_key]
                useralias_userid_relation = maxia_pipedrive.data_handler.load_relation(maxia_pipedrive.consts.Relations.useralias_userid)
                if field_value in useralias_userid_relation.keys():
                    validated_organization_dict[field_key] = useralias_userid_relation[field_value]
                elif field_value in useralias_userid_relation.values():
                    validated_organization_dict[field_key] = field_value
        return validated_organization_dict


class Person(Model):
    person_id = 'ID'
    organization_id = 'Organização ID'
    owner_id = 'Proprietário'
    name = 'Nome'
    role = 'Cargo'
    # role2 = 'Cargo2'
    phone_number = 'Telefone'
    email = 'E-mail'

    @classmethod
    def get_api_code_dict(cls):
        return {
            cls.person_id: 'id',
            cls.organization_id: 'org_id',
            cls.owner_id: 'owner_id',
            cls.name: 'name',
            # cls.role: '3ccc4d5d8c63aea0bf8f268c68f4de355a66bc2c',
            cls.role: '9d6ab3058edd25304245f7574200756b349bd960',
            cls.phone_number: 'phone',
            cls.email: 'email'
        }


class Deal(Model):
    deal_id = 'ID'  # id
    organization_id = 'Organização ID'  # org_id
    person_id = 'Pessoa de Contato'  # person_id
    owner_id = 'Proprietário'  # user_id
    funil = 'Funil'  # pipeline_id
    stage_id = 'Stage'
    title = 'Título'  # title
    n_pruducts = 'Quantidade de produtos' # product_quantity
    value_products = 'Valor de produtos' #  product_amount
    assigned_sdr = 'SDR'
    year = 'Ano'
    priority = 'PRIO'

    @classmethod
    def get_api_code_dict(cls):
        return {
            cls.deal_id: 'id',
            cls.organization_id: 'org_id',
            cls.person_id: 'person_id',
            cls.owner_id: 'user_id',
            cls.funil: 'pipeline_id',
            cls.stage_id: 'stage_id',
            cls.title: 'title',
            cls.n_pruducts: 'product_quantity',
            cls.value_products: 'product_amount',
            cls.assigned_sdr: 'df413230ed612db93126a3180078543d209f389d',
            cls.priority: 'ca7c2c934d2f359315393b99090d3c4846264975'
        }
    @classmethod
    def validate_fields(cls, deal_dict):
        from maxia_pipedrive.api_handler.fields import get_deal_field_info
        from maxia_pipedrive.data_handler import load_relation
        # Validate update_dict (change each label to the id)
        validated_deal_dict = {}
        for field_key, field_value in deal_dict.items():
            
            field_info = get_deal_field_info(field_key)
            
            if field_info is None:
                continue
            if field_info['field_type'] in ['enum', 'set', 'visible_to']:
                if field_value != '' and field_value is not None:
                    field_options_ids = {
                        el['label']: str(el['id'])
                        for el in field_info['options']
                    }
                    field_values = str(field_value).split(',')
                    # Check if the labels are ids or actually labels

                    field_values = [
                        field_options_ids.get(str(label))
                        if str(label) in field_options_ids.keys() and str(label) not in field_options_ids.values()
                        else str(label)
                        for label in field_values]
                    validated_deal_dict[field_key] = ','.join(
                        field_values)
                else:
                    validated_deal_dict[field_key] = None
            elif field_info['field_type'] in ['double', 'address', 'varchar']:
                validated_deal_dict[field_key] = field_value
            elif field_info['field_type'] in ['user']:
                # Get user ID
                # Check if the user_id was sent
                if isinstance(field_value, dict):
                    deal_dict[field_key] = deal_dict[field_key]['id']
                    field_value = deal_dict[field_key]
                useralias_userid_relation = load_relation(maxia_pipedrive.consts.Relations.useralias_userid)
                if field_value in useralias_userid_relation.keys():
                    validated_deal_dict[field_key] = useralias_userid_relation[field_value]
                elif field_value in useralias_userid_relation.values():
                    validated_deal_dict[field_key] = field_value
                else:
                    validated_deal_dict[field_key] = field_value
        return validated_deal_dict
class Product(Model):
    owner_id = 'user_id'
    product_id = 'product_id'
    quantity = 'quantity'
    deal_id = 'deal_id'
    discount_percentage = 'discount_percentage'
    item_price = 'item_price'
   
    @classmethod
    def get_api_code_dict(cls):
        return {
            cls.product_id: 'product_id',
            cls.quantity: 'quantity',
            cls.deal_id: 'deal_id',
            cls.discount_percentage: 'discount_percentage',
            cls.item_price: 'item_price',
            cls.owner_id: 'owner_id'
        }

