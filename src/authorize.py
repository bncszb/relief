import utils.reports as rep
import pandas as pd
import time


path = "/home/data/local/search_results/all_keys.xlsx"

all_results_df = pd.read_excel(path, index_col=0)
timestr = time.strftime("%y-%m-%d_%H-%M")
title =f"report_{timestr}"
rep.upload_sheet(all_results_df, title)

merged_results_df=all_results_df.groupby(["title","date"]).aggregate(set).reset_index()
merged_results_df.to_excel("/home/data/local/search_results/merged_keys.xlsx")
title =f"report_merged_{timestr}"
rep.upload_sheet(merged_results_df, title)