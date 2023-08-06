from .SHDownloader import SHDownloader
from sentinelhub import MosaickingOrder


class SHS2Downloader(SHDownloader):
    def __init__(self, download_folder):
        super().__init__(download_folder)
        self.resolution = 10  # mpp
        self.mosaicking_order = MosaickingOrder.LEAST_CC
        self.script = """
            //VERSION=3
            function setup() {
                return {
                    input: [{
                        bands: ["B01","B02","B03","B04","B05","B06","B07","B08","B8A","B09","B11","B12"],
                        units: "DN"
                    }],
                    output: {
                        bands: 12,
                        sampleType: "INT16"
                    }
                };
            }

            function evaluatePixel(sample) {
                return [sample.B01,
                        sample.B02,
                        sample.B03,
                        sample.B04,
                        sample.B05,
                        sample.B06,
                        sample.B07,
                        sample.B08,
                        sample.B8A,
                        sample.B09,
                        sample.B11,
                        sample.B12];
            }
        """
