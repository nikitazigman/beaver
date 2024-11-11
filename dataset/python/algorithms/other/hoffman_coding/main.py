import heapq


class Node:
    def __init__(self, value, left=None, right=None, parent_node=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent_node = parent_node

    def set_parent(self, parent_node):
        self.parent_node = parent_node

    def __lt__(self, other):
        return self.value[0] < other.value[0]


def get_huffman_code(input_str):
    char_nodes = count_chars(input_str)
    priority_queue = get_priority_queue(char_nodes)
    while len(priority_queue) > 1:
        node1 = heapq.heappop(priority_queue)
        node2 = heapq.heappop(priority_queue)
        parent_node = Node((node1.value[0] + node2.value[0], None), left=node1, right=node2)
        node1.set_parent(parent_node)
        node2.set_parent(parent_node)
        heapq.heappush(priority_queue, parent_node)
    huffman_dictionary = create_huffman_dictionary(char_nodes)
    encoded_text = encode_text(input_str, huffman_dictionary)
    padded_encoded_text = pad_encoded_text(encoded_text)
    return huffman_dictionary, to_byte_array(padded_encoded_text)


def decode_huffman_code(byte_array, huffman_dictionary):
    bit_string = "".join(format(byte, "08b") for byte in byte_array)
    reverse_huffman_dictionary = get_reverse_huffman_dictionary(huffman_dictionary)
    encoded_text = remove_extra_padding(bit_string)
    decoded_text = decode_text(encoded_text, reverse_huffman_dictionary)
    return decoded_text


def encode_text(text, huffman_dictionary):
    return "".join(map(lambda symbol: huffman_dictionary[symbol], list(text)))


def pad_encoded_text(encoded_text):
    extra_padding = 8 - len(encoded_text) % 8
    encoded_text += "0" * extra_padding
    padded_info = f"{extra_padding:08b}"
    encoded_text = padded_info + encoded_text
    return encoded_text


def to_byte_array(padded_encoded_text):
    byte_array = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i : i + 8]
        byte_array.append(int(byte, 2))
    return byte_array


def count_chars(input_str):
    chars_dictionary = {}
    for char in input_str:
        chars_dictionary[char] = (chars_dictionary.get(char) or 0) + 1
    nodes = []
    for key in chars_dictionary:
        nodes.append(Node((chars_dictionary[key], key)))
    return nodes


def get_priority_queue(char_nodes):
    heap = []
    for node in char_nodes:
        heapq.heappush(heap, node)
    return heap


def create_huffman_dictionary(char_nodes):
    huffman_dictionary = {}
    for node in char_nodes:
        temp = node
        byte_sequence = ""
        while temp.parent_node is not None:
            byte_sequence = ("0" if temp == temp.parent_node.left else "1") + byte_sequence
            temp = temp.parent_node
        huffman_dictionary[node.value[1]] = byte_sequence
    return huffman_dictionary


def get_reverse_huffman_dictionary(huffman_dictionary):
    reverse_huffman_dictionary = {}
    for key in huffman_dictionary:
        value = huffman_dictionary[key]
        reverse_huffman_dictionary[value] = key
    return reverse_huffman_dictionary


def remove_extra_padding(bit_string):
    padded_info = bit_string[:8]
    extra_padding = int(padded_info, 2)
    bit_string = bit_string[8:]
    encoded_text = bit_string[:-extra_padding]
    return encoded_text


def decode_text(encoded_text, reverse_huffman_dictionary):
    current_code = ""
    decoded_text = ""

    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_huffman_dictionary:
            character = reverse_huffman_dictionary[current_code]
            decoded_text += character
            current_code = ""

    return decoded_text
