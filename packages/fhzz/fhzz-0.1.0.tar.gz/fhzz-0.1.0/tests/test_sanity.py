"""
Some basic sanity checks.
"""

import pytest


# Small import test first...
def test_import():
    """Test that the package can be imported."""
    with pytest.raises(NameError):
        fhzz
    import fhzz
    fhzz


# ...then properly import package and run the rest of the sanity tests
import fhzz


def test_has_author():
    """Test that the package has an author."""
    fhzz.__author__


def test_has_email():
    """Test that an email address is associated with the package."""
    fhzz.__email__


def test_has_version():
    """Test that the package has a version."""
    fhzz.__version__
