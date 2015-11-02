"""State unit tests."""

import pytest
from vivid.Classes.ValueSet import ValueSet
from vivid.Classes.State import State
from vivid.Classes.State import AttributeSystem
from vivid.Classes.State import AttributeStructure
from vivid.Classes.State import Attribute, Relation

def test___init__():
    """Test State constructor."""
    def test_TypeError(attribute_system, ascriptions={}):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            State(attribute_system, ascriptions)

    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)
    
    #test no attribute system
    test_TypeError(a)
    test_TypeError(object)
    test_TypeError(None)
    #test bad ascriptions
    test_TypeError(asys, [])
    test_TypeError(asys, None)
    test_TypeError(asys, object)

    s = State(asys)
    assert s._attribute_system == asys
    assert s._attribute_system is not asys
    s = State(asys, {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']})

    assert s[(('color', 's1'))] == ValueSet(['R'])
    assert s[(('color', 's2'))] == ValueSet(['G', 'B'])
    assert s[(('size', 's1'))] == ValueSet(['M'])
    assert s[(('size', 's2'))] == ValueSet(['L', 'S'])

def test___eq__():
    """Test == operator."""
    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    s = State(asys)
    s1 = State(asys, {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']})

    s2 = State(asys, {
        ('size', 's1'): ['M'],
        ('color', 's2'): ['B', 'G'],
        ('color', 's1'): ['R'],
        ('size', 's2'): ['L', 'S']})

    assert s1 == s2

    assert not s == s1
    s.set_ascription(('color', 's1'), ['R'])
    assert not s == s1
    s.set_ascription(('color', 's2'), ['B', 'G'])
    assert not s == s1
    s.set_ascription(('size', 's1'), ['M'])
    assert not s == s1
    s.set_ascription(('size', 's2'), ['L', 'S'])
    assert s == s1
    assert s == s1 == s2


def test___lt__():
    """Test < operator overloaded for proper extension."""
    pass

def test___le__():
    """Test <= operator overloaded for extension."""
    pass

def test___ne__():
    """Test != operator."""
    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    s = State(asys)
    s1 = State(asys, {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']})

    s2 = State(asys, {
        ('size', 's1'): ['M'],
        ('color', 's2'): ['B', 'G'],
        ('color', 's1'): ['R'],
        ('size', 's2'): ['L', 'S']})

    assert not s1 != s2

    assert s != s1
    s.set_ascription(('color', 's1'), ['R'])
    assert s != s1
    s.set_ascription(('color', 's2'), ['B', 'G'])
    assert s != s1
    s.set_ascription(('size', 's1'), ['M'])
    assert s != s1
    s.set_ascription(('size', 's2'), ['L', 'S'])
    assert not s != s1
    assert not s != s1 != s2

def test___deepcopy__():
    """Test deepcopy"""
    pass

def test_set_ascription():
    """Test set_ascription function."""
    def test_TypeError(state, ascription, valueset):
        """Test set_ascription for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            state.set_ascription(ascription, valueset)

    def test_ValueError(state, ascription, valueset):
        """Test set_ascription for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            state.set_ascription(ascription, valueset)

    def test_KeyError(state, ascription, valueset):
        """Test set_ascription for KeyErrors with given params."""
        with pytest.raises(KeyError) as excinfo:
            state.set_ascription(ascription, valueset)

    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])

    a = AttributeStructure(color, size)
    o = ['s1', 's2']

    asys = AttributeSystem(a, o)
    s = State(asys)

    #test bad ao_pair types/values
    test_TypeError(s, [], ['R'])
    test_ValueError(s, (), ['R'])
    test_ValueError(s, (1,2,3), ['R'])
    test_ValueError(s, (1, 2), ['R'])
    test_ValueError(s, (1, ''), ['R'])
    test_ValueError(s, ('', 1), ['R'])
    #test bad types for ValueSet
    test_TypeError(s, ('color', 's1'), None)
    test_TypeError(s, ('color', 's1'), ())
    test_TypeError(s, ('color', 's1'), 'a')
    test_TypeError(s, ('color', 's1'), object)
    #test empty ValueSet catching
    test_ValueError(s, ('color', 's1'), [])
    test_ValueError(s, ('color', 's1'), set([]))
    test_ValueError(s, ('color', 's1'), ValueSet([]))
    #test bad ao-pair keys
    test_KeyError(s, ('color', 'bad object'), ['R'])
    test_KeyError(s, ('bad label', 's2'), ['R'])
    #test nonsubset valuesets
    test_ValueError(s, ('color', 's2'), ['a'])
    test_ValueError(s, ('color', 's2'), [1])

    s.set_ascription(('color', 's2'), ['R'])
    assert s[('color', 's2')] == ValueSet(['R'])
    #check reversion to superset is possible
    s.set_ascription(('color', 's2'), ['R', 'G'])
    assert s[('color', 's2')] == ValueSet(['R', 'G'])
    s.set_ascription(('size', 's1'), ['M', 'S'])
    assert s[('size', 's1')] == ValueSet(['S', 'M'])

def test___getitem__():
    """Test indexing for State"""
    pass

def test_is_valuation():
    """Test is_valuation function."""
    pass

def test_is_world():
    """Test is_world function."""
    pass

def test_get_worlds():
    """Test get_worlds function."""
    pass

def test_is_alternate_extension():
    """Test is_alternate_extension function."""
    pass

def test_get_alternate_extensions():
    """Test get_alternate_extensions function."""
    pass

def test___str__():
    """Test str(State)"""
    pass

def test___repr__():
    """."""
    pass
