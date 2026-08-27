from etl.pipeline import ETLPipeline


def main():
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
