#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/03/30
------------------------------------------
@Modify: 2022/03/30
------------------------------------------
@Description:
"""
from farm.modeling.tokenization import Tokenizer
from farm.data_handler.data_silo import DataSilo
from farm.data_handler.processor import TextClassificationProcessor
from farm.modeling.optimization import initialize_optimizer
from farm.modeling.language_model import LanguageModel
from farm.modeling.prediction_head import MultiLabelTextClassificationHead
from farm.modeling.adaptive_model import AdaptiveModel
from farm.train import Trainer
from farm.infer import Inferencer
from farm.utils import set_all_seeds, initialize_device_settings

from utils import train_data_dir, save_model_dir


class SentenceClassifier:
    set_all_seeds(seed=42)
    device, n_gpu = initialize_device_settings(use_cuda=True)
    n_epochs = 1
    batch_size = 32

    evaluate_every = 500
    pretrained_model_name = 'bert-base-uncased'
    do_lower_case = True

    langauge_model = LanguageModel.load(pretrained_model_name)

    # [-1, 1, 2, ..., 88]
    num_labels = 89
    label_list = ['__label__-1'] + ['__label__' + str(_) for _ in range(1, num_labels)]
    metric = 'acc'

    def __init__(self):
        self.data_dir = train_data_dir()
        self.save_dir = save_model_dir("sentence_classifier_base_farm_" + self.pretrained_model_name)

    def train(self):
        tokenizer = Tokenizer.load(
            pretrained_model_name_or_path=self.pretrained_model_name,
            do_lower_case=self.do_lower_case)

        processor = TextClassificationProcessor(
            tokenizer=tokenizer,
            max_seq_len=360,
            data_dir=self.data_dir,
            label_list=self.label_list,
            metric=self.metric,
            text_column_name="sentence",
            label_column_name="label",
            multilabel=True,
            train_filename="train_data.csv",
            test_filename="test_data.csv",
            dev_split=0,
        )

        data_silo = DataSilo(
            processor=processor,
            batch_size=self.batch_size
        )

        prediction_head = MultiLabelTextClassificationHead(num_labels=self.num_labels)

        model = AdaptiveModel(
            language_model=self.langauge_model,
            prediction_heads=[prediction_head],
            embeds_dropout_prob=0.1,
            lm_output_types=['per_sequence'],
            device=self.device
        )

        model, optimizer, lr_schedule = initialize_optimizer(
            model=model,
            learning_rate=3e-5,
            device=self.device,
            n_batches=len(data_silo.loaders['train']),
            n_epochs=self.n_epochs
        )

        trainer = Trainer(
            model=model,
            optimizer=optimizer,
            data_silo=data_silo,
            epochs=self.n_epochs,
            n_gpu=self.n_gpu,
            lr_schedule=lr_schedule,
            evaluate_every=self.evaluate_every,
            device=self.device
        )

        trainer.train()

        model.save(self.save_dir)
        processor.save(self.save_dir)

    def predict(self, sentence):
        model = Inferencer.load(self.save_dir)
        result = model.inference_from_dicts(dicts=[{
            "text": sentence
        }])
        print(result)


if __name__ == '__main__':
    sentence_classifier = SentenceClassifier()
    sentence_classifier.train()
