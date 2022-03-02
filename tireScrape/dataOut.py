import pandas as pd

tires_df = pd.read_csv("tireData.csv")
#
tires_df.to_parquet('s3://sagemaker-studio-share/datasets/crawling/tirerack/tireData.parquet')
# from tireScrape import spiders as sd
import tireScrape.spiders.tire_scrape as ts
import fastparquet
import s3fs
import boto3

# s3_client = boto3.client('s3')
#
# s3_client.upload_file("tireData.csv", 'sagemaker-studio-share', 'tireData.csv')
# d = {
#     'tire': ts.item
# }
#
# tire_df = pd.DataFrame(data = d)
#
# print(tire_df)




