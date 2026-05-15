# this file enforces business rules
# right now there is only 1 rule that no discount should exceed max_discount_rate
from week9_10.config import MAX_DISCOUNT_RATE


def apply_policy_cap(discount_rate: float):
    if discount_rate <= MAX_DISCOUNT_RATE:
        return discount_rate, None
    else:
        warning = (
            f"Discount rate {discount_rate:.2f} exceeded the policy cap of "
            f"{MAX_DISCOUNT_RATE:.2f} and was reduced to {MAX_DISCOUNT_RATE:.2f}."
        )
        return MAX_DISCOUNT_RATE, warning


def is_within_policy(discount_rate: float):
    return discount_rate <= MAX_DISCOUNT_RATE


# just to test apply_policy_cap
if __name__ == "__main__":
    test_rates = [0.00, 0.05, 0.15, 0.20, 0.25, 0.50]
    for rate in test_rates:
        capped, warning = apply_policy_cap(rate)
        print(f"input={rate:.2f}  ->  capped={capped:.2f}  warning={warning}")
