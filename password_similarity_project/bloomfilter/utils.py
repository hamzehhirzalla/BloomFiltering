import hashlib

class BloomFilter:
    def __init__(self, size=1000, num_hashes=15):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _ngrams(self, item, n=2):
        return [item[i:i+n] for i in range(len(item) - n + 1)]

    def _hashes(self, item):
        ngrams = self._ngrams(item)
        combined_hashes = [0] * (len(item) - 1)
        counter = 0
        for ngram in ngrams:
            hash1 = int(hashlib.md5(ngram.encode()).hexdigest(), 16)
            hash2 = int(hashlib.sha256(ngram.encode()).hexdigest(), 16)
            for i in range(self.num_hashes):
                current_hash = (hash1 + (i * hash2))
                combined_hashes[counter] |= current_hash
            counter += 1
        for i in range(len(item) - 1):
            combined_hashes[i] = combined_hashes[i] % self.size
        return combined_hashes

    def add(self, item):
        hash_values = self._hashes(item)
        for hash_value in hash_values:
            self.bit_array[hash_value] = 1
        return hash_values

    def check(self, item, threshold):
        hash_values = self._hashes(item)
        matches = sum(self.bit_array[hash_value] for hash_value in hash_values) / (len(item) - 1)
        return matches >= threshold

    def save_to_model(self, model_instance):
        model_instance.bit_array = bytearray(self.bit_array)
        model_instance.save()

    @classmethod
    def load_from_model(cls, model_instance):
        bf = cls(size=model_instance.size, num_hashes=model_instance.num_hashes)
        bf.bit_array = list(model_instance.bit_array)
        return bf

    def bit_array_to_string(self):
        return ''.join(str(bit) for bit in self.bit_array)
