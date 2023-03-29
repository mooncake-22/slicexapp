# ==================================================================================
#
#       Copyright (c) 2020 Samsung Electronics Co., Ltd. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ==================================================================================

from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='slicexapp',
    version='0.0.1',
    packages=find_packages(),
    license='Apache 2.0',
    description="Slice XAPP for O-RAN RIC Platform",
    python_requires='>=3.8',
    install_requires=["ricxappframe==2.3.0","schedule>=0.0.0", "influxdb", "grpcio==1.51.3"],
    entry_points={"console_scripts": ["run-slicexapp.py=src.main:launchXapp"]},  # adds a magical entrypoint for Docker
)

