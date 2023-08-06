import datetime
import uuid
import enum
from dataclasses import field
from pydantic.dataclasses import dataclass
import numpy as np
from pydantic import validator, constr
from typing import Union, Any, Dict, List
import pint.errors

import sunpeek.components as cmp
from sunpeek.common.unit_uncertainty import Q
from sunpeek.components.base import IsVirtual
from sunpeek.components.helpers import SensorMap, DatetimeTemplates, AccuracyClass, InstallCondition
from sunpeek.components.fluids import UninitialisedFluid
from sunpeek.base_model import BaseModel


class ComponentBase(BaseModel):
    sensor_map: Union[Dict[str, Union[str, None]], None]

    @validator('sensor_map', pre=True)
    def get_raw_name(cls, v):
        out = {}
        for key, item in v.items():
            if isinstance(item, SensorMap):
                try:
                    out[key] = item.sensor.raw_name
                except AttributeError:
                    pass
            else:
                out[key] = item
        return out


def np_to_list(val):
    if isinstance(val, np.ndarray) and val.ndim == 1:
        return list(val)
    elif isinstance(val, np.ndarray) and val.ndim > 1:
        out = []
        for array in list(val):
            out.append(np_to_list(array))
        return out
    return val


class Quantity(BaseModel):
    magnitude: Union[float, List[float], List[List[float]]]
    units: str

    @validator('magnitude', pre=True)
    def convert_numpy(cls, val):
        return np_to_list(val)

    @validator('units', pre=True)
    def pretty_unit(cls, val):
        if isinstance(val, pint.Unit):
            return f"{val:~P}"
        return val


class SensorTypeValidator(BaseModel):
    name: str
    compatible_unit_str: str
    description: Union[str, None]
    # min_limit: Union[Quantity, None]
    # max_limit: Union[Quantity, None]
    # # non_neg: bool
    # max_fill_period: Union[datetime.timedelta, None]
    # sensor_hangs_period: Union[datetime.timedelta, None]
    # # high_maxerr_const: Union[Quantity, None]
    # # high_maxerr_perc: Union[Quantity, None]
    # # medium_maxerr_const: Union[Quantity, None]
    # # medium_maxerr_perc: Union[Quantity, None]
    # # low_maxerr_const: Union[Quantity, None]
    # # low_maxerr_perc: Union[Quantity, None]
    # # standard_install_maxerr_const: Union[Quantity, None]
    # # standard_install_maxerr_perc: Union[Quantity, None]
    # # poor_install_maxerr_const: Union[Quantity, None]
    # # poor_install_maxerr_perc: Union[Quantity, None]
    info_checks: Union[dict, None]
    max_fill_period: Union[datetime.timedelta, None]
    sensor_hangs_period: Union[datetime.timedelta, None]
    lower_replace_min: Union[Quantity, None]
    lower_replace_max: Union[Quantity, None]
    lower_replace_value: Union[Quantity, None]
    upper_replace_min: Union[Quantity, None]
    upper_replace_max: Union[Quantity, None]
    upper_replace_value: Union[Quantity, None]
    equation: Union[str, None]
    common_units: Union[list, None]


class IAM_Method(BaseModel):
    method_type: str


class IAM_ASHRAE(IAM_Method):
    method_type = 'ASHRAE'
    b: Quantity


class IAM_K50(IAM_Method):
    method_type = 'K50'
    k50: Quantity


class IAM_Ambrosetti(IAM_Method):
    method_type = 'Ambrosetti'
    kappa: Quantity


class IAM_Interpolated(IAM_Method):
    method_type = 'Interpolated'
    aoi_reference: Quantity
    iam_reference: Quantity


class CollectorTypeBase(BaseModel):
    test_reference_area: str
    test_type: str
    gross_length: Quantity
    iam_method: Union[IAM_ASHRAE, IAM_K50, IAM_Ambrosetti, IAM_Interpolated, None]
    name: str
    manufacturer_name: Union[str, None]
    product_name: Union[str, None]
    test_report_id: Union[str, None]
    licence_number: Union[str, None]
    certificate_date_issued: Union[str, datetime.datetime, None]
    certificate_lab: Union[str, None]
    certificate_details: Union[str, None]
    area_gr: Union[Quantity, None]
    area_ap: Union[Quantity, None]
    gross_width: Union[Quantity, None]
    gross_height: Union[Quantity, None]
    a1: Union[Quantity, None]
    a2: Union[Quantity, None]
    a5: Union[Quantity, None]
    kd: Union[Quantity, None]
    eta0b: Union[Quantity, None]
    eta0hem: Union[Quantity, None]
    f_prime: Union[Quantity, None]


class CollectorType(CollectorTypeBase):
    id: int
    b0: Union[Quantity, None]
    kb_50: Union[Quantity, None]
    khem_50: Union[Quantity, None]


class CollectorTypeQDT(CollectorTypeBase):
    a1: Quantity
    a2: Quantity
    a5: Quantity


class CollectorTypeSST(CollectorTypeBase):
    ceff: Quantity


class SensorBase(BaseModel):
    description: Union[str, None]
    accuracy_class: Union[AccuracyClass, None]
    installation_condition: Union[InstallCondition, None]
    info: Union[dict, None] = {}
    raw_name: Union[str, None]
    native_unit: Union[str, None]

    @validator('info', pre=True)
    def convert_info(cls, v):
        if isinstance(v, cmp.SensorInfo):
            return v._info
        return v

    @validator('native_unit', pre=True)
    def check_unit(cls, v):
        if isinstance(v, str):
            Q(1, v)

        return v



class Sensor(SensorBase):
    id: Union[int, None]
    plant_id: Union[int, None]
    raw_name: Union[str, None]
    sensor_type: Union[str, None]
    native_unit: Union[str, None]
    formatted_unit: Union[str, None]
    is_virtual: Union[bool, None]
    can_calculate: Union[bool, None]
    is_mapped: Union[bool, None]

    @validator('sensor_type', pre=True)
    def convert_sensor_type(cls, v):
        if isinstance(v, cmp.SensorType):
            return v.name
        return v


class NewSensor(SensorBase):
    raw_name: str
    native_unit: str = None


class BulkUpdateSensor(Sensor):
    id: int


class FluidDefintion(SensorBase):
    id: Union[int, None]
    model_type: str
    name: str
    manufacturer: Union[str, None]
    description: Union[str, None]
    is_pure: bool
    dm_model_sha1: Union[str, None]
    hc_model_sha1: Union[str, None]
    heat_capacity_unit_te: Union[str, None]
    heat_capacity_unit_out: Union[str, None]
    heat_capacity_unit_c: Union[str, None]
    density_unit_te: Union[str, None]
    density_unit_out: Union[str, None]
    density_unit_c: Union[str, None]
    # heat_capacity_onnx: Union[str, None]
    # density_onnx: Union[str, None]

    # @validator('heat_capacity_onnx', 'density_onnx', pre=True)
    # def onnx_to_str(cls, v):
    #     try:
    #         return v.hex()
    #     except AttributeError:
    #         return v


class Fluid(BaseModel):
    id: Union[int, None]
    name: Union[str, None]
    manufacturer_name: Union[str, None]
    product_name: Union[str, None]
    fluid: FluidDefintion
    concentration: Union[Quantity, None]


class FluidSummary(BaseModel):
    name: Union[str, None]
    fluid: str
    concentration: Union[Quantity, None]

    @validator('fluid', pre=True)
    def fluid_name(cls, v):
        try:
            return v.name
        except AttributeError:
            return v


# class ArrayBase(BaseModel):
class Array(ComponentBase):
    id: Union[int, None]
    plant_id: Union[int, None]
    name: Union[str, None]
    collector_type: Union[str, None]
    area_gr: Union[Quantity, None]
    area_ap: Union[Quantity, None]
    azim: Union[Quantity, None]
    tilt: Union[Quantity, None]
    row_spacing: Union[Quantity, None]
    n_rows: Union[Quantity, None]
    ground_tilt: Union[Quantity, None]
    mounting_level: Union[Quantity, None]
    fluidvol_total: Union[Quantity, None]
    rho_ground: Union[Quantity, None]
    rho_colbackside: Union[Quantity, None]
    rho_colsurface: Union[Quantity, None]
    max_aoi_shadow: Union[Quantity, None]
    min_elevation_shadow: Union[Quantity, None]

    @validator('collector_type', pre=True)
    def convert_col_type(cls, v):
        if isinstance(v, cmp.CollectorType):
            return v.name
        return v


class NewArray(Array):
    name: str
    collector_type: str
    sensors: Union[Dict[str, NewSensor], None]
    sensor_map: Union[dict, None]


class DataUploadDefaults(BaseModel):
    id: Union[int, None]
    datetime_template: Union[DatetimeTemplates, None]
    datetime_format: Union[str, None]
    timezone: Union[str, None]
    csv_separator: Union[str, None]
    csv_decimal: Union[str, None]
    csv_encoding: Union[str, None]
    index_col: Union[int, None]


class PlantBase(ComponentBase):
    owner: Union[str, None]
    operator: Union[str, None]
    description: Union[str, None]
    location_name: Union[str, None]
    altitude: Union[Quantity, None]
    fluid_solar: Union[FluidSummary, str, None]
    arrays: Union[List[Array], None]
    fluid_vol: Union[Quantity, None]
    raw_sensors: Union[List[Sensor], None]

    @validator('fluid_solar', pre=True)
    def convert_fluid(cls, v):
        if isinstance(v, cmp.Fluid):
            if isinstance(v, UninitialisedFluid):
                return FluidSummary(name=v.fluid_def_name, fluid=v.fluid_def_name, concentration=None)
            return FluidSummary(name=v.name, fluid=v.fluid.name, concentration=getattr(v, 'concentration', None))
        return v


class Plant(PlantBase):
    name: Union[str, None]
    id: Union[int, None]
    latitude: Union[Quantity, None]
    longitude: Union[Quantity, None]
    fluid_solar: Union[FluidSummary, str, None]
    local_tz_string_with_DST: Union[str, None]
    data_upload_defaults: Union[DataUploadDefaults, None]


class UpdatePlant(Plant):
    sensors: Union[Dict[str, NewSensor], None]
    fluid_solar: Union[FluidSummary, None]


class NewPlant(PlantBase):
    name: str
    latitude: Quantity
    longitude: Quantity
    fluid_solar: Union[FluidSummary, None]
    raw_sensors: Union[List[NewSensor], None]
    sensor_map: Union[dict, None]


class PlantSummaryBase(BaseModel):
    name: Union[str, None]
    owner: Union[str, None]
    operator: Union[str, None]
    description: Union[str, None]
    location_name: Union[str, None]
    latitude: Union[Quantity, None]
    longitude: Union[Quantity, None]
    altitude: Union[Quantity, None]


class PlantSummary(PlantSummaryBase):
    id: int
    name: str


class Error(BaseModel):
    error: str
    message: str
    detail: str


class Job(BaseModel):
    id: uuid.UUID
    status: cmp.helpers.ResultStatus
    result_url: Union[str, None]
    plant: Union[str, None]

    @validator('plant', pre=True)
    def plant_to_str(cls, v):
        if v is not None:
            return v.name


class JobReference(BaseModel):
    job_id: uuid.UUID
    href: str

    @validator('job_id')
    def uuid_to_str(cls, v):
        if v is not None:
            return str(v)


class ConfigExport(BaseModel):
    collectors: List[CollectorType]
    sensor_types: List[SensorTypeValidator]
    fluid_definitions: List[FluidDefintion]
    plant: Plant


class SensorSlotValidator(BaseModel):
    """
    A pydantic class used to hold and validate information on a component sensor slot.

    Parameters
    ----------
    name : str
        The name of the slot, which beahvaes like a component attribute and can be used to access the mapped sensor from
        the component. e.g. te_amb. `name` only needs to be unique and understandable in the context of a specific
        component, e.g. the `tp` slot of a plant includes the total power of all arrays, whereas `tp` of an array is
        just that array's power.
    descriptive_name : str
        A longer more descriptive name, e.g. for display to a user in a front end client. Limited to 24 characters
    description : str
        A description of the purpose and use of the slot.
    virtual : enum
        Whether the sensor for a slot is always virtual, can be virtual given certain conditions, or is never virtual
    """

    name: str
    sensor_type: Union[str, SensorTypeValidator]
    descriptive_name: constr(max_length=57)
    virtual: IsVirtual
    description: Union[str, None]

    # def __init__(self,
    #              name: str,
    #              sensor_type: str,
    #              descriptive_name: str,
    #              virtual: Union[IsVirtual, str],
    #              description: str = None):
    #     super().__init__(name=name, sensor_type=sensor_type, descriptive_name=descriptive_name, virtual=virtual,
    #                      description=description)


class PCMethodOutputPlant(BaseModel):
    id: Union[int, None]
    plant: Plant

    n_intervals: Union[int, None]
    datetime_intervals_start: Union[List[datetime.datetime], None]
    datetime_intervals_end: Union[List[datetime.datetime], None]

    tp_measured: Union[Quantity, None]
    tp_sp_measured: Union[Quantity, None]
    tp_sp_estimated: Union[Quantity, None]
    tp_sp_estimated_safety: Union[Quantity, None]
    mean_tp_sp_measured: Union[Quantity, None]
    mean_tp_sp_estimated: Union[Quantity, None]
    mean_tp_sp_estimated_safety: Union[Quantity, None]

    target_actual_slope: Union[Quantity, None]
    target_actual_slope_safety: Union[Quantity, None]

    fluid_solar: Union[FluidSummary, None]
    mean_temperature: Union[Quantity, None]
    mean_fluid_density: Union[Quantity, None]
    mean_fluid_heat_capacity: Union[Quantity, None]

    @validator('datetime_intervals_start', 'datetime_intervals_end', pre=True)
    def array_to_list(cls, val):
        if isinstance(val, np.ndarray):
            return list(val)


class PCMethodOutputArray(BaseModel):
    id: Union[int, None]
    array: Array

    tp_sp_measured: Union[Quantity, None]
    tp_sp_estimated: Union[Quantity, None]
    tp_sp_estimated_safety: Union[Quantity, None]
    mean_tp_sp_measured: Union[Quantity, None]
    mean_tp_sp_estimated: Union[Quantity, None]
    mean_tp_sp_estimated_safety: Union[Quantity, None]


class PCMethodOutput(BaseModel):
    id: Union[int, None]
    plant: PlantSummary

    datetime_eval_start: datetime.datetime
    datetime_eval_end: datetime.datetime

    # Algorithm settings
    pc_method_name: str
    evaluation_mode: str
    equation: int
    wind_used: bool

    # Results
    settings: Dict[str, Any]  # Type checking done in PCSettings
    plant_output: PCMethodOutputPlant
    array_output: List[PCMethodOutputArray]


class OperationalEvent(BaseModel):
    id: Union[int, None]
    plant: Union[str, PlantSummary]
    event_start: datetime.datetime
    event_end: Union[datetime.datetime, None]
    ignored_range: bool = False
    description: Union[str, None]
    original_timezone: Union[str, None]


# def dataclass_to_pydantic(cls: dataclasses.dataclass, name: str) -> BaseModel:
#     # get attribute names and types from dataclass into pydantic format
#     pydantic_field_kwargs = dict()
#     for _field in dataclasses.fields(cls):
#         # check is field has default value
#         if isinstance(_field.default, dataclasses._MISSING_TYPE):
#             # no default
#             default = ...
#         else:
#             default = _field.default
#
#         try:
#             for i, typ in enumerate(_field.type.__args__):
#
#         except AttributeError:
#             pass
#
#         pydantic_field_kwargs[ _field.name] = (_field.type, default)
#
#     return pydantic.create_model(name, **pydantic_field_kwargs, __base__=BaseModel)


class ProblemType(str, enum.Enum):
    component_slot = 'Component slot'
    component_attrib = 'Component attribute'
    sensor_info = 'Sensor info'
    component_missing = 'Component missing'
    other_problem = 'Unspecified problem'
    unexpected_in_calc = 'Unexpected calculation error'
    unexpected_getting_problems = 'Unexpected error getting problem report'


@dataclass
class AlgoProblem:
    """A pydantic class used to hold information on a problem / missing info for a calculation / CoreStrategy.
    Can be used to track problems / missing information back to the root cause.

    Parameters
    ----------
    problem_type : ProblemType enum
    affected_component : ComponentBase, optional
        The component where some problem occurs / information is missing.
    affected_item_name : str, optional
        Typically the name of the affected sensor slot or attribute of the affected component.
    description : str, optional
    """
    problem_type: ProblemType
    affected_component: Union[Plant, Array, None] = None
    affected_item_name: Union[str, None] = None
    description: Union[str, None] = None


@dataclass
class ProblemReport:
    """Standardized reporting of problems / missing information required to perform some calculation.

    This applies to all calculations in SunPeek, i.e. both virtual sensors and other calculations e.g. PC method.
    Any CoreStrategy and CoreAlgorithm holds / can return a ProblemReport which holds structured information as to
    what problems / missing information there is that prevents the strategy / algo to complete.

    ProblemReport implements an n-level tree, where each node (ProblemReport) has n leaves (own_problems) and points
    at m other nodes (sub_problems). sub_problems are implemented as dict with key == strategy name.

    Parameters
    ----------
    success : bool, optional, default True
        True if the algo or strategy holding / producing the problem report is successful, meaning that at least
        parts of its results can be calculated and / or only optional information is missing.
    own_problems : List[AlgoProblem], optional
        List of reported problems that affect the algo / strategy itself (as opposed to problems coming from called /
        sub algorithms). Example: Strategy needs some component attribute, but that attribute is None.
    sub_reports : Dict[str, ProblemReport], optional
        Problems that are not directly associated to the algo / strategy holding this ProblemReport, but rather stem
        from a previous calculation / strategy. Example: Strategy needs some virtual sensor, but that had its own
        problems, reported as a ProblemReport.
    problem_slots : List[str], optional
        Set by virtual sensor strategies, problem_slots can be used to report partial success, i.e.:
        If a strategy is successful for some but not all virtual sensors, the success flag can be set to True,
        and the ProblemReport applies only to the virtual sensor slot names which cannot be calculated,
        i.e. the problem_slots.
    """
    success: Union[bool, None] = True
    own_problems: Union[List[AlgoProblem], None] = None
    sub_reports: Union[Dict[str, 'ProblemReport'], None] = None
    problem_slots: Union[List[str], None] = field(default_factory=list)  # Used if some virtual sensors / slots fail

    @property
    def successful_strategy_str(self) -> Union[str, None]:
        """Loop through strategies, return name of first successful strategy, or None if no strategy was successful.
        """
        if not self.success:
            return None
        for strategy_name, problem in self.sub_reports.items():
            if problem.success:
                return strategy_name
        return None

    def add_own(self, algo_problem: AlgoProblem):
        lst = [] if self.own_problems is None else self.own_problems
        lst.append(algo_problem)
        self.own_problems = lst
        self.success = False

    def add_sub(self, strategy_name: str, problem_report: 'ProblemReport'):
        dct = {} if self.sub_reports is None else self.sub_reports
        dct.update({strategy_name: problem_report})
        self.sub_reports = dct
        self.success = False

    def parse(self, include_successful_strategies: bool = False, include_problem_slots: bool = True) -> str:
        def parse_problem(algo_problem: AlgoProblem) -> str:
            result = f'- {algo_problem.problem_type.value}: '
            if algo_problem.affected_item_name is not None:
                # result += f'item "{algo_problem.affected_item_name}" '
                result += f'"{algo_problem.affected_item_name}" '
            if algo_problem.affected_component is not None:
                result += f'in {algo_problem.affected_component.__class__.__name__} "{algo_problem.affected_component.name}"'
                # result += f'in component "{algo_problem.affected_component.name}"'
            if algo_problem.description is not None:
                result += f': {algo_problem.description}'
            else:
                result += '.'
            result = '\n' + result if result else ''
            return result

        def parse_sub_reports(reports: Dict[str, 'ProblemReport']) -> str:
            # Recursive walk through the problem reports of all strategies (strategy name is dict key).
            result = ''
            for strategy_name, problem_report in reports.items():
                include_slots = self.problem_slots and include_problem_slots
                skip = problem_report.success and not include_successful_strategies and not include_slots
                # if problem_report.success and include_successful_strategies:
                if skip:
                    continue
                if not problem_report.success:
                    sub = problem_report.parse(include_successful_strategies, include_problem_slots)
                else:
                    if not self.problem_slots:
                        sub = ' No problems found.'
                    else:  # partial success, some virtual sensors missing
                        sub = f'Some virtual sensors could not be calculated: {", ".join(self.problem_slots)}. '
                        # if not problem_report.no_problems:
                        sub += problem_report.parse(include_successful_strategies, include_problem_slots)
                result += '\n' if result else ''
                result += f'Strategy "{strategy_name}":{sub}'
            return result

        result = ''
        if self.own_problems is not None:
            for algo_problem in self.own_problems:
                result += parse_problem(algo_problem)

        if self.sub_reports is not None:
            result += parse_sub_reports(self.sub_reports)

        return result


# Goal = Report success / problems of a specific PC method strategy.
@dataclass
class PCMethodProblem:
    evaluation_mode: str
    equation: int
    wind_used: bool
    success: bool
    problem_str: str
