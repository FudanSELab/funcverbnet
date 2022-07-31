import os
from pathlib import Path

# from pyfasttext import FastText
from fasttext import FastText

root_path = os.path.abspath(os.path.dirname(__file__)).split('model.py')[0]
path = Path(root_path)
# DATA_PATH = str(path / "data" / "final_train_data.csv")
DATA_PATH = str(path / "data" / "new_train_data.csv")
TEST_DATA_PATH = str(path / "data" / "test_data.csv")


class FuncSentenceClassifier:
    def __init__(self):
        self.classifier = None
        self.train_data_path = DATA_PATH
        self.test_data_path = TEST_DATA_PATH
        self.model_path = str(path / "model" / "sentence_classification_new.model")
        self.load_model()
        # self.train_model()

    def load_model(self, ):
        """
        load fast-text model
        :return:
        """
        if os.path.exists(self.model_path):
            self.classifier = FastText.load_model(self.model_path)
        else:
            print("no such model, train now")
            self.train_model()

    def set_model_path(self, new_path):
        """
        set model path
        :param new_path: str
        :return:
        """
        self.model_path = new_path

    def train_model(self):
        """
        train fast-text model
        :return:
        """
        classifier = FastText.train_supervised(input=self.train_data_path, lr=1, ws=4, loss="hs", epoch=25)
        # classifier = FastText.train_supervised(input=self.train_data_path, lr=1, wordNgrams=2, verbose=2, minCount=1, epoch=25, loss="hs")

        classifier.save_model(self.model_path)
        self.classifier = classifier
        print("test result in training data:")
        result = classifier.test(self.train_data_path)
        print(result)
        print("test result in testing data:")
        result = classifier.test(self.test_data_path)
        print(result)

    def predict(self, sentence):
        """
        give a sentence, return the most similar sentence and score
        :param sentence: str
        :return: (str,score)
        """
        try:
            label = self.classifier.predict(sentence)
            # print(self.classifier.predict(sentence, k=5))
            # print('probability', label[1][0])
            if len(str(label[0][0])) > 10:
                label = str(label[0][0][9]) + str(label[0][0][10])
            else:
                label = str(label[0][0][9])
            return int(label)
        except Exception as e:
            print(e, sentence)
            return 0

    # def multi_predict(self, sentence, top_k):
    #     try:
    #         labels = self.classifier.predict(sentence, k=top_k)
    #     except Exception as e:
    #         print(e, sentence)

    def new_predict(self, sentence):
        try:
            label = self.classifier.predict(sentence)
            probability = label[1][0]
            if len(str(label[0][0])) > 10:
                label = str(label[0][0][9]) + str(label[0][0][10])
            else:
                label = str(label[0][0][9])
            return int(label), probability
        except Exception as e:
            print(e)

    # def data_select(self, sentence_list, limit):
    #     """
    #     given a list of sentence, select the best quality sentences based the limited number
    #     :param sentence_list: list
    #     :param limit: int
    #     :return: list of str
    #     """
    #     sentence2score = {}
    #     for sentecte_item in sentence_list:
    #         sentence = sentecte_item
    #         if isinstance(sentecte_item, Sentence):
    #             sentence = sentecte_item.sentence
    #         label, score = self.predict(sentence)
    #         if label == 0:
    #             # score -= 1
    #             continue
    #         sentence2score[sentecte_item] = score
    #     sorted_sentence2score = sorted(sentence2score.items(), key=lambda x: x[1], reverse=True)
    #     return sorted_sentence2score[:limit]

    # def cal_experiment_indexes(self, path, data_type="train_data"):
    #     """
    #     path of train data or test data, they have real labels
    #     :param path: str
    #     :return:
    #     """
    #     with open(path, 'r', encoding="utf8") as f:
    #         content = f.read().splitlines()
    #     label_list = []
    #     save_list = []
    #     for item in content:
    #         real_label = int(item[9])
    #         sentence = item[12:]
    #         predict_label, _ = self.predict(sentence)
    #         label_list.append((real_label, predict_label))
    #         save_list.append(
    #             {"sentence": sentence, "real_label": real_label, "predict_label": predict_label, "score": _})
    #     with open(self.data_dir / ("result_for_" + data_type + ".json"), "w") as f:
    #         json.dump(save_list, f)
    #     return self.experiment_indexes(label_list)
    #
    # def experiment_indexes(self, data_list):
    #     """
    #     [(real label, predict label)...]
    #     :param data_list: data contain real label and predict label
    #     :return:
    #     """
    #     num_tp = 0
    #     num_fn = 0
    #     num_fp = 0
    #     num_tn = 0
    #     for real_label, predict_label in data_list:
    #         if real_label == 1 and predict_label == 1:
    #             num_tp += 1
    #         elif real_label == 1 and predict_label == 0:
    #             num_fn += 1
    #         elif real_label == 0 and predict_label == 1:
    #             num_fp += 1
    #         elif real_label == 0 and predict_label == 0:
    #             num_tn += 1
    #     if num_tp == 0:
    #         precision_p = 0
    #         recall_p = 0
    #         f_1_p = 0
    #     else:
    #         precision_p = num_tp / (num_tp + num_fp)
    #         recall_p = num_tp / (num_tp + num_fn)
    #         f_1_p = (2 * precision_p * recall_p) / (precision_p + recall_p)
    #
    #     if num_tn == 0:
    #         precision_n = 0
    #         recall_n = 0
    #         f_1_n = 0
    #     else:
    #         precision_n = num_tn / (num_fn + num_tn)
    #         recall_n = num_tn / (num_fp + num_tn)
    #         f_1_n = (2 * precision_n * recall_n) / (precision_n + recall_n)
    #
    #     accuracy = (num_tp + num_tn) / (num_tp + num_fn + num_fp + num_tn)
    #
    #     print("1  precision:{}  recall:{}  f1:{}  support:{}".format(precision_p, recall_p, f_1_p, num_tp + num_fn))
    #     print("0  precision:{}  recall:{}  f1:{}  support:{}".format(precision_n, recall_n, f_1_n, num_fp + num_tn))
    #     print("accuracy: ", accuracy)
    #     return {"1": {"precision": precision_p, "recall": recall_p, "f1": f_1_p, "support": num_tp + num_fn},
    #             "0": {"precision": precision_n, "recall": recall_n, "f1": f_1_n, "support": num_fp + num_tn}
    #             }
