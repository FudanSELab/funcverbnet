import pandas as pd
from sklearn.metrics import f1_score

# 转换为FastText需要的格式
train_df = pd.read_csv('./data/sentences_with_annotation.csv')
print(train_df)
# train_df['final_annotation_type'] = train_df['final_annotation_type'].replace(54, -1)
# criteria = train_df['final_annotation_type'] == -1
# print(train_df[criteria].head())
train_df.loc[train_df['final_annotation_type'] == 53, 'final_annotation_type'] = -1
df1 = train_df.loc[train_df['final_annotation_type'] == -1]
print(df1)
df = train_df.loc[(train_df['final_annotation_type'] < 53) & (train_df['final_annotation_type'] >= 0)]
print(df)
train_df.loc[
    (train_df['final_annotation_type'] < 53) & (train_df['final_annotation_type'] >= 0), 'final_annotation_type'] = df[
                                                                                                                        'final_annotation_type'] + 1
train_df.sort_values("final_annotation_type", inplace=True)
print(train_df)

train_df['label_ft'] = '__label__' + train_df['final_annotation_type'].astype(str)
train_df[['single_description', 'label_ft']].to_csv('upadte_train_data.csv', index=None, header=None, sep='\t')
train_df[['single_description', 'label_ft']].iloc[-500:].to_csv('test_data.csv', index=None, header=None, sep='\t')
import fasttext
model = fasttext.train_supervised('upadte_train_data.csv', lr=1, wordNgrams=2,
                                  verbose=2, minCount=1, epoch=25, loss="hs")

val_pred = [model.predict(x)[0][0].split('__')[-1] for x in train_df.iloc[-5000:]['single_description']]
print(model.predict("Apply a gravity constant to an object and take care if layout direction is RTL or not."))
print(train_df['final_annotation_type'].values[-5000:].astype(str))

print(f1_score(train_df['final_annotation_type'].values[-5000:].astype(str), val_pred, average='macro'))
print(val_pred)
