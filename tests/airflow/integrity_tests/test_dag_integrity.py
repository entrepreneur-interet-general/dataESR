"""Test integrity of dags."""

import importlib
import os

import pytest
from airflow.models import DAG

DAG_PATH = os.getenv('DAGS_HOME')
DAG_FILES = [f for f in os.listdir(DAG_PATH) if f.endswith('.py')]


@pytest.mark.parametrize('dag_file', DAG_FILES)
def test_dag_integrity(dag_file):
    """Import dag files and check for DAG."""
    module_name, _ = os.path.splitext(dag_file)
    module_path = os.path.join(DAG_PATH, dag_file)
    mod_spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(module)
    assert any(
        isinstance(var, DAG)
        for var in vars(module).values())
