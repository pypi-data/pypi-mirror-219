"""
Convert SGML text to dictionary.

support:   https://gitlab.com/dhbmarcos/sgml2dict
copyright: 2023 (c) D. H. B. Marcos. All rights reserved.
"""

_STATE_NONE             = 0
_STATE_TAG_NAME         = 1
_STATE_TAG_ATTRIBUTE    = 2
_STATE_TAG_CONTENT      = 3
_STATE_ATTRIBUTE_SPEC   = 4
_STATE_ATTRIBUTE_STRING = 5
_SEPARATOR              = "\x1f"


def _filter_attributes(text):
    state      = _STATE_ATTRIBUTE_SPEC
    name       = ""
    value      = ""
    attributes = []
    text       = text.strip()
    text       = text.replace("/", "")

    buffer   = ""
    position = 0
    while position < len(text):
        current = text[position]

        if (position - 1) < 0:
            previous = ""
        else:
            previous = text[position - 1]

        if (position + 1) >= len(text):
            next = ""
        else:
            next = text[position + 1]

        if state == _STATE_ATTRIBUTE_SPEC:
            if current == " " or current == _SEPARATOR:
                if previous == " " or previous == "=" or  next == "=":
                    position += 1
                    continue

                current = _SEPARATOR

            if current == '"':
                state = _STATE_ATTRIBUTE_STRING
        elif state == _STATE_ATTRIBUTE_STRING:
            if current == '"':
                state = _STATE_ATTRIBUTE_SPEC

        buffer   += current
        position += 1

    return buffer


def _parse_attributes(text):
    text = text.strip()
    if len(text) == 0:
        return None

    text       = _filter_attributes(text)
    text       = _filter_attributes(text)
    attributes = text.split(_SEPARATOR)
    buffer     = {}

    for attribute in attributes:
        tokens = attribute.split("=")
        if len(tokens) == 1:
            buffer[tokens[0]] = True
            continue
        buffer[tokens[0]] = tokens[1].strip('"')

    return buffer



def _parse_tag(text):
    state      = _STATE_NONE
    name       = ""
    attributes = ""
    content    = ""
    over       = ""
    position   = 0
    

    for character in text:
        position += 1

        if state == _STATE_NONE:
            if character == "<":
                state = _STATE_TAG_NAME
                continue

        if state == _STATE_TAG_NAME:
            if character == " ":
                state = _STATE_TAG_ATTRIBUTE
                continue

            if character == ">":
                state = _STATE_TAG_CONTENT
                continue

            name += character
            continue
            
        if state == _STATE_TAG_ATTRIBUTE:
            if character == ">":
                state = _STATE_TAG_CONTENT
                continue

            attributes += character
            continue

        if state == _STATE_TAG_CONTENT:
            content += character

            pattern = f"</{name}>"
            length  = (len(name) + len(pattern) - len(name) ) * -1
            sample  = content[length:]

            if sample == pattern:
                over    = text[position:]
                content = content[:length]
                break

    if name == "":
        return text

    tag = {
        "name":       name,
        "attributes": _parse_attributes(attributes),
        "content":    _parse_tags(content),
        "over":       over.strip()
    }

    if name[0] == "/":
        tag = tag["content"]
        
    return tag



def _parse_tags(text):
    tags = []

    if not text:
        return None

    while (len(text) > 0):
        content = _parse_tag(text)
        
        if isinstance(content, str):
            return content

        if not content:
            break

        text = content["over"]
        tag  = {"name": content["name"]}

        if content["attributes"]:
            tag["attributes"] = content["attributes"]

        if content["content"]:
            tag["content"] = content["content"]

        if tag["name"][-1] == "/":
            sub_tag     = content["content"]
            tag["name"] = tag["name"][:-1]
            if "content" in tag:
                del tag["content"]
            tags.append(tag)

            if sub_tag:
                tags.append(sub_tag)
            continue

        tags.append(tag)

    if len(tags) == 1:
        return tags[0]
    
    return tags


def convert(text):
    """
    Convert SGML text to dictionary.
    """
    return _parse_tags(text)
