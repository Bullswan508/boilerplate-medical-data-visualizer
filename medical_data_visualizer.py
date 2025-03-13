import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('./medical_examination.csv')

# 2
df['overweight'] = np.where((df['weight'] / ((df['height'] / 100) ** 2)) > 25, 1, 0)


# 3
df['cholesterol'] = (df['cholesterol'] != 1).astype(int)
df['gluc'] = (df['gluc'] != 1).astype(int)

# 4
def draw_cat_plot():
    # 5
    df_cat = df.melt(id_vars=['cardio'], value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])


    # 6
    df_cat = df_cat.groupby('cardio').value_counts().sort_index().reset_index(name='total')

    print(df_cat)


    # 7


    cat_plot = sns.catplot(
        data=df_cat, x='variable', y='total', col='cardio',
        kind='bar', hue='value', estimator='sum'
    )


    # 8
    fig = cat_plot.figure


    # # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df.drop(df[(df['ap_lo'] > df['ap_hi']) | 
                         (df['height'] < df['height'].quantile(0.025)) | 
                         (df['height'] > df['height'].quantile(0.975)) | 
                         (df['weight'] < df['weight'].quantile(0.025)) | 
                         (df['weight'] > df['weight'].quantile(0.975))].index, inplace=False)

    # 12
    corr = df_heat.corr()

    # 13

    mask_dict = {}

    for column in corr.columns:
        mask_dict[column] = [False for _ in range(14)]

    for i, item in enumerate(mask_dict.items()):
        mask_dict[item[0]][:i + 1] = [True for _ in range(i + 1)]

    mask = pd.DataFrame(data=mask_dict, index=[i for i in corr.index])


    # 14
    fig, ax = plt.subplots()

    # 15

    fig.set_size_inches(10,8)

    sns.heatmap(data=corr, mask=mask, annot=True, fmt='.1f', linewidth=.5, ax=ax)

    # 16
    fig.savefig('heatmap.png')
    return fig

draw_heat_map()
