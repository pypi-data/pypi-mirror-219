import random
import string


def generate_random_id(hub, length: int):
    """
    Returns a random id. The string will be alphanumeric, and start with a letter.

    Each character represents approximately 6 bits. Specifically, the number of
    unique strings=52*62^(length-1). So a length of 4 has 12 million combinations, 8 has
    1.8 trillion combinations. This is roughly 65% that of 64^8.

    Args:
        length(int): The number of characters to generate. Each character represents approximately 6 bits of entropy.

    Returns:
        The generated random ID.
    """
    try:
        # prefer to use system random number generator
        rand = random.SystemRandom()
    except NotImplementedError:
        # if that isn't available, fall back to pseudo-random number seeded by time
        rand = random.Random()

    # This random data is used for generating IDs. Common requirements are for it to start alphabetical.
    data = [rand.choice(string.ascii_letters)]

    # The original data produced b64 encoded data. Let's use b64 compatible characters, minus +/, which
    #  are often not allowed as ids.
    charset = string.ascii_letters + string.digits
    data.extend(rand.choices(charset, k=length - 1))

    return "".join(data[:length])
