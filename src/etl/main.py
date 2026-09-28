from etl.pipeline import ETLPipeline
from etl.pubsub_publisher import PubSubPublisher
from etl.settings import Settings
import logging

publisher = PubSubPublisher(
    project_id=Settings.PROJECT_ID, topic_name=Settings.TOPIC_NAME
)


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    pipeline = ETLPipeline()

    try:
        pipeline.run()
    except Exception as e:
        publisher.publish({"event": "etl_failed", "error": str(e)})
        raise


if __name__ == "__main__":
    main()

""" 
- monitoring - job failures
- build bots
- bot integration/publish hazard alerts
- anaytics/data visualization
 """
