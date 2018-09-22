import perf
import decimal
import datetime

from dataclass_structor import structure, unstructure


def unstructure_assorted_primatives():
    unstructure("Potato")
    unstructure(1)
    unstructure(1.0)
    unstructure(True)


def structure_assorted_primatives():
    structure("Tomato", str)
    structure(1, int)
    structure(1.0, float)


def unstructure_assorted_simple_types():
    unstructure(decimal.Decimal(1.0))
    unstructure(datetime.datetime(2018, 2, 1, 2, 2, 2))
    unstructure(datetime.date(2018, 8, 28))


def structure_assorted_simple_types():
    structure("Tomato", str)
    structure(1, int)
    structure(1.0, float)


runner = perf.Runner(processes=5)
runner.bench_func('unstructure_assorted_primatives', unstructure_assorted_primatives)
runner.bench_func('structure_assorted_primatives', structure_assorted_primatives)
runner.bench_func('unstructure_assorted_simple_types', unstructure_assorted_simple_types)
runner.bench_func('structure_assorted_simple_types', structure_assorted_simple_types)
