from typing import Tuple, Generator, List, Callable

import numpy as np
import math
from warnings import warn

from ismrmrd.xsd.ismrmrdschema.ismrmrd import ismrmrdHeader as AcquisitionsHeader
from ismrmrd.acquisition import Acquisition, AcquisitionHeader
from ismrmrd.file import Acquisitions
from pyscivis.visualizer.dataclasses.config import ParserConfig

from .base_parser import BaseParser
from pyscivis.visualizer.dataclasses.parser import ParsedData

default_acquisition_dimension_names = ("AVERAGE", "SLICE", "CONTRAST", "PHASE", "REPETITION",
                                       "SET", "SEGMENT", "COIL", "Z", "Y", "X",)

ISMRMRD_ACQ_IS_NOISE_MEASUREMENT = 19


# Utility function that generates a (start,stop) tuple for each chunk
def chunk_ranges(total: int, size: int) -> Generator[Tuple[int, int], None, None]:
    yield from zip(range(0, total, size), range(size, total+size, size))


class AcquisitionParser(BaseParser):
    """
    A parser to extract a kspace and its metadata from either ismrmrd-Aquisitions or complex numpy-arrays.
    """

    @staticmethod
    def parse_with_header(acq_data: Acquisitions,
                          header: AcquisitionsHeader,
                          config: ParserConfig,
                          printer: Callable[[str], None]
                          ) -> ParsedData:
        """
        Take Acquisition-data from ismrmrd-files and compile a kspace.

        First, the dimensions of the kspace are retrieved by reading the header.
        These dimensions are then used to create a np.ndarray filled with NaNs.
        The Acquisitions-object is then iterated over chunk-wise to limit RAM-consumption.
        Then the dimensions of each Acquisition is determined and its data is written into
        the np.ndarray at that specific dimension.
        Finally the kspace and relevant header information is returned

        Args:
            acq_data: An ismrmrd-Aquisitions object.
            header: An ismrmrd-AcquisitionHeader containing relevant metadata.
            config: An object containing the parser configuration.
            printer: A callable that accepts a string and displays it.

        Returns:
            A ParsedData object.
        """
        try:
            chunk_nbytes = config.chunk_size
            collapse_parallel = config.collapse_parallel
            shape_x = None
            encoding = header.encoding[0]
            for acq in acq_data:
                if not acq.is_flag_set(ISMRMRD_ACQ_IS_NOISE_MEASUREMENT):
                    shape_x = len(acq.data[0])
                    break

            if shape_x is None:
                raise ValueError("No non-noise measurement in acquisitions")

            # required attribute, want an exception
            shape_y = encoding.encodingLimits.kspace_encoding_step_1.maximum + 1
            try:
                shape_z = encoding.encodingLimits.kspace_encoding_step_2.maximum + 1
            except AttributeError:
                shape_z = 1

            try:
                enc_s_1_acc = encoding.parallelImaging.accelerationFactor.kspace_encoding_step_1
                enc_s_2_acc = encoding.parallelImaging.accelerationFactor.kspace_encoding_step_2
            except AttributeError:
                enc_s_1_acc = 1
                enc_s_2_acc = 1

            if collapse_parallel:
                shape_y = math.ceil(shape_y/enc_s_1_acc)
                shape_z = math.ceil(shape_z/enc_s_2_acc)

            try:
                shape_avg = encoding.encodingLimits.average.maximum + 1
            except AttributeError:
                shape_avg = 1
            try:
                shape_slice = encoding.encodingLimits.slice.maximum + 1
            except AttributeError:
                shape_slice = 1
            try:
                shape_contrast = encoding.encodingLimits.contrast.maximum + 1
            except AttributeError:
                shape_contrast = 1
            try:
                shape_phase = encoding.encodingLimits.phase.maximum + 1
            except AttributeError:
                shape_phase = 1
            try:
                shape_repetition = encoding.encodingLimits.repetition.maximum + 1
            except AttributeError:
                shape_repetition = 1
            try:
                shape_set = encoding.encodingLimits.set.maximum + 1
            except AttributeError:
                shape_set = 1

            shape_segment = 1  # turning segments into a whole
            shape_coils = acq_data[0].active_channels

            kspace = np.full((shape_avg, shape_slice, shape_contrast, shape_phase,
                              shape_repetition, shape_set, shape_segment, shape_z,
                              shape_y, shape_coils, shape_x),
                             fill_value=np.nan, dtype="complex64")

            def get_acquisition_dimensions(acq_header: AcquisitionHeader):
                """Retrieving acquisition dimensions from header."""

                enc_stp1 = acq_header.idx.kspace_encode_step_1
                enc_stp2 = acq_header.idx.kspace_encode_step_2

                # adjusting y&z's since skipped data was deleted before
                if collapse_parallel:
                    enc_stp1 //= enc_s_1_acc
                    enc_stp2 //= enc_s_2_acc

                avg = acq_header.idx.average
                slc = acq_header.idx.slice
                cntrst = acq_header.idx.contrast
                phs = acq_header.idx.phase
                rpttn = acq_header.idx.repetition
                st = acq_header.idx.set
                sgmnt = 0  # We ignore segment as we want to reassemble the kspace # TODO: only overwrite nans
                return avg, slc, cntrst, phs, rpttn, st, sgmnt, enc_stp2, enc_stp1

            nrows = len(acq_data)  # number of acq-rows
            row_nbytes = acq_data[0].data.nbytes  # size of one row in bytes
            if chunk_nbytes < row_nbytes:
                warn("chunk bytesize set lower than row bytesize; resetting")
                chunk_nbytes = row_nbytes
            chunk_nrows = chunk_nbytes // row_nbytes  # rows per chunk

            # Used for printing current state
            cur_chunk = 0
            n_chunks = math.ceil(nrows/chunk_nrows)  # number of chunks that will be loaded

            for start, stop in chunk_ranges(nrows, chunk_nrows):
                cur_chunk += 1
                printer(f"Loading Chunk {cur_chunk} of {n_chunks}...")
                chunk: List[Acquisition] = acq_data[start:stop]  # grabbing part of acq-rows
                for acq in chunk:
                    if acq.is_flag_set(ISMRMRD_ACQ_IS_NOISE_MEASUREMENT):
                        continue
                    acq_dim = get_acquisition_dimensions(acq.getHead())
                    kspace[acq_dim] = acq.data  # filling kspace with row-data

            # we transpose our current data
            # ("AVERAGE", "SLICE", "CONTRAST", "PHASE", "REPETITION", "SET", "SEGMENT", "Z", "Y", "COIL", "X")
            # to this
            # ("AVERAGE", "SLICE", "CONTRAST", "PHASE", "REPETITION", "SET", "SEGMENT", "COIL", "Z", "Y", "X")
            transpose_order = (0, 1, 2, 3, 4, 5, 6, 9, 7, 8, 10)
            kspace = np.transpose(kspace, transpose_order)
            units = ("pixel",)*11
            return ParsedData(kspace, default_acquisition_dimension_names, kspace.shape, units)
        except Exception as ex:
            printer("Something went wrong...")
            raise ex
