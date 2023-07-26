from policyengine_core.data import Dataset
import numpy as np
from pathlib import Path
from typing import Type
import pandas as pd
from policyengine_us.data.storage import STORAGE_FOLDER
from ..cps import CPS_2023


class CalibratedCPS(Dataset):
    input_dataset: Type[Dataset]
    input_dataset_year: int
    min_loss: float = 0.19
    learning_rate: float = 2e2
    log_dir: str = "."
    time_period: str = None
    log_verbose: bool = False

    @staticmethod
    def from_dataset(
        dataset: Type[Dataset],
        new_name: str = None,
        new_label: str = None,
        year: int = None,
        out_year: int = 2023,
        log_folder: str = None,
        verbose: bool = True,
    ):
        class CalibratedCPSFromDataset(CalibratedCPS):
            name = new_name
            label = new_label
            input_dataset = dataset
            input_dataset_year = year or dataset.time_period
            time_period = out_year
            log_dir = log_folder
            file_path = STORAGE_FOLDER / f"{new_name}.h5"
            data_format = dataset.data_format
            log_verbose = verbose

        return CalibratedCPSFromDataset

    def generate(self):
        from .output_cps import OutputDataset
        from survey_enhance.reweight import CalibratedWeights
        from .loss import Loss, calibration_parameters

        input_dataset = OutputDataset.from_dataset(self.input_dataset)()

        original_weights = input_dataset.household.household_weight.values

        calibrated_weights = CalibratedWeights(
            original_weights,
            input_dataset,
            Loss,
            calibration_parameters,
        )
        weights = calibrated_weights.calibrate(
            "2023-01-01",
            min_loss=self.min_loss,
            learning_rate=self.learning_rate,
            verbose=self.log_verbose,
            log_dir=self.log_dir,
        )

        data = self.input_dataset().load_dataset()

        data["household_weight"] = weights
        del data["tax_unit_weight"]
        del data["person_weight"]
        del data["family_weight"]
        del data["spm_unit_weight"]

        self.remove()

        self.save_dataset(data)


CalibratedCPS_2023 = CalibratedCPS.from_dataset(
    CPS_2023,
    new_name="calibrated_cps_2023",
    new_label="Calibrated CPS 2023",
    out_year=2023,
    log_folder=Path(__file__).parent.parent / "logs",
)
