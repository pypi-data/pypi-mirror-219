import logging
from . import _az_facade as az

log = logging.getLogger(__name__)

def prepare(data: dict):
    applicationId = data.get('applicationId')
    if applicationId:
        log.info("Initializing with configured SP.")
        applicationSecret = data.get('applicationSecret')
        #az.login(applicationId, applicationSecret, )

    
    # _az_facade.login(provider['applicationId'], provider['applicationSecret'], directory_id)
    # _az_facade.set_subscription(subscription_id)
    else:
        log.info("No configured SP found. Using Azure CLI stored login.")