import math


def _check_prime(number: int) -> bool:
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True


def get_primes(number: int) -> list:
    return [i for i in range(2, number) if _check_prime(i)]


if __name__ == "__main__":
    print(get_primes(1))
    print(get_primes(10))
    print(get_primes(100))
