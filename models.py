"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.
        Hanlding data types are moved to `extract.py`

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = info.get('designation')
        self.name = info.get('name')
        self.diameter = info.get('diameter')
        self.hazardous = info.get('hazardous')
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name:
            return f"{self.designation} {self.name}"
        return f"{self.designation}"

    def serialize(self):
        """Return a dictionary containing relevant attributes of this NEO for CSV or JSON serialization

        Relevant attributes are designation, name, diameter_km, potentially_hazardous
        """

        return {
            'designation': self.designation,
            'name': self.name or '',
            'diameter_km': self.diameter,
            'potentially_hazardous': self.hazardous
        }

    def __str__(self):
        """Return `str(self)`."""
        return f"A NearEarthObject {self.fullname} has a diameter of {self.diameter:.2f} km " \
               f"and {'is' if self.hazardous else 'is not'} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.2f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.
        Hanlding data types are moved to `extract.py`

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = info.get('designation')
        self.time = cd_to_datetime(info.get('time')) if info.get(
            'time') else info.get('time')
        self.distance = info.get('distance', float('nan'))
        self.velocity = info.get('velocity', float('nan'))
        self.neo = info.get('neo')

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return self.time and datetime_to_str(self.time)

    def link_neos_and_approaches(self, neos_mapping):
        """Link NEO to approach and approaches to NEO.

        :param neos_mapping: dictionary of designation and corresponding NEO.
        :return: this close approach.
        """
        if self._designation in neos_mapping:
            # Get NEO from mappings using approach's designation
            neo = neos_mapping[self._designation]
            if self._designation == neo.designation:
                # If they belong together, link them
                neo.approaches.append(self)
            self.neo = neo
        return self

    def serialize(self):
        """Return a dictionary containing relevant attributes of this Close Approach for CSV or JSON serialization

        Relevant attributes are datetime_utc, distance_au, velocity_km_s
        """

        return {
            'datetime_utc': self.time_str,
            'distance_au': self.distance,
            'velocity_km_s': self.velocity
        }

    def __str__(self):
        """Return `str(self)`."""
        return f"On {self.time_str}, {self.neo.fullname} approaches earth at a distance of {self.distance:.2f} au " \
               f"and at a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
