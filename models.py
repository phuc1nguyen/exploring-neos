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
    def __init__(self, designation: str, name: str, diameter: str, hazardous: str, approaches = []):
        """Create a new `NearEarthObject`.

        :param designation: the primary designation for this NEO.
        :param name: the IAU name for this NEO.
        :param diameter: the diameter, in kilometers, of this NEO.
        :param hazardous: whether or not this NEO is potentially hazardous.
        :param approaches: a collection of this NEO's close approaches to Earth.
        """
        self.designation = designation
        self.name = name or None
        self.diameter = float(diameter) if diameter else float('nan')
        self.hazardous = True if hazardous == 'Y' else False

        # Create an empty initial collection of linked approaches.
        self.approaches = approaches

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name: return f"{self.designation} {self.name}"
        return f"{self.designation}"

    def __str__(self):
        """Return `str(self)`."""
        return f"NEO {self.fullname} has a diameter of {self.diameter} km and {'is' if self.hazardous else 'is not'} potentially hazardous."
        
    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


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
    def __init__(self, time: str, distance: str, velocity: str, neo):
        """Create a new `CloseApproach`.

        :param time: the date and time, in UTC, at which the NEO passes closest to Earth.
        :param distance: the nominal approach distance, in astronomical units, of the NEO to Earth at the closest point.
        :param velocity: the velocity, in kilometers per second, of the NEO relative to Earth at the closest point.
        :param neo: the NEO that is making a close approach to Earth.
        """
        self._designation = neo.designation if neo else ''
        self._name = neo.name if neo else ''
        self.time = cd_to_datetime(time)
        self.distance = round(float(distance), 2)
        self.velocity = round(float(velocity), 2)

        # Create an attribute for the referenced NEO, originally None.
        self.neo = neo or None

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
        return datetime_to_str(self.time)

    @property
    def fullname(self):
        return f"{self._designation} {self._name}"

    def __str__(self):
        """Return `str(self)`."""
        return f"On {self.time_str}, '{self.fullname}' approached Earth at a distance of " \
                f"{round(self.distance, 2)} au and a velocity of {round(self.velocity, 2)} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
