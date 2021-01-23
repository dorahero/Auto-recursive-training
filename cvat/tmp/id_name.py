import pandas as pd
import argparse
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--keyword', type=str)
args = parser.parse_args()
df = pd.read_csv("./lp_task.csv", names=["id", "name", ""])
lp_df = df[df['name'].str.contains(args.keyword)]
for i, j in zip(lp_df["id"], lp_df["name"]):
    print(str(i)+","+str(j))