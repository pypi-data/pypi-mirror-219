from abc import abstractmethod
from typing import Dict, List, Optional, Union

import pandas as pd

from predibase.pql.api import Session
from predibase.resource.connection import Connection
from predibase.resource.dataset import Dataset
from predibase.resource.llm import GeneratedResponse


class LlmMixin:
    session: Session

    def prompt(
        self,
        templates: Union[str, List[str]],
        model_name: Union[str, List[str]],
        index_name: Optional[Union[str, Dataset]] = None,
        dataset_name: Optional[Union[str, Dataset]] = None,
        limit: Optional[int] = None,
        options: Optional[Dict[str, float]] = None,
        return_df: bool = False,
    ) -> Union[List[GeneratedResponse], pd.DataFrame]:
        options_str = ", ".join(f"{k}={v}" for k, v in options.items()) if options else ""
        options_clause = f"WITH OPTIONS ({options_str}) " if options_str else ""

        models = [model_name] if isinstance(model_name, str) else model_name
        models_str = ", ".join(f'"{m}"' for m in models)
        model_clause = f"USING {models_str} " if models_str else ""

        index = self.get_dataset(index_name) if isinstance(index_name, str) else index_name
        index_clause = f'OVER "{index.connection.name}"."{index.name}" ' if index else ""

        dataset = self.get_dataset(dataset_name) if isinstance(dataset_name, str) else dataset_name
        limit_clause = f" LIMIT {limit}" if limit else ""
        given_clause = (
            f'GIVEN select * from "{dataset.connection.name}"."{dataset.name}"{limit_clause}' if dataset else ""
        )

        templates = [templates] if isinstance(templates, str) else templates
        templates_str = ", ".join(f"'{t}'" for t in templates)
        query_str = f"PROMPT {templates_str} {options_clause}{model_clause}{index_clause}{given_clause};"

        conn_id = None
        if isinstance(dataset, Dataset):
            conn_id = dataset.connection_id
        elif isinstance(index, Dataset):
            conn_id = index.connection_id
        else:
            conn_id = self.list_connections()[0].id

        df = self.session.execute(
            query_str,
            connection_id=conn_id,
        )
        return GeneratedResponse.to_responses(df) if not return_df else df

    def deploy_llm(self, deployment_name: str, model_name: str, engine_template: Optional[str] = None):
        self.session.post_json(
            "/llms",
            json={
                "name": deployment_name,
                "modelName": model_name,
                "engineTemplate": engine_template,
            },
        )

    def delete_llm(self, deployment_name: str):
        self.session.delete_json(f"/llms/{deployment_name}")

    @abstractmethod
    def get_dataset(self) -> Dataset:
        pass

    @abstractmethod
    def list_connections(self) -> List[Connection]:
        pass
