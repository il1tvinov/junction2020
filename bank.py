import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
import squarify
from aito.schema import AitoStringType, AitoTextType, AitoDelimiterAnalyzerSchema, AitoTableSchema, AitoColumnLinkSchema, AitoDatabaseSchema
from aito.client import AitoClient
import aito.api as aito_api
from statsmodels.graphics.mosaicplot import mosaic


def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result


data_folder = "data"
link_bank = data_folder + "/bank" + "/final_transaction_table.csv"
link_codes = data_folder + "/bank" + "/codes.xlsx"

instance = "https://hipsters.aito.app"
api_key = "3XnUjV3wov4reqIUvZVq362onm4huY3y31tGsI1Y"

# Reconfigure transactions data frame
df_codes = pd.read_excel(link_codes)
tr_categories = df_codes.tr_type.unique()
df_transactions = pd.read_csv(link_bank, sep=";")
df_transactions.accountName = df_transactions.accountName.astype('category').cat.codes

# Make plots for single users
print(df_transactions['accountName'])
for user in range(0, len(df_transactions.accountName.unique())):
    print(user)
    df_slice = df_transactions[df_transactions.accountName == user]
    df_slice.index = np.arange(0, len(df_slice))
    print(len(df_slice))
    df_slice.reindex()
    df_hist = pd.DataFrame(columns=["category", "money"])
    df_hist.category = tr_categories
    df_hist.money = np.zeros(len(df_hist))

    for i in range(0, len(df_codes)):
        for j in range(0, len(df_slice)):
            if df_slice.taplajikd[j] == df_codes.code[i]:
                df_hist.loc[df_hist.category == df_codes.tr_type[i], "money"] = \
                    df_hist.loc[df_hist.category == df_codes.tr_type[i], "money"] + df_slice.amount[j]

    df_hist1 = df_hist[df_hist.money != 0]
    fig = plt.figure(figsize=(5, 5), dpi=200, facecolor='w', edgecolor='k')
    # plt.pie(df_hist1.money, labels=df_hist1.category)
    # mosaic(df_hist1, ['money'])
    squarify.plot(sizes=df_hist1.money, label=df_hist1.category, alpha=0.6)
    plt.savefig("visualization/square_plots/" + str(user) + ".png", bbox_inches='tight')
    plt.close()


# # Make overall plots
df_hist = pd.DataFrame(columns=["income", "outcome", "other"])
df_hist.income = np.zeros(len(df_transactions.accountName.unique()))
df_hist.outcome = np.zeros(len(df_transactions.accountName.unique()))
df_hist.other = np.zeros(len(df_transactions.accountName.unique()))

for user in range(0, len(df_transactions.accountName.unique())):
    print(user)
    df_slice = df_transactions[df_transactions.accountName == user]
    df_slice.index = np.arange(0, len(df_slice))
    print(len(df_slice))
    df_slice.reindex()
    for j in range(0, len(df_slice)):
        if 500 <= df_slice.taplajikd[j] < 600:
            df_hist.income[user] = df_hist.income[user] + df_slice.amount[j]
        elif 100 <= df_slice.taplajikd[j] < 200:
            df_hist.outcome[user] = df_hist.outcome[user] + df_slice.amount[j]
        else:
            df_hist.other[user] = df_hist.other[user] + df_slice.amount[j]
print(df_hist)
df_hist.to_excel("data/export/outcome_income_2.xlsx")


df_hist = pd.read_excel("data/export/outcome_income.xlsx")
df_hist.outcome = df_hist["outcome"].abs()
df_hist.income = df_hist["income"].abs()

# df_hist = normalize(df_hist)
df_hist_norm = df_hist.div(df_hist.sum(axis=1), axis=0)
df_hist_norm.columns = ["income_norm", "outcome_norm"]
df_hist = pd.concat([df_hist, df_hist_norm], axis=1)
df_hist = df_hist.sort_values(by=['income_norm'])
print(df_hist)
x = df_hist.values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df_hist = pd.DataFrame(x_scaled)
df_hist2 = pd.DataFrame(min_max_scaler.fit_transform(df_hist.T), columns=df_hist.columns, index=df_hist.index)
df_hist_norm.plot.bar(stacked=True)
plt.show()

fig, axes = plt.subplots(nrows=2, ncols=1)
ax1 = fig.add_subplot(2, 1, 1)
data1 = df_hist[df_hist.columns.intersection(["income", "outcome"])]
data1.plot.bar(stacked=True, ax=axes[0])
ax2 = fig.add_subplot(2, 1, 2)
data2 = df_hist[df_hist.columns.intersection(["income_norm", "outcome_norm"])]
data2.plot.bar(stacked=True, ax=axes[1])
plt.ylim((0, 1))
plt.show()

