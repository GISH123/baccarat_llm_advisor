# src/baccarat_stats.py
import numpy as np
from src.baccarat_rules import calculate_hand_value, determine_winner, card_values as card_points

def calculate_win_probabilities(player_hand, banker_hand, deck):
    """
    Estimate win probabilities for Player, Banker, and Tie based on current hands.
    
    Args:
        player_hand (list): List of card descriptions (e.g., ['A Spade', '5 Heart']).
        banker_hand (list): List of card descriptions for Banker.
        deck (list): Remaining cards in the deck (simplified as empty for now).
    
    Returns:
        dict: Probabilities for 'player', 'banker', and 'tie' in percentages.
    """
    # Calculate initial totals
    player_total = calculate_hand_value(player_hand)
    banker_total = calculate_hand_value(banker_hand)

    # Check for natural 8 or 9 (no third cards drawn)
    if player_total >= 8 or banker_total >= 8:
        winner = determine_winner(player_hand, banker_hand)
        return {
            'player': 100.0 if winner == 'player' else 0.0,
            'banker': 100.0 if winner == 'banker' else 0.0,
            'tie': 100.0 if winner == 'tie' else 0.0
        }

    # If hands already have 3 cards, no further draws
    if len(player_hand) == 3 and len(banker_hand) == 3:
        winner = determine_winner(player_hand, banker_hand)
        return {
            'player': 100.0 if winner == 'player' else 0.0,
            'banker': 100.0 if winner == 'banker' else 0.0,
            'tie': 100.0 if winner == 'tie' else 0.0
        }

    # Simulate third-card draws (initially 2 cards each)
    outcomes = {'player': 0, 'banker': 0, 'tie': 0}
    total_simulations = 10000  # Increased for better accuracy

    # Simplified deck: 13 values (A, 2-10, J, Q, K), 4 suits each, excluding used cards
    card_names = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['Spade', 'Heart', 'Diamond', 'Club']
    all_cards = [f"{value} {suit}" for value in card_names for suit in suits]
    used_cards = set(player_hand + banker_hand)
    remaining_deck = [card for card in all_cards if card not in used_cards]

    for _ in range(total_simulations):
        sim_player = player_hand.copy()
        sim_banker = banker_hand.copy()
        sim_remaining_deck = remaining_deck.copy()  # Each simulation has its own deck

        # Player's third card rule
        if len(sim_player) == 2 and player_total <= 5:
            player_third_card = np.random.choice(sim_remaining_deck)
            sim_player.append(player_third_card)
            sim_remaining_deck.remove(player_third_card)

        # Banker's third card rule
        if len(sim_banker) == 2:
            if len(sim_player) == 2:  # Player stood (total 6-7)
                if banker_total <= 5:
                    banker_third_card = np.random.choice(sim_remaining_deck)
                    sim_banker.append(banker_third_card)
                    sim_remaining_deck.remove(banker_third_card)
            else:  # Player drew a third card
                player_third_value = card_points[sim_player[2].split()[0]]
                if banker_total <= 2:
                    banker_third_card = np.random.choice(sim_remaining_deck)
                    sim_banker.append(banker_third_card)
                    sim_remaining_deck.remove(banker_third_card)
                elif banker_total == 3 and player_third_value != 8:
                    banker_third_card = np.random.choice(sim_remaining_deck)
                    sim_banker.append(banker_third_card)
                    sim_remaining_deck.remove(banker_third_card)
                elif banker_total == 4 and 2 <= player_third_value <= 7:
                    banker_third_card = np.random.choice(sim_remaining_deck)
                    sim_banker.append(banker_third_card)
                    sim_remaining_deck.remove(banker_third_card)
                elif banker_total == 5 and 4 <= player_third_value <= 7:
                    banker_third_card = np.random.choice(sim_remaining_deck)
                    sim_banker.append(banker_third_card)
                    sim_remaining_deck.remove(banker_third_card)
                elif banker_total == 6 and player_third_value in [6, 7]:
                    banker_third_card = np.random.choice(sim_remaining_deck)
                    sim_banker.append(banker_third_card)
                    sim_remaining_deck.remove(banker_third_card)

        # Determine winner of this simulation
        winner = determine_winner(sim_player, sim_banker)
        outcomes[winner] += 1

    # Calculate probabilities as percentages
    total = sum(outcomes.values())
    return {k: v / total * 100 for k, v in outcomes.items()}