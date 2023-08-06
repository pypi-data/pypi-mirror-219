"""
Material property definitions and interfaces for multiple CAE packages
as part of `pymatunits`

Copyright (C) 2023 Adam Cox, Coleby Friedland

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

mat_prop : Material property module originally built to work with
    Abaqus, using the categorical definitions from Abaqus. Capability
    added to interact with Nastran using nastran_utils.

Dependencies
-----------------  -----------------------------------------------------
Abaqus              Code must be Python 2.7 compatible with no outside
                    packages to be used in Abaqus Python interpreter.
nastran_utils       Module written by Adam Cox to interact with Nastran
                    in object-oriented fashion. (Must have Nastran
                    obviously if you wish to use the created model)
pint                Physical quantity manipulation package
numpy               For mean function and indirectly in utils
"""
from os.path import isfile
from math import sqrt
import json
from json.decoder import JSONDecodeError
from pandas import DataFrame
from . import numerical_tolerance
from .units import Q_, convert, UnitSystem
from .utils import rotate_vector
try:
    from abaqusConstants import ENGINEERING_CONSTANTS
except ImportError:
    ENGINEERING_CONSTANTS = 'ENGINEERING_CONSTANTS'
try:
    from abaqusConstants import ISOTROPIC
except ImportError:
    ISOTROPIC = 'ISOTROPIC'
try:
    from abaqusConstants import LAMINA
except ImportError:
    LAMINA = 'LAMINA'
try:
    from abaqusConstants import TRACTION
except ImportError:
    TRACTION = 'TRACTION'
try:
    from abaqusConstants import ENERGY
except ImportError:
    ENERGY = 'ENERGY'
try:
    from abaqusConstants import BK
except ImportError:
    BK = 'BK'
try:
    from abaqusConstants import CARTESIAN
except ImportError:
    CARTESIAN = 'CARTESIAN'
try:
    from abaqusConstants import SHELL
except ImportError:
    SHELL = 'SHELL'
try:
    from abaqusConstants import AXIS_1
except ImportError:
    AXIS_1 = 'AXIS_1'
try:
    from abaqusConstants import AXIS_2
except ImportError:
    AXIS_2 = 'AXIS_2'
try:
    from abaqusConstants import AXIS_3
except ImportError:
    AXIS_3 = 'AXIS_3'
try:
    from abaqusConstants import STACK_1
except ImportError:
    STACK_1 = 'STACK_1'
try:
    from abaqusConstants import STACK_2
except ImportError:
    STACK_2 = 'STACK_2'
try:
    from abaqusConstants import STACK_3
except ImportError:
    STACK_3 = 'STACK_3'
try:
    from abaqusConstants import SPECIFY_ORIENT
except ImportError:
    SPECIFY_ORIENT = 'SPECIFY_ORIENT'
try:
    from abaqusConstants import SPECIFY_THICKNESS
except ImportError:
    SPECIFY_THICKNESS = 'SPECIFY_THICKNESS'
try:
    from abaqusConstants import VALUE
except ImportError:
    VALUE = 'VALUE'
try:
    from abaqusConstants import SOLID
except ImportError:
    SOLID = 'SOLID'
try:
    from abaqusConstants import CONTINUUM_SHELL
except ImportError:
    CONTINUUM_SHELL = 'CONTINUUM_SHELL'
try:
    import nastran_utils
except ImportError:
    nastran_utils = None

ROOM_TEMP = Q_(70.0, 'degF')


class Composite(object):
    def __init__(self, name, ply_materials, orientations, unit_system,
                 layup_thickness=None, thicknesses=None, ply_names=None,
                 symmetric=False):
        """
        Composite object consisting of Material objects with their
        corresponding ply orientations and names

        Parameters
        ----------
        name : str
            Name of composite layup
        unit_system : UnitSystem
            Values will be converted to quantities in this unit system
            for internal consistency
        ply_materials : List[Material]
            List of Material objects to use for plies
        orientations : List[Union[float, Quantity]]
            List of orientation angles
        unit_system : UnitSystem
            Values will be converted to quantities in this unit system
            for internal consistency
        layup_thickness : float, optional
            Thickness of entire layup. Entire this or thicknesses must
            be defined.
        thicknesses : List[Union[float, Quantity]], optional
            List of thickness of each ply. Either this or
            layup_thickness must be defined. If both are defined,
            layup_thickness will be used.
        ply_names : List[str], optional
            List of ply names for building laminate. Default value is
            "ply-{#}"
        symmetric : bool, optional
            Flag for laminate symmetry. Currently only used in Abaqus
            section definition. Default value is False
        """
        self.name = name
        self.ply_materials = ply_materials
        self.orientations = [convert(unit_system, _, 'angle')
                             for _ in orientations]
        if any((all(_ is not None for _ in [layup_thickness, thicknesses]),
                all(_ is None for _ in [layup_thickness, thicknesses]))):
            raise IOError('One of either layup_thickness or thicknesses must '
                          'be defined.')
        elif layup_thickness is not None:
            _t = layup_thickness / len(ply_materials)
            thicknesses = [_t for _ in range(len(ply_materials))]
        elif thicknesses is not None:
            layup_thickness = sum(thicknesses)
        self.layup_thickness = convert(unit_system, layup_thickness, 'length')
        self.thicknesses = [convert(unit_system, _, 'length')
                            for _ in thicknesses]
        if ply_names is None:
            ply_names = ['ply-{}'.format(_) for _ in range(len(ply_materials))]
        self.ply_names = ply_names
        self.symmetric = symmetric
        self.unit_system = unit_system

    def __eq__(self, other):
        try:
            assert isinstance(other, self.__class__)
        except AssertionError:
            return False
        else:
            try:
                assert self.to_dict() == other.to_dict()
            except AssertionError:
                return False
            else:
                return True

    def __str__(self):
        """
        String of information about composite laminate

        Notes
        -----
        Overwrites superclass (Material) __str__

        Returns
        -------
        string : str
        """
        str_ = 'Composite Layup : {}'.format(self.name)
        str_ += '\n' + '-' * len(str_) + '\n'
        str_ += 'Unit System : ' + self.unit_system.name + '\n'
        str_ += 'Symmetric : {}'.format(self.symmetric) + '\n'
        str_ += str(self.data)
        return str_

    @property
    def data(self):
        """
        Dataframe of layup

        Notes
        -----
        - Returns full stack, i.e. if symmetric is True, returns
          mirrored stack instead of just input parameter data
        - Doesn't include layup name, unit system, layup thickness, or
          symmetric flag

        Returns
        -------
        data : DataFrame
            Table of ply names, materials, thicknesses, and orientations
        """
        columns = ('Ply Name', 'Material', 'Thickness', 'Orientation')
        data = {'Ply Name': self.ply_names, 'Material': self.ply_materials,
                'Thickness': self.thicknesses,
                'Orientation': self.orientations}
        if self.symmetric:
            for key, value in data.items():
                data[key] = value + list(reversed(value))
        data = DataFrame(data, columns=columns)
        return data

    def define_in_abaqus(self, model, part, region, axis=2,
                         angles=(0.0, 0.0, 0.0), unit_system=None):
        """
        Define Composite Layup in Abaqus.

        Parameters
        ----------
        model : Model
            Current model object
        part : str
            String name of part for composite layup creation
        region : str
            String name of part set for composite layup creation
        axis : int, optional
            Normal/stacking axis for composite layup creation. Default
            value is axis 2.
        angles : tuple[Union[float, Quantity]], optional
            Csys rotation angles (about X, Y, and Z) from global part
            X-Y plane. Default value is (0.0, 0.0, 0.0).
        unit_system : UnitSystem
            If provided, converts to Abaqus model unit system prior to
            definition
        """
        if not unit_system:
            unit_system = self.unit_system
        axis_dict = {1: AXIS_1, 2: AXIS_2, 3: AXIS_3}
        stack_dict = {1: STACK_1, 2: STACK_2, 3: STACK_3}
        material_names = [_.name for _ in self.ply_materials]
        material = None
        for material in self.ply_materials:
            if material not in model.ply_materials:
                material.define_in_abaqus(model)
        part = model.parts[part]
        region = part.sets[region]
        angles = [convert(unit_system, _angle, 'angle') for _angle in angles]
        angles = [_angle.to('degree').m for _angle in angles]
        angles = tuple(angles)
        _csys = part.DatumCsysByThreePoints(
            CARTESIAN, (0.0, 0.0, 0.0), rotate_vector((1.0, 0.0, 0.0), angles),
            rotate_vector((0.0, 1.0, 0.0), angles), name='csys')
        csys = part.datums[_csys.id]
        # elementType could also be CONTINUUM_SHELL or SOLID
        composite = part.CompositeLayup(self.name, elementType=SHELL,
                                        symmetric=self.symmetric)
        composite.Section(poissonDefinition=VALUE, poisson=0.5,
                          thicknessModulus=material.E2.magnitude)
        composite.ReferenceOrientation(localCsys=csys, axis=axis_dict[axis],
                                       stackDirection=stack_dict[axis])
        for name, thickness, orientation, material in zip(
                self.ply_names, self.thicknesses, self.orientations,
                material_names):
            _t = thickness.magnitude
            _o = orientation.to('degree').magnitude
            composite.CompositePly(
                thickness=_t, region=region, material=material, plyName=name,
                orientationType=SPECIFY_ORIENT,
                thicknessType=SPECIFY_THICKNESS, orientationValue=_o)

    @classmethod
    def from_dict(cls, saved):
        kwargs = dict()
        for key in saved:
            if key == 'unit_system':
                kwargs[key] = UnitSystem.from_dict(saved[key])
            elif key == 'ply_materials':
                kwargs['ply_materials'] = [Lamina.from_dict(_)
                                           for _ in saved[key]]
            else:
                kwargs[key] = saved[key]
        try:
            kwargs.pop('cls')
        except KeyError:
            pass
        return cls(**kwargs)

    @classmethod
    def read_json(cls, path):
        if not isfile(path):
            try:
                return cls.from_dict(json.loads(path))
            except JSONDecodeError:
                raise FileNotFoundError('Invalid path or JSON string')
        with open(path, 'r') as f:
            return cls.from_dict(json.load(f))

    def to_dict(self):
        kwargs = {
            'name': self.name,
            'ply_materials': [_.to_dict() for _ in self.ply_materials],
            'orientations': [_.m for _ in self.orientations],
            'unit_system': self.unit_system.to_dict(),
            'thicknesses': [_.m for _ in self.thicknesses],
            'symmetric': self.symmetric
        }
        if self.ply_names:
            kwargs['ply_names'] = self.ply_names
        return kwargs

    def to_json(self, path=None):
        kwargs = {
            'name': self.name,
            'ply_materials': [_.to_dict() for _ in self.ply_materials],
            'orientations': [_.m for _ in self.orientations],
            'unit_system': self.unit_system.to_dict(),
            'thicknesses': [_.m for _ in self.thicknesses],
            'symmetric': self.symmetric
        }
        if self.ply_names:
            kwargs['ply_names'] = self.ply_names
        kwargs['cls'] = self.__class__.__name__
        if not path:
            return json.dumps(kwargs)
        with open(path, 'w') as f:
            json.dump(kwargs, f)


class Material(object):
    type_ = None

    def __init__(self, name, unit_system, rho, tref=None):
        """
        Material class for model generation.

        Parameters
        ----------
        name : str
            Name of material
        unit_system : UnitSystem
            Unit system for storage of created material
        rho : Union[float, Quantity]
            Density of material
        tref : Union[float, Quantity], optional
            Reference temperature. default value is room temp

        Methods
        -------
        define_in_abaqus
        create_mat_abaqus
        create_density_abaqus
        create_elastic_abaqus

        Notes
        -----
        Currently built from Abaqus notation but will attempt to generalize
        later. Temperature dependence could be built in later by making
        each input lists.
        """
        self.name = name
        self.unit_system = unit_system
        self.rho = convert(unit_system, rho, 'density')
        if tref is None:
            tref = ROOM_TEMP
        tref = convert(unit_system, tref, 'temperature')
        self.tref = tref
        self._mat = None

    def __eq__(self, other):
        try:
            assert isinstance(other, self.__class__)
        except AssertionError:
            return False
        else:
            try:
                assert self.__dict__ == other.__dict__
            except AssertionError:
                return False
            else:
                return True

    def __hash__(self):
        keys = sorted(self.__dict__.keys(), key=str.lower)
        values = list()
        for key in keys:
            value = self.__dict__[key]
            if not value:
                values.append(value)
            else:
                try:
                    values.append(value.magnitude)
                except AttributeError:
                    pass
        return hash(tuple(values))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        """
        CamelCase representation of material name

        Returns
        -------
        name : str
        """
        return self.name.title().replace(' ', str())

    def create_damage_evolution_abaqus(self):
        raise NotImplementedError('Subclass specific method')

    def create_density_abaqus(self):
        rho = self.rho.magnitude
        if rho > 0:
            self._mat.Density(((rho,),))

    def create_elastic_abaqus(self):
        if not any([_ is None for _ in self.elastic]):
            elastic = tuple(_.magnitude for _ in self.elastic)
            self._mat.Elastic((elastic,), self.type_)

    def create_mat_abaqus(self, model):
        """
        Instantiate a material in an Abaqus model

        Parameters
        ----------
        model : Abaqus model object
        """
        self._mat = model.Material(self.name)

    def create_stress_limit_abaqus(self):
        raise NotImplementedError('Subclass specific method')

    def define_2d_nastran(self, model=None, id_=None, add=False):
        raise AttributeError('Only used by some subclasses')

    def define_3d_nastran(self, model=None, id_=None, add=False):
        raise AttributeError('Only used by some subclasses')

    def define_in_abaqus(self, model, damage=True):
        """
        Define material in Abaqus

        Parameters
        ----------
        model : object
            Abaqus model object
        damage : boolean, optional
            Flag to add damage initiation and evolution to material. Default
            value is True.
        """
        self.create_mat_abaqus(model)
        self.create_density_abaqus()
        self.create_elastic_abaqus()
        if damage:
            self.create_stress_limit_abaqus()
            self.create_damage_evolution_abaqus()

    def define_in_nastran(self, model=None, id_=None, add=False):
        raise NotImplementedError

    def define_in_patran(self, ses, mat_name=None):
        raise NotImplementedError

    @property
    def elastic(self):
        raise ValueError('No elastic properties defined')

    @classmethod
    def from_dict(cls, saved):
        kwargs = dict()
        for key in saved:
            if key == 'unit_system':
                kwargs[key] = UnitSystem.from_dict(saved[key])
            elif '_' in key[0]:
                kwargs[key[1:]] = saved[key]
            else:
                kwargs[key] = saved[key]
        try:
            kwargs.pop('cls')
        except KeyError:
            pass
        return cls(**kwargs)

    @staticmethod
    def read_json(path):
        if not isfile(path):
            try:
                json_dict = json.loads(path)
            except JSONDecodeError:
                raise FileNotFoundError('Invalid path or JSON string')
        else:
            with open(path, 'r') as f:
                json_dict = json.load(f)
        if mat_classes[json_dict['cls']] == Composite:
            return Composite.read_json(path)
        kwargs = dict()
        for key in json_dict:
            if key == 'unit_system':
                kwargs[key] = UnitSystem.from_dict(json_dict[key])
            elif '_' in key[0]:
                kwargs[key[1:]] = json_dict[key]
            else:
                kwargs[key] = json_dict[key]
        cls = mat_classes[kwargs.pop('cls')]
        return cls(**kwargs)

    def to_dict(self):
        kwargs = dict()
        for key in self.__dict__:
            if key == 'unit_system':
                kwargs[key] = self.__dict__[key].to_dict()
            elif self.__dict__[key] is None:
                continue
            else:
                value = self.__dict__[key]
                try:
                    value = value.magnitude
                except AttributeError:
                    pass
                kwargs[key] = value
        return kwargs

    def to_json(self, path=None):
        kwargs = self.to_dict()
        kwargs['cls'] = self.__class__.__name__
        if not path:
            return json.dumps(kwargs)
        with open(path, 'w') as f:
            json.dump(kwargs, f)

    def stress_limit(self):
        raise ValueError('No stress limit defined')


class EngineeringConstants(Material):
    def __init__(self, name, unit_system, rho, E1, E2, E3, nu12, nu13, nu23,
                 G12, G13, G23, tref=None, Xt=None, Xc=None, Yt=None, Yc=None,
                 S=None):
        """
        Engineering Constants material class

        Parameters
        ----------
        name : str
            Name of material
        unit_system : UnitSystem
            Values will be converted to quantities in this unit system
            for internal consistency
        rho : Union[float, Quantity]
            Density of material
        E1, E2, E3 : Union[float, Quantity]
            Young's modulus
        nu12, nu13, nu23 : float
            Poisson ratio
        G12, G13, G23 : Union[float, Quantity]
            Shear modulus
        tref : Union[float, Quantity], optional
            Reference temperature. Default value is room temperature.
        Xt, Xc : Union[float, Quantity], optional
            Stress limits in longitudinal tensile/compressive directions
        Yt, Yc : Union[float, Quantity], optional
            Stress limits in transverse tensile/compressive directions
        S : Union[float, Quantity], optional
            Stress limit in shear direction
        """
        super(EngineeringConstants, self).__init__(
            name, unit_system, rho, tref)
        self.E1 = convert(unit_system, E1, 'pressure')
        self.E2 = convert(unit_system, E2, 'pressure')
        self.E3 = convert(unit_system, E3, 'pressure')
        self.nu12 = float(nu12)
        self.nu13 = float(nu13)
        self.nu23 = float(nu23)
        self.G12 = convert(unit_system, G12, 'pressure')
        self.G13 = convert(unit_system, G13, 'pressure')
        self.G23 = convert(unit_system, G23, 'pressure')
        self.Xt = convert(unit_system, Xt, 'pressure')
        self.Xc = convert(unit_system, Xc, 'pressure')
        self.Yt = convert(unit_system, Yt, 'pressure')
        self.Yc = convert(unit_system, Yc, 'pressure')
        self.S = convert(unit_system, S, 'pressure')

    def __repr__(self):
        return ('EngineeringConstants(name={x.name!r}, rho={x.rho!s}, '
                'E1={x.E1!s}, E2={x.E2!s}, E3={x.E3!s}, nu12={x.nu12!s}, '
                'nu13={x.nu13!s}, nu23={x.nu23!s}, G12={x.G12!s}, '
                'G13={x.G13!s}, G23={x.G23!s}, tref={x.tref!s}, Xt={x.Xt!s}, '
                'Xc={x.Xc!s}, Yt={x.Yt!s}, Yc={x.Yc!s}, '
                'S={x.S!s})'.format(x=self))

    def create_damage_evolution_abaqus(self):
        """
        Create damage evolution in Abaqus

        Notes
        -----
        Only implemented in Lamina and Traction
        """
        pass

    def create_stress_limit_abaqus(self):
        """Create stress limit/damage initiation in Abaqus"""
        if not any(_ is None for _ in self.stress_limit):
            stress_limit = tuple(_.magnitude for _ in self.stress_limit)
            self._mat.elastic.FailStress((stress_limit,))

    def define_2d_nastran(self, model=None, id_=None, add=False):
        """
        Define material entry (MAT8) for Nastran model for 2D elements

        Parameters
        ----------
        model : obj, optional
            NatranInputFile object. If provided, will get material ID based on
            max ID in model and will add material to bulk entries.
        id_ : int, optional
            Material ID for Nastran file. Needed if model is not provided.
            Default value is 1.
        add : bool, optional
            Flag to add new entry to model bulk entries. Default value is
            False.

        Returns
        -------
        material : obj
            nastran_utils.MAT1 object
        """
        E1, E2 = self.E1.magnitude, self.E2.magnitude
        nu12, G12 = self.nu12, self.G12.magnitude
        rho, G13 = self.rho.magnitude, self.G13.magnitude
        G23, tref = self.G23.magnitude, self.tref.magnitude
        if id_ is None:
            if model is not None:
                id_ = model.get_max_id('Material') + 1
            else:
                id_ = 1
        properties = {'name': self.name, 'mid': id_, 'E1': E1, 'E2': E2,
                      'nu12': nu12, 'G12': G12, 'rho': rho, 'G1z': G13,
                      'G2z': G23, 'tref': tref}
        for name, value in zip(['Xt', 'Xc', 'Yt', 'Yc', 'S'],
                               [self.Xt, self.Xc, self.Yt, self.Yc, self.S]):
            if value is not None:
                properties[name] = value.magnitude
        if nastran_utils:
            material = nastran_utils.MAT8(**properties)
            if model is not None:
                if add:
                    model.add(material)
            return material
        else:
            raise ImportError('Nastran utils does not seem to have imported.')

    def define_3d_nastran(self, model=None, id_=None, add=False):
        """
        Define material entry (MAT9) for Nastran model for 3D elements

        Parameters
        ----------
        model : obj, optional
            NatranInputFile object. If provided, will get material ID based on
            max ID in model and will add material to bulk entries.
        id_ : int, optional
            Material ID for Nastran file. Needed if model is not provided.
            Default value is 1.
        add : bool, optional
            Flag to add new entry to model bulk entries. Default value is
            False.

        Returns
        -------
        material : obj
            nastran_utils.MAT1 object
        """
        if id_ is None:
            if model is not None:
                id_ = model.get_max_id('Material') + 1
            else:
                id_ = 1
        properties = {'name': self.name, 'mid': id_, 'rho': self.rho}
        E1, E2, E3 = self.E1.magnitude, self.E2.magnitude, self.E3.magnitude
        nu12, nu13 = self.nu12, self.nu13
        nu23, nu21 = self.nu23, self.nu21
        nu31, nu32 = self.nu31, self.nu32
        G44, G66 = self.G12.magnitude, self.G13.magnitude
        G55, tref = self.G23.magnitude, self.tref.magnitude
        delta = (1 - nu12 * nu21 - nu23 * nu32 - nu31 * nu13 -
                 2 * nu21 * nu32 * nu13) / (E1 * E2 * E3)
        G11 = (1 - nu23 * nu32) / (E2 * E3 * delta)
        G12 = (nu21 + nu31 * nu23) / (E2 * E3 * delta)
        G13 = (nu31 + nu21 * nu32) / (E2 * E3 * delta)
        G22 = (1 - nu13 * nu31) / (E1 * E3 * delta)
        G23 = (nu32 + nu23 * nu31) / (E1 * E3 * delta)
        G33 = (1 - nu12 * nu21) / (E1 * E2 * delta)
        G14, G15, G16, G24, G25, G26 = (0.0 for _ in range(6))
        G34, G35, G36, G45, G46, G56 = (0.0 for _ in range(6))
        for _name, _value in zip(['tref', 'G11', 'G12', 'G13', 'G14', 'G15',
                                  'G16', 'G22', 'G23', 'G24', 'G25', 'G26',
                                  'G33', 'G34', 'G35', 'G36', 'G44', 'G45',
                                  'G46', 'G55', 'G56', 'G66'],
                                 [tref, G11, G12, G13, G14, G15, G16, G22, G23,
                                  G24, G25, G26, G33, G34, G35, G36, G44, G45,
                                  G46, G55, G56, G66]):
            properties[_name] = _value
        if nastran_utils:
            material = nastran_utils.MAT9(**properties)
            if model is not None:
                if add:
                    model.add(material)
            return material
        else:
            raise ImportError('Nastran utils does not seem to have imported.')

    def define_in_nastran(self, model=None, id_=None, add=False):
        raise AttributeError('Not valid for this material type, use 2d or 3d')

    def define_in_patran(self, ses, mat_name=None):
        raise NotImplementedError

    @property
    def elastic(self):
        """
        Elastic properties table

        Returns
        -------
        tuple
        """
        return (self.E1, self.E2, self.E3, self.nu12, self.nu13, self.nu23,
                self.G12, self.G13, self.G23)

    @elastic.setter
    def elastic(self, damage):
        if damage == 1:
            tol = Q_(numerical_tolerance, self.unit_system.pressure)
        else:
            tol = Q_(0, self.unit_system.pressure)
        self.E1 = (1 - damage) * self.E1 + tol
        self.E2 = (1 - damage) * self.E2 + tol
        self.E3 = (1 - damage) * self.E3 + tol
        self.G12 = (1 - damage) * self.G12 + tol
        self.G13 = (1 - damage) * self.G13 + tol
        self.G23 = (1 - damage) * self.G23 + tol

    @property
    def nu21(self):
        return self.E2.magnitude * self.nu12 / self.E1.magnitude

    @property
    def nu31(self):
        return self.E3.magnitude * self.nu13 / self.E1.magnitude

    @property
    def nu32(self):
        return self.E3.magnitude * self.nu23 / self.E2.magnitude

    @property
    def stress_limit(self):
        """
        Stress limit table

        Returns
        -------
        tuple
        """
        return self.Xt, self.Xc, self.Yt, self.Yc, self.S


class Fluid(Material):
    def __init__(self, name, unit_system, rho, pref=None, tref=None,
                 bulk_modulus=None, c=None, ge=None, alpha=None):
        """
        Fluid material property definition

        Parameters
        ----------
        name : str
            Name of material
        unit_system : UnitSystem
            Values will be converted to quantities in this unit system
            for internal consistency
        rho : Union[float, Quantity]
            Density of material at given pressure and temperature
        pref : Union[float, Quantity], optional
            Reference pressure. Used for cryogenic propellants. Not used
            by Nastran. Default value is 1 atmosphere.
        tref : Union[float, Quantity], optional
            Reference temperature. Default value is room temperature.
        bulk_modulus : Union[float, Quantity], optional
            Bulk modulus, equivalent to c ** 2 * rho
        c : Union[float, Quantity], optional
            Speed of sound in fluid
        ge : float, optional
            Fluid element damping coefficient
        alpha : float, optional
            Normalized admittance coefficient for porous material, also
            known as alpha. If a value of alpha is entered in Nastran,
            bulk_modulus, rho, and ge may have negative values.
        """
        super(Fluid, self).__init__(name, unit_system, rho, tref)
        if pref is None:
            pref = Q_(1.0, 'atm')
        self.pref = convert(unit_system, pref, 'pressure')
        self.bulk_modulus = convert(unit_system, bulk_modulus, 'pressure')
        self.c = convert(unit_system, c, 'speed')
        self.ge = ge
        self.alpha = alpha

    def create_damage_evolution_abaqus(self):
        raise NotImplementedError

    def create_stress_limit_abaqus(self):
        raise NotImplementedError

    def define_in_nastran(self, model=None, id_=None, add=False):
        if id_ is None:
            if model is not None:
                id_ = model.get_max_id('Material') + 1
            else:
                id_ = 1
        bulk = self.bulk_modulus.magnitude
        rho = self.rho.magnitude
        c = self.c.magnitude
        ge = self.ge
        alpha = self.alpha
        if nastran_utils:
            nastran_utils.MAT10(id_, bulk, rho, c, ge, alpha)
        else:
            raise ImportError('Nastran utils does not seem to have imported.')

    def define_in_patran(self, ses, mat_name=None):
        raise NotImplementedError


class Isotropic(Material):
    def __init__(self, name, unit_system, rho, E, nu=None, G=None, tref=None,
                 Xt=None, Xc=None, Xs=None):
        """
        Isotropic material class

        Parameters
        ----------
        name : str
            Name of material
        unit_system : UnitSystem
            Values will be converted to quantities in this unit system
            for internal consistency
        rho : Union[float, Quantity]
            Density of material
        E : Union[float, Quantity]
            Young's modulus
        nu : float, optional
            Poisson ratio. If not assigned, will be calculated using linear
            elastic relationship from E and G.
        G : Union[float, Quantity], optional
            Shear modulus, also sometimes called mu, not used as an input for
            Abaqus. If not assigned will be calculated using linear elastic
            relationship from E and nu.
        tref : Union[float, Quantity], optional
            Reference temperature. Default value is room temperature.
        Xt, Xc, Xs : Union[float, Quantity], optional
            Stress limits in tension, compression, and shear

        Notes
        -----
        Either nu or G must be defined. If only one is defined, linear elastic
        relationship will be used to define the other.

        Raises
        ------
        ValueError
            If E/nu/G ratio under-defined or not linearly elastic
        """
        super(Isotropic, self).__init__(name, unit_system, rho, tref)
        E = convert(unit_system, E, 'pressure')
        G = convert(unit_system, G, 'pressure')
        if nu is not None:
            nu = float(nu)
        self.E = E
        if nu is not None and G is not None:
            if 1 - E.m / float(2 * G.m * (1 + nu)) >= 0.01:
                raise ValueError(
                    'Ratio of E, G, and nu not linearly elastic, recommend '
                    'changing values or going with another material type.')
        elif nu is None and G is None:
            raise ValueError('Either nu or G must be defined')
        self._nu = nu
        self._G = G
        self.Xt = convert(unit_system, Xt, 'pressure')
        self.Xc = convert(unit_system, Xc, 'pressure')
        self.Xs = convert(unit_system, Xs, 'pressure')

    def __repr__(self):
        return ('Isotropic(name={x.name!r}, rho={x.rho!s}, E={x.E!s}, '
                'nu={x.nu!s}, G={x.G!s}, tref={x.tref!s}, Xt={x.Xt!s}, '
                'Xc={x.Xc!s}, Xs={x.Xs!s})'.format(x=self))

    def create_damage_evolution_abaqus(self):
        """
        Create damage evolution in Abaqus

        Notes
        -----
        Only implemented in Lamina and Traction
        """
        pass

    def create_stress_limit_abaqus(self):
        """
        Create stress limit/damage initiation in Abaqus
        """
        if not any([_ is None for _ in self.stress_limit]):
            stress_limit = tuple(_.magnitude for _ in self.stress_limit)
            self._mat.elastic.FailStress((stress_limit,))

    def define_in_nastran(self, model=None, id_=None, add=False):
        """
        Define material entry (MAT1) for Nastran model

        Parameters
        ----------
        model : obj, optional
            NatranInputFile object. If provided, will get material ID based on
            max ID in model and will add material to bulk entries.
        id_ : int, optional
            Material ID for Nastran file. Needed if model is not provided.
            Default value is 1.
        add : bool, optional
            Flag to add new entry to model bulk entries. Default value is
            False.

        Returns
        -------
        material : obj
            nastran_utils.MAT1 object
        """
        if id_ is None:
            if model is not None:
                id_ = model.get_max_id('Material') + 1
            else:
                id_ = 1
        E, G, nu = self.E.magnitude, self.G.magnitude, self.nu
        rho, tref = self.rho.magnitude, self.tref.magnitude
        properties = {'name': self.name, 'mid': id_, 'E': E, 'G': G, 'nu': nu,
                      'rho': rho, 'tref': tref}
        for name, value in zip(['St', 'Sc', 'Ss'],
                               [self.Xt, self.Xc, self.Xs]):
            if value is not None:
                properties[name] = value.magnitude
        if nastran_utils:
            material = nastran_utils.MAT1(**properties)
            if model is not None and add:
                model.add(material)
            return material
        else:
            raise ImportError('Nastran utils does not seem to have imported.')

    def define_in_patran(self, ses, mat_name=None):
        """
        Define material in Patran

        Parameters
        ----------
        ses : File
            Open Patran session file object
        mat_name : str, optional
            Material name to use in Patran. Default will get object's name.

        Notes
        -----
        - Only implemented for Isotropic
        """
        E, G, nu = self.E.magnitude, self.G.magnitude, self.nu
        rho = self.rho.magnitude
        if mat_name is None:
            mat_name = self.name
        if self.tref is None:
            tref = str()
        else:
            tref = self.tref.magnitude
        ses.write(self.patran_material_string.format(
            name=mat_name, E=E, nu=nu, G=G, rho=rho, alpha=str(), GE=str(),
            tref=tref))

    @property
    def elastic(self):
        """
        Elastic properties table

        Returns
        -------
        tuple
        """
        return self.E, self.nu

    @elastic.setter
    def elastic(self, damage):
        if damage == 1:
            tol = Q_(numerical_tolerance, self.unit_system.pressure)
        else:
            tol = Q_(0, self.unit_system.pressure)
        self.E = (1 - damage) * self.E + tol

    @property
    def G(self):
        """
        Shear modulus G/mu, as input or calculated using linear elastic
        relationship.

        Returns
        -------
        G : Q_
            Shear modulus pint quantity in pressure units
        """
        if self._G is None:
            self._G = self.E / 2 / (1 + self.nu)
        return self._G

    @property
    def nu(self):
        """
        Poisson's ratio as input or calculated using linear elastic
        relationship

        Returns
        -------
        nu : Q_
            Poisson's ratio as unitless pint quantity
        """
        if self._nu is None:
            E, G = self.E.magnitude, self.G.magnitude
            self._nu = (E - 2 * G) / (2 * G)
        return self._nu

    @property
    def patran_material_string(self):
        """
        PCL material creation command string

        String Arguments
        ----------------
        name, E, nu, G, rho, alpha, GE, tref

        Returns
        -------
        material_string : str
            Formatted Patran command language string
        """
        material_string = ('material.create( "Analysis code ID", 1, "Analysis '
                           'type ID", 1, "{name}", 0, "", "Isotropic", 1, '
                           '"Directionality", 1, "Linearity", 1, "Homogeneous"'
                           ', 0, "Linear Elastic", 1, "Model Options & IDs", '
                           '["", "", "", "", ""], [0, 0, 0, 0, 0], "Active '
                           'Flag", 1, "Create", 10, "External Flag",  FALSE, '
                           '"Property IDs", ["Elastic Modulus", "Poisson '
                           'Ratio", "Shear Modulus", "Density", "Thermal '
                           'Expan. Coeff", "Structural Damping Coeff", '
                           '"Reference Temperature"], [2, 5, 8, 16, 24, 30, 1,'
                           ' 0], "Property Values", ["{E}", "{nu}", "{G}", '
                           '"{rho}", "{alpha}", "{GE}", "{tref}", ""] )\n')
        return material_string

    @property
    def stress_limit(self):
        """
        Stress limit table

        Returns
        -------
        tuple
        """
        return self.Xt, self.Xc, self.Xt, self.Xc, self.Xs

    @property
    def bulk_modulus(self):
        """
        Bulk modulus of the material

        Returns
        -------
        bulk_modulus : Quantity
        """
        return self.E / 3 / (1 - 2 * self.nu)

    @property
    def wave_speed(self):
        """
        Speed of wave through material

        Notes
        -----
        Assumes pressure-density unit compatibility

        Returns
        -------
        wave_speed : float
        """
        return Q_(sqrt(self.bulk_modulus.magnitude / self.rho.magnitude),
                  self.unit_system.speed)

    @classmethod
    def generic_aluminum(cls, name='Aluminum', unit_system=None):
        """
        Based on Aluminum 6061-T6

        Parameters
        ----------
        name : str, optional
        unit_system : UnitSystem, optional

        Notes
        -----
        - Default tref is ~70 degrees Fahrenheit "room temperature"
        - Default failure stresses are yield
        - Tensile/shear stress relation from
          http://www.roymech.co.uk/Useful_Tables/Matter/shear_tensile.htm
        - Properties from
          http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=ma6061t6

        Returns
        -------
        material : Isotropic
        """
        rho = Q_(2.7, 'g/cc')
        E = Q_(68.9, 'GPa')
        nu = 0.33
        G = Q_(26.0, 'GPa')
        tref = ROOM_TEMP
        Xt = Q_(276.0, 'MPa')
        Xc = Xt
        Xs = 0.55 * Xt
        if not unit_system:
            unit_system = UnitSystem.mks()
        return cls(name, unit_system, rho, E, nu, G, tref, Xt, Xc, Xs)

    @classmethod
    def generic_steel(cls, name='Steel', unit_system=None):
        """
        Based on AISI 4140 Steel

        Parameters
        ----------
        name : str, optional
        unit_system : UnitSystem, optional

        Notes
        -----
        - Uses upper value when given a range.
        - Default tref is ~70 degrees Fahrenheit "room temperature"
        - Default failure stresses are yield
        - Tensile/shear stress relation from
          http://www.roymech.co.uk/Useful_Tables/Matter/shear_tensile.htm
        - Properties from http://www.azom.com/article.aspx?ArticleID=6769

        Returns
        -------
        material : Isotropic
        """
        rho = Q_(7.85, 'g/cc')
        E = Q_(210.0, 'GPa')
        nu = 0.3
        G = Q_(80.0, 'GPa')
        tref = ROOM_TEMP
        Xt = Q_(415.0, 'MPa')
        Xc = Xt
        Xs = 0.58 * Xt
        if not unit_system:
            unit_system = UnitSystem.mks()
        return cls(name, unit_system, rho, E, nu, G, tref, Xt, Xc, Xs)

    @classmethod
    def unobtanium(cls, name='Unobtanium', unit_system=None):
        """
        Generic very-high stiffness, negligible density material for rigid
        structures

        Parameters
        ----------
        name : str, optional
        unit_system : UnitSystem, optional

        Returns
        -------
        material : Isotropic
        """
        rho = 1e-8
        E = Q_(1e9, 'psi')
        nu = 0.3
        G = None
        tref = ROOM_TEMP
        Xt = 1.0
        Xc = 1.0
        Xs = 1.0
        if not unit_system:
            unit_system = UnitSystem.mks()
        return cls(name, unit_system, rho, E, nu, G, tref, Xt, Xc, Xs)


class Lamina(Material):
    """
    Lamina material class for shell orthotropic materials

    Parameters
    ----------
    name : str
        Name of material
    unit_system : UnitSystem
            Values will be converted to quantities in this unit system
            for internal consistency
    rho : Union[float, Quantity]
        Density of material
    E1, E2 : Union[float, Quantity]
        Young's modulus
    nu12 : float
        Poisson ratio
    G12, G13, G23 : Union[float, Quantity]
        Shear modulus
    tref : Union[float, Quantity], optional
        Reference temperature
    Xt, Xc : Union[float, Quantity], optional
        Lamina stress limits in longitudinal tensile/compressive directions
    Yt, Yc : Union[float, Quantity], optional
        Lamina stress limits in transverse tensile/compressive directions
    SL, St : Union[float, Quantity], optional
        Lamina stress limits in shear longitudinal/transverse directions
    Gft, Gfc : Union[float, Quantity], optional
        Fiber fracture energies in tensile and compressive directions
    Gmf, Gmc : Union[float, Quantity], optional
        Matrix fracture energies in tensile and compressive directions
    """
    def __init__(self, name, unit_system, rho, E1, E2, nu12, G12, G13=None,
                 G23=None, tref=None, Xt=None, Xc=None, Yt=None, Yc=None,
                 SL=None, St=None, Gft=None, Gfc=None, Gmf=None, Gmc=None):
        super(Lamina, self).__init__(name, unit_system, rho, tref)
        self.E1 = convert(unit_system, E1, 'pressure')
        self.E2 = convert(unit_system, E2, 'pressure')
        self.nu12 = float(nu12)
        self.G12 = convert(unit_system, G12, 'pressure')
        self.G13 = convert(unit_system, G13, 'pressure')
        self.G23 = convert(unit_system, G23, 'pressure')
        self.Xt = convert(unit_system, Xt, 'pressure')
        self.Xc = convert(unit_system, Xc, 'pressure')
        self.Yt = convert(unit_system, Yt, 'pressure')
        self.Yc = convert(unit_system, Yc, 'pressure')
        self.SL = convert(unit_system, SL, 'pressure')
        self.St = convert(unit_system, St, 'pressure')
        self.Gft = convert(unit_system, Gft, 'energy')
        self.Gfc = convert(unit_system, Gfc, 'energy')
        self.Gmf = convert(unit_system, Gmf, 'energy')
        self.Gmc = convert(unit_system, Gmc, 'energy')

    def __repr__(self):
        return ('Lamina(name={x.name!r}, rho={x.rho!s}, E1={x.E1!s}, '
                'E2={x.E2!s}, nu12={x.nu12!s}, G12={x.G12!s}, G13={x.G13!s}, '
                'G23={x.G23!s}, tref={x.tref!s}, Xt={x.Xt!s}, Xc={x.Xc!s}, '
                'Yt={x.Yt!s}, Yc={x.Yc!s}, SL={x.SL!s}, St={x.St!s}, '
                'Gft={x.Gft!s}, Gfc={x.Gfc!s}, Gmf={x.Gmf!s}, '
                'Gmc={x.Gmc!s})'.format(x=self))

    def create_damage_evolution_abaqus(self):
        """
        Create damage evolution in Abaqus

        Notes
        -----
        - Only implemented in Lamina and Traction
        - Hashin damage evolution
        """
        if not any([_ is None for _ in self.fracture_energy]):
            fracture_energy = tuple(_.magnitude for _ in self.fracture_energy)
            self._mat.hashinDamageInitiation.DamageEvolution(
                ENERGY, (fracture_energy,))

    def create_stress_limit_abaqus(self):
        """
        Create stress limit/damage initiation in Abaqus

        Notes
        -----
        Hashin damage criterion
        """
        if not any([_ is None for _ in self.stress_limit]):
            stress_limit = tuple(_.magnitude for _ in self.stress_limit)
            self._mat.HashinDamageInitiation((stress_limit,))

    def define_in_nastran(self, model=None, id_=None, add=False):
        """
        Define material entry (MAT8) for Nastran model

        Parameters
        ----------
        model : obj, optional
            NatranInputFile object. If provided, will get material ID based on
            max ID in model and will add material to bulk entries.
        id_ : int, optional
            Material ID for Nastran file. Needed if model is not provided.
            Default value is 1.
        add : bool, optional
            Flag to add new entry to model bulk entries. Default value is
            False.

        Returns
        -------
        material : obj
            nastran_utils.MAT1 object
        """
        if id_ is None:
            if model is not None:
                id_ = model.get_max_id('Material') + 1
            else:
                id_ = 1
        E1, E2 = self.E1.magnitude, self.E2.magnitude
        nu12, rho = self.nu12, self.rho.magnitude
        G12, G13 = self.G12.magnitude, self.G13.magnitude
        G23, tref = self.G23.magnitude, self.tref.magnitude
        properties = {'name': self.name, 'mid': id_, 'E1': E1, 'E2': E2,
                      'nu12': nu12, 'G12': G12, 'rho': rho, 'G1z': G13,
                      'G2z': G23, 'tref': tref}
        for name, value in zip(['Xt', 'Xc', 'Yt', 'Yc'],
                               [self.Xt, self.Xc, self.Yt, self.Yc]):
            if value is not None:
                properties[name] = value
        S = Q_(0, self.unit_system.pressure)
        for s in [self.SL, self.St]:
            if s and s > S:
                S = s
        if S:
            properties['S'] = S.magnitude
        try:
            material = nastran_utils.MAT8(**properties)
        except AttributeError:
            raise ImportError('Nastran utils does not seem to have imported.')
        else:
            if model is not None:
                if add:
                    model.add(material)
            return material

    def define_in_patran(self, ses, mat_name=None):
        raise NotImplementedError

    @property
    def elastic(self):
        """
        Elastic properties table
        Returns
        -------
        tuple
        """
        return self.E1, self.E2, self.nu12, self.G12, self.G13, self.G23

    @elastic.setter
    def elastic(self, damage):
        if damage == 1:
            tol = Q_(numerical_tolerance, self.unit_system.pressure)
        else:
            tol = Q_(0, self.unit_system.pressure)
        self.E1 = (1 - damage) * self.E1 + tol
        self.E2 = (1 - damage) * self.E2 + tol
        self.G12 = (1 - damage) * self.G12 + tol
        self.G13 = (1 - damage) * self.G13 + tol
        self.G23 = (1 - damage) * self.G23 + tol

    @property
    def fracture_energy(self):
        """
        Fracture energy properties table

        Returns
        -------
        tuple
        """
        return self.Gft, self.Gfc, self.Gmf, self.Gmc

    @property
    def nu21(self):
        return self.nu12 * (self.E2 / self.E1).magnitude

    @property
    def stress_limit(self):
        """
        Stress limit properties table

        Returns
        -------
        tuple
        """
        return self.Xt, self.Xc, self.Yt, self.Yc, self.SL, self.St


class Traction(Material):
    def __init__(self, name, unit_system, rho, Enn, Ess, Ett, tref=None,
                 tn=None, ts=None, tt=None, Gn=None, Gs=None, Gt=None, bk=1.5):
        """
        Traction material class

        Parameters
        ----------
        name : str
            Name of material
        unit_system : UnitSystem
            Values will be converted to quantities in this unit system
            for internal consistency
        rho : Union[float, Quantity]
            Density of material
        Enn, Ess, Ett : Union[float, Quantity]
            Stiffnesses
        tref : Union[float, Quantity], optional
            Reference temperature
        tn, ts, tt : Union[float, Quantity], optional
            Quads damage initiation stress in normal and first and
            second shear directions
        Gn, Gs, Gt : Union[float, Quantity], optional
            Quads damage evolution energies in normal and first and
            second shear directions
        bk : float, optional
            Benzeggagh-Kenane fracture criterion

        Notes
        -----
        - Specified for cohesive elements currently
        - Quads damage initiation is the only method implemented currently
        """
        super(Traction, self).__init__(name, unit_system, rho, tref)
        self.Enn = convert(unit_system, Enn, 'pressure')
        self.Ess = convert(unit_system, Ess, 'pressure')
        self.Ett = convert(unit_system, Ett, 'pressure')
        self.tn = convert(unit_system, tn, 'pressure')
        self.ts = convert(unit_system, ts, 'pressure')
        self.tt = convert(unit_system, tt, 'pressure')
        self.Gn = convert(unit_system, Gn, 'energy')
        self.Gs = convert(unit_system, Gs, 'energy')
        self.Gt = convert(unit_system, Gt, 'energy')
        self.bk = float(bk)

    def __repr__(self):
        return ('Traction(name={x.name!r}, rho={x.rho!s}, Enn={x.Enn!s}, '
                'Ess={x.Ess!s}, Ett={x.Ett!s}, tref={x.tref!s}, tn={x.tn!s}, '
                'ts={x.ts!s}, tt={x.tt!s}, Gn={x.Gn!s}, Gs={x.Gs!s}, '
                'Gt={x.Gt!s}, bk={x.bk!s})'.format(x=self))

    def create_damage_evolution_abaqus(self):
        """
        Create damage evolution in Abaqus

        Notes
        -----
        - Only implemented in Lamina and Traction
        - Quads damage evolution
        """
        if not any([_ is None for _ in self.fracture_energy]):
            fracture_energy = tuple(_.magnitude for _ in self.fracture_energy)
            self._mat.quadsDamageInitiation.DamageEvolution(
                ENERGY, (fracture_energy,), mixedModeBehavior=BK,
                power=self.bk)

    def define_in_nastran(self, model=None, id_=None, add=False):
        raise NotImplementedError

    def define_in_patran(self, ses, mat_name=None):
        raise NotImplementedError

    def create_stress_limit_abaqus(self):
        """
        Create stress limit/damage initiation in Abaqus

        Notes
        -----
        Limited for now to Quads damage initiation
        """
        if not any([_ is None for _ in self.stress_limit]):
            stress_limit = tuple(_.magnitude for _ in self.stress_limit)
            self._mat.QuadsDamageInitiation((stress_limit,))

    @property
    def elastic(self):
        """
        Elastic properties table

        Returns
        -------
        tuple
        """
        return self.Enn, self.Ess, self.Ett

    @elastic.setter
    def elastic(self, damage):
        if damage == 1:
            tol = Q_(numerical_tolerance, self.unit_system.pressure)
        else:
            tol = Q_(0, self.unit_system.pressure)
        self.Enn = (1 - damage) * self.Enn + tol
        self.Ess = (1 - damage) * self.Ess + tol
        self.Ett = (1 - damage) * self.Ett + tol

    @property
    def fracture_energy(self):
        """
        Fracture energy properties table

        Returns
        -------
        tuple
        """
        return self.Gn, self.Gs, self.Gt

    @property
    def stress_limit(self):
        """
        Stress limit table

        Returns
        -------
        tuple
        """
        return self.tn, self.ts, self.tt


mat_classes = {
    'Composite': Composite, 'Material': Material,
    'EngineeringConstants': EngineeringConstants, 'Fluid': Fluid,
    'Isotropic': Isotropic, 'Lamina': Lamina, 'Traction': Traction
}
