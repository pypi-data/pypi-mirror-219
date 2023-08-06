# returns the consolidated elastic_search compliance
from OBP_reliability_pillar.elastic_search.elastic_search_in_vpc_only import *


def elastic_search_compliance(self, regions):
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside elastic_search :: elastic_search_compliance()")

    response = [
        elastic_search_in_vpc_only(self, regions)
    ]

    return response