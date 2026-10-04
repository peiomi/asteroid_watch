from cloud_function.event_handler import ETLEventHandler


# google requires both params even if context not being used
def etl_event(event, context):
    handler = ETLEventHandler()
    handler.handle(event)
