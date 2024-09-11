from src.main import decode_huffman_code, get_huffman_code


def test_huffman_coding():
    input_str = "this is an example for huffman encoding"
    huffman_dictionary, encoded = get_huffman_code(input_str)
    decoded = decode_huffman_code(encoded, huffman_dictionary)
    assert decoded == input_str


def test_huffman_coding_with_repeated_chars():
    input_str = "aaaaabbbcccccc"
    huffman_dictionary, encoded = get_huffman_code(input_str)
    decoded = decode_huffman_code(encoded, huffman_dictionary)
    assert decoded == input_str


def test_huffman_coding_with_empty_string():
    input_str = ""
    huffman_dictionary, encoded = get_huffman_code(input_str)
    decoded = decode_huffman_code(encoded, huffman_dictionary)
    assert decoded == input_str
