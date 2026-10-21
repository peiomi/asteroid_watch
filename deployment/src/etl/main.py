from deployment.src.etl.pipeline import ETLPipeline
from deployment.src.etl.pubsub_publisher import PubSubPublisher
from deployment.src.etl.settings import Settings
from deployment.src.bots.bluesky_publisher import BlueSkyPublisher

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

    bluesky = BlueSkyPublisher()

    try:
        pipeline.run()
        logging.info("ETL completed successfully")

        # message = bluesky.generate_post()
        # bluesky.post(message)

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

REMINDER FOR TOMORROW ME:
- docker image needs to be rebuilt
- scheduler now has correct permissions and should start to run daily
- look at r/dataisbeautiful for ideas to make the dashboard prettier 
- BEFOREEEE trying to connect BQ or bluesky or discord focus on making dashboard pretty
- once you have pretty png, refactor to connect to BQ/bluesky
- then focus on cloud run service for discord bot
- THEN you can move on to notebooks for the discord commands 
- ideas for notebooks: scatter plot of risk levels, daily count for hazardous objects, are we gunna die today

- !!!!! dont forget to uncomment code for bluesky post once dashboard is ready !!!!!!
 """
