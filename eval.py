VALID_LOGIC = {
    "raining": "umbrella",
    "sunny": "sunglasses",
    "snowing": "coat",
    # add more valid mappings here
}


def validate_condition(cond: dict) -> str | None:
    """
    Validate a single condition block (if/elseif/else).
    Returns an error string if invalid, otherwise None.
    """
    if "if" in cond or "elseif" in cond:
        key = "if" if "if" in cond else "elseif"
        condition = cond[key]
        action = cond["action"]

        expected_action = VALID_LOGIC.get(condition)
        if expected_action is None:
            return f"unknown condition: {condition}"
        if action != expected_action:
            return f"incorrect logic: {condition} → {action}"

    # 'else' doesn’t need validation of condition, only action can exist
    return None


def build_expected_sequence(conditions: list[dict]) -> list[str]:
    """
    Build the expected sequence of tokens from condition blocks.
    """
    expected = []
    for cond in conditions:
        if "if" in cond:
            expected.extend(["if", cond["if"], cond["action"]])
        elif "elseif" in cond:
            expected.extend(["elseif", cond["elseif"], cond["action"]])
        elif "else" in cond:
            expected.append("else")
            if cond["else"]:
                expected.append(cond["else"])
    return expected


def generate_output(parsed_data: dict) -> str:
    sequence = parsed_data.get("sequence", [])
    conditions = parsed_data.get("conditions", [])
    colors = parsed_data.get("colors", [])
    loop_count = parsed_data.get("loop_count", 1)

    # 1️⃣ Validate conditions (condition → correct action)
    for cond in conditions:
        error = validate_condition(cond)
        if error:
            return error  # e.g., "incorrect logic: raining → sunglasses"

    # 2️⃣ Validate conditional order (CFG structure)
    conditional_sequence = [tok for tok in sequence if tok not in colors]
    expected_conditional_sequence = build_expected_sequence(conditions)

    if conditional_sequence != expected_conditional_sequence:
        return "wrong arrangement"

    # 3️⃣ Generate final output
    if colors:
        return " ".join(colors * loop_count)

    if conditions:
        return " ".join(sequence)  # join if/elseif/else structure

    return "No valid blocks detected."
