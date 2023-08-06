from typing import Dict, List, Optional, Tuple, Union, Callable
from queue import Queue
from daisyfl.common import (
    Code,
    Task,
    Report,
    CURRENT_ROUND,
    EVALUATE,
    TIMEOUT,
    FIT_SAMPLES,
    EVALUATE_SAMPLES,
    LOSS,
    METRICS,
    DisconnectRes,
    EvaluateIns,
    EvaluateRes,
    FitIns,
    FitRes,
    Parameters,
    ReconnectIns,
    Scalar,
    CheckResults,
    CurrentReturns,
    PARTICIPATION,
    SUBTASK_RETURNS_FAILURES,
    SUBTASK_RETURNS_RESULTS,
    SUBTASK_RETURNS_SELECTED,
    INDIVIDUAL_CLIENT_METRICS,
    CID,
)
from daisyfl.common.logger import log
from daisyfl.common.typing import GetParametersIns
from daisyfl.server.server import Server
from daisyfl.server.client_proxy import ClientProxy
from daisyfl.operator.strategy import Strategy
from threading import Condition

FitResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, FitRes]],
    List[Union[Tuple[ClientProxy, FitRes], BaseException]],
]
EvaluateResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, EvaluateRes]],
    List[Union[Tuple[ClientProxy, EvaluateRes], BaseException]],
]
ReconnectResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, DisconnectRes]],
    List[Union[Tuple[ClientProxy, DisconnectRes], BaseException]],
]


def get_configure_fit(
    strategy: Strategy,
    server_round: int,
    parameters: Parameters,
    server: Server,
    config: Dict,
    credential: str,
) -> List[Tuple[ClientProxy, FitIns]]:
    client_instructions = strategy.configure_fit(
        server_round=server_round,
        parameters=parameters,
        server=server,
        credential=credential,
    )
    for i in range(len(client_instructions)):
        client_instructions[i][1].config = config.copy()
    return client_instructions

def get_configure_evaluate(
    strategy: Strategy,
    server_round: int,
    parameters: Parameters,
    server: Server,
    config: Dict,
    credential: str,
) -> List[Tuple[ClientProxy, EvaluateIns]]:
    client_instructions = strategy.configure_evaluate(
        server_round=server_round,
        parameters=parameters,
        server=server,
        credential=credential,
    )
    for i in range(len(client_instructions)):
        client_instructions[i][1].config = config.copy()
    return client_instructions

def get_clients_from_list(
    server: Server,
    clients: List[Tuple[ClientProxy, Union[FitIns, EvaluateIns]]],
    timeout: float,
    credential: str,
) -> List[Tuple[ClientProxy, Union[FitIns, EvaluateIns]]]:
    return server.get_clients_from_list(clients=clients, timeout=timeout, credential=credential,)

def aggregate_fit(
    strategy: Strategy,
    server_round: int,
    results: List[Tuple[ClientProxy, FitRes]],
    failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]],
    selected_num: Optional[int] = None,
    results_num: Optional[int] = None,
    failures_num: Optional[int] = None,
) -> Tuple[Optional[Parameters], int, Dict[str, Scalar]]:
    """Aggregate fit results using weighted average."""
    results_for_aggregate = []
    participation = {
        SUBTASK_RETURNS_SELECTED: selected_num,
        SUBTASK_RETURNS_RESULTS: results_num,
        SUBTASK_RETURNS_FAILURES: failures_num,
    }
    calculate = (selected_num is not None) and (results_num is not None) and (failures_num is not None)

    for client, res in results:
        results_for_aggregate.append((
            client, type('',(object,),{
                "parameters": res.parameters,
                "prime": res.parameters,
                "num_examples": res.config[FIT_SAMPLES],
                "metrics": res.config[METRICS],
                "config": res.config,
            })()
        ))

        if calculate:
            # uploaded by zones
            if res.config[METRICS].__contains__(PARTICIPATION):
                participation[SUBTASK_RETURNS_SELECTED] += res.config[METRICS][PARTICIPATION][SUBTASK_RETURNS_SELECTED] - 1
                participation[SUBTASK_RETURNS_RESULTS] += res.config[METRICS][PARTICIPATION][SUBTASK_RETURNS_RESULTS] - 1
                participation[SUBTASK_RETURNS_FAILURES] += res.config[METRICS][PARTICIPATION][SUBTASK_RETURNS_FAILURES]
        
    # Aggregate training results
    parameters, metrics = strategy.aggregate_fit(server_round, results_for_aggregate, failures)
    metrics[PARTICIPATION] = participation
    # num_examples
    num_examples = int(sum([res.config[FIT_SAMPLES] for _, res in results]))
    return parameters, num_examples, metrics

def aggregate_evaluate(
    strategy: Strategy,
    server_round: int,
    results: List[Tuple[ClientProxy, EvaluateRes]],
    failures: List[Union[Tuple[ClientProxy, EvaluateRes], BaseException]],
) -> Tuple[Optional[float], int, Dict[str, Scalar]]:
    """Aggregate evaluation losses using weighted average."""
    results_for_aggregate = []
    individual_metrics = {}
    for client, res in results:
        results_for_aggregate.append((
            client, type('',(object,),{
                "loss": res.config[LOSS],
                "num_examples": res.config[EVALUATE_SAMPLES],
                "metrics": res.config[METRICS],
                "config": res.config,
            })()
        ))
        # uploaded by clients
        if not res.config[METRICS].__contains__(INDIVIDUAL_CLIENT_METRICS):
            individual_metrics[res.config[CID]] = {
                CURRENT_ROUND: res.config[CURRENT_ROUND],
                LOSS: res.config[LOSS],
                METRICS: res.config[METRICS]
            }
        # uploaded by zones
        else:
            individual_metrics.update(res.config[METRICS][INDIVIDUAL_CLIENT_METRICS])

    # Aggregate the evaluation results
    loss, metrics = strategy.aggregate_evaluate(server_round, results_for_aggregate, failures)
    metrics[INDIVIDUAL_CLIENT_METRICS] = individual_metrics
    # num_examples
    num_examples = int(sum([res.config[EVALUATE_SAMPLES] for _, res in results]))
    return loss, num_examples, metrics

def generate_fit_report(
    server_round: int,
    samples: int,
    metrics_aggregated: Dict[str, Scalar],
)-> Report:
    return Report(config={
        CURRENT_ROUND: server_round,
        FIT_SAMPLES: samples,
        METRICS: metrics_aggregated,
    })
    
def generate_evaluate_report(
    server_round: int,
    samples: int,
    loss_aggregated: Optional[float],
    metrics_aggregated: Dict[str, Scalar],
) -> Report:
    # (loss, num_examples, metrics) -> Report
    return Report(config={
        CURRENT_ROUND: server_round,
        LOSS: loss_aggregated,
        EVALUATE_SAMPLES: samples,
        METRICS: metrics_aggregated,
    })

def wait_for_results(
    strategy: Strategy, current_returns: CurrentReturns,
) -> bool:
    cnd = current_returns.cnd
    with cnd:
        cnd.wait_for(lambda: strategy.check_results(current_returns) in [CheckResults.OK, CheckResults.FAIL])
    if strategy.check_results(current_returns) == CheckResults.OK:
        return True
    return False
