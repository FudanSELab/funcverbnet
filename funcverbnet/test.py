import pandas as pd
from sklearn.metrics import f1_score

# 转换为FastText需要的格式
train_df = pd.read_csv('./data/sentences_with_annotation.csv')
print(train_df.head())
train_df['label_ft'] = '__label__' + train_df['final_annotation_type'].astype(str)
train_df[['single_description', 'label_ft']].to_csv('train.csv', index=None, header=None, sep='\t')
train_df[['single_description', 'label_ft']].iloc[-500:].to_csv('test_data.csv', index=None, header=None, sep='\t')
import fasttext
model = fasttext.train_supervised('train.csv', lr=1, wordNgrams=2,
                                  verbose=2, minCount=1, epoch=25, loss="hs")

val_pred = [model.predict(x)[0][0].split('__')[-1] for x in train_df.iloc[-5000:]['single_description']]
print(model.predict("Apply a gravity constant to an object and take care if layout direction is RTL or not."))
print(train_df['final_annotation_type'].values[-5000:].astype(str))

print(f1_score(train_df['final_annotation_type'].values[-5000:].astype(str), val_pred, average='macro'))
print(val_pred)
