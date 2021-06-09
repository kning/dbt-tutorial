import datetime

from airflow import models
from airflow.kubernetes.secret import Secret
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

secret_volume = Secret(
    deploy_type='volume',
    # Path where we mount the secret as volume
    deploy_target='/var/secrets/google',
    # Name of Kubernetes Secret
    secret='dbt-prod-service-account',
    # Key in the form of service account file name
    key='dbt-prod-service-account.json')


with models.DAG(
        dag_id='dbt_dag',
        schedule_interval=datetime.timedelta(days=1),
        start_date=YESTERDAY) as dag:
    # Only name, namespace, image, and task_id are required to create a
    # KubernetesPodOperator. In Cloud Composer, currently the operator defaults
    # to using the config file found at `/home/airflow/composer_kube_config if
    # no `config_file` parameter is specified. By default it will contain the
    # credentials for Cloud Composer's Google Kubernetes Engine cluster that is
    # created upon environment creation.

    dbt_run = KubernetesPodOperator(
        # The ID specified for the task.
        task_id='dbt-run',
        # Name of task you want to run, used to generate Pod ID.
        name='dbt-run',
        # Entrypoint of the container, if not specified the Docker container's
        # entrypoint is used. The cmds parameter is templated.
        cmds=['dbt', 'run'],
        # The namespace to run within Kubernetes, default namespace is
        # `default`. There is the potential for the resource starvation of
        # Airflow workers and scheduler within the Cloud Composer environment,
        # the recommended solution is to increase the amount of nodes in order
        # to satisfy the computing requirements. Alternatively, launching pods
        # into a custom namespace will stop fighting over resources.
        namespace='default',
        # Docker image specified. Defaults to hub.docker.com, but any fully
        # qualified URLs will point to a custom repository. Supports private
        # gcr.io images if the Composer Environment is under the same
        # project-id as the gcr.io images and the service account that Composer
        # uses has permission to access the Google Container Registry
        # (the default service account has permission)
        image='gcr.io/dbt-tutorial-314920/dbt:latest',
        # This specifies no caching policy. The default is to cache the images which gives us a headache if we only ever want the latest.
        image_pull_policy='Always',
        # Mounts the google service account json
        secrets=[secret_volume]
    )
    
    dbt_test = KubernetesPodOperator(
        # The ID specified for the task.
        task_id='dbt-test',
        # Name of task you want to run, used to generate Pod ID.
        name='dbt-test',
        # Entrypoint of the container, if not specified the Docker container's
        # entrypoint is used. The cmds parameter is templated.
        cmds=['dbt', 'test'],
        # The namespace to run within Kubernetes, default namespace is
        # `default`. There is the potential for the resource starvation of
        # Airflow workers and scheduler within the Cloud Composer environment,
        # the recommended solution is to increase the amount of nodes in order
        # to satisfy the computing requirements. Alternatively, launching pods
        # into a custom namespace will stop fighting over resources.
        namespace='default',
        # Docker image specified. Defaults to hub.docker.com, but any fully
        # qualified URLs will point to a custom repository. Supports private
        # gcr.io images if the Composer Environment is under the same
        # project-id as the gcr.io images and the service account that Composer
        # uses has permission to access the Google Container Registry
        # (the default service account has permission)
        image='gcr.io/dbt-tutorial-314920/dbt:latest',
        # This specifies no caching policy. The default is to cache the images which gives us a headache if we only ever want the latest.
        image_pull_policy='Always',
        # Mounts the google service account json
        secrets=[secret_volume]
    )

    dbt_run >> dbt_test
