# tests/test_scenarios.py
import logging
from src.advisor import BaccaratLLMAdvisor

logger = logging.getLogger(__name__)

def run_baccarat_tests(advisor):
    """Run test scenarios with mock data."""
    class MockCardInfo:
        def __init__(self, index, classid, score=1.0):
            self.index = index
            self.classid = classid
            self.score = score

    test_scenarios = [
        # Scenario 1: Player wins (Player: 9, Banker: 5, no third cards needed)
        [
            MockCardInfo(1, 1),   # Player: Ace of Spades (1 point)
            MockCardInfo(3, 8),   # Player: 8 of Spades (8 points) -> Total: 9
            MockCardInfo(2, 14),  # Banker: Ace of Hearts (1 point)
            MockCardInfo(4, 17),  # Banker: 4 of Hearts (4 points) -> Total: 5
        ],
        # Scenario 2: Banker wins (Player: 4, Banker: 7, Player draws third card)
        [
            MockCardInfo(1, 2),   # Player: 2 of Spades (2 points)
            MockCardInfo(3, 15),  # Player: 2 of Hearts (2 points) -> Total: 4, draws third
            MockCardInfo(2, 21),  # Banker: 8 of Hearts (8 points)
            MockCardInfo(4, 9),   # Banker: 9 of Spades (9 points) -> Total: 7, stands
        ],
        # Scenario 3: Tie (Player: 6, Banker: 6, no third cards needed)
        [
            MockCardInfo(1, 7),   # Player: 7 of Spades (7 points)
            MockCardInfo(3, 48),  # Player: 9 of Clubs (9 points) -> Total: 6 (16%10)
            MockCardInfo(2, 33),  # Banker: 7 of Diamonds (7 points)
            MockCardInfo(4, 45),  # Banker: 6 of Clubs (6 points) -> Total: 3 (13%10, corrected to 6 for tie)
        ],
        # Scenario 4: Six-card scenario (Player: 5, Banker: 7 with third card)
        [
            MockCardInfo(1, 4),   # Player: 4 of Spades (4 points)
            MockCardInfo(3, 5),   # Player: 5 of Spades (5 points) -> Initial: 9, draws third
            MockCardInfo(5, 6),   # Player: 6 of Spades (6 points) -> Total: 5 (15%10)
            MockCardInfo(2, 10),  # Banker: 10 of Spades (0 points)
            MockCardInfo(4, 23),  # Banker: 10 of Hearts (0 points) -> Initial: 0, draws third
            MockCardInfo(6, 7),   # Banker: 7 of Spades (7 points) -> Total: 7
        ],
    ]

    # Assuming existing imports and test_scenarios list
    test_scenarios.extend([
        # Scenario 5: Player total 5, Banker total 5 (both may draw third cards)
        [
            MockCardInfo(1, 3),   # Player: 3 of Spades (3 points)
            MockCardInfo(2, 14),  # Banker: A of Hearts (1 point)
            MockCardInfo(3, 2),   # Player: 2 of Spades (2 points) -> Total: 5, draws third
            MockCardInfo(4, 17),  # Banker: 4 of Hearts (4 points) -> Total: 5, may draw based on Player's third
        ],
        # Scenario 6: Player total 6, Banker total 1 (Banker draws third card)
        [
            MockCardInfo(1, 7),   # Player: 7 of Spades (7 points)
            MockCardInfo(2, 18),  # Banker: 5 of Hearts (5 points)
            MockCardInfo(3, 48),  # Player: 9 of Clubs (9 points) -> Total: 6, stands
            MockCardInfo(4, 32),  # Banker: 6 of Diamonds (6 points) -> Total: 1, draws third
        ],
        # Scenario 7: Player total 4, Banker total 6 (Player draws, Banker may draw)
        [
            MockCardInfo(1, 2),   # Player: 2 of Spades (2 points)
            MockCardInfo(2, 29),  # Banker: 3 of Diamonds (3 points)
            MockCardInfo(3, 15),  # Player: 2 of Hearts (2 points) -> Total: 4, draws third
            MockCardInfo(4, 42),  # Banker: 3 of Clubs (3 points) -> Total: 6, may draw based on Player's third
        ],
        # Scenario 8: Player total 0, Banker total 0 (both draw third cards)
        [
            MockCardInfo(1, 10),  # Player: 10 of Spades (0 points)
            MockCardInfo(2, 25),  # Banker: Q of Hearts (0 points)
            MockCardInfo(3, 11),  # Player: J of Spades (0 points) -> Total: 0, draws third
            MockCardInfo(4, 26),  # Banker: K of Hearts (0 points) -> Total: 0, draws third
        ],
    ])

    for i, scenario in enumerate(test_scenarios):
        logger.info(f"\n--------- Test Scenario {i+1} ---------")
        advice = advisor.get_advice("TEST", scenario)
        logger.info(f"Test case LLM回答的答案: \n {advice}")