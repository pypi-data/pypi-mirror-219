# Dict with fuzzy key matching 

## pip install fuzzyydictyy 

#### Tested against Windows 10 / Python 3.10 / Anaconda 


### Approximate Key Lookups: 

The fuzzy matching capability allows users to retrieve values even if the exact key is not available. This can be beneficial when dealing with user input, search queries, or data with potential typos or variations.

### Data Normalization: 

By allowing fuzzy matching, FuzzDict can help normalize input keys to a standard form. For example, if you have keys like "JohnDoe," "john_doe," and "John-Doe," you can use FuzzDict to map them to a standardized key, such as "johndoe," ensuring consistent access to the associated values.

### Data Deduplication: 

When working with large datasets, fuzzy key matching can assist in identifying and handling duplicate keys with slight variations. Instead of creating multiple keys for similar values, you can consolidate them under a single key, reducing redundancy and improving data organization.

### Improved User Experience: 

With fuzzy matching, FuzzDict can enhance user experience by accommodating user errors or variations in input. It can provide suggestions or automatically retrieve the closest matching value, reducing frustration and increasing usability.

### Time Efficiency: 

By leveraging the rapidfuzz library, FuzzDict performs efficient fuzzy matching algorithms, enabling quick lookup of values based on approximate keys. This can be especially advantageous when dealing with large datasets or real-time applications that require fast responses.


```python
from fuzzyydictyy import FuzzDict, dict_config
from rapidfuzz import fuzz
dict_config.fuzzycfg = {
  'scorer': fuzz.WRatio,
}
d = FuzzDict()
d["hans"] = 3
d["bobo"] = 30
d["baba"] = 320
print(d['hjan'])  # Output: 3 (Exact match for 'hjan' is not found)
print(d['boba'])  # Output: 30 (Exact match for 'boba' is not found)
print(d['babaa'])  # Output: 320 (Exact match for 'babaa' is not found)
```