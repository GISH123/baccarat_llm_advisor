# src/baccarat_rules.py
card_values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 0, 'J': 0, 'Q': 0, 'K': 0}

def calculate_hand_value(cards):
    """Calculate hand value modulo 10."""
    return sum(card_values[card.split()[0]] for card in cards) % 10

def determine_winner(player_hand, banker_hand):
    """Decide the winner based on final hand values."""
    player_value = calculate_hand_value(player_hand)
    banker_value = calculate_hand_value(banker_hand)
    if player_value > banker_value:
        return 'player'
    elif banker_value > player_value:
        return 'banker'
    else:
        return 'tie'