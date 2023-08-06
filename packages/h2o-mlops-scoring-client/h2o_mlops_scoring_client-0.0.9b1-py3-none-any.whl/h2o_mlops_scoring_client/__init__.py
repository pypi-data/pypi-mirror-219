import datetime as _datetime
import logging as _logging
import os as _os
import typing as _typing

import pandas as _pandas
import pyspark as _pyspark

from h2o_mlops_scoring_client import _utils
from h2o_mlops_scoring_client._utils import Format
from h2o_mlops_scoring_client._utils import WriteMode
from h2o_mlops_scoring_client._version import version as __version__  # noqa: F401


_logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%y/%m/%d %H:%M:%S",
    level=_logging.INFO,
)
logger = _logging.getLogger(__name__)
spark_conf_dir = _os.environ.get("SPARK_CONF_DIR")
spark_master = _os.environ.get("MASTER", "local[*]")
if spark_master.startswith("local"):
    # quiet spark warnings
    import importlib.resources

    try:
        resource = importlib.resources.files(  # type: ignore
            "h2o_mlops_scoring_client"
        ).joinpath("log4j.properties")
    except AttributeError:
        # fallback for Python < 3.9
        with importlib.resources.path(
            "h2o_mlops_scoring_client", "log4j.properties"
        ) as resource:
            pass
    _os.environ["LOG4J_CONFIGURATION_FILE"] = str(resource)
    # ignore local SPARK_HOME
    _os.environ.pop("SPARK_HOME", None)


def get_capabilities(
    mlops_endpoint_url: str, passphrase: _typing.Optional[str] = None
) -> _typing.List[str]:
    """Capabilities of the scoring endpoint.

    Args:
        mlops_endpoint_url: MLOps deployment scoring endpoint URL
        passphrase: passphrase for protected MLOps endpoint
    """
    return _utils.MLOpsEndpoint(mlops_endpoint_url, passphrase).capabilities


def get_experiment_id(
    mlops_endpoint_url: str, passphrase: _typing.Optional[str] = None
) -> str:
    """ID of experiment used for scoring by the scoring endpoint.

    Args:
        mlops_endpoint_url: MLOps deployment scoring endpoint URL
        passphrase: passphrase for protected MLOps endpoint
    """
    return _utils.MLOpsEndpoint(mlops_endpoint_url, passphrase).experiment_id


def get_schema(
    mlops_endpoint_url: str, passphrase: _typing.Optional[str] = None
) -> _typing.Dict[str, _typing.Any]:
    """Column names and types expected by the scoring endpoint.

    Args:
        mlops_endpoint_url: MLOps deployment scoring endpoint URL
        passphrase: passphrase for protected MLOps endpoints
    """
    return _utils.MLOpsEndpoint(mlops_endpoint_url, passphrase).schema


def get_spark_session(
    app_name: str = "h2o_mlops_scoring_client",
    mini_batch_size: int = 1000,
    spark_config_overrides: _typing.Optional[_typing.Dict[str, str]] = None,
) -> _pyspark.sql.SparkSession:
    """Get or create a Spark session configured for the scoring client.

    Args:
        app_name: name of application in Spark
        mini_batch_size: number of rows per scorer call
        spark_config_overrides: pass Spark configuration options to the Spark context
    """

    if spark_master.startswith("local") and spark_conf_dir:
        _utils.preflight(spark_conf_dir)
        _os.environ["SPARK_CONF_DIR"] = _os.path.abspath(spark_conf_dir)
    spark = _utils.get_spark_session(
        app_name=app_name,
        master=spark_master,
        mini_batch_size=mini_batch_size,
        spark_config=spark_config_overrides,
    )
    return spark


def score_source_sink(
    *,
    mlops_endpoint_url: str,
    id_column: str,
    source_data: str,
    source_format: Format,
    sink_location: str,
    sink_format: Format,
    sink_write_mode: WriteMode,
    passphrase: _typing.Optional[str] = None,
    source_config: _typing.Optional[_typing.Dict[str, str]] = None,
    sink_config: _typing.Optional[_typing.Dict[str, str]] = None,
    preprocess_method: _typing.Optional[_typing.Callable] = None,
    postprocess_method: _typing.Optional[_typing.Callable] = None,
    mini_batch_size: int = 1000,
    spark_config_overrides: _typing.Optional[_typing.Dict[str, str]] = None,
) -> None:
    """Use Spark to do parallelized scoring in mini-batches against a MLOps deployment.

    Args:
        mlops_endpoint_url: MLOps deployment scoring endpoint URL
        id_column: name of column in data to be scored
            - column should contain unique row identifiers
        source_data: path or query for data to be scored
        source_format: file type or table type data to be scored is stored in
        sink_location: path or query for scored data to be written to
        sink_format: file type or table type for scored data when written
        sink_write_mode: write behavior when data already exists in sink location
        passphrase: passphrase for protected MLOps endpoint
        source_config: pass Spark data source options for the specified format
            (useful for JDBC_QUERY and JDBC_TABLE formats)
        sink_config: pass Spark data source options for the specified format
            (useful for JDBC_QUERY and JDBC_TABLE formats)
        preprocess_method: method that takes and returns a Spark dataframe
            before scoring
        postprocess_method: method that takes and returns a Spark dataframe
            after scoring
        mini_batch_size: number of rows per scorer call
        spark_config_overrides: pass Spark configuration options to the Spark context
    """
    try:
        start = _datetime.datetime.now().replace(microsecond=0)

        spark = get_spark_session(
            mini_batch_size=mini_batch_size,
            spark_config_overrides=spark_config_overrides,
        )

        logger.info(f"Connecting to H2O.ai MLOps scorer at '{mlops_endpoint_url}'")
        mlops_endpoint = _utils.MLOpsEndpoint(mlops_endpoint_url, passphrase)

        sdf = _utils.read_source(spark, source_data, source_format, source_config)

        if preprocess_method:
            logger.info("Applying preprocess method")
            sdf = preprocess_method(sdf)

        logger.info(f"Starting scoring from '{source_data}' to '{sink_location}'")
        start_scoring = _datetime.datetime.now().replace(microsecond=0)
        scored_sdf = mlops_endpoint.score_spark_dataframe(sdf, id_column=id_column)

        if postprocess_method:
            logger.info("Applying postprocess method")
            scored_sdf = postprocess_method(scored_sdf)

        _utils.write_sink(
            scored_sdf, sink_location, sink_format, sink_write_mode, sink_config
        )

        logger.info("Scoring complete")
        stop = _datetime.datetime.now().replace(microsecond=0)

        logger.info(f"Total run time: {stop - start}")
        logger.info(f"Scoring run time: {stop - start_scoring}")

    finally:
        if spark_master.startswith("local"):
            try:
                spark.stop()
            except UnboundLocalError:
                pass


def score_data_frame(
    *,
    mlops_endpoint_url: str,
    id_column: str,
    data_frame: _typing.Union[_pandas.DataFrame, _pyspark.sql.DataFrame],
    mini_batch_size: int = 1000,
    passphrase: _typing.Optional[str] = None,
    spark_config_overrides: _typing.Optional[_typing.Dict[str, str]] = None,
) -> _typing.Union[_pandas.DataFrame, _pyspark.sql.DataFrame]:
    """Do scoring of a data frame against a MLOps deployment. Parallelized mini-batch
    scoring with Spark is done if the data frame row count is more than mini_batch_size.

    Args:
        mlops_endpoint_url: MLOps deployment scoring endpoint URL
        id_column: name of column in data to be scored
            - column should contain unique row identifiers
        data_frame: Pandas DataFrame
        mini_batch_size: number of rows per scorer call
        passphrase: passphrase for protected MLOps endpoint
        spark_config_overrides: pass Spark configuration options to the Spark context
    """
    if (
        isinstance(data_frame, _pandas.DataFrame)
        and data_frame.shape[0] <= mini_batch_size
    ):
        return _score_data_frame_direct(
            mlops_endpoint_url=mlops_endpoint_url,
            passphrase=passphrase,
            id_column=id_column,
            data_frame=data_frame,
        )
    else:
        return _score_data_frame_spark(
            mlops_endpoint_url=mlops_endpoint_url,
            passphrase=passphrase,
            id_column=id_column,
            data_frame=data_frame,
            mini_batch_size=mini_batch_size,
            spark_config_overrides=spark_config_overrides,
        )


def _score_data_frame_direct(
    *,
    mlops_endpoint_url: str,
    id_column: str,
    data_frame: _pandas.DataFrame,
    passphrase: _typing.Optional[str] = None,
) -> _pandas.DataFrame:
    start = _datetime.datetime.now().replace(microsecond=0)

    logger.info(f"Connecting to H2O.ai MLOps scorer at '{mlops_endpoint_url}'")
    mlops_endpoint = _utils.MLOpsEndpoint(mlops_endpoint_url, passphrase)

    logger.info("Starting scoring data frame")
    start_scoring = _datetime.datetime.now().replace(microsecond=0)
    scored_df = mlops_endpoint.score_pandas_dataframe(data_frame, id_column=id_column)

    logger.info("Scoring complete")
    stop = _datetime.datetime.now().replace(microsecond=0)

    logger.info(f"Total run time: {stop - start}")
    logger.info(f"Scoring run time: {stop - start_scoring}")

    return scored_df


def _score_data_frame_spark(
    *,
    mlops_endpoint_url: str,
    id_column: str,
    data_frame: _typing.Union[_pandas.DataFrame, _pyspark.sql.DataFrame],
    mini_batch_size: int = 1000,
    passphrase: _typing.Optional[str] = None,
    spark_config_overrides: _typing.Optional[_typing.Dict[str, str]] = None,
) -> _typing.Union[_pandas.DataFrame, _pyspark.sql.DataFrame]:
    try:
        start = _datetime.datetime.now().replace(microsecond=0)

        is_pandas = isinstance(data_frame, _pandas.DataFrame)

        spark = get_spark_session(
            mini_batch_size=mini_batch_size,
            spark_config_overrides=spark_config_overrides,
        )

        logger.info(f"Connecting to H2O.ai MLOps scorer at '{mlops_endpoint_url}'")
        mlops_endpoint = _utils.MLOpsEndpoint(mlops_endpoint_url, passphrase)

        if is_pandas:
            sdf = spark.createDataFrame(data_frame)
        else:
            sdf = data_frame

        logger.info("Starting scoring data frame")
        start_scoring = _datetime.datetime.now().replace(microsecond=0)
        scored_sdf = mlops_endpoint.score_spark_dataframe(sdf, id_column=id_column)

        logger.info("Scoring complete")

        if is_pandas:
            scored_df = scored_sdf.toPandas()
        else:
            scored_df = scored_sdf

        stop = _datetime.datetime.now().replace(microsecond=0)

        logger.info(f"Total run time: {stop - start}")
        logger.info(f"Scoring run time: {stop - start_scoring}")

        return scored_df

    finally:
        if is_pandas and spark_master.startswith("local"):
            try:
                spark.stop()
            except UnboundLocalError:
                pass
