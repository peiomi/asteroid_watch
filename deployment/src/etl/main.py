from src.etl.pipeline import ETLPipeline
from src.etl.pubsub_publisher import PubSubPublisher
from src.etl.settings import Settings
import logging
import traceback  # added bc 'gcloud beta run jobs executions logs read' command stopped working


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    pipeline = ETLPipeline()

    publisher = PubSubPublisher(
        project_id=Settings.PROJECT_ID, topic_name=Settings.TOPIC_NAME
    )
    logging.info("PROJECT_ID=%s", Settings.PROJECT_ID)
    logging.info("TOPIC=%s", Settings.TOPIC_NAME)

    try:
        pipeline.run()
        logging.info("ETL completed successfully")
    except Exception:
        error = traceback.format_exc()
        logging.exception("ETL pipeline failed")

        try:
            publisher.publish({"event": "etl_failed", "error": error})
        except Exception:
            logging.exception("Failed to publish failure event")
        raise


if __name__ == "__main__":
    main()

""" 
- monitoring - job failures
- build bots
- bot integration/publish hazard alerts
- anaytics/data visualization
 """
