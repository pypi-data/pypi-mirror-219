import maxia_pipedrive.data_handler
import maxia_pipedrive.models
import maxia_pipedrive.api_handler.fields
import maxia_pipedrive.api_handler.utils
import maxia_pipedrive.consts


def get_all_products():
    return maxia_pipedrive.api_handler.utils.get_all_request(maxia_pipedrive.consts.Endpoints.products)


def add_product_to_deal(deal_id, product_id, quantity=1, discount_percentage=0):
    return add_product_to_multiple_deals([{
        'id': deal_id,
        'product_id': product_id,
        'quantity': quantity,
        'discount_percentage': discount_percentage,
        'item_price': maxia_pipedrive.data_handler.load_relation(maxia_pipedrive.consts.Relations.products_info)[product_id]
    }])


def add_product_to_multiple_deals(list_product_deal_dict, save=True):
    # Validate product fields (TODO)
    return maxia_pipedrive.api_handler.utils.multiple_post_request(
        maxia_pipedrive.consts.Endpoints.product_to_deal,
        list_product_deal_dict,
        maxia_pipedrive.consts.MigrationKind.product_to_deal,
        save=save)


def get_products_from_deal(deal_id):
    return maxia_pipedrive.api_handler.utils.get_all_request(maxia_pipedrive.consts.Endpoints.product_to_deal % (deal_id,))


def remove_product_from_deal(deal_id, product_attachment_id):
    return maxia_pipedrive.api_handler.utils.composed_delete_request(
        maxia_pipedrive.consts.Endpoints.product_from_deal % (deal_id, product_attachment_id,),
        maxia_pipedrive.consts.MigrationKind.product_to_deal
    )


def flush_products_from_deal(deal_id, save=True):
    all_products = get_products_from_deal(deal_id)
    list_outdict = []
    for product in all_products:
        list_outdict.append(remove_product_from_deal(
            deal_id, product[maxia_pipedrive.consts.Consts.id]))

    if save:
        return maxia_pipedrive.api_handler.utils.save_migration(
            maxia_pipedrive.consts.MigrationMethods.delete,
            maxia_pipedrive.consts.MigrationKind.multiproduct_to_deal, list_outdict
        )
    else:
        return list_outdict
