from etl.pipeline import ETLPipeline
from etl.pubsub_publisher import PubSubPublisher
import logging

publisher = PubSubPublisher()


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
