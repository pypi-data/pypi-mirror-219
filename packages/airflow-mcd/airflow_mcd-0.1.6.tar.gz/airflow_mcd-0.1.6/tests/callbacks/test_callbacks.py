import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from unittest import TestCase
from unittest.mock import create_autospec, patch

import pytz
from airflow.models import DagRun, TaskInstance, SlaMiss, DAG
from sgqlc.types import Variable

from airflow_mcd.callbacks.client import AirflowEventsClient, AirflowEnv
from airflow_mcd.callbacks.utils import AirflowEventsClientUtils


# needed to have a successful assert_called_with as Variable doesn't implement __eq__
class EqVariable(Variable):
    def __eq__(self, other):
        return other.name == self.name



class CallbacksTests(TestCase):
    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_dag_result_success(self,  mock_client_upload_result):
        self._test_upload_dag_result(True, mock_client_upload_result)

    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_dag_result_failure(self, mock_client_upload_result):
        self._test_upload_dag_result(False, mock_client_upload_result)

    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_task_result_success(self, mock_client_upload_result):
        self._test_upload_task_result(True, False, mock_client_upload_result)

    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_task_result_failure(self, mock_client_upload_result):
        self._test_upload_task_result(False, False, mock_client_upload_result)

    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_task_result_running(self, mock_client_upload_result):
        self._test_upload_task_result(True, True, mock_client_upload_result)

    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_sla_misses(self, mock_client_upload_result):
        utils = AirflowEventsClientUtils()

        dag = create_autospec(DAG)
        dag.dag_id = "dag_123"
        dag.params = {}

        sla_miss_1 = create_autospec(SlaMiss)
        sla_miss_1.task_id = "task_123"
        sla_miss_1.execution_date = datetime.now(tz=pytz.UTC) - timedelta(seconds=10)
        sla_miss_1.timestamp = datetime.now(tz=pytz.UTC)

        sla_miss_2 = create_autospec(SlaMiss)
        sla_miss_2.task_id = "task_234"
        sla_miss_2.execution_date = datetime.now(tz=pytz.UTC) - timedelta(seconds=10)
        sla_miss_2.timestamp = datetime.now(tz=pytz.UTC)

        sla_misses = [
            sla_miss_1,
            sla_miss_2,
        ]
        utils.mcd_post_sla_misses(dag, sla_misses)

        mock_client_upload_result.assert_called()
        mock_client_upload_result.assert_called_with(
            AirflowEventsClient._UPLOAD_AIRFLOW_SLA_MISSES_OPERATION,
            {
                "dag_id": dag.dag_id,
                "env": self._get_graphql_env(),
                "payload": EqVariable("payload"),
            },
            {
                "event_type": "sla_miss",
                "dag_id": dag.dag_id,
                "env": self._get_env(),
                "sla_misses": [
                    {
                        "task_id": m.task_id,
                        "execution_date": m.execution_date.isoformat(),
                        "timestamp": m.timestamp.isoformat(),
                    }
                    for m in sla_misses
                ]
            }
        )

    def test_env_loading(self):
        no_env = AirflowEnv()
        self.assertEqual("airflow", no_env.env_name)
        self.assertIsNone(no_env.env_id)
        self.assertIsNone(no_env.version)
        self.assertIsNone(no_env.base_url)

        # AWS
        with patch.dict(os.environ, {
            "AIRFLOW_ENV_NAME": "aws_env_name",
            "AIRFLOW_ENV_ID": "aws_env_id",
            "AIRFLOW_VERSION": "aws_version",
            "AIRFLOW__WEBSERVER__BASE_URL": "aws_url",
        }):
            env = AirflowEnv()
            self.assertEqual("aws_env_name", env.env_name)
            self.assertEqual("aws_env_id", env.env_id)
            self.assertEqual("aws_version", env.version)
            self.assertEqual("aws_url", env.base_url)

        # GCP Composer
        with patch.dict(os.environ, {
            "COMPOSER_ENVIRONMENT": "gcp_env_name",
            "COMPOSER_GKE_NAME": "gcp_env_id",
            "MAJOR_VERSION": "gcp_version",
            "AIRFLOW__WEBSERVER__BASE_URL": "gcp_url",
        }):
            env = AirflowEnv()
            self.assertEqual("gcp_env_name", env.env_name)
            self.assertEqual("gcp_env_id", env.env_id)
            self.assertEqual("gcp_version", env.version)
            self.assertEqual("gcp_url", env.base_url)

        # Astronomer
        with patch.dict(os.environ, {
            "AIRFLOW__WEBSERVER__INSTANCE_NAME": "astro_env_name",
            "ASTRO_DEPLOYMENT_ID": "astro_env_id",
            "ASTRONOMER_RUNTIME_VERSION": "astro_version",
            "AIRFLOW__WEBSERVER__BASE_URL": "astro_url",
        }):
            env = AirflowEnv()
            self.assertEqual("astro_env_name", env.env_name)
            self.assertEqual("astro_env_id", env.env_id)
            self.assertEqual("astro_version", env.version)
            self.assertEqual("astro_url", env.base_url)

        params_env = AirflowEnv(
            env_name="name",
            env_id="id",
            version="1.0",
            base_url="url"
        )
        self.assertEqual("name", params_env.env_name)
        self.assertEqual("id", params_env.env_id)
        self.assertEqual("1.0", params_env.version)
        self.assertEqual("url", params_env.base_url)

    def _test_upload_dag_result(
            self,
            success: bool,
            mock_client_upload_result
    ):
        dag_context = self._create_dag_context(success)
        dag: DAG = dag_context["dag"]
        dag_run: DagRun = dag_context["dag_run"]
        task_instances: List[TaskInstance] = dag_run.get_task_instances()

        utils = AirflowEventsClientUtils()
        utils.mcd_post_dag_result(dag_context, success)

        mock_client_upload_result.assert_called()
        mock_client_upload_result.assert_called_with(
            AirflowEventsClient._UPLOAD_AIRFLOW_DAG_RESULT_OPERATION,
            {
                "dag_id": dag.dag_id,
                "run_id": dag_context["run_id"],
                "success": success,
                "reason": dag_context.get("reason"),
                "state": dag_run.state,
                "execution_date": dag_run.execution_date.isoformat(),
                "start_date": dag_run.start_date.isoformat(),
                "end_date": dag_run.end_date.isoformat(),
                "env": self._get_graphql_env(),
                "payload": EqVariable("payload"),
            },
            {
                "dag_id": dag.dag_id,
                "env": self._get_env(),
                "run_id": dag_context["run_id"],
                "success": success,
                "tasks": [
                    self._get_dag_task_instance_result(ti) for ti in task_instances
                ],
                "state": dag_run.state,
                "execution_date": dag_run.execution_date.isoformat(),
                "start_date": dag_run.start_date.isoformat(),
                "end_date": dag_run.end_date.isoformat(),
                "reason": dag_context.get("reason"),
                "event_type": "dag",
            }
        )

    @staticmethod
    def _get_graphql_env() -> Dict:
        return {
            "env_name": "airflow",
        }

    @staticmethod
    def _get_env() -> Dict:
        return {
            "env_name": "airflow",
            "env_id": None,
            "version": None,
            "base_url": None
        }

    def _create_dag_context(self, success: bool, task_running: bool = False) -> Dict:
        dag = create_autospec(DAG)
        dag.dag_id = "dag_123"
        dag.params = {}
        dag_run = create_autospec(DagRun)
        task_instances = [
            self._create_task_instance(
                dag_id=dag.dag_id,
                task_id="task_123",
                state="running" if task_running else "success",
                running=task_running,
            ),
            self._create_task_instance(
                dag_id=dag.dag_id,
                task_id="task_234",
                state="success",
            ),
        ]
        state = "success" if success else "failed"
        dag_run.get_task_instances.return_value = task_instances
        dag_run.state = state
        dag_run.execution_date = datetime.now(tz=pytz.UTC) - timedelta(seconds=10)
        dag_run.start_date = datetime.now(tz=pytz.UTC) - timedelta(seconds=9)
        dag_run.end_date = datetime.now(tz=pytz.UTC)

        dag_context = {
            "dag": dag,
            "run_id": '123',
            "dag_run": dag_run,
            "reason": "succeeded" if success else "task failed",
        }
        return dag_context

    def _test_upload_task_result(
            self,
            success: bool,
            task_running: bool,
            mock_client_upload_result
    ):
        dag_context = self._create_dag_context(success, task_running)
        state = "running" if task_running else "success" if success else "failed"
        exception_message: str = "task failed" if not success else None
        if not success:
            dag_context["exception"] = Exception(exception_message)
        dag: DAG = dag_context["dag"]
        dag_run: DagRun = dag_context["dag_run"]
        task_instances: List[TaskInstance] = dag_run.get_task_instances()
        task_instance = task_instances[0]
        task_instance.state = state
        dag_context["task_instance"] = task_instance
        utils = AirflowEventsClientUtils()
        utils.mcd_post_task_result(success, dag_context)

        expected_graphql_payload = {
            "dag_id": dag.dag_id,
            "run_id": dag_context["run_id"],
            "task_id": task_instance.task_id,
            "success": success,
            "env": self._get_graphql_env(),
            "state": state,
            "log_url": f"http://airflow.com/{dag.dag_id}/{task_instance.task_id}/log",
            "execution_date": task_instance.execution_date.isoformat(),
            'start_date': task_instance.start_date.isoformat(),
            'end_date': task_instance.end_date.isoformat(),
            'duration': task_instance.duration or 0,
            'attempt_number': task_instance.prev_attempted_tries,
            "payload": EqVariable("payload"),
        }
        if exception_message and not success:
            expected_graphql_payload["exception_message"] = exception_message

        mock_client_upload_result.assert_called()
        mock_client_upload_result.assert_called_with(
            AirflowEventsClient._UPLOAD_AIRFLOW_TASK_RESULT_OPERATION,
            expected_graphql_payload,
            {
                "dag_id": dag.dag_id,
                "env": self._get_env(),
                "run_id": dag_context["run_id"],
                "success": success,
                "task": self._get_dag_task_instance_result(task_instance, exception_message),
                "event_type": "task",
            }
        )

    @staticmethod
    def _create_task_instance(dag_id: str, task_id: str, state: str, running: bool = False) -> TaskInstance:
        task_instance = create_autospec(TaskInstance)
        task_instance.task_id = task_id
        task_instance.state = state
        task_instance.log_url = f"http://airflow.com/{dag_id}/{task_instance.task_id}/log"
        task_instance.prev_attempted_tries = 0
        task_instance.duration = 10.5 if not running else None
        task_instance.execution_date = datetime.now(tz=pytz.UTC) - timedelta(seconds=10)
        task_instance.start_date = datetime.now(tz=pytz.UTC) - timedelta(seconds=9)
        task_instance.end_date = datetime.now(tz=pytz.UTC)
        task_instance.max_tries = 3
        task_instance.try_number = 1
        return task_instance

    @staticmethod
    def _get_dag_task_instance_result(task_instance: TaskInstance, exception_message: Optional[str] = None) -> Dict:
        return {
            "task_id": task_instance.task_id,
            "state": task_instance.state,
            "log_url": task_instance.log_url,
            "prev_attempted_tries": task_instance.prev_attempted_tries,
            "duration": task_instance.duration or 0,
            "execution_date": task_instance.execution_date.isoformat(),
            "start_date": task_instance.start_date.isoformat(),
            "end_date": task_instance.end_date.isoformat(),
            "next_retry_datetime": None,
            "max_tries": task_instance.max_tries,
            "try_number": task_instance.try_number,
            "exception_message": exception_message,
            "inlets": None,
            "outlets": None,
        }

