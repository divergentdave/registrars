from aws_lambda_builders.workflows.python_pip.workflow import PythonPipWorkflow
PythonPipWorkflow.EXCLUDED_FILES = tuple(
    pat for pat in PythonPipWorkflow.EXCLUDED_FILES
    if pat != "*.so"
)
