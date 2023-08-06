# -*- coding: utf-8 -*-
__author__ = "Monica Figuera and Philipp D. Rohde"

from SHACL2SPARQLpy.VariableGenerator import VariableType
from SHACL2SPARQLpy.constraints.Constraint import Constraint


class MinOnlyConstraint(Constraint):

    def __init__(self, varGenerator, id, path, min, isPos, datatype=None, value=None, shapeRef=None, targetDef=None):
        super().__init__(id, isPos, None, datatype, value, shapeRef, targetDef)
        self.varGenerator = varGenerator
        self.path = path
        self.min = min
        self.max = -1
        self.variables = self.computeVariables()

    def computeVariables(self):
        atomicConstraint = Constraint()
        return atomicConstraint.generateVariables(self.varGenerator, VariableType.VALIDATION, self.min)

    @property
    def getMin(self):
        return self.min

    @property
    def getPath(self):
        return self.path
