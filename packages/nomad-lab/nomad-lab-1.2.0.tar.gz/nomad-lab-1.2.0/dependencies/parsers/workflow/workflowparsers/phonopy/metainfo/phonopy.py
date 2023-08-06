#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD.
# See https://nomad-lab.eu for further info.
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
#
import numpy as np            # pylint: disable=unused-import
import typing                 # pylint: disable=unused-import
from nomad.metainfo import (  # pylint: disable=unused-import
    MSection, MCategory, Category, Package, Quantity, Section, SubSection, SectionProxy,
    Reference
)
from nomad.datamodel.metainfo import simulation


m_package = Package()


class x_phonopy_input(MCategory):
    '''
    Information about properties that concern phonopy calculations.
    '''

    m_def = Category()


class Method(simulation.method.Method):

    m_def = Section(validate=False, extends_base_section=True)

    x_phonopy_displacement = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        Amplitude of the atom diplacement for the phonopy supercell
        ''',
        categories=[x_phonopy_input])

    x_phonopy_symprec = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        Symmetry threshold for the space group identification of the crystal for which the
        vibrational properties are to be calculated
        ''',
        categories=[x_phonopy_input])


class System(simulation.system.System):

    m_def = Section(validate=False, extends_base_section=True)

    x_phonopy_original_system_ref = Quantity(
        type=simulation.system.System,
        shape=[],
        description='''
        Original cell from which the supercell for the DFT calculations was constructed
        ''')
