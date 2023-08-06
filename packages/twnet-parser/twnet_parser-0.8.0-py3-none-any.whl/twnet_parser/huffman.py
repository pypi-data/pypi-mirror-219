from twnet_parser.external.huffman import huffman

HAS_LIBTW2 = False

try:
    import libtw2_huffman # type: ignore
    HAS_LIBTW2 = True
except ImportError:
    HAS_LIBTW2 = False

def backend_name() -> str:
    if HAS_LIBTW2:
        return 'rust-libtw2'
    return 'python-TeeAI'

def compress(data: bytes) -> bytes:
    if HAS_LIBTW2:
        return libtw2_huffman.compress(data)
    return huffman.decompress(bytearray(data))

def decompress(data: bytes) -> bytes:
    if HAS_LIBTW2:
        return libtw2_huffman.decompress(data)
    return huffman.decompress(bytearray(data))
