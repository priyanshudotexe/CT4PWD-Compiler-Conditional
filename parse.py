# parse.py

def _parse_if(blocks, i):
    cond = blocks[i + 1].get("value") if i + 1 < len(blocks) and blocks[i + 1]["type"] == "condition" else None
    action = blocks[i + 2].get("value") if i + 2 < len(blocks) and blocks[i + 2]["type"] == "action" else None

    entry = {"if": cond, "action": action}
    seq = ["if"] + ([cond] if cond else []) + ([action] if action else [])
    return entry, seq, i + 3


def _parse_elseif(blocks, i):
    cond = blocks[i + 1].get("value") if i + 1 < len(blocks) and blocks[i + 1]["type"] == "condition" else None
    action = blocks[i + 2].get("value") if i + 2 < len(blocks) and blocks[i + 2]["type"] == "action" else None

    entry = {"elseif": cond, "action": action}
    seq = ["elseif"] + ([cond] if cond else []) + ([action] if action else [])
    return entry, seq, i + 3


def _parse_else(blocks, i):
    action = blocks[i + 1].get("value") if i + 1 < len(blocks) and blocks[i + 1]["type"] == "action" else None

    entry = {"else": action}
    seq = ["else"] + ([action] if action else [])
    return entry, seq, i + 2


def parse_blocks(blocks, loop_count, colors_from_image=None):
    """
    Parse blocks from detect_qr_and_blocks().

    Note: colors_from_image is accepted for backward compatibility but ignored.
    Colors are taken only from QR text (type == "color").
    """
    colors, conditions, sequence = [], [], []

    i = 0
    n = len(blocks)

    while i < n:
        b = blocks[i]
        t, v = b.get("type"), b.get("value")

        if t == "loop":
            i += 1
            continue

        if t == "control":
            if v == "if":
                entry, seq, i = _parse_if(blocks, i)
                conditions.append(entry)
                sequence.extend(seq)
                continue
            elif v == "elseif":
                entry, seq, i = _parse_elseif(blocks, i)
                conditions.append(entry)
                sequence.extend(seq)
                continue
            elif v == "else":
                entry, seq, i = _parse_else(blocks, i)
                conditions.append(entry)
                sequence.extend(seq)
                continue
            else:
                sequence.append(v)
                i += 1
                continue

        if t == "color":
            colors.append(v)
            sequence.append(v)
            i += 1
            continue

        if t in {"condition", "action", "label"}:
            sequence.append(v)
            i += 1
            continue

        i += 1

    return {
        "colors": colors,
        "loop_count": loop_count,
        "conditions": conditions,
        "sequence": sequence
    }
