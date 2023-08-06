# SPDX-FileCopyrightText: 2022 Contributors to the Power Grid Model project <dynamic.grid.calculation@alliander.com>
#
# SPDX-License-Identifier: MPL-2.0


"""
Main power grid model class
"""
from enum import IntEnum
from typing import Dict, List, Optional, Set, Union

import numpy as np

from power_grid_model.core.data_handling import (
    create_output_data,
    get_output_type,
    is_batch_calculation,
    prepare_input_view,
    prepare_output_view,
    prepare_update_view,
    reduce_output_data,
)
from power_grid_model.core.error_handling import PowerGridBatchError, assert_no_error, handle_errors
from power_grid_model.core.index_integer import IdNp, IdxNp
from power_grid_model.core.options import Options
from power_grid_model.core.power_grid_core import IDPtr, IdxPtr, ModelPtr
from power_grid_model.core.power_grid_core import power_grid_core as pgc
from power_grid_model.enum import CalculationMethod, CalculationType


class PowerGridModel:
    """
    Main class for Power Grid Model
    """

    _model_ptr: ModelPtr
    _all_component_count: Optional[Dict[str, int]]
    _batch_error: Optional[PowerGridBatchError]

    @property
    def batch_error(self) -> Optional[PowerGridBatchError]:
        """
        Get the batch error object, if present

        Returns: Batch error object, or None

        """
        return self._batch_error

    @property
    def _model(self):
        if not self._model_ptr:
            raise TypeError("You have an empty instance of PowerGridModel!")
        return self._model_ptr

    @property
    def all_component_count(self) -> Dict[str, int]:
        """
        Get count of number of elements per component type.
        If the count for a component type is zero, it will not be in the returned dictionary.
        Returns:
            a dictionary with
                key: component type name
                value: integer count of elements of this type
        """
        if self._all_component_count is None:
            raise TypeError("You have an empty instance of PowerGridModel!")
        return self._all_component_count

    def copy(self) -> "PowerGridModel":
        """

        Copy the current model

        Returns:
            a copy of PowerGridModel
        """
        new_model = PowerGridModel.__new__(PowerGridModel)
        new_model._model_ptr = pgc.copy_model(self._model)  # pylint: disable=W0212
        assert_no_error()
        new_model._all_component_count = self._all_component_count  # pylint: disable=W0212
        return new_model

    def __copy__(self):
        return self.copy()

    def __new__(cls, *_args, **_kwargs):
        instance = super().__new__(cls)
        instance._model_ptr = ModelPtr()
        instance._all_component_count = None
        return instance

    def __init__(self, input_data: Dict[str, np.ndarray], system_frequency: float = 50.0):
        """
        Initialize the model from an input data set.

        Args:
            input_data: input data dictionary
                key: component type name
                value: 1D numpy structured array for this component input
            system_frequency: frequency of the power system, default 50 Hz
        """
        # destroy old instance
        pgc.destroy_model(self._model_ptr)
        self._all_component_count = None
        # create new
        prepared_input = prepare_input_view(input_data)
        self._model_ptr = pgc.create_model(
            system_frequency,
            components=prepared_input.components,
            n_components=prepared_input.n_components,
            component_sizes=prepared_input.n_component_elements_per_scenario,
            input_data=prepared_input.data_ptrs_per_component,
        )
        assert_no_error()
        self._all_component_count = {
            k: v.n_elements_per_scenario for k, v in prepared_input.dataset.items() if v.n_elements_per_scenario > 0
        }

    def update(self, *, update_data: Dict[str, np.ndarray]):
        """
        Update the model with changes.
        Args:
            update_data: update data dictionary
                key: component type name
                value: 1D numpy structured array for this component update
        Returns:
            None
        """
        prepared_update = prepare_update_view(update_data)
        pgc.update_model(
            self._model,
            prepared_update.n_components,
            prepared_update.components,
            prepared_update.n_component_elements_per_scenario,
            prepared_update.data_ptrs_per_component,
        )
        assert_no_error()

    def get_indexer(self, component_type: str, ids: np.ndarray):
        """
        Get array of indexers given array of ids for component type

        Args:
            component_type: type of component
            ids: array of ids

        Returns:
            array of inderxers, same shape as input array ids

        """
        ids_c = np.ascontiguousarray(ids, dtype=IdNp).ctypes.data_as(IDPtr)
        indexer = np.empty_like(ids, dtype=IdxNp, order="C")
        indexer_c = indexer.ctypes.data_as(IdxPtr)
        size = ids.size
        # call c function
        pgc.get_indexer(self._model, component_type, size, ids_c, indexer_c)
        assert_no_error()
        return indexer

    def _get_output_component_count(self, calculation_type: CalculationType):
        exclude_types = {
            CalculationType.power_flow: ["sensor", "fault"],
            CalculationType.state_estimation: ["fault"],
            CalculationType.short_circuit: ["sensor"],
        }.get(calculation_type, [])

        def include_type(component_type: str):
            for exclude_type in exclude_types:
                if exclude_type in component_type:
                    return False
            return True

        return {k: v for k, v in self.all_component_count.items() if include_type(k)}

    def _construct_output(
        self,
        output_component_types: Optional[Union[Set[str], List[str]]],
        calculation_type: CalculationType,
        symmetric: bool,
        batch_size: int,
    ) -> Dict[str, np.ndarray]:
        all_component_count = self._get_output_component_count(calculation_type=calculation_type)

        # limit all component count to user specified component types in output
        if output_component_types is None:
            output_component_types = set(all_component_count.keys())

        return create_output_data(
            output_component_types=output_component_types,
            output_type=get_output_type(calculation_type=calculation_type, symmetric=symmetric),
            all_component_count=all_component_count,
            batch_size=batch_size,
        )

    @staticmethod
    def _options(**kwargs) -> Options:
        if "calculation_method" in kwargs:
            calculation_method = kwargs["calculation_method"]
            if isinstance(calculation_method, str):
                kwargs["calculation_method"] = CalculationMethod[calculation_method]

        opt = Options()
        for key, value in kwargs.items():
            setattr(opt, key, value.value if isinstance(value, IntEnum) else value)
        return opt

    def _handle_errors(self, continue_on_batch_error: bool, batch_size: int):
        self._batch_error = handle_errors(continue_on_batch_error=continue_on_batch_error, batch_size=batch_size)

    # pylint: disable=too-many-arguments
    def _calculate_impl(
        self,
        calculation_type: CalculationType,
        symmetric: bool,
        update_data: Optional[Dict[str, Union[np.ndarray, Dict[str, np.ndarray]]]],
        output_component_types: Optional[Union[Set[str], List[str]]],
        options: Options,
        continue_on_batch_error: bool,
    ):
        """
        Core calculation routine

        Args:
            options:
            update_data:
            output_component_types:
            continue_on_batch_error:

        Returns:

        """
        self._batch_error = None
        batch_calculation = is_batch_calculation(update_data=update_data)

        prepared_update = prepare_update_view(update_data)
        batch_size = prepared_update.batch_size

        output_data = self._construct_output(
            output_component_types=output_component_types,
            calculation_type=calculation_type,
            symmetric=symmetric,
            batch_size=batch_size,
        )
        prepared_result = prepare_output_view(
            output_data=output_data,
            output_type=get_output_type(calculation_type=calculation_type, symmetric=symmetric),
        )

        # run calculation
        pgc.calculate(
            # model and options
            self._model,
            options.opt,
            # result dataset
            prepared_result.n_components,
            prepared_result.components,
            prepared_result.data_ptrs_per_component,
            # update dataset
            batch_size,
            prepared_update.n_components,
            prepared_update.components,
            prepared_update.n_component_elements_per_scenario,
            prepared_update.indptrs_per_component,
            prepared_update.data_ptrs_per_component,
        )

        self._handle_errors(continue_on_batch_error=continue_on_batch_error, batch_size=batch_size)

        return reduce_output_data(output_data=output_data, batch_calculation=batch_calculation)

    def calculate_power_flow(
        self,
        *,
        symmetric: bool = True,
        error_tolerance: float = 1e-8,
        max_iterations: int = 20,
        calculation_method: Union[CalculationMethod, str] = CalculationMethod.newton_raphson,
        update_data: Optional[Dict[str, Union[np.ndarray, Dict[str, np.ndarray]]]] = None,
        threading: int = -1,
        output_component_types: Optional[Union[Set[str], List[str]]] = None,
        continue_on_batch_error: bool = False,
    ) -> Dict[str, np.ndarray]:
        """
        Calculate power flow once with the current model attributes.
        Or calculate in batch with the given update dataset in batch

        Args:
            symmetric:
                True: three-phase symmetric calculation, even for asymmetric loads/generations
                False: three-phase asymmetric calculation
            error_tolerance:
                error tolerance for voltage in p.u., only applicable when the calculation method is iterative
            max_iterations:
                maximum number of iterations, only applicable when the calculation method is iterative
            calculation_method: an enumeration or string
                newton_raphson: use Newton-Raphson iterative method (default)
                linear: use linear method
            update_data:
                None: calculate power flow once with the current model attributes
                A dictionary for batch calculation with batch update
                    key: component type name to be updated in batch
                    value:
                        a 2D numpy structured array for homogeneous update batch
                            Dimension 0: each batch
                            Dimension 1: each updated element per batch for this component type
                        **or**
                        a dictionary containing two keys, for inhomogeneous update batch
                            indptr: a 1D integer numpy array with length n_batch + 1
                                given batch number k, the update array for this batch is
                                data[indptr[k]:indptr[k + 1]]
                                This is the concept of compressed sparse structure
                                https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html
                            data: 1D numpy structured array in flat
            threading:
                only applicable for batch calculation
                < 0 sequential
                = 0 parallel, use number of hardware threads
                > 0 specify number of parallel threads
            output_component_types: list or set of component types you want to be present in the output dict.
                By default all component types will be in the output
            continue_on_batch_error: if the program continues (instead of throwing error) if some scenarios fail

        Returns:
            dictionary of results of all components
                key: component type name to be updated in batch
                value:
                    for single calculation: 1D numpy structured array for the results of this component type
                    for batch calculation: 2D numpy structured array for the results of this component type
                        Dimension 0: each batch
                        Dimension 1: the result of each element for this component type
            Error handling:
                in case an error in the core occurs, an exception will be thrown
        """
        calculation_type = CalculationType.power_flow
        options = self._options(
            calculation_type=calculation_type,
            symmetric=symmetric,
            error_tolerance=error_tolerance,
            max_iterations=max_iterations,
            calculation_method=calculation_method,
            threading=threading,
        )
        return self._calculate_impl(
            calculation_type=calculation_type,
            symmetric=symmetric,
            update_data=update_data,
            output_component_types=output_component_types,
            options=options,
            continue_on_batch_error=continue_on_batch_error,
        )

    def calculate_state_estimation(
        self,
        *,
        symmetric: bool = True,
        error_tolerance: float = 1e-8,
        max_iterations: int = 20,
        calculation_method: Union[CalculationMethod, str] = CalculationMethod.iterative_linear,
        update_data: Optional[Dict[str, Union[np.ndarray, Dict[str, np.ndarray]]]] = None,
        threading: int = -1,
        output_component_types: Optional[Union[Set[str], List[str]]] = None,
        continue_on_batch_error: bool = False,
    ) -> Dict[str, np.ndarray]:
        """
        Calculate state estimation once with the current model attributes.
        Or calculate in batch with the given update dataset in batch

        Args:
            symmetric:
                True: three-phase symmetric calculation, even for asymmetric loads/generations
                False: three-phase asymmetric calculation
            error_tolerance:
                error tolerance for voltage in p.u., only applicable when the calculation method is iterative
            max_iterations:
                maximum number of iterations, only applicable when the calculation method is iterative
            calculation_method: an enumeration
                iterative_linear: use iterative linear method
            update_data:
                None: calculate state estimation once with the current model attributes
                A dictionary for batch calculation with batch update
                    key: component type name to be updated in batch
                    value:
                        a 2D numpy structured array for homogeneous update batch
                            Dimension 0: each batch
                            Dimension 1: each updated element per batch for this component type
                        **or**
                        a dictionary containing two keys, for inhomogeneous update batch
                            indptr: a 1D integer numpy array with length n_batch + 1
                                given batch number k, the update array for this batch is
                                data[indptr[k]:indptr[k + 1]]
                                This is the concept of compressed sparse structure
                                https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html
                            data: 1D numpy structured array in flat
            threading:
                only applicable for batch calculation
                < 0 sequential
                = 0 parallel, use number of hardware threads
                > 0 specify number of parallel threads
            output_component_types: list or set of component types you want to be present in the output dict.
                By default all component types will be in the output
            continue_on_batch_error: if the program continues (instead of throwing error) if some scenarios fail


        Returns:
            dictionary of results of all components
                key: component type name to be updated in batch
                value:
                    for single calculation: 1D numpy structured array for the results of this component type
                    for batch calculation: 2D numpy structured array for the results of this component type
                        Dimension 0: each batch
                        Dimension 1: the result of each element for this component type
            Error handling:
                in case an error in the core occurs, an exception will be thrown
        """
        calculation_type = CalculationType.state_estimation
        options = self._options(
            calculation_type=calculation_type,
            symmetric=symmetric,
            error_tolerance=error_tolerance,
            max_iterations=max_iterations,
            calculation_method=calculation_method,
            threading=threading,
        )
        return self._calculate_impl(
            calculation_type=calculation_type,
            symmetric=symmetric,
            update_data=update_data,
            output_component_types=output_component_types,
            options=options,
            continue_on_batch_error=continue_on_batch_error,
        )

    def calculate_short_circuit(
        self,
        *,
        calculation_method: Union[CalculationMethod, str] = CalculationMethod.iec60909,
        update_data: Optional[Dict[str, Union[np.ndarray, Dict[str, np.ndarray]]]] = None,
        threading: int = -1,
        output_component_types: Optional[Union[Set[str], List[str]]] = None,
        continue_on_batch_error: bool = False,
    ) -> Dict[str, np.ndarray]:
        """
        Calculate a short circuit once with the current model attributes.
        Or calculate in batch with the given update dataset in batch

        Args:
            calculation_method: an enumeration
                iec60909: use the iec60909 standard
            update_data:
                None: calculate a short circuit once with the current model attributes
                A dictionary for batch calculation with batch update
                    key: component type name to be updated in batch
                    value:
                        a 2D numpy structured array for homogeneous update batch
                            Dimension 0: each batch
                            Dimension 1: each updated element per batch for this component type
                        **or**
                        a dictionary containing two keys, for inhomogeneous update batch
                            indptr: a 1D integer numpy array with length n_batch + 1
                                given batch number k, the update array for this batch is
                                data[indptr[k]:indptr[k + 1]]
                                This is the concept of compressed sparse structure
                                https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html
                            data: 1D numpy structured array in flat
            threading:
                only applicable for batch calculation
                < 0 sequential
                = 0 parallel, use number of hardware threads
                > 0 specify number of parallel threads
            output_component_types: list or set of component types you want to be present in the output dict.
                By default all component types will be in the output
            continue_on_batch_error: if the program continues (instead of throwing error) if some scenarios fail


        Returns:
            dictionary of results of all components
                key: component type name to be updated in batch
                value:
                    for single calculation: 1D numpy structured array for the results of this component type
                    for batch calculation: 2D numpy structured array for the results of this component type
                        Dimension 0: each batch
                        Dimension 1: the result of each element for this component type
            Error handling:
                in case an error in the core occurs, an exception will be thrown
        """
        calculation_type = CalculationType.short_circuit
        symmetric = False

        options = self._options(
            calculation_type=calculation_type,
            symmetric=symmetric,
            calculation_method=calculation_method,
            threading=threading,
        )
        return self._calculate_impl(
            calculation_type=calculation_type,
            symmetric=symmetric,
            update_data=update_data,
            output_component_types=output_component_types,
            options=options,
            continue_on_batch_error=continue_on_batch_error,
        )

    def __del__(self):
        pgc.destroy_model(self._model_ptr)
