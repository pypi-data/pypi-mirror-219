ctypedef (double*, ) ptr_tuple_1


cdef class VariableValues(BaseCValues):
    def __init__(VariableValues self):
        cdef ptr_tuple_1 ptr = (&self.value, )
        cdef tuple params = ("value", )
        self.setup(params, sizeof(ptr), <double**>&ptr)


cdef class VariableWorkspace(ElementWorkspace):
    def __init__(self, owner):
        super().__init__(owner, VariableValues())
        self.vv = self.values
