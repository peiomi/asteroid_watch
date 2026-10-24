from deployment.src.etl.pipeline import ETLPipeline
from deployment.src.etl.pubsub_publisher import PubSubPublisher
from deployment.src.etl.settings import Settings
from deployment.src.etl.bluesky_publisher import BlueSkyPublisher

import logging
import traceback


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

    bluesky = BlueSkyPublisher()

    try:
        pipeline.run()
        logging.info("ETL completed successfully")

        message = bluesky.generate_post()
        image = bluesky.get_chart_image()
        bluesky.post(message=message, image=image)

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
- ENV in dockerfile was causing problems with local testing removed it entirely so everything 
runs on the same import path
- scheduler now has correct permissions and should start to run daily

REMINDER FOR TOMORROW ME:
- logic for graph png is done refactor it into a module that runs in the pipeline
- uncomment bluesky post code then rebuild docker/terraform apply
- then focus on cloud run service for discord bot
- THEN you can move on to notebooks for the discord commands 

- ideas for notebooks: are we gunna die today
 """
