import ctypes
import pathlib
import platform
import sys

from typing import List

from em_st_artifacts.utils.EmotionalMathException import EmotionalMathException
from em_st_artifacts.utils.lib_settings import (ArtifactDetectSetting, MathLibSetting, MentalAndSpectralSetting,
                               ShortArtifactDetectSetting, )
from em_st_artifacts.utils.support_classes import MindData, RawChannels, RawChannelsArray, RawSpectVals, SpectralDataPercents

_main_lib_name = None
_support_lib_name = None
_filters_lib_name = None
if sys.platform == "win32":
    arc = platform.architecture()
    if arc[0].__contains__("64"):
        _main_lib_name = pathlib.Path(__file__).parent.resolve() / "libs" / "x64" / "em_st_artifacts-x64.dll"
        _support_lib_name = pathlib.Path(__file__).parent.resolve() / "libs" / "x64" / "artifacts-x64.dll"
        _filters_lib_name = pathlib.Path(__file__).parent.resolve() / "libs" / "x64" / "filters.dll"
    else:
        _main_lib_name = pathlib.Path(__file__).parent.resolve() / "libs" / "x86" / "em_st_artifacts-x86.dll"
        _support_lib_name = pathlib.Path(__file__).parent.resolve() / "libs" / "x86" / "artifacts-x86.dll"
        _filters_lib_name = pathlib.Path(__file__).parent.resolve() / "libs" / "x86" / "filters.dll"
elif sys.platform.startswith("linux"):
    print('Add linux lib')
elif sys.platform == "darwin":
    print('Add macos lib')
else:
    raise FileNotFoundError("This platform (%s) is currently not supported by pyem-st-artifactslib." % sys.platform)

ctypes.windll.LoadLibrary(str(_filters_lib_name))
ctypes.windll.LoadLibrary(str(_support_lib_name))
_em_st_artifacts_lib = ctypes.WinDLL(str(_main_lib_name))


class EmotionalMath:
    class _NativeMathLibSetting(ctypes.Structure):
        _fields_ = [('sampling_rate', ctypes.c_int32), ('process_win_freq', ctypes.c_int32),
                    ('fft_window', ctypes.c_int32), ('n_first_sec_skipped', ctypes.c_int32),
                    ('bipolar_mode', ctypes.c_int32), ('channels_number', ctypes.c_int32),
                    ('channel_for_analysis', ctypes.c_int32)]

    class _NativeArtifactDetectSetting(ctypes.Structure):
        _fields_ = [('art_bord', ctypes.c_int32), ('allowed_percent_artpoints', ctypes.c_int32),
                    ('raw_betap_limit', ctypes.c_int32), ('total_pow_border', ctypes.c_int32),
                    ('global_artwin_sec', ctypes.c_int32), ('spect_art_by_totalp', ctypes.c_int32),
                    ('hanning_win_spectrum', ctypes.c_int32), ('hamming_win_spectrum', ctypes.c_int32),
                    ('num_wins_for_quality_avg', ctypes.c_int32)]

    class _NativeShortArtifactDetectSetting(ctypes.Structure):
        _fields_ = [('ampl_art_detect_win_size', ctypes.c_int), ('ampl_art_zerod_area', ctypes.c_int),
                    ('ampl_art_extremum_border', ctypes.c_int)]

    class _NativeMentalAndSpectralSetting(ctypes.Structure):
        _fields_ = [('n_sec_for_instant_estimation', ctypes.c_int), ('n_sec_for_averaging', ctypes.c_int)]

    class _NativeOpStatus(ctypes.Structure):
        _fields_ = [('Success', ctypes.c_uint8), ('Error', ctypes.c_uint32), ('ErrorMsg', ctypes.c_char * 512)]

    class _NativeMindData(ctypes.Structure):
        _fields_ = [('Rel_Attention', ctypes.c_double), ('Rel_Relaxation', ctypes.c_double),
                    ('Inst_Attention', ctypes.c_double), ('Inst_Relaxation', ctypes.c_double)]

    class _NativeSpectralDataPercents(ctypes.Structure):
        _fields_ = [('Delta', ctypes.c_double), ('Theta', ctypes.c_double), ('Alpha', ctypes.c_double),
                    ('Beta', ctypes.c_double), ('Gamma', ctypes.c_double)]

    class _NativeRawChannels(ctypes.Structure):
        _fields_ = [('left_bipolar', ctypes.c_double), ('right_bipolar', ctypes.c_double)]

    class _NativeRawChannelsArray(ctypes.Structure):
        _fields_ = [('channels', ctypes.POINTER(ctypes.c_double))]

    class _NativeRawSpectVals(ctypes.Structure):
        _fields_ = [('alpha', ctypes.c_double), ('beta', ctypes.c_double)]

    def __init__(self,
                 mls: MathLibSetting,
                 ads: ArtifactDetectSetting,
                 sads: ShortArtifactDetectSetting,
                 mss: MentalAndSpectralSetting):
        math_lib = ctypes.POINTER(ctypes.c_void_p)
        self._native_ptr = None

        self._create_math_lib = _em_st_artifacts_lib.createMathLib
        self._create_math_lib.restype = ctypes.POINTER(math_lib)
        self._create_math_lib.argtypes = (
            self._NativeMathLibSetting, self._NativeArtifactDetectSetting, self._NativeShortArtifactDetectSetting,
            self._NativeMentalAndSpectralSetting, ctypes.c_void_p)

        self._free_math_lib = _em_st_artifacts_lib.freeMathLib
        self._free_math_lib.restype = ctypes.c_uint8
        self._free_math_lib.argtypes = (ctypes.POINTER(math_lib), ctypes.c_void_p)

        self._set_mental_estimation_mode = _em_st_artifacts_lib.MathLibSetMentalEstimationMode
        self._set_mental_estimation_mode.restype = ctypes.c_uint8
        self._set_mental_estimation_mode.argtypes = (ctypes.POINTER(math_lib), ctypes.c_bool, ctypes.c_void_p)

        self._set_hanning_win_spect = _em_st_artifacts_lib.MathLibSetHanningWinSpect
        self._set_hanning_win_spect.restype = ctypes.c_uint8
        self._set_hanning_win_spect.argtypes = (ctypes.POINTER(math_lib), ctypes.c_void_p)

        self._set_hamming_win_spect = _em_st_artifacts_lib.MathLibSetHammingWinSpect
        self._set_hamming_win_spect.restype = ctypes.c_uint8
        self._set_hamming_win_spect.argtypes = (ctypes.POINTER(math_lib), ctypes.c_void_p)

        self._set_calibration_length = _em_st_artifacts_lib.MathLibSetCallibrationLength
        self._set_calibration_length.restype = ctypes.c_uint8
        self._set_calibration_length.argtypes = (ctypes.POINTER(math_lib), ctypes.c_int, ctypes.c_void_p)

        self._set_skip_wins_after_artifact = _em_st_artifacts_lib.MathLibSetSkipWinsAfterArtifact
        self._set_skip_wins_after_artifact.restype = ctypes.c_uint8
        self._set_skip_wins_after_artifact.argtypes = (ctypes.POINTER(math_lib), ctypes.c_int, ctypes.c_void_p)

        self._push_data = _em_st_artifacts_lib.MathLibPushData
        self._push_data.restype = ctypes.c_uint8
        self._push_data.argtypes = (ctypes.POINTER(math_lib), ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p)

        self._push_data_arr = _em_st_artifacts_lib.MathLibPushDataArr
        self._push_data_arr.restype = ctypes.c_uint8
        self._push_data_arr.argtypes = (ctypes.POINTER(math_lib), ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p)

        self._process_window = _em_st_artifacts_lib.MathLibProcessWindow
        self._process_window.restype = ctypes.c_uint8
        self._process_window.argtypes = (ctypes.POINTER(math_lib), ctypes.c_void_p)

        self._process_data = _em_st_artifacts_lib.MathLibProcessData
        self._process_data.restype = ctypes.c_uint8
        self._process_data.argtypes = (ctypes.POINTER(math_lib), ctypes.c_int, ctypes.c_void_p)

        self._process_data_arr = _em_st_artifacts_lib.MathLibProcessDataArr
        self._process_data_arr.restype = ctypes.c_uint8
        self._process_data_arr.argtypes = (ctypes.POINTER(math_lib), ctypes.c_void_p)

        self._set_priority_side = _em_st_artifacts_lib.MathLibSetPrioritySide
        self._set_priority_side.restype = ctypes.c_uint8
        self._set_priority_side.argtypes = (ctypes.POINTER(math_lib), ctypes.c_int, ctypes.c_void_p)

        self._start_calibration = _em_st_artifacts_lib.MathLibStartCalibration
        self._start_calibration.restype = ctypes.c_uint8
        self._start_calibration.argtypes = (ctypes.POINTER(math_lib), ctypes.c_void_p)

        self._calibration_finished = _em_st_artifacts_lib.MathLibCalibrationFinished
        self._calibration_finished.restype = ctypes.c_uint8
        self._calibration_finished.argtypes = (ctypes.POINTER(math_lib), ctypes.c_void_p, ctypes.c_void_p)

        self._is_artifacted_win = _em_st_artifacts_lib.MathLibIsArtifactedWin
        self._is_artifacted_win.restype = ctypes.c_uint8
        self._is_artifacted_win.argtypes = (ctypes.POINTER(math_lib), ctypes.c_int, ctypes.c_bool, ctypes.c_void_p)

        self._is_artifacted_sequence = _em_st_artifacts_lib.MathLibIsArtifactedSequence
        self._is_artifacted_sequence.restype = ctypes.c_uint8
        self._is_artifacted_sequence.argtypes = (ctypes.POINTER(math_lib), ctypes.c_void_p, ctypes.c_void_p)

        self._is_both_sides_artifacted = _em_st_artifacts_lib.MathLibIsBothSidesArtifacted
        self._is_both_sides_artifacted.restype = ctypes.c_uint8
        self._is_both_sides_artifacted.argtypes = (ctypes.POINTER(math_lib), ctypes.c_void_p, ctypes.c_void_p)

        self._read_mental_data_arr_size = _em_st_artifacts_lib.MathLibReadMentalDataArrSize
        self._read_mental_data_arr_size.restype = ctypes.c_uint8
        self._read_mental_data_arr_size.argtypes = (ctypes.POINTER(math_lib), ctypes.c_void_p, ctypes.c_void_p)

        self._read_mental_data_arr = _em_st_artifacts_lib.MathLibReadMentalDataArr
        self._read_mental_data_arr.restype = ctypes.c_uint8
        self._read_mental_data_arr.argtypes = (
            ctypes.POINTER(math_lib), ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)

        self._read_average_mental_data = _em_st_artifacts_lib.MathLibReadAverageMentalData
        self._read_average_mental_data.restype = ctypes.c_uint8
        self._read_average_mental_data.argtypes = (
            ctypes.POINTER(math_lib), ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)

        self._read_spectral_data_percents_arr_size = _em_st_artifacts_lib.MathLibReadSpectralDataPercentsArrSize
        self._read_spectral_data_percents_arr_size.restype = ctypes.c_uint8
        self._read_spectral_data_percents_arr_size.argtypes = (
            ctypes.POINTER(math_lib), ctypes.c_void_p, ctypes.c_void_p)

        self._read_spectral_data_percents_arr = _em_st_artifacts_lib.MathLibReadSpectralDataPercentsArr
        self._read_spectral_data_percents_arr.restype = ctypes.c_uint8
        self._read_spectral_data_percents_arr.argtypes = (
            ctypes.POINTER(math_lib), ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)

        self._read_raw_spectral_vals = _em_st_artifacts_lib.MathLibReadRawSpectralVals
        self._read_raw_spectral_vals.restype = ctypes.c_uint8
        self._read_raw_spectral_vals.argtypes = (ctypes.POINTER(math_lib), ctypes.c_void_p, ctypes.c_void_p)

        self._set_zero_spect_waves = _em_st_artifacts_lib.MathLibSetZeroSpectWaves
        self._set_zero_spect_waves.restype = ctypes.c_uint8
        self._set_zero_spect_waves.argtypes = (
            ctypes.POINTER(math_lib), ctypes.c_bool, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_int, ctypes.c_void_p)

        self._set_weights_for_spectra = _em_st_artifacts_lib.MathLibSetWeightsForSpectra
        self._set_weights_for_spectra.restype = ctypes.c_uint8
        self._set_weights_for_spectra.argtypes = (
            ctypes.POINTER(math_lib), ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,
            ctypes.c_double, ctypes.c_void_p)

        self._set_spect_normalization_by_bands_width = _em_st_artifacts_lib.MathLibSetSpectNormalizationByBandsWidth
        self._set_spect_normalization_by_bands_width.restype = ctypes.c_uint8
        self._set_spect_normalization_by_bands_width.argtypes = (
            ctypes.POINTER(math_lib), ctypes.c_bool, ctypes.c_void_p)

        self._set_spect_normalization_by_coeffs = _em_st_artifacts_lib.MathLibSetSpectNormalizationByCoeffs
        self._set_spect_normalization_by_coeffs.restype = ctypes.c_uint8
        self._set_spect_normalization_by_coeffs.argtypes = (ctypes.POINTER(math_lib), ctypes.c_bool, ctypes.c_void_p)

        self._get_calibration_percents = _em_st_artifacts_lib.MathLibGetCallibrationPercents
        self._get_calibration_percents.restype = ctypes.c_uint8
        self._get_calibration_percents.argtypes = (ctypes.POINTER(math_lib), ctypes.c_void_p, ctypes.c_void_p)

        native_lib_setting = self._NativeMathLibSetting(mls.sampling_rate,
                                                        mls.process_win_freq,
                                                        mls.fft_window,
                                                        mls.n_first_sec_skipped,
                                                        mls.bipolar_mode,
                                                        mls.channels_number,
                                                        mls.channel_for_analysis)

        native_art_setting = self._NativeArtifactDetectSetting(ads.art_bord,
                                                               ads.allowed_percent_artpoints,
                                                               ads.raw_betap_limit,
                                                               ads.global_artwin_sec,
                                                               ads.hanning_win_spectrum,
                                                               ads.hamming_win_spectrum,
                                                               ads.num_wins_for_quality_avg)

        native_short_art_setting = self._NativeShortArtifactDetectSetting(sads.ampl_art_detect_win_size,
                                                                          sads.ampl_art_zerod_area,
                                                                          sads.ampl_art_extremum_border)

        native_mental_spectral_setting = self._NativeMentalAndSpectralSetting(mss.n_sec_for_instant_estimation,
                                                                              mss.n_sec_for_averaging)

        op_status = self._NativeOpStatus()

        self._native_ptr = self._create_math_lib(native_lib_setting,
                                                 native_art_setting,
                                                 native_short_art_setting,
                                                 native_mental_spectral_setting,
                                                 ctypes.byref(op_status))
        self._check_error(op_status)

        self.set_mental_estimation_mode(False)
        self.set_zero_spect_waves(True, 0, 1, 1, 1, 0)
        self.set_calibration_length(6)
        self.set_skip_wins_after_artifact(5)

    def set_mental_estimation_mode(self, independent: bool):
        op_status = self._NativeOpStatus()
        self._set_mental_estimation_mode(self._native_ptr, independent, ctypes.byref(op_status))
        self._check_error(op_status)

    def set_hanning_win_spect(self):
        op_status = self._NativeOpStatus()
        self._set_hanning_win_spect(self._native_ptr, ctypes.byref(op_status))
        self._check_error(op_status)

    def set_hamming_win_spect(self):
        op_status = self._NativeOpStatus()
        self._set_hamming_win_spect(self._native_ptr, ctypes.byref(op_status))
        self._check_error(op_status)

    def set_calibration_length(self, s: int):
        op_status = self._NativeOpStatus()
        self._set_calibration_length(self._native_ptr, s, ctypes.byref(op_status))
        self._check_error(op_status)

    def set_skip_wins_after_artifact(self, nwins: int):
        op_status = self._NativeOpStatus()
        self._set_skip_wins_after_artifact(self._native_ptr, nwins, ctypes.byref(op_status))
        self._check_error(op_status)

    def push_data(self, samples: List[RawChannels]):
        op_status = self._NativeOpStatus()
        self._push_data(self._native_ptr,
                        (self._NativeRawChannels * len(samples))(*samples),
                        len(samples),
                        ctypes.byref(op_status))
        self._check_error(op_status)

    def push_data_arr(self, samples: List[RawChannelsArray]):
        native_list = []

        for x in samples:
            channels_list = [y for y in x.channels]
            channels_array = (ctypes.c_double * len(channels_list))(*channels_list)
            native_list.append(self._NativeRawChannelsArray(channels_array))

        native_array = (self._NativeRawChannelsArray * len(native_list))(*native_list)

        op_status = self._NativeOpStatus()
        self._push_data_arr(self._native_ptr, native_array, len(samples), ctypes.byref(op_status))
        self._check_error(op_status)

    def process_window(self):
        op_status = self._NativeOpStatus()
        self._process_window(self._native_ptr, ctypes.byref(op_status))
        self._check_error(op_status)

    def process_data(self, side: int):
        op_status = self._NativeOpStatus()
        self._process_data(self._native_ptr, side, ctypes.byref(op_status))
        self._check_error(op_status)

    def process_data_arr(self):
        op_status = self._NativeOpStatus()
        self._process_data_arr(self._native_ptr, ctypes.byref(op_status))
        self._check_error(op_status)

    def set_priority_side(self, side: int):
        op_status = self._NativeOpStatus()
        self._set_priority_side(self._native_ptr, side, ctypes.byref(op_status))
        self._check_error(op_status)

    def start_calibration(self):
        op_status = self._NativeOpStatus()
        self._start_calibration(self._native_ptr, ctypes.byref(op_status))
        self._check_error(op_status)

    def calibration_finished(self) -> bool:
        result = ctypes.c_bool(False)

        op_status = self._NativeOpStatus()
        self._calibration_finished(self._native_ptr, ctypes.byref(result), ctypes.byref(op_status))
        self._check_error(op_status)

        return result.value

    def is_artifacted_win(self, side: int, print_info: bool) -> bool:
        result = ctypes.c_bool(False)

        op_status = self._NativeOpStatus()
        self._is_artifacted_win(self._native_ptr, side, print_info, ctypes.byref(result), ctypes.byref(op_status))
        self._check_error(op_status)

        return result.value

    def is_artifacted_sequence(self) -> bool:
        result = ctypes.c_bool(False)

        op_status = self._NativeOpStatus()
        self._is_artifacted_sequence(self._native_ptr, ctypes.byref(result), ctypes.byref(op_status))
        self._check_error(op_status)

        return result.value

    def is_both_sides_artifacted(self) -> bool:
        result = ctypes.c_bool(False)

        op_status = self._NativeOpStatus()
        self._is_both_sides_artifacted(self._native_ptr, ctypes.byref(result), ctypes.byref(op_status))
        self._check_error(op_status)

        return result.value

    def read_mental_data_arr_size(self) -> int:
        result = ctypes.c_int(0)

        op_status = self._NativeOpStatus()
        self._read_mental_data_arr_size(self._native_ptr, ctypes.byref(result), ctypes.byref(op_status))
        self._check_error(op_status)

        return result.value

    def read_mental_data_arr(self) -> List[MindData]:
        arr_size = self.read_mental_data_arr_size()

        if arr_size == 0:
            return []

        native_result = (self._NativeMindData * arr_size)()

        op_status = self._NativeOpStatus()
        self._read_mental_data_arr(self._native_ptr, native_result, arr_size, ctypes.byref(op_status))
        self._check_error(op_status)

        return [MindData(x.Rel_Attention, x.Rel_Relaxation, x.Inst_Attention, x.Inst_Relaxation) for x in native_result]

    def read_average_mental_data(self, n_last_wins_to_average: int) -> MindData:
        native_result = self._NativeMindData()

        op_status = self._NativeOpStatus()
        self._read_average_mental_data(self._native_ptr,
                                       n_last_wins_to_average,
                                       ctypes.byref(native_result),
                                       ctypes.byref(op_status))
        self._check_error(op_status)

        return MindData(native_result.Rel_Attention,
                        native_result.Rel_Relaxation,
                        native_result.Inst_Attention,
                        native_result.Inst_Relaxation)

    def read_spectral_data_percents_arr_size(self) -> int:
        result = ctypes.c_int(0)

        op_status = self._NativeOpStatus()
        self._read_spectral_data_percents_arr_size(self._native_ptr, ctypes.byref(result), ctypes.byref(op_status))
        self._check_error(op_status)

        return result.value

    def read_spectral_data_percents_arr(self) -> List[SpectralDataPercents]:
        arr_size = self.read_spectral_data_percents_arr_size()

        if arr_size == 0:
            return []

        native_result = (self._NativeSpectralDataPercents * arr_size)()

        op_status = self._NativeOpStatus()
        self._read_spectral_data_percents_arr(self._native_ptr, native_result, arr_size, ctypes.byref(op_status))
        self._check_error(op_status)

        return [SpectralDataPercents(x.Delta, x.Theta, x.Alpha, x.Beta, x.Gamma) for x in native_result]

    def read_raw_spectral_vals(self) -> RawSpectVals:
        native_result = self._NativeRawSpectVals()

        op_status = self._NativeOpStatus()
        self._read_raw_spectral_vals(self._native_ptr, ctypes.byref(native_result), ctypes.byref(op_status))
        self._check_error(op_status)

        return RawSpectVals(native_result.alpha, native_result.beta)

    def set_zero_spect_waves(self, active: bool, delta: int, theta: int, alpha: int, beta: int, gamma: int):
        op_status = self._NativeOpStatus()
        self._set_zero_spect_waves(self._native_ptr, active, delta, theta, alpha, beta, gamma, ctypes.byref(op_status))
        self._check_error(op_status)

    def set_weights_for_spectra(self, delta_c: float, theta_c: float, alpha_c: float, beta_c: float, gamma_c: float):
        op_status = self._NativeOpStatus()
        self._set_weights_for_spectra(self._native_ptr,
                                      delta_c,
                                      theta_c,
                                      alpha_c,
                                      beta_c,
                                      gamma_c,
                                      ctypes.byref(op_status))
        self._check_error(op_status)

    def set_spect_normalization_by_bands_width(self, fl: bool):
        op_status = self._NativeOpStatus()
        self._set_spect_normalization_by_bands_width(self._native_ptr, fl, ctypes.byref(op_status))
        self._check_error(op_status)

    def set_spect_normalization_by_coeffs(self, fl: bool):
        op_status = self._NativeOpStatus()
        self._set_spect_normalization_by_coeffs(self._native_ptr, fl, ctypes.byref(op_status))
        self._check_error(op_status)

    def get_calibration_percents(self) -> int:
        result = ctypes.c_int(0)

        op_status = self._NativeOpStatus()
        self._get_calibration_percents(self._native_ptr, ctypes.byref(result), ctypes.byref(op_status))
        self._check_error(op_status)

        return result.value

    @staticmethod
    def _check_error(op_status: _NativeOpStatus):
        if not op_status.Success:
            error_msg = "".join([op_status.ErrorMsg[x] for x in range(512)])
            raise EmotionalMathException(error_msg)

    def __del__(self):
        if self._native_ptr is None:
            op_status = self._NativeOpStatus()

            self._free_math_lib(self._native_ptr, ctypes.byref(op_status))

            self._check_error(op_status)

            self._native_ptr = None
