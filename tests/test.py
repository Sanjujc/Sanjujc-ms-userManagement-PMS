def cardPackets(cardTypes):
    n = len(cardTypes)
    min_additional_cards = float('inf')  # Initialize with a large number

    for packets in range(2, max(cardTypes) + 1):  # Start from 2 packets
        additional_cards = 0

        for cards in cardTypes:
            remainder = cards % packets
            if remainder != 0:
                additional_cards += (packets - remainder)

        min_additional_cards = min(min_additional_cards, additional_cards)

    return min_additional_cards


# Sample Input
cardTypes = [3, 8, 7, 6, 4]

print(cardPackets(cardTypes))  # Output should be 2
