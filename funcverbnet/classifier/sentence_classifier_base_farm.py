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
from farm.eval import Evaluator
from farm.utils import set_all_seeds, MLFlowLogger, initialize_device_settings

from funcverbnet.classifier.utils import train_data_dir, save_model_dir
from funcverbnet.utils import save_logs, LogsUtil

logger = LogsUtil.get_log_util()


class SentenceClassifier:
    set_all_seeds(seed=42)

    n_epochs = 25
    batch_size = 16

    evaluate_every = 500
    pretrained_model_name = 'bert-base-uncased'
    do_lower_case = True

    metric = ['f1_macro', 'acc']

    # [-1, 1, 2, ..., 88]
    num_labels = 89
    label_list = ['__label__-1'] + ['__label__' + str(_) for _ in range(1, num_labels)]

    ml_logger = MLFlowLogger(tracking_uri=save_logs(pretrained_model_name))

    def __init__(self):
        self.device, self.n_gpu = initialize_device_settings(use_cuda=True)
        self.data_dir = train_data_dir()
        self.save_dir = save_model_dir("sentence_classifier_base_farm_" + self.pretrained_model_name)

    def train(self):
        self.ml_logger.init_experiment(experiment_name=f'training with {self.pretrained_model_name}')
        tokenizer = Tokenizer.load(
            pretrained_model_name_or_path=self.pretrained_model_name,
            do_lower_case=self.do_lower_case
        )
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
        model = AdaptiveModel(
            language_model=LanguageModel.load(self.pretrained_model_name),
            prediction_heads=[MultiLabelTextClassificationHead(num_labels=self.num_labels)],
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
        infer = Inferencer.load(self.save_dir)
        prediction = infer.inference_from_dicts(dicts=[{"text": sentence}])
        prediction_dict = {
            'label': prediction[0]['predictions'][0]['label'],
            'probability': prediction[0]["predictions"][0]["probability"][0]
        }
        return prediction_dict

    def evaluate(self, evaluation_filename):
        tokenizer = Tokenizer.load(
            pretrained_model_name_or_path=self.save_dir,
            do_lower_case=self.do_lower_case
        )
        processor = TextClassificationProcessor(
            tokenizer=tokenizer,
            max_seq_len=360,
            data_dir=self.data_dir,
            label_list=self.label_list,
            metric=self.metric,
            text_column_name="sentence",
            label_column_name="label",
            multilabel=True,
            train_filename="",
            dev_filename=None,
            test_filename=evaluation_filename,
            dev_split=0,
        )
        data_silo = DataSilo(
            processor=processor,
            batch_size=self.batch_size
        )
        evaluator = Evaluator(
            data_loader=data_silo.get_data_loader("test"),
            tasks=data_silo.processor.tasks,
            device=self.device
        )
        model = AdaptiveModel.load(
            self.save_dir,
            device=self.device
        )
        model.connect_heads_with_processor(data_silo.processor.tasks, require_labels=True)
        result = evaluator.eval(model)
        logger.info(result[0]['loss'], result[0]['report'])
