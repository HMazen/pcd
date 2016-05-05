from Pyro4.util import SerializerBase

from utilities import *


def flow_config_class_to_dict(obj):
    return dict(__class__="flow_config", flow_id=obj.flow_id, source=obj.source, destination=obj.destination,
                protocol=obj.protocol, ps=obj.ps, ps_distro=obj.ps_distro, idt=obj.idt, idt_distro=obj.idt_distro,
                starting_date=obj.starting_date, trans_duration=obj.trans_duration,
                mesure=obj.mesure)


def flow_config_dict_to_class(classname, d):
    f = flow_config()
    f.flow_id = d["flow_id"]
    f.source = d["source"]
    f.destination = d["destination"]
    f.idt = d["idt"]
    f.idt_distro = d["idt_distro"]
    f.ps = d["ps"]
    f.ps_distro = d["ps_distro"]
    f.protocol = d["protocol"]
    f.starting_date = d["starting_date"]
    f.trans_duration = d["trans_duration"]
    f.mesure = d["mesure"]
    m = mesure_config()
    m.metrics = d["mesure"]["metrics"]
    m.sampling_interval = d["mesure"]["sampling_interval"]
    m.finish_date = d["mesure"]["finish_date"]
    m.start_date = d["mesure"]["start_date"]
    f.mesure = m
    return f


SerializerBase.register_class_to_dict(flow_config, flow_config_class_to_dict)
SerializerBase.register_dict_to_class("flow_config", flow_config_dict_to_class)


def mesure_config_class_to_dict(obj):
    return dict(__class__="mesure_config", metrics=obj.metrics, start_date=obj.start_date, finish_date=obj.finish_date,
                sampling_interval=obj.sampling_interval)


def mesure_config_dict_to_class(classname, d):
    m = mesure_config()
    m.metrics = d["metrics"]
    m.sampling_interval = d["sampling_interval"]
    m.finish_date = d["finish_date"]
    m.start_date = d["start_date"]
    return m


SerializerBase.register_class_to_dict(mesure_config, mesure_config_class_to_dict)
SerializerBase.register_dict_to_class("mesure_config", mesure_config_dict_to_class)


def metric_config_class_to_dict(obj):
    return dict(__class__="metric", name=obj.name, values=obj.values)


def metric_config_dict_to_class(classname, d):
    m = metric()
    m.name = d["name"]
    m.values = d["values"]
    return m


SerializerBase.register_class_to_dict(metric, metric_config_class_to_dict)
SerializerBase.register_dict_to_class("metric", metric_config_dict_to_class)


def result_config_class_to_dict(obj):
    return dict(__class__="result", metrics=obj.metrics, flow_id=obj.flow_id)


def result_config_dict_to_class(classname, d):
    r = result()
    r.flow_id = d["flow_id"]
    for key in d["metrics"]:
        m = metric_config_dict_to_class("metric", key)
        r.metrics.append(m)
    return r


SerializerBase.register_class_to_dict(result, result_config_class_to_dict)
SerializerBase.register_dict_to_class("result", result_config_dict_to_class)
