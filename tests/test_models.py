from lib.models.key_value_pair import KeyValuePair

def test_new_pair():
    """
    GIVEN a KeyValuePair model
    WHEN a new pair is created
    THEN check the key and value are defined correctly
    """
    pair = KeyValuePair(key='key_1', value='value_1')
    assert pair.key == 'key_1'
    assert pair.value == 'value_1'
