from event_handler import ETLEventHandler
import logging
import functions_framework  # requried for gen2

logging.basicConfig(level=logging.INFO)


# gen2 doesnt require a context param you wont use :O
@functions_framework.cloud_event
def etl_event(cloud_event):
    print("=== FUNCTION TRIGGERED ===")
    print(cloud_event.data)
    logging.info("ENTRYPOINT CALLED")
    logging.info("EVENT: %s", cloud_event)

    handler = ETLEventHandler()
    handler.handle(cloud_event.data)
