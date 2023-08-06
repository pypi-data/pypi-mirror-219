import glob, sys
import logging

import numpy as np

np.set_printoptions(threshold=sys.maxsize)
import scipy

from ctapipe_io_magic import MAGICEventSource

from ctapipe.instrument import CameraGeometry
from ctapipe.image import hillas_parameters

import argparse

from magicctapipe.utils import MAGIC_Badpixels

# from magicctapipe.utils import bad_pixel_treatment
from magicctapipe.utils import MAGIC_Cleaning

logger = logging.getLogger(__name__)


def main():
    usage = "usage: %(prog)s [options] "
    description = "Run gtselect and gtmktime on one or more FT1 files.  "
    "Note that gtmktime will be skipped if no FT2 file is provided."
    parser = argparse.ArgumentParser(usage=usage, description=description)
    parser.add_argument("-m", "--mc", dest="mc", action="store_true")

    args = parser.parse_args()

    tel_id = 1

    # when comparing to MARS images
    mars_camera = CameraGeometry.from_name("MAGICCamMars")

    # for consistent usage within ctapipe/with LST - image is mirrored on x=-y axis
    # ars_camera = CameraGeometry.from_name("MAGICCam")

    neighbors = mars_camera.neighbor_matrix_sparse
    outermost = []
    for pix in range(mars_camera.n_pixels):
        if neighbors[pix].getnnz() < 5:
            outermost.append(pix)

    cleaning_config = dict(
        picture_thresh=6,
        boundary_thresh=3.5,
        max_time_off=4.5 * 1.64,
        max_time_diff=1.5 * 1.64,
        usetime=True,
        usesum=True,
        findhotpixels=True,
    )

    bad_pixels_config = dict(
        pedestalLevel=400, pedestalLevelVariance=4.5, pedestalType="FromExtractorRndm"
    )

    magic_clean = MAGIC_Cleaning.magic_clean(mars_camera, cleaning_config)
    badpixel_calculator = MAGIC_Badpixels.MAGICBadPixelsCalc(config=bad_pixels_config)

    all_events = []

    if args.mc:
        """MC FILES"""
        mars_file_mask = "/remote/ceph/group/magic/MAGIC-LST/MCs/MAGIC/ST.03.07/za05to35/Train_sample/1.Calibrated/GA_M1*root"
        mars_file_list = glob.glob(
            mars_file_mask
        )  #  Here makes array which contains files matching the input condition (GA_M1*root).
        file_list = list(filter(lambda name: "123" in name, mars_file_list))
        print("Number of files : %s" % len(file_list))
    else:
        """DATA FILES"""
        mars_file_mask = (
            "/Users/moritz/Documents/MAGIC-data/Crab/Data/Sorcerer/2020*.root"
        )
        mars_file_list = glob.glob(
            mars_file_mask
        )  #  Here makes array which contains files matching the input condition (GA_M1*root).
        file_list = list(filter(lambda name: "0" in name, mars_file_list))
        print("Number of files : %s" % len(file_list))

    for ix, file_name in enumerate(file_list):
        magic_event_source = MAGICEventSource(input_url=file_name)
        event_generator = magic_event_source._mono_event_generator("M1")

        for i, event in enumerate(event_generator):
            if i > 1e30:
                break
            if i % 1000 == 0:
                print("Event %s" % i)

            if args.mc:
                all_events.append(event.mc.energy.value)

            badrmspixel_mask = badpixel_calculator.get_badrmspixel_mask(event)
            deadpixel_mask = badpixel_calculator.get_deadpixel_mask(event)
            unsuitable_mask = np.logical_or(badrmspixel_mask[0], deadpixel_mask[0])

            event_image = event.dl1.tel[tel_id].image
            event_pulse_time = event.dl1.tel[tel_id].peak_time

            clean_mask, event_image, event_pulse_time = magic_clean.clean_image(
                event_image, event_pulse_time, unsuitable_mask=unsuitable_mask
            )

            event_image_cleaned = event_image.copy()
            event_image_cleaned[~clean_mask] = 0

            event_pulse_time_cleaned = event_pulse_time.copy()
            event_pulse_time_cleaned[~clean_mask] = 0

            if scipy.any(event_image_cleaned):
                try:
                    hillas_params = hillas_parameters(mars_camera, event_image_cleaned)
                except:
                    continue

                logger.debug(
                    "EvtNum : %i, Size : %f, Core : %i, Used %i"
                    % (
                        event.dl0.event_id,
                        hillas_params.intensity,
                        magic_clean.core_pix,
                        magic_clean.used_pix,
                    )
                )


if __name__ == "__main__":
    main()
