from pydantic import BaseModel
from pureml.predictor.predictor import BasePredictor
from .grade import Grader
from pureml.components import dataset
from typing import Any
from importlib import import_module
from rich import print
from pureml.schema import FastAPISchema, PredictSchema, PathSchema
from pureml.package.fastapi import get_predict_file
import shutil

prediction_schema = PredictSchema()



class Evaluator(BaseModel):
    task_type: str
    label_model: str
    label_dataset: str
    predictor: BasePredictor = None
    predictor_path: str = prediction_schema.PREDICT_NAME_TEMP
    grader: Grader = None
    dataset: Any = None

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

    def load_dataset(self):
        self.dataset = dataset.fetch(self.label_dataset)
        print("[bold green] Succesfully fetched the dataset")

    def load_predictor(self):
        get_predict_file(self.label_model,None)
        shutil.copy(prediction_schema.PATH_PREDICT, self.predictor_path)
        module_path = self.predictor_path.replace(".py", "")
        print(f"Module Path{module_path} and {self.predictor_path}")
        module_import = import_module(module_path)

        predictor_class = getattr(module_import, "Predictor")

        self.predictor = predictor_class()
        print("[bold green] Succesfully fetched the predictor")

    def load_model(self):
        self.predictor.load_models()
        print("[bold green] Succesfully fetched the model")

    def load(self):
        self.load_dataset()
        self.load_predictor()
        self.load_model()

    def evaluate(self):
        pred = self.predictor.predict(self.dataset["x_test"])
        self.grader = Grader(task_type=self.task_type)
        values = self.grader.compute(
            references=self.dataset["y_test"], predictions=pred
        )

        return values


def eval(label_model: str, label_dataset: str, task_type: str):
    evaluator = Evaluator(
        task_type=task_type, label_dataset=label_dataset, label_model=label_model
    )

    evaluator.load()

    values = evaluator.evaluate()

    return values
