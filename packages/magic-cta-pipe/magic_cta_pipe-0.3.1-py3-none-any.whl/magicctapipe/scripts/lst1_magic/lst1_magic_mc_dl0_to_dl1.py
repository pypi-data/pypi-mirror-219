#!/usr/bin/env python
# coding: utf-8

"""
This script processes LST-1 and MAGIC events of simtel MC DL0 data
(*.simtel.gz) and computes the DL1 parameters, i.e., Hillas, timing and
leakage parameters. It saves only the events that all the DL1 parameters
are successfully reconstructed.

Since it cannot identify the telescopes of the input file, please assign
the correct telescope ID to each telescope in the configuration file.

When saving data to an output file, the telescope IDs will be reset to
the following ones to match with those of real data:

LST-1: tel_id = 1,  MAGIC-I: tel_id = 2,  MAGIC-II: tel_id = 3

In addition, the telescope coordinate will be converted to the one
relative to the center of the LST-1 and MAGIC positions (including the
altitude) for the convenience of the geometrical stereo reconstruction.

Usage:
$ python lst1_magic_mc_dl0_to_dl1.py
--input-file dl0/gamma_40deg_90deg_run1.simtel.gz
(--output-dir dl1)
(--config-file config.yaml)
"""

import argparse
import logging
import re
import time
from pathlib import Path

import numpy as np
import yaml
from astropy import units as u
from astropy.coordinates import Angle, angular_separation
from ctapipe.calib import CameraCalibrator
from ctapipe.image import (
    apply_time_delta_cleaning,
    hillas_parameters,
    leakage_parameters,
    number_of_islands,
    tailcuts_clean,
    timing_parameters,
)
from ctapipe.instrument import SubarrayDescription
from ctapipe.io import EventSource, HDF5TableWriter
from lstchain.image.cleaning import apply_dynamic_cleaning
from lstchain.image.modifier import (
    add_noise_in_pixels,
    random_psf_smearer,
    set_numba_seed,
)
from magicctapipe.image import MAGICClean
from magicctapipe.io import SimEventInfoContainer, format_object
from magicctapipe.utils import calculate_disp, calculate_impact
from traitlets.config import Config

__all__ = ["mc_dl0_to_dl1"]

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

# The CORSIKA particle types
PARTICLE_TYPES = {1: "gamma", 3: "electron", 14: "proton", 402: "helium"}


def mc_dl0_to_dl1(input_file, output_dir, config):
    """
    Processes LST-1 and MAGIC events of simtel MC DL0 data and computes
    the DL1 parameters.

    Parameters
    ----------
    input_file: str
        Path to an input simtel MC DL0 data file
    output_dir: str
        Path to a directory where to save an output DL1 data file
    config: dict
        Configuration for the LST-1 + MAGIC analysis
    """

    assigned_tel_ids = config["mc_tel_ids"]

    logger.info("\nAssigned telescope IDs:")
    logger.info(format_object(assigned_tel_ids))

    tel_id_lst1 = assigned_tel_ids["LST-1"]
    tel_id_m1 = assigned_tel_ids["MAGIC-I"]
    tel_id_m2 = assigned_tel_ids["MAGIC-II"]

    # Load the input file
    logger.info(f"\nInput file: {input_file}")

    event_source = EventSource(
        input_file,
        allowed_tels=list(assigned_tel_ids.values()),
        focal_length_choice="effective",
    )

    obs_id = event_source.obs_ids[0]
    subarray = event_source.subarray

    tel_descriptions = subarray.tel
    tel_positions = subarray.positions

    logger.info("\nSubarray description:")
    logger.info(format_object(tel_descriptions))

    camera_geoms = {}
    for tel_id, telescope in tel_descriptions.items():
        camera_geoms[tel_id] = telescope.camera.geometry

    # Configure the LST event processors
    config_lst = config["LST"]

    logger.info("\nLST image extractor:")
    logger.info(format_object(config_lst["image_extractor"]))

    extractor_type_lst = config_lst["image_extractor"].pop("type")
    config_extractor_lst = {extractor_type_lst: config_lst["image_extractor"]}

    calibrator_lst = CameraCalibrator(
        image_extractor_type=extractor_type_lst,
        config=Config(config_extractor_lst),
        subarray=subarray,
    )

    logger.info("\nLST NSB modifier:")
    logger.info(format_object(config_lst["increase_nsb"]))

    logger.info("\nLST PSF modifier:")
    logger.info(format_object(config_lst["increase_psf"]))

    increase_nsb = config_lst["increase_nsb"].pop("use")
    increase_psf = config_lst["increase_psf"].pop("use")

    if increase_nsb:
        rng = np.random.default_rng(obs_id)

    if increase_psf:
        set_numba_seed(obs_id)

    logger.info("\nLST tailcuts cleaning:")
    logger.info(format_object(config_lst["tailcuts_clean"]))

    logger.info("\nLST time delta cleaning:")
    logger.info(format_object(config_lst["time_delta_cleaning"]))

    logger.info("\nLST dynamic cleaning:")
    logger.info(format_object(config_lst["dynamic_cleaning"]))

    use_time_delta_cleaning = config_lst["time_delta_cleaning"].pop("use")
    use_dynamic_cleaning = config_lst["dynamic_cleaning"].pop("use")

    use_only_main_island = config_lst["use_only_main_island"]
    logger.info(f"\nLST use only main island: {use_only_main_island}")

    # Configure the MAGIC event processors
    config_magic = config["MAGIC"]

    logger.info("\nMAGIC image extractor:")
    logger.info(format_object(config_magic["image_extractor"]))

    extractor_type_magic = config_magic["image_extractor"].pop("type")
    config_extractor_magic = {extractor_type_magic: config_magic["image_extractor"]}

    calibrator_magic = CameraCalibrator(
        image_extractor_type=extractor_type_magic,
        config=Config(config_extractor_magic),
        subarray=subarray,
    )

    logger.info("\nMAGIC charge correction:")
    logger.info(format_object(config_magic["charge_correction"]))

    use_charge_correction = config_magic["charge_correction"].pop("use")

    if config_magic["magic_clean"]["find_hotpixels"]:
        logger.warning(
            "\nWARNING: Hot pixels do not exist in a simulation. "
            "Setting the `find_hotpixels` option to False..."
        )
        config_magic["magic_clean"].update({"find_hotpixels": False})

    logger.info("\nMAGIC image cleaning:")
    logger.info(format_object(config_magic["magic_clean"]))

    magic_clean = {
        tel_id_m1: MAGICClean(camera_geoms[tel_id_m1], config_magic["magic_clean"]),
        tel_id_m2: MAGICClean(camera_geoms[tel_id_m2], config_magic["magic_clean"]),
    }

    # Prepare for saving data to an output file
    Path(output_dir).mkdir(exist_ok=True, parents=True)

    sim_config = event_source.simulation_config
    corsika_inputcard = event_source.file_.corsika_inputcards[0].decode()

    regex = r".*\nPRMPAR\s+(\d+)\s+.*"

    particle_id = int(re.findall(regex, corsika_inputcard)[0])
    particle_type = PARTICLE_TYPES.get(particle_id, "unknown")

    zenith = 90 - sim_config["max_alt"].to_value("deg")
    azimuth = Angle(sim_config["max_az"]).wrap_at("360 deg").degree

    output_file = (
        f"{output_dir}/dl1_{particle_type}_zd_{zenith.round(3)}deg_"
        f"az_{azimuth.round(3)}deg_LST-1_MAGIC_run{obs_id}.h5"
    )

    # Loop over every shower event
    logger.info("\nProcessing the events...")

    with HDF5TableWriter(output_file, group_name="events", mode="w") as writer:
        for event in event_source:
            if event.count % 100 == 0:
                logger.info(f"{event.count} events")

            tels_with_trigger = event.trigger.tels_with_trigger

            # Check if the event triggers both M1 and M2 or not
            trigger_m1 = tel_id_m1 in tels_with_trigger
            trigger_m2 = tel_id_m2 in tels_with_trigger

            magic_stereo = trigger_m1 and trigger_m2

            for tel_id in tels_with_trigger:
                if tel_id == tel_id_lst1:
                    # Calibrate the LST-1 event
                    calibrator_lst._calibrate_dl0(event, tel_id)
                    calibrator_lst._calibrate_dl1(event, tel_id)

                    image = event.dl1.tel[tel_id].image.astype(np.float64)
                    peak_time = event.dl1.tel[tel_id].peak_time.astype(np.float64)

                    if increase_nsb:
                        # Add extra noise in pixels
                        image = add_noise_in_pixels(
                            rng, image, **config_lst["increase_nsb"]
                        )

                    if increase_psf:
                        # Smear the image
                        image = random_psf_smearer(
                            image=image,
                            fraction=config_lst["increase_psf"]["fraction"],
                            indices=camera_geoms[tel_id].neighbor_matrix_sparse.indices,
                            indptr=camera_geoms[tel_id].neighbor_matrix_sparse.indptr,
                        )

                    # Apply the image cleaning
                    signal_pixels = tailcuts_clean(
                        camera_geoms[tel_id], image, **config_lst["tailcuts_clean"]
                    )

                    if use_time_delta_cleaning:
                        signal_pixels = apply_time_delta_cleaning(
                            geom=camera_geoms[tel_id],
                            mask=signal_pixels,
                            arrival_times=peak_time,
                            **config_lst["time_delta_cleaning"],
                        )

                    if use_dynamic_cleaning:
                        signal_pixels = apply_dynamic_cleaning(
                            image, signal_pixels, **config_lst["dynamic_cleaning"]
                        )

                    if use_only_main_island:
                        _, island_labels = number_of_islands(
                            camera_geoms[tel_id], signal_pixels
                        )
                        n_pixels_on_island = np.bincount(island_labels.astype(np.int64))

                        # The first index means the pixels not surviving
                        # the cleaning, so should not be considered
                        n_pixels_on_island[0] = 0
                        max_island_label = np.argmax(n_pixels_on_island)
                        signal_pixels[island_labels != max_island_label] = False

                else:
                    # Calibrate the MAGIC event
                    calibrator_magic._calibrate_dl0(event, tel_id)
                    calibrator_magic._calibrate_dl1(event, tel_id)

                    image = event.dl1.tel[tel_id].image.astype(np.float64)
                    peak_time = event.dl1.tel[tel_id].peak_time.astype(np.float64)

                    if use_charge_correction:
                        # Scale the charges by the correction factor
                        image *= config_magic["charge_correction"]["factor"]

                    # Apply the image cleaning
                    signal_pixels, image, peak_time = magic_clean[tel_id].clean_image(
                        event_image=image, event_pulse_time=peak_time
                    )

                if not any(signal_pixels):
                    logger.info(
                        f"--> {event.count} event (event ID: {event.index.event_id}, "
                        f"telescope {tel_id}) could not survive the image cleaning. "
                        "Skipping..."
                    )
                    continue

                n_pixels = np.count_nonzero(signal_pixels)
                n_islands, _ = number_of_islands(camera_geoms[tel_id], signal_pixels)

                camera_geom_masked = camera_geoms[tel_id][signal_pixels]
                image_masked = image[signal_pixels]
                peak_time_masked = peak_time[signal_pixels]

                if any(image_masked < 0):
                    logger.info(
                        f"--> {event.count} event (event ID: {event.index.event_id}, "
                        f"telescope {tel_id}) cannot be parametrized due to the pixels "
                        "with negative charges. Skipping..."
                    )
                    continue

                # Parametrize the image
                hillas_params = hillas_parameters(camera_geom_masked, image_masked)

                timing_params = timing_parameters(
                    camera_geom_masked, image_masked, peak_time_masked, hillas_params
                )

                if np.isnan(timing_params.slope):
                    logger.info(
                        f"--> {event.count} event (event ID: {event.index.event_id}, "
                        f"telescope {tel_id}) failed to extract finite timing "
                        "parameters. Skipping..."
                    )
                    continue

                leakage_params = leakage_parameters(
                    camera_geoms[tel_id], image, signal_pixels
                )

                # Calculate additional parameters
                true_disp = calculate_disp(
                    pointing_alt=event.pointing.tel[tel_id].altitude,
                    pointing_az=event.pointing.tel[tel_id].azimuth,
                    shower_alt=event.simulation.shower.alt,
                    shower_az=event.simulation.shower.az,
                    cog_x=hillas_params.x,
                    cog_y=hillas_params.y,
                    camera_frame=camera_geoms[tel_id].frame,
                )

                true_impact = calculate_impact(
                    shower_alt=event.simulation.shower.alt,
                    shower_az=event.simulation.shower.az,
                    core_x=event.simulation.shower.core_x,
                    core_y=event.simulation.shower.core_y,
                    tel_pos_x=tel_positions[tel_id][0],
                    tel_pos_y=tel_positions[tel_id][1],
                    tel_pos_z=tel_positions[tel_id][2],
                )

                off_axis = angular_separation(
                    lon1=event.pointing.tel[tel_id].azimuth,
                    lat1=event.pointing.tel[tel_id].altitude,
                    lon2=event.simulation.shower.az,
                    lat2=event.simulation.shower.alt,
                )

                # Set the event information
                event_info = SimEventInfoContainer(
                    obs_id=event.index.obs_id,
                    event_id=event.index.event_id,
                    pointing_alt=event.pointing.tel[tel_id].altitude,
                    pointing_az=event.pointing.tel[tel_id].azimuth,
                    true_energy=event.simulation.shower.energy,
                    true_alt=event.simulation.shower.alt,
                    true_az=event.simulation.shower.az,
                    true_disp=true_disp,
                    true_core_x=event.simulation.shower.core_x,
                    true_core_y=event.simulation.shower.core_y,
                    true_impact=true_impact,
                    off_axis=off_axis,
                    n_pixels=n_pixels,
                    n_islands=n_islands,
                    magic_stereo=magic_stereo,
                )

                # Reset the telescope IDs
                if tel_id == tel_id_lst1:
                    event_info.tel_id = 1

                elif tel_id == tel_id_m1:
                    event_info.tel_id = 2

                elif tel_id == tel_id_m2:
                    event_info.tel_id = 3

                # Save the parameters to the output file
                writer.write(
                    "parameters",
                    (event_info, hillas_params, timing_params, leakage_params),
                )

        n_events_processed = event.count + 1
        logger.info(f"\nIn total {n_events_processed} events are processed.")

    # Convert the telescope coordinate to the one relative to the center
    # of the LST-1 and MAGIC positions, and reset the telescope IDs
    position_mean = u.Quantity(list(tel_positions.values())).mean(axis=0)

    tel_positions_lst1_magic = {
        1: tel_positions[tel_id_lst1] - position_mean,  # LST-1
        2: tel_positions[tel_id_m1] - position_mean,  # MAGIC-I
        3: tel_positions[tel_id_m2] - position_mean,  # MAGIC-II
    }

    tel_descriptions_lst1_magic = {
        1: tel_descriptions[tel_id_lst1],  # LST-1
        2: tel_descriptions[tel_id_m1],  # MAGIC-I
        3: tel_descriptions[tel_id_m2],  # MAGIC-II
    }

    subarray_lst1_magic = SubarrayDescription(
        "LST1-MAGIC-Array", tel_positions_lst1_magic, tel_descriptions_lst1_magic
    )

    # Save the subarray description
    subarray_lst1_magic.to_hdf(output_file)

    # Save the simulation configuration
    with HDF5TableWriter(output_file, group_name="simulation", mode="a") as writer:
        writer.write("config", sim_config)

    logger.info(f"\nOutput file: {output_file}")


def main():
    start_time = time.time()

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input-file",
        "-i",
        dest="input_file",
        type=str,
        required=True,
        help="Path to an input simtel MC DL0 data file",
    )

    parser.add_argument(
        "--output-dir",
        "-o",
        dest="output_dir",
        type=str,
        default="./data",
        help="Path to a directory where to save an output DL1 data file",
    )

    parser.add_argument(
        "--config-file",
        "-c",
        dest="config_file",
        type=str,
        default="./config.yaml",
        help="Path to a configuration file",
    )

    args = parser.parse_args()

    with open(args.config_file, "rb") as f:
        config = yaml.safe_load(f)

    # Process the input data
    mc_dl0_to_dl1(args.input_file, args.output_dir, config)

    logger.info("\nDone.")

    process_time = time.time() - start_time
    logger.info(f"\nProcess time: {process_time:.0f} [sec]\n")


if __name__ == "__main__":
    main()
