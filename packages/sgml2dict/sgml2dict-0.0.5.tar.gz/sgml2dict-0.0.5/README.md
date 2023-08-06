# sgml2dict

Convert SGML text to dictionary.

## API

### Initiate

```py
import sgml2dict
```

### convert(text)

parameter
- text: SGML text

return: dict

```py
import sgml2dict
result = sgml2dict.convert("<hello world/></hello>")
```

## Example

```py
import json
import sgml2dict

text = "<hello world/></hello>"
data = sgml2dict.convert(text)

print("Dictionary view:", data)
print("JSON view:", json.dumps(data))
```

Return:
```
Dictionary view: {'name': 'hello', 'attributes': {'world': True}}
JSON view: {"name": "hello", "attributes": {"world": true}}
```

## Support

https://gitlab.com/dhbmarcos/sgml2dict

## License

 - MIT License
 - Copyright (c) 2023 D. H. B. Marcos. All rights reserved.
