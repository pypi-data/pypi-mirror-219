# Copyright 2004-2023 Bright Computing Holding BV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from glob import glob

from clusterondemand.images.find import CODImage, ImageSource


class LocalManifestImageSource(ImageSource):
    @classmethod
    def from_config(cls, config, ids=None):
        return LocalManifestImageSource(
            ids=ids if ids is not None else config["ids"],
            tags=config["tags"],
            version=config["version"],
            distro=config["distro"],
            package_groups=config["package_groups"],
            revision=config["revision"],
            status=config["status"],
            advanced=config["advanced"],
            image_visibility=config["image_visibility"],
            cloud_type=config["cloud_type"],
        )

    def _iter_from_source(self):
        manifest_files = find_manifest_files(self.ids)
        return (make_cod_image_from_manifest(manifest_file) for manifest_file in manifest_files)


def make_cod_image_from_manifest(manifest_file):
    """
    Wraps CODImage.from_manifest_file, implemented for readability and consistency with other imageX modules
    Constructs CODImage object from the manifest file
    :param manifest_file: path to the manifest file
    :return: CODImage object
    """
    return CODImage.from_manifest_file(manifest_file)


def find_manifest_files(ids=None, path="."):
    """
    find manifest files in the current (by default) or other directory and return their paths
    :param path: path to manifest, by default current directory. Currently not used, for future compatibility
    :param ids: list of id, revision pairs: [('ubuntu1604-9.0', 4)]
    :return: ["path/to/manifest"]
    """
    if not ids:  # If no image ids specified on the command line, detect all .manifest files
        ids = [("*", "*")]

    manifests = []
    for id_rev in ids:
        image_id, revision = id_rev
        manifests += (glob(f"{path}/*-{image_id}-{revision}*manifest"))
    return manifests
