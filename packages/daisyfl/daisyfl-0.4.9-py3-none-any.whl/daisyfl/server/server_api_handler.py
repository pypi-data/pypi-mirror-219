from flask import Flask, request, make_response, Response
from typing import Callable
from daisyfl.server.task_manager import TaskManager
import threading
from daisyfl.common import (
    CURRENT_ROUND,
    PARTICIPATION,
    SUBTASK_RETURNS_SELECTED,
    SUBTASK_RETURNS_RESULTS,
    SUBTASK_RETURNS_FAILURES,
    SUBTASK_TIMER,
    TIMER_ROUND,
    METRICS,
    LOSS,
    ACCURACY,
)

class ServerListener:
    def __init__(
            self,
            ip: str,
            port: int,
            task_manager: TaskManager,
            cnd_stop: threading.Condition,
        ):
        self.app = Flask(__name__)
        self._ip: str = ip
        self._port: int = port
        self._task_manager: TaskManager = task_manager
        self._cnd_stop: threading.Condition = cnd_stop
        
        @self.app.route("/shutdown", methods=["POST"])
        def shutdown():
            with self._cnd_stop:
                self._cnd_stop.notify()
            return {}, 200
        
        @self.app.route("/receive_task", methods=["POST"])
        def receive_task():
            js = request.get_json()
            self._task_manager.receive_task(task_config=js)
            return js, 200
        
        @self.app.route("/metrics")
        def metrics():
            res = ""
            meta_tasks = self._task_manager.get_metrics()
            for mt in meta_tasks:
                # task id
                tid = mt.tid
                labels = "{" + "tid=\"{0}\"".format(tid) + "}"
                res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                    "task_id", "get_operating_task_ids", "gauge", labels, 87
                )
                # current_round
                res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                    "current_round", "get_current_round_of_the_task", "counter", labels, mt.subtask.config[CURRENT_ROUND]
                )
                # accuracy
                if mt.history.metrics_distributed.__contains__(ACCURACY):
                    if len(mt.history.metrics_distributed[ACCURACY]) > 0:
                        res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                            "acc_round", "x_axis_of_accuracy", "counter", labels, mt.history.metrics_distributed[ACCURACY][-1][0]
                        )
                        res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                            "accuracy", "get_accuracy_of_the_task", "gauge", labels, mt.history.metrics_distributed[ACCURACY][-1][1]
                        )
                        res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                            "loss_round", "x_axis_of_loss", "counter", labels, mt.history.losses_distributed[-1][0]
                        )
                        res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                            "loss", "get_loss_of_the_task", "gauge", labels, mt.history.losses_distributed[-1][1]
                        )
                    if mt.history.metrics_distributed.__contains__("mloss"):
                        loss_list_global = mt.history.metrics_distributed["mloss"][-1][1] # [lbox, lobj, lcls]
                        res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                            "loss_box_global", "global_loss_box", "gauge", labels, loss_list_global[0]
                        )
                        res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                            "loss_object_global", "global_loss_object", "gauge", labels, loss_list_global[1]
                        )
                        res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                            "loss_class_global", "global_loss_class", "gauge", labels, loss_list_global[2]
                        )
                # subtask_returns
                if (mt.subtask_returns.__contains__(PARTICIPATION)):
                    res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                        "subtask_round", "which_rounds_are_the_subtasks", "counter", labels, mt.subtask_returns[CURRENT_ROUND]
                    )
                    res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                        "subtask_returns_selcted", "number_of_clients_which_are_selected", "gauge", labels, mt.subtask_returns[PARTICIPATION][SUBTASK_RETURNS_SELECTED]
                    )
                    res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                        "subtask_returns_results", "number_of_clients_which_uploads_their_models_successfully", "gauge", labels, mt.subtask_returns[PARTICIPATION][SUBTASK_RETURNS_RESULTS]
                    )
                    res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                        "subtask_returns_failures", "number_of_clients_which_didn't_upload_their_models", "gauge", labels, mt.subtask_returns[PARTICIPATION][SUBTASK_RETURNS_FAILURES]
                    )
                if (mt.subtask_returns.__contains__(SUBTASK_TIMER)):
                    res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                        "subtask_timer", "time_cost_of_this_subtask", "gauge", labels, mt.subtask_returns[SUBTASK_TIMER]
                    )
                    res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                        "subtask_timer_round", "x_axis_of_time_cost", "counter", labels, mt.subtask_returns[TIMER_ROUND]
                    )


                # individual client metrics
                if (len(mt.individual_metrics) > 0):
                    for cid in list(mt.individual_metrics.keys()):
                        client_metrics = mt.individual_metrics[cid]
                        labels = "{" + "tid=\"{0}\"".format(tid) + "}"
                        res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                            "individual_metrics_round", "current_round_of_the_individual_client_metrics", "counter", labels, client_metrics[CURRENT_ROUND]
                        )
                        labels = "{" + "tid=\"{0}\", cid=\"{1}\"".format(tid, cid) + "}"
                        res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                            "client_id", "get_selected_client_ids_for_this_round", "gauge", labels, 87
                        )                        
                        if client_metrics[METRICS].__contains__(ACCURACY):
                            res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                                "accuracy_individual", "accuracy_of_the_individual_clients", "gauge", labels, client_metrics[METRICS][ACCURACY]
                            )
                        if client_metrics[METRICS].__contains__("mloss"):
                            # yolo
                            loss_list = client_metrics[METRICS]["mloss"] # [lbox, lobj, lcls]
                            res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                                "loss_box", "loss_box_of_the_individual_clients", "gauge", labels, loss_list[0]
                            )
                            res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                                "loss_object", "loss_object_of_the_individual_clients", "gauge", labels, loss_list[1]
                            )
                            res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                                "loss_class", "loss_class_of_the_individual_clients", "gauge", labels, loss_list[2]
                            )
                        res += "# HELP {0} {1}\n# TYPE {0} {2}\n{0}{3} {4}\n".format(
                            "loss_individual", "loss_of_the_individual_clients", "gauge", labels, client_metrics[LOSS]
                        )
            print(res)
            response = make_response(res)
            response.headers["content-type"] = "text/plain"
            return response

    def run(self,):
        self.app.run(host=self._ip, port=self._port)

