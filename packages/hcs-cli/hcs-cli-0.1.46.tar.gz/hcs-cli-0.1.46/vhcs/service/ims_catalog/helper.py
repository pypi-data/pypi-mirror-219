"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from . import images, image_copies

def get_images_by_provider_instance_with_asset_details(providerInstanceId: str):
    all_images = images.list()
    copies = image_copies.list(include_catalog_details=True,
                      search=f"providerInstanceId $eq {providerInstanceId}")
    ret = []
    for copy in copies:
        imageId = copy["catalogDetails"]["imageId"]
        for image in all_images:
            if image['id'] == imageId:
                # add additional info
                image['_assetDetails'] = copy['assetDetails']
                ret.append(image)
                break
    return ret 