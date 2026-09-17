from etl.pipeline import ETLPipeline
import logging


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    pipeline = ETLPipeline()
    pipeline.run()
    return


if __name__ == "__main__":
    main()

""" 
- fetch nasa
- noramlize
- score
- write to BigQuery
- store raw JSON
- handle errors
- publish hazard alerts 
 """
