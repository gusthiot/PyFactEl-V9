class ErreurConsistance(Exception):
    """Erreur levée lorsqu'une inconsistance est détectée dans les entrées."""
    def __str__(self):
        return "Erreur de consistance"


class ErreurCoherence(Exception):
    """Erreur levée lorsqu'une incohérence est détectée dans le déroulement."""
    def __str__(self):
        return "Erreur de cohérence"
