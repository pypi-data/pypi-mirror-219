import string
import random
import numpy as np



__ALL__ = [
    "get_string",
    "NpArray",
    "normalize",
    "project_vector_on_vector",
    "project_vector_on_plane",
    "PDFMerger",
]


def get_string(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def PDFMerger(output_path, input_paths):
    """ Merges all pdfs at `input_paths` and creates a unique pdf at `output_path` """
    try:
        import PyPDF2
    except ImportError:
        from gatools.colors import bc
        print(f"{bc.FAIL}You need to install PyPDF2 to use <utils.PDFMerger> function: `pip install PyPDF2`{bc.ENDC}")
        raise
    
    from PyPDF2 import PdfFileWriter, PdfFileReader

    pdf_writer = PdfFileWriter()

    for path in input_paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

    with open(output_path, "wb") as fh:
        pdf_writer.write(fh)



# NUMPY
def normalize(vec):
    return np.array(vec) / np.linalg.norm(vec)


def project_vector_on_vector(v1, v2):
    """
    Project v1 on v2
    """
    v1, v2 = np.array(v1), np.array(v2)
    return np.dot(v1, v2) * v2 / np.linalg.norm(v2)


def project_vector_on_plane(v, n):
    """
    Project vector v on plane with normal vector n
    """
    v, n = np.array(v), np.array(n)
    return v - project_vector_on_vector(v, n)


# Inherit from numpy arrays
class NpArray(np.ndarray):
    """
    An array with extra attributes, being passed on to views and results of
    ufuncs.
    """

    def __new__(cls, array, *args, **kwargs):
        """
        Some magic stolen from numpy docs.

        https://docs.scipy.org/doc/numpy/user/basics.subclassing.html
        """
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(array).view(cls)
        # add the new attributes to the created instance
        for key, value in kwargs.items():
            setattr(obj, key, value)
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        """
        This function ensures that attributes are present in all ways instances
        are created, including views on the array.
        """
        if type(obj) is not np.ndarray and hasattr(obj, "__dict__"):
            for key, value in vars(obj).items():
                setattr(self, key, value)

    def __array_wrap__(self, obj, context=None):
        """Ensure that scalar type is returned instead of 0D array"""
        if obj.shape == ():
            return obj[()]  # if ufunc output is scalar, return it
        else:
            return np.ndarray.__array_wrap__(self, obj)
