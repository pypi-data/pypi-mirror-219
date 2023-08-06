from setuptools import Command, find_packages, setup

__lib_name__ = "STGMVA"
__lib_version__ = "1.0.0"
__description__ = "Clustering, imputation, and integration for spatial transcriptomics using spatiotemporal gaussian mixture variational autoencoder"
__url__ = "https://github.com/narutoten520/STGMVA"
__author__ = "Teng Liu"
__author_email__ = "tengliu17@gmail.com"
__license__ = "MIT"
__keywords__ = ["Spatial transcriptomics", "gaussian mixture model", "variational graph autoencoder", "spatial clustering", "gene imputation", "multi-sample integration"]
__requires__ = ["requests",]

with open("README.rst", "r", encoding="utf-8") as f:
    __long_description__ = f.read()

setup(
    name = __lib_name__,
    version = __lib_version__,
    description = __description__,
    url = __url__,
    author = __author__,
    author_email = __author_email__,
    license = __license__,
    packages = ["STGMVA"],
    install_requires = __requires__,
    zip_safe = False,
    include_package_data = True,
    long_description = """ In this study, we present STGMVA, a comprehensive analysis toolkit employs a spatiotemporal gaussian mixture variational autoencoder to tackle these tasks effectively. STGMVA consists of two stages: pretraining the gene expression and spatial location using a gaussian mixture model, and learning the embedding vectors through a variational graph autoencoder. Results demonstrate STGMVA surpasses state-of-the-art approaches on various spatial transcriptomics datasets, exhibiting superior performance across different scales and resolutions. Notably, STGMVA achieves the highest clustering accuracy in human brain, mouse hippocampus, and mouse olfactory bulb tissues. Furthermore, STGMVA enhances and denoises gene expression patterns for gene imputation task. Additionally, STGMVA has the capability to correct batch effects and achieve joint analysis when integrating multiple tissue slices. """,
    long_description_content_type="text/markdown"
)
