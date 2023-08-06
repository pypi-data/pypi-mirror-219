from dataclasses import dataclass


@dataclass
class MathLibSetting:
    sampling_rate: int
    fft_window: int
    channel_for_analysis: int
    process_win_freq: int = 25
    n_first_sec_skipped: int = 4
    bipolar_mode: bool = False
    channels_number: int = 4


@dataclass
class ArtifactDetectSetting:
    art_bord: int = 70
    allowed_percent_artpoints: int = 50
    raw_betap_limit: int = 800000
    total_pow_border: int = 3 * 1e7
    global_artwin_sec: int = 4
    spect_art_by_totalp: int = False
    hanning_win_spectrum: int = False
    hamming_win_spectrum: int = False
    num_wins_for_quality_avg: int = 100


@dataclass
class ShortArtifactDetectSetting:
    ampl_art_detect_win_size: int = 200
    ampl_art_zerod_area: int = 200
    ampl_art_extremum_border: int = 30


@dataclass
class MentalAndSpectralSetting:
    n_sec_for_instant_estimation: int = 2
    n_sec_for_averaging: int = 2
