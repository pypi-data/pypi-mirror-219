#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
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

import re
import numpy as np
from typing import List, Union, Any, Optional, Iterable
import ase.data
from matid import SymmetryAnalyzer  # pylint: disable=import-error
import matid.geometry  # pylint: disable=import-error

from nomad import config
from nomad import atomutils
from nomad.utils import traverse_reversed
from nomad.atomutils import Formula
from nomad.normalizing.normalizer import Normalizer
from nomad.normalizing.method import MethodNormalizer
from nomad.normalizing.material import MaterialNormalizer
from nomad.datamodel.metainfo.workflow import Workflow
from nomad.datamodel.metainfo.simulation.system import System, Symmetry as SystemSymmetry
from nomad.datamodel.metainfo.simulation.workflow import ThermodynamicsResults
from nomad.normalizing.common import structures_2d
from nomad.datamodel.results import (
    BandGap,
    BandGapDeprecated,
    RadialDistributionFunction,
    RadiusOfGyration,
    MeanSquaredDisplacement,
    Results,
    Material,
    Method,
    GeometryOptimization,
    Trajectory,
    MolecularDynamics,
    MDProvenance,
    TemperatureDynamic,
    VolumeDynamic,
    PressureDynamic,
    EnergyDynamic,
    Properties,
    StructuralProperties,
    DynamicalProperties,
    EnergyVolumeCurve,
    BulkModulus,
    ShearModulus,
    MechanicalProperties,
    ElectronicProperties,
    VibrationalProperties,
    ThermodynamicProperties,
    BandStructureElectronic,
    BandStructurePhonon,
    DOSElectronic,
    DOSPhonon,
    GreensFunctionsElectronic,
    EnergyFreeHelmholtz,
    HeatCapacityConstantVolume,
)

re_label = re.compile("^([a-zA-Z][a-zA-Z]?)[^a-zA-Z]*")
elements = set(ase.data.chemical_symbols)


def valid_array(array: Any) -> bool:
    """Checks if the given variable is a non-empty array.
    """
    return array is not None and len(array) > 0


def isint(value: Any) -> bool:
    """Checks if the given variable can be interpreted as an integer.
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


class ResultsNormalizer(Normalizer):
    domain = None

    def normalize(self, logger=None) -> None:
        # Setup logger
        if logger is not None:
            self.logger = logger.bind(normalizer=self.__class__.__name__)

        results = self.entry_archive.results
        if results is None:
            results = self.entry_archive.m_create(Results)
        if results.properties is None:
            results.m_create(Properties)

        if self.section_run:
            self.normalize_run(logger=self.logger)

        for measurement in self.entry_archive.measurement:
            self.normalize_measurement(measurement)

    def normalize_sample(self, sample) -> None:
        material = self.entry_archive.m_setdefault("results.material")

        if sample.elements and len(sample.elements) > 0:
            material.elements = sample.elements
        else:
            # Try to guess elements from sample formula or name
            if sample.chemical_formula:
                try:
                    material.elements = list(set(ase.Atoms(sample.chemical_formula).get_chemical_symbols()))
                except Exception:
                    if sample.name:
                        try:
                            material.elements = list(set(ase.Atoms(sample.name).get_chemical_symbols()))
                        except Exception:
                            pass
        if sample.chemical_formula:
            material.chemical_formula_descriptive = sample.chemical_formula

        try:
            if material.chemical_formula_descriptive:
                formula = Formula(material.chemical_formula_descriptive)
                if not material.elements:
                    material.elements = formula.elements()
                material.elemental_composition = formula.elemental_composition()
                material.chemical_formula_hill = formula.format('hill')
                material.chemical_formula_reduced = formula.format('reduced')
                material.chemical_formula_iupac = formula.format('iupac')
                material.chemical_formula_descriptive = formula.format('descriptive')
        except Exception as e:
            self.logger.warn('could not normalize material', exc_info=e)

    def normalize_measurement(self, measurement) -> None:
        results = self.entry_archive.results

        # Method
        if results.method is None:
            results.method = Method(
                method_name=measurement.method_abbreviation)

        # Sample
        if results.material is None:
            results.material = Material(elements=[])
        if len(measurement.sample) > 0:
            self.normalize_sample(measurement.sample[0])

    def normalize_run(self, logger=None) -> None:
        # Fetch different information resources from which data is gathered
        repr_system = None
        for section in self.section_run.system:
            if section.is_representative:
                repr_system = section
                break
        try:
            optimade = self.entry_archive.metadata.optimade
        except Exception:
            optimade = None

        repr_symmetry = None
        if repr_system and repr_system.symmetry:
            repr_symmetry = repr_system.symmetry[0]

        # Create the section and populate the subsections
        results = self.entry_archive.results
        properties, conv_atoms, wyckoff_sets, spg_number = self.properties(repr_system, repr_symmetry)
        results.properties = properties
        results.material = MaterialNormalizer(
            self.entry_archive,
            repr_system,
            repr_symmetry,
            spg_number,
            conv_atoms,
            wyckoff_sets,
            properties,
            optimade,
            logger
        ).material()

        results.method = MethodNormalizer(self.entry_archive, repr_system, results.material, logger).method()

        # set entry type based on method and material
        workflow = self.entry_archive.workflow2
        if workflow is not None:

            workflow_name = workflow.name if workflow.name else workflow.m_def.name

            tag = ''
            if results.method.simulation:
                tag = 'simulation'

            try:
                method_name = results.method.method_name
                program_name = results.method.simulation.program_name
                if workflow_name == 'SinglePoint' and method_name:
                    self.entry_archive.metadata.entry_type = f'{program_name} {method_name} {workflow_name}'
                else:
                    self.entry_archive.metadata.entry_type = f'{program_name} {workflow_name}'
            except Exception:
                self.entry_archive.metadata.entry_type = workflow_name
            type_tag = f'{self.entry_archive.metadata.entry_type} {tag}'

            # Populate entry_name
            material = results.material
            if material and material.chemical_formula_descriptive:
                self.entry_archive.metadata.entry_name = f'{material.chemical_formula_descriptive} {type_tag}'
            else:
                self.entry_archive.metadata.entry_name = f'{type_tag}'

    def resolve_band_gap(self, path: list[str]) -> Union[List[BandGap], None]:
        """Extract all band gaps from the given `path` and return them in a list along
        with their provenance.
        """
        band_gaps = traverse_reversed(self.entry_archive, path)
        if not band_gaps:
            return None
        bg_root: List[BandGap] = []
        for bg in band_gaps:
            bg_new = BandGap()
            bg_new.index = bg.index
            bg_new.value = bg.value
            bg_new.type = bg.type
            bg_new.energy_highest_occupied = bg.energy_highest_occupied
            bg_new.energy_lowest_unoccupied = bg.energy_lowest_unoccupied
            bg_new.provenance = bg.provenance
            bg_root.insert(0, bg_new)
        return bg_root

    def resolve_band_structure(self, path: list[str]) -> Union[List[BandStructureElectronic], None]:
        """Returns a new section containing an electronic band structure. In
        the case of multiple valid band structures, only the latest one is
        considered.

        Band structure is reported only under the following conditions:
            - There is a non-empty array of kpoints.
            - There is a non-empty array of energies.
        """
        band_structures = traverse_reversed(self.entry_archive, path)
        if not band_structures:
            return None
        bs_root: List[BandStructureElectronic] = []
        for bs in band_structures:
            if not bs.segment:
                continue
            valid = True
            for segment in bs.segment:
                energies = segment.energies
                k_points = segment.kpoints
                if not valid_array(energies) or not valid_array(k_points):
                    valid = False
                    break
            if valid:
                # Fill band structure data to the newer, improved data layout
                bs_new = BandStructureElectronic()
                bs_new.reciprocal_cell = bs
                bs_new.segment = bs.segment
                bs_new.spin_polarized = bs_new.segment[0].energies.shape[0] > 1
                bs_new.energy_fermi = bs.energy_fermi

                for info in bs.band_gap:
                    info_new = BandGapDeprecated().m_from_dict(info.m_to_dict())
                    bs_new.m_add_sub_section(BandStructureElectronic.band_gap, info_new)
                bs_root.insert(0, bs_new)
        return bs_root

    def resolve_dos(self, path: list[str]) -> Union[List[DOSElectronic], None]:
        """Returns a reference to the section containing an electronic dos. In
        the case of multiple valid DOSes, only the latest one is reported.

        DOS is reported only under the following conditions:
            - There is a non-empty array of dos_values_normalized.
            - There is a non-empty array of dos_energies.
        """
        doss = traverse_reversed(self.entry_archive, path)
        if not doss:
            return None
        dos_root: List[DOSElectronic] = []
        for dos in doss:
            energies = dos.energies
            values = np.array([d.value.magnitude for d in dos.total])
            if valid_array(energies) and valid_array(values):
                dos_new = DOSElectronic()
                dos_new.energies = dos
                dos_new.total = dos.total
                n_channels = values.shape[0]
                dos_new.spin_polarized = n_channels > 1
                dos_new.energy_fermi = dos.energy_fermi
                for info in dos.band_gap:
                    info_new = BandGapDeprecated().m_from_dict(info.m_to_dict())
                    dos_new.m_add_sub_section(DOSElectronic.band_gap, info_new)
                dos_root.insert(0, dos_new)
        return dos_root

    def resolve_greens_functions(self, path: list[str]) -> Union[List[GreensFunctionsElectronic], None]:
        """Returns a reference to the section containing the electronic Green's functions.
        In the case of multiple valid Green's functions sections, only the latest one is reported.

        Green's functions are reported only under the following conditions:
            - There is a non-empty array of greens_function_tau or self_energy_iw or occupancies.
            - There is a non-empty array of tau or matsubara_freq.
        """
        greens_functions = traverse_reversed(self.entry_archive, path)
        if not greens_functions:
            return None
        gfs_root: List[GreensFunctionsElectronic] = []
        for gfs in greens_functions:
            tau = gfs.tau
            iw = gfs.matsubara_freq
            values_gtau = np.array([np.absolute(gtau) for gtau in gfs.greens_function_tau.real])
            values_siw = np.array([siw for siw in gfs.self_energy_iw.imag])
            if (valid_array(tau) and valid_array(values_gtau)) or (valid_array(iw) and valid_array(values_siw)):
                gfs_new = GreensFunctionsElectronic()
                gfs_new.chemical_potential = gfs.chemical_potential
                if valid_array(tau) and valid_array(values_gtau):
                    gfs_new.tau = tau
                    gfs_new.real_greens_function_tau = values_gtau
                if valid_array(iw) and valid_array(values_siw):
                    gfs_new.matsubara_freq = iw
                    gfs_new.imag_self_energy_iw = values_siw
                if valid_array(gfs.orbital_occupations):
                    gfs_new.orbital_occupations = gfs.orbital_occupations
                if valid_array(gfs.quasiparticle_weights):
                    gfs_new.quasiparticle_weights = gfs.quasiparticle_weights

                gfs_root.insert(0, gfs_new)
        return gfs_root

    def gw_workflow_properties(self):
        bg_electronic = self.electronic_properties[0]
        bs_electronic = self.electronic_properties[1]
        dos_electronic = self.electronic_properties[2]
        for method in ['dft', 'gw']:
            name = method.upper()
            bgs = self.resolve_band_gap(["workflow2", "results", f"band_gap_{method}"])
            bss = self.resolve_band_structure(["workflow2", "results", f"band_structure_{method}"])
            doss = self.resolve_dos(["workflow2", "results", f"dos_{method}"])
            for bg in bgs:
                bg.label = name
                bg_electronic.append(bg)
            for bs in bss:
                bs.label = name
                for band_gap in bs.band_gap:
                    band_gap.label = name
                bs_electronic.append(bs)
            for d in doss:
                d.label = name
                for band_gap in d.band_gap:
                    band_gap.label = name
                dos_electronic.append(d)
        return [bg_electronic, bs_electronic, dos_electronic, []]

    def band_structure_phonon(self) -> Union[BandStructurePhonon, None]:
        """Returns a new section containing a phonon band structure. In
        the case of multiple valid band structures, only the latest one is
        considered.

       Band structure is reported only under the following conditions:
          - There is a non-empty array of kpoints.
          - There is a non-empty array of energies.
        """
        path = ["run", "calculation", "band_structure_phonon"]
        for bs in traverse_reversed(self.entry_archive, path):
            if not bs.segment:
                continue
            valid = True
            for segment in bs.segment:
                energies = segment.energies
                k_points = segment.kpoints
                if not valid_array(energies) or not valid_array(k_points):
                    valid = False
                    break
            if valid:
                # Fill band structure data to the newer, improved data layout
                bs_new = BandStructurePhonon()
                bs_new.segment = bs.segment
                return bs_new

        return None

    def dos_phonon(self) -> Union[DOSPhonon, None]:
        """Returns a section containing phonon dos data. In the case of
        multiple valid data sources, only the latest one is reported.

       DOS is reported only under the following conditions:
          - There is a non-empty array of values.
          - There is a non-empty array of energies.
        """
        path = ["run", "calculation", "dos_phonon"]
        for dos in traverse_reversed(self.entry_archive, path):
            energies = dos.energies
            values = np.array([d.value.magnitude for d in dos.total])
            if valid_array(energies) and valid_array(values):
                dos_new = DOSPhonon()
                dos_new.energies = dos
                dos_new.total = dos.total
                return dos_new

        return None

    def energy_free_helmholtz(self) -> Union[EnergyFreeHelmholtz, None]:
        """Returns a section Helmholtz free energy data. In the case of
        multiple valid data sources, only the latest one is reported.

       Helmholtz free energy is reported only under the following conditions:
          - There is a non-empty array of temperatures.
          - There is a non-empty array of energies.
        """
        workflow = self.entry_archive.workflow2
        if workflow is None or not hasattr(workflow, 'results'):
            return None
        if not isinstance(workflow.results, ThermodynamicsResults):
            return None

        path = ["workflow2", "results"]

        for thermo_prop in traverse_reversed(self.entry_archive, path):
            temperatures = thermo_prop.temperature
            energies = thermo_prop.vibrational_free_energy_at_constant_volume
            if valid_array(temperatures) and valid_array(energies):
                energy_free = EnergyFreeHelmholtz()
                energy_free.energies = thermo_prop
                energy_free.temperatures = thermo_prop
                return energy_free

        return None

    def heat_capacity_constant_volume(self) -> Union[HeatCapacityConstantVolume, None]:
        """Returns a section containing heat capacity data. In the case of
        multiple valid data sources, only the latest one is reported.

       Heat capacity is reported only under the following conditions:
          - There is a non-empty array of temperatures.
          - There is a non-empty array of energies.
        """
        workflow = self.entry_archive.workflow2
        if workflow is None or not hasattr(workflow, 'results'):
            return None
        if not isinstance(workflow.results, ThermodynamicsResults):
            return None

        path = ["workflow2", "results"]
        for thermo_prop in traverse_reversed(self.entry_archive, path):
            temperatures = thermo_prop.temperature
            heat_capacities = thermo_prop.heat_capacity_c_v
            if valid_array(temperatures) and valid_array(heat_capacities):
                heat_cap = HeatCapacityConstantVolume()
                heat_cap.heat_capacities = thermo_prop
                heat_cap.temperatures = thermo_prop
                return heat_cap

        return None

    def geometry_optimization(self) -> Union[GeometryOptimization, None]:
        """Populates both geometry optimization methodology and calculated
        properties based on the first found geometry optimization workflow.
        """
        path = ["workflow2"]
        for workflow in traverse_reversed(self.entry_archive, path):
            # Check validity
            if workflow.m_def.name == 'GeometryOptimization':
                geo_opt = GeometryOptimization()
                if workflow.results:
                    geo_opt.trajectory = workflow.results.calculations_ref
                    if workflow.results.calculation_result_ref:
                        geo_opt.system_optimized = workflow.results.calculation_result_ref.system_ref
                    geo_opt.energies = workflow.results
                    geo_opt.final_energy_difference = workflow.results.final_energy_difference
                    geo_opt.final_force_maximum = workflow.results.final_force_maximum
                    geo_opt.final_displacement_maximum = workflow.results.final_displacement_maximum
                if workflow.method is not None:
                    geo_opt.type = workflow.method.type
                    geo_opt.convergence_tolerance_energy_difference = workflow.method.convergence_tolerance_energy_difference
                    geo_opt.convergence_tolerance_force_maximum = workflow.method.convergence_tolerance_force_maximum
                return geo_opt

        return None

    def get_md_provenance(self, workflow: Workflow) -> Optional[MolecularDynamics]:
        """Retrieves the MD provenance from the given workflow.
        """
        md = None
        if workflow.m_def.name == 'MolecularDynamics':
            try:
                md = MolecularDynamics()
                md.time_step = workflow.method.integration_timestep
                md.ensemble_type = workflow.method.thermodynamic_ensemble
            except Exception:
                pass
        return md

    def trajectory(self) -> List[Trajectory]:
        """Returns a list of trajectories.
        """
        path = ["workflow2"]
        trajs = []
        for workflow in traverse_reversed(self.entry_archive, path):
            # Check validity
            if workflow.m_def.name == "MolecularDynamics":
                traj = Trajectory()
                md = self.get_md_provenance(workflow)
                if md:
                    traj.provenance = MDProvenance(molecular_dynamics=md)

                # Loop through calculations, gather thermodynamics directly
                # from each step in the workflow.
                volume = []
                volume_time = []
                pressure = []
                pressure_time = []
                temperature = []
                temperature_time = []
                potential_energy = []
                potential_energy_time = []

                calculations_ref = []
                if workflow.results and workflow.results.calculations_ref:
                    calculations_ref = workflow.results.calculations_ref
                for calc in calculations_ref:
                    time = calc.time
                    if time is not None:
                        time = time.magnitude
                        if calc.volume is not None:
                            volume.append(calc.volume.magnitude)
                            volume_time.append(time)
                        if calc.pressure is not None:
                            pressure.append(calc.pressure.magnitude)
                            pressure_time.append(time)
                        if calc.temperature is not None:
                            temperature.append(calc.temperature.magnitude)
                            temperature_time.append(time)
                        if calc.energy:
                            if calc.energy.potential is not None:
                                potential_energy.append(calc.energy.potential.value.magnitude)
                                potential_energy_time.append(time)

                available_properties = []
                if volume:
                    traj.volume = VolumeDynamic(value=volume, time=volume_time)
                    available_properties.append('volume')
                if pressure:
                    traj.pressure = PressureDynamic(value=pressure, time=pressure_time)
                    available_properties.append('pressure')
                if temperature:
                    traj.temperature = TemperatureDynamic(value=temperature, time=temperature_time)
                    available_properties.append('temperature')
                if potential_energy:
                    traj.energy_potential = EnergyDynamic(value=potential_energy, time=potential_energy_time)
                    available_properties.append('energy_potential')
                if available_properties:
                    traj.available_properties = available_properties
                trajs.append(traj)
        return trajs

    def rdf(self) -> List[RadialDistributionFunction]:
        """Returns a list of radial distribution functions.
        """
        workflow = self.entry_archive.workflow2
        if workflow is None or workflow.m_def.name != 'MolecularDynamics':
            return None

        path = ["workflow2", "results", "radial_distribution_functions"]
        rdfs = []
        for rdf_workflow in traverse_reversed(self.entry_archive, path):
            rdf_values = rdf_workflow.radial_distribution_function_values
            if rdf_values is not None:
                for rdf_value in rdf_values or []:
                    rdf = RadialDistributionFunction()
                    try:
                        rdf.bins = rdf_value.bins
                        rdf.n_bins = rdf_value.n_bins
                        rdf.value = rdf_value.value
                        rdf.label = rdf_value.label
                        rdf.frame_start = rdf_value.frame_start
                        rdf.frame_end = rdf_value.frame_end
                        rdf.type = rdf_workflow.type
                        md = self.get_md_provenance(rdf_workflow.m_parent.m_parent.m_parent)
                        if md:
                            rdf.provenance = MDProvenance(
                                molecular_dynamics=md
                            )
                    except Exception as e:
                        self.logger.error('error in resolving radial distribution data', exc_info=e)
                    else:
                        rdfs.append(rdf)

        return rdfs

    def rg(self) -> List[RadiusOfGyration]:
        """Returns a list of Radius of gyration trajectories.
        """
        path_workflow = ["workflow2"]
        rgs: List[RadiusOfGyration] = []
        for workflow in traverse_reversed(self.entry_archive, path_workflow):

            # Check validity
            if workflow.m_def.name == "MolecularDynamics" and workflow.results:
                results = workflow.results
                md = self.get_md_provenance(workflow)
                if results.calculations_ref and results.calculations_ref[0].radius_of_gyration:
                    for rg_index, rg in enumerate(results.calculations_ref[0].radius_of_gyration):
                        for rg_values_index, __ in enumerate(rg.radius_of_gyration_values):
                            rg_results = RadiusOfGyration()
                            rg_value = []
                            rg_time = []
                            if md:
                                rg_results.provenance = MDProvenance(molecular_dynamics=md)
                            for calc in results.calculations_ref:
                                sec_rg = calc.radius_of_gyration[rg_index]
                                rg_results.kind = sec_rg.kind
                                time = calc.time
                                if time is not None:
                                    time = time.magnitude
                                sec_rg_values = sec_rg.radius_of_gyration_values[rg_values_index]
                                rg_results.label = sec_rg_values.label
                                rg_results.atomsgroup_ref = sec_rg_values.atomsgroup_ref
                                rg_time.append(time)
                                rg_value.append(sec_rg_values.value.magnitude)
                            rg_results.time = rg_time
                            rg_results.value = rg_value
                    rgs.append(rg_results)
        return rgs

    def msd(self) -> List[MeanSquaredDisplacement]:
        """Returns a list of mean squared displacements.
        """
        workflow = self.entry_archive.workflow2
        if workflow is None or workflow.m_def.name != 'MolecularDynamics':
            return None

        path = ["workflow2", "results", "mean_squared_displacements"]
        msds = []
        for msd_workflow in traverse_reversed(self.entry_archive, path):
            msd_values = msd_workflow.mean_squared_displacement_values
            if msd_values is not None:
                for msd_value in msd_values or []:
                    msd = MeanSquaredDisplacement()
                    try:
                        msd.times = msd_value.times
                        msd.n_times = msd_value.n_times
                        msd.value = msd_value.value
                        msd.label = msd_value.label
                        msd.errors = msd_value.errors
                        msd.type = msd_workflow.type
                        msd.direction = msd_workflow.direction
                        msd.error_type = msd_workflow.error_type
                        diffusion_constant = msd_value.diffusion_constant
                        if diffusion_constant is not None:
                            msd.diffusion_constant_value = diffusion_constant.value
                            msd.diffusion_constant_error_type = diffusion_constant.error_type
                            msd.diffusion_constant_errors = diffusion_constant.errors

                        md = self.get_md_provenance(msd_workflow.m_parent.m_parent.m_parent)
                        if md:
                            msd.provenance = MDProvenance(
                                molecular_dynamics=md
                            )
                    except Exception as e:
                        self.logger.error('error in resolving mean squared displacement data', exc_info=e)
                    else:
                        msds.append(msd)

        return msds

    def properties(
            self,
            repr_system: System,
            repr_symmetry: SystemSymmetry) -> tuple:
        """Returns a populated Properties subsection."""
        properties = Properties()

        # Structures
        conv_atoms = None
        wyckoff_sets = None
        spg_number = None
        if repr_system:
            original_atoms = repr_system.m_cache.get("representative_atoms")
            if original_atoms:
                structural_type = repr_system.type
                if structural_type == "bulk":
                    conv_atoms, _, wyckoff_sets, spg_number = self.structures_bulk(repr_symmetry)
                elif structural_type == "2D":
                    conv_atoms, _, wyckoff_sets, spg_number = structures_2d(original_atoms)
                elif structural_type == "1D":
                    conv_atoms, _ = self.structures_1d(original_atoms)

        # Electronic properties
        bg_electronic = self.resolve_band_gap(['run', 'calculation', 'band_gap'])
        bs_electronic = self.resolve_band_structure(['run', 'calculation', 'band_structure_electronic'])
        dos_electronic = self.resolve_dos(['run', 'calculation', 'dos_electronic'])
        gfs_electronic = self.resolve_greens_functions(['run', 'calculation', 'greens_functions'])
        self.electronic_properties = [bg_electronic, bs_electronic, dos_electronic, gfs_electronic]
        workflow = self.entry_archive.workflow2
        if workflow:
            workflow_name = workflow.m_def.name
            if workflow_name == 'GW':
                self.electronic_properties = self.gw_workflow_properties()

        method_def = {value.sub_section.name: value for _, value in ElectronicProperties.m_def.all_sub_sections.items()}
        if any(self.electronic_properties):
            electronic = ElectronicProperties()
            for electronic_property in self.electronic_properties:
                if electronic_property:
                    if isinstance(electronic_property, Iterable):
                        for prop in electronic_property:
                            electronic.m_add_sub_section(method_def[prop.m_def.name], prop)
                    else:
                        continue
            properties.electronic = electronic

        # Vibrational
        bs_phonon = self.band_structure_phonon()
        dos_phonon = self.dos_phonon()
        energy_free = self.energy_free_helmholtz()
        heat_cap = self.heat_capacity_constant_volume()
        if bs_phonon or dos_phonon or energy_free or heat_cap:
            vibrational = VibrationalProperties()
            if dos_phonon:
                vibrational.dos_phonon = dos_phonon
            if bs_phonon:
                vibrational.band_structure_phonon = bs_phonon
            if energy_free:
                vibrational.energy_free_helmholtz = energy_free
            if heat_cap:
                vibrational.heat_capacity_constant_volume = heat_cap
            properties.vibrational = vibrational

        # Mechanical
        energy_volume_curves = self.energy_volume_curves()
        bulk_modulus = self.bulk_modulus()
        shear_modulus = self.shear_modulus()
        geometry_optimization = self.geometry_optimization()
        if energy_volume_curves or bulk_modulus or shear_modulus or geometry_optimization:
            mechanical = MechanicalProperties()
            for ev in energy_volume_curves:
                mechanical.m_add_sub_section(MechanicalProperties.energy_volume_curve, ev)
            for bm in bulk_modulus:
                mechanical.m_add_sub_section(MechanicalProperties.bulk_modulus, bm)
            for sm in shear_modulus:
                mechanical.m_add_sub_section(MechanicalProperties.shear_modulus, sm)
            properties.mechanical = mechanical

        # Geometry optimization
        properties.geometry_optimization = self.geometry_optimization()

        # Thermodynamic
        trajectory = self.trajectory()
        if trajectory:
            thermodynamic = ThermodynamicProperties()
            thermodynamic.trajectory = trajectory
            properties.thermodynamic = thermodynamic

        # Structural
        rdf = self.rdf()
        rg = self.rg()
        if rdf or rg:
            structural = StructuralProperties()
            structural.radial_distribution_function = rdf
            structural.radius_of_gyration = rg
            properties.structural = structural

        # Dynamical
        msd = self.msd()
        if msd:
            dynamical = DynamicalProperties()
            dynamical.mean_squared_displacement = msd
            properties.dynamical = dynamical

        try:
            n_calc = len(self.section_run.calculation)
        except Exception:
            n_calc = 0
        properties.n_calculations = n_calc

        return properties, conv_atoms, wyckoff_sets, spg_number

    def structures_bulk(self, repr_symmetry):
        """The symmetry of bulk structures has already been analyzed. Here we
        use the cached results.
        """
        conv_atoms = None
        prim_atoms = None
        wyckoff_sets = None
        spg_number = None
        if repr_symmetry:
            symmetry_analyzer = repr_symmetry.m_cache.get("symmetry_analyzer")
            if symmetry_analyzer:
                spg_number = symmetry_analyzer.get_space_group_number()
                conv_atoms = symmetry_analyzer.get_conventional_system()
                prim_atoms = symmetry_analyzer.get_primitive_system()

                # For some reason MatID seems to drop the periodicity, reintroduce it here.
                conv_atoms.set_pbc(True)
                prim_atoms.set_pbc(True)
                try:
                    wyckoff_sets = symmetry_analyzer.get_wyckoff_sets_conventional(return_parameters=True)
                except Exception:
                    self.logger.error('Error resolving Wyckoff sets.')
                    wyckoff_sets = []

        return conv_atoms, prim_atoms, wyckoff_sets, spg_number

    def structures_1d(self, original_atoms):
        conv_atoms = None
        prim_atoms = None
        try:
            # First get a symmetry analyzer and the primitive system
            symm_system = original_atoms.copy()
            symm_system.set_pbc(True)
            symmetry_analyzer = SymmetryAnalyzer(
                symm_system,
                config.normalize.symmetry_tolerance,
                config.normalize.flat_dim_threshold
            )
            prim_atoms = symmetry_analyzer.get_primitive_system()
            prim_atoms.set_pbc(True)

            # Get dimension of system by also taking into account the covalent radii
            dimensions = matid.geometry.get_dimensions(prim_atoms, [True, True, True])
            basis_dimensions = np.linalg.norm(prim_atoms.get_cell(), axis=1)
            gaps = basis_dimensions - dimensions
            periodicity = gaps <= config.normalize.cluster_threshold

            # If one axis is not periodic, return. This only happens if the vacuum
            # gap is not aligned with a cell vector.
            if sum(periodicity) != 1:
                self.logger.warning("could not detect the periodic dimensions in a 1D system")
                return conv_atoms, prim_atoms

            # Translate to center of mass
            conv_atoms = prim_atoms.copy()
            pbc_cm = matid.geometry.get_center_of_mass(prim_atoms)
            cell_center = 0.5 * np.sum(conv_atoms.get_cell(), axis=0)
            translation = cell_center - pbc_cm
            translation[periodicity] = 0
            conv_atoms.translate(translation)
            conv_atoms.wrap()
            conv_atoms.set_pbc(periodicity)

            # Reduce cell size to just fit the system in the non-periodic dimensions.
            conv_atoms = atomutils.get_minimized_structure(conv_atoms)

            # Swap the cell axes so that the periodic one is always the first
            # basis (=a)
            swap_dim = 0
            for i, periodic in enumerate(periodicity):
                if periodic:
                    periodic_dim = i
                    break
            if periodic_dim != swap_dim:
                atomutils.swap_basis(conv_atoms, periodic_dim, swap_dim)

            prim_atoms = conv_atoms
        except Exception as e:
            self.logger.error(
                'could not construct a conventional system for a 1D material',
                exc_info=e
            )
        return conv_atoms, prim_atoms

    def energy_volume_curves(self) -> List[EnergyVolumeCurve]:
        """Returns a list containing the found EnergyVolumeCurves.
        """
        workflow = self.entry_archive.workflow2
        ev_curves: List[EnergyVolumeCurve] = []
        # workflow must be equation of state
        if workflow is None or workflow.m_def.name != 'EquationOfState' or workflow.results is None:
            return ev_curves

        # Volumes must be present
        volumes = workflow.results.volumes
        if not valid_array(volumes):
            self.logger.warning("missing eos volumes")
            return ev_curves

        # Raw EV curve
        energies_raw = workflow.results.energies
        if valid_array(energies_raw):
            ev_curves.append(EnergyVolumeCurve(
                type="raw",
                volumes=workflow.results,
                energies_raw=workflow.results,
            ))
        else:
            self.logger.warning("missing eos energies")

        # Fitted EV curves
        fits = workflow.results.eos_fit
        if not fits:
            return ev_curves
        for fit in fits:
            energies_fitted = fit.fitted_energies
            function_name = fit.function_name
            if valid_array(energies_fitted):
                ev_curves.append(EnergyVolumeCurve(
                    type=function_name,
                    volumes=workflow.results,
                    energies_fit=fit,
                ))

        return ev_curves

    def bulk_modulus(self) -> List[BulkModulus]:
        """Returns a list containing the found BulkModulus.
        """
        workflow = self.entry_archive.workflow2
        bulk_modulus: List[BulkModulus] = []
        if workflow is None or not hasattr(workflow, 'results') or workflow.results is None:
            return bulk_modulus

        if workflow.m_def.name == 'Elastic':
            bulk_modulus_vrh = workflow.results.bulk_modulus_hill
            if bulk_modulus_vrh:
                bulk_modulus.append(BulkModulus(
                    type="voigt_reuss_hill_average",
                    value=bulk_modulus_vrh,
                ))
            bulk_modulus_voigt = workflow.results.bulk_modulus_voigt
            if bulk_modulus_voigt:
                bulk_modulus.append(BulkModulus(
                    type="voigt_average",
                    value=bulk_modulus_voigt,
                ))
            bulk_modulus_reuss = workflow.results.bulk_modulus_reuss
            if bulk_modulus_reuss:
                bulk_modulus.append(BulkModulus(
                    type="reuss_average",
                    value=bulk_modulus_reuss,
                ))

        if workflow.m_def.name == 'EquationOfState':
            fits = workflow.results.eos_fit
            if not fits:
                return bulk_modulus

            for fit in fits:
                modulus = fit.bulk_modulus
                function_name = fit.function_name
                if modulus is not None and function_name:
                    bulk_modulus.append(BulkModulus(
                        type=function_name,
                        value=modulus,
                    ))
                else:
                    self.logger.warning("missing eos fitted energies and/or function name")

        return bulk_modulus

    def shear_modulus(self) -> List[ShearModulus]:
        """Returns a list containing the found ShearModulus.
        """
        workflow = self.entry_archive.workflow2
        shear_modulus: List[ShearModulus] = []
        if workflow is None or not hasattr(workflow, 'results') or workflow.results is None:
            return shear_modulus

        if workflow.m_def.name != 'Elastic':
            return shear_modulus

        shear_modulus_vrh = workflow.results.shear_modulus_hill
        if shear_modulus_vrh:
            shear_modulus.append(ShearModulus(
                type="voigt_reuss_hill_average",
                value=shear_modulus_vrh,
            ))
        shear_modulus_voigt = workflow.results.shear_modulus_voigt
        if shear_modulus_voigt:
            shear_modulus.append(ShearModulus(
                type="voigt_average",
                value=shear_modulus_voigt,
            ))
        shear_modulus_reuss = workflow.results.shear_modulus_reuss
        if shear_modulus_reuss:
            shear_modulus.append(ShearModulus(
                type="reuss_average",
                value=shear_modulus_reuss,
            ))

        return shear_modulus
