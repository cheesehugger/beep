
def is_even(num: int) -> bool:
    if num == 1:
        return False

    elif num == 2:
        return True

    elif num == 3:
        return False

    elif num == 4:
        return True

    elif num == 5:
        return False

    elif num == 6:
        return True

    elif num == 7:
        return False

    elif num == 8:
        return True

    elif num == 9:
        return False

    elif num == 10:
        return True


if __name__ == "__main__":
    n = int(input("Enter your number: "))
    print(f"{n} is even" if is_even(n) else f"{n} is odd or unknown")
