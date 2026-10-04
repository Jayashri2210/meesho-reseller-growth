def alias_for(reseller_id: str) -> str:
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    return not any(name in text for name in reseller_names)


if __name__ == "__main__":
    # Required positive case
    assert alias_for("RS019") == "ALIAS-19"
    assert alias_for("RS006") == "ALIAS-06"

    # Required negative and positive masking cases
    safe_text = "West reseller ALIAS-19 generated strong total spend."
    leaked_text = "Mumbai Reseller 1 generated strong total spend."

    assert assert_no_raw_names_leak(
        safe_text,
        ["Mumbai Reseller 1"]
    ) is True

    assert assert_no_raw_names_leak(
        leaked_text,
        ["Mumbai Reseller 1"]
    ) is False

    print("Masking checks passed.")
