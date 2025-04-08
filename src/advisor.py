# advisor.py
import yaml
import logging
import time
from src.model_loader import LLMModelLoader
from src.baccarat_rules import calculate_hand_value
from src.baccarat_stats import calculate_win_probabilities

logger = logging.getLogger(__name__)

class BaccaratLLMAdvisor:
    def __init__(self, config_path):
        """Initialize the advisor with a config file."""
        self.config = self._load_config(config_path)
        if self.config.get("enabled", True):
            self.model_loader = LLMModelLoader(
                self.config["model_path"],
                self.config.get("use_gpu", True)
            )
        else:
            self.model_loader = None

    def _load_config(self, config_path):
        """Load configuration from a YAML file."""
        try:
            with open(config_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}

    def _format_cards_for_prompt(self, resultlist):
        """
        Format card results into a dictionary. We'll compute
        player_points, banker_points for use in user-facing text or in logic.
        """
        player_cards = []
        banker_cards = []

        for card in resultlist:
            card_desc = self._get_card_description(card.classid)
            if card.index in [1, 3, 5]:  # Player positions
                player_cards.append(card_desc)
            elif card.index in [2, 4, 6]:  # Banker positions
                banker_cards.append(card_desc)

        player_points = calculate_hand_value(player_cards)
        banker_points = calculate_hand_value(banker_cards)

        player_text = "，".join(player_cards) if player_cards else "无牌"
        banker_text = "，".join(banker_cards) if banker_cards else "无牌"

        return {
            "player_cards": player_text,
            "player_points": player_points,
            "banker_cards": banker_text,
            "banker_points": banker_points
        }

    def _create_user_state_string(self, game_state, probabilities, EV_player, EV_banker, EV_tie, third_card_info):
        """
        Build a user-friendly text that shows:
          - player's & banker's hands
          - probabilities
          - EV
        We'll display/log it, but NOT feed it to the LLM directly.
        """
        user_state = (
            f"当前状态：\n"
            f"玩家牌：{game_state['player_cards']}（总计 {game_state['player_points']} 点）\n"
            f"庄家牌：{game_state['banker_cards']}（总计 {game_state['banker_points']} 点）\n"
            f"游戏当前状态：{third_card_info}\n\n"
            f"获胜概率(以模拟后的概率)：\n"
            f"- 玩家：{probabilities['player']:.2f}%\n"
            f"- 庄家：{probabilities['banker']:.2f}%\n"
            f"- 和局：{probabilities['tie']:.2f}%\n\n"
            f"期望值(概率 * 赔率回报)：\n"
            f"- 玩家投注：{EV_player:.4f}\n"
            f"- 庄家投注：{EV_banker:.4f}\n"
            f"- 和局投注：{EV_tie:.4f}\n"
        )
        return user_state

    def _create_prompt(self, EV_player, EV_banker, EV_tie):
        """
        A short internal prompt. We add '###' at the end so we can truncate any repeated text
        that appears before the model's actual response in post-processing.
        """
        prompt = f"""
你是一位百家乐专家，请根据以下规则给出简短回答：

规则：
1) 如果三个选项(玩家/庄家/和局)的期望值都为负，则选择(4)不下注。
2) 否则，选择期望值最大的那个选项。

给定期望值：
- 玩家EV = {EV_player:.4f}
- 庄家EV = {EV_banker:.4f}
- 和局EV = {EV_tie:.4f}

仅输出两行：
(你的建议)：(1 或 2 或 3 或 4)
(你的解释)：(用中文简要说明原因，不要超过两句)

请严格遵守上述规则。

###  <-- STOP MARKER
"""
        return prompt.strip()

    def _get_card_description(self, classid):
        """Convert classid to human-readable card description."""
        suits = ["Spade", "Heart", "Diamond", "Club"]
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        suit_idx = (classid - 1) // 13
        value_idx = (classid - 1) % 13
        return f"{values[value_idx]} {suits[suit_idx]}"

    def _get_fallback_advice(self, resultlist):
        """Return fallback advice if the model is unavailable."""
        return "模型未加载，建议根据经验或规则投注。"

    def _determine_third_card_info(self, player_total, banker_total, player_cards, banker_cards):
        """
        A helper to produce a short text describing who might draw the third card,
        for user display.
        """
        # Check for natural
        natural_win = (
            (len(player_cards) == 2 and player_total >= 8) or
            (len(banker_cards) == 2 and banker_total >= 8)
        )
        if natural_win:
            return "双方或一方已达自然胜，通常不再抽第三张牌"

        # Player draws if total <= 5 (with exactly 2 cards)
        if len(player_cards) == 2 and player_total <= 5:
            info = "玩家将抽第三张牌"
            info += "，庄家可能根据玩家的第三张牌抽牌"
            return info
        else:
            info = "玩家停止抽牌"
            if len(banker_cards) == 2 and banker_total <= 5:
                info += "，庄家将抽第三张牌"
            else:
                info += "，庄家停止抽牌"
            return info

    def get_advice(self, gmcode, resultlist):
        """
        Generate advice using the loaded model or return fallback.
        We'll separate the 'user state' text from the 'prompt' text,
        then log both, plus the final LLM advice. We'll also do post-processing
        to remove repeated prompt text.
        """
        # 1) Check if model is loaded
        if not self.config.get("enabled", True) or \
           self.model_loader is None or \
           self.model_loader.model is None:
            return self._get_fallback_advice(resultlist)

        # 2) Format card data
        game_state = self._format_cards_for_prompt(resultlist)

        # 3) Probability simulation
        deck = []
        sim_start_time = time.time()
        logger.info("Starting 1000-game simulation for probabilities")
        probabilities = calculate_win_probabilities(
            game_state['player_cards'].split('，'),
            game_state['banker_cards'].split('，'),
            deck
        )
        sim_elapsed_time = time.time() - sim_start_time
        logger.info(f"1000-game simulation completed in {sim_elapsed_time:.2f} seconds")

        # 4) Who draws a third card?
        third_card_info = self._determine_third_card_info(
            game_state['player_points'],
            game_state['banker_points'],
            game_state['player_cards'].split('，'),
            game_state['banker_cards'].split('，')
        )

        # 5) Compute EV for each bet
        prob_player = probabilities['player'] / 100
        prob_banker = probabilities['banker'] / 100
        prob_tie    = probabilities['tie']    / 100

        EV_player = prob_player * 1 + (prob_banker + prob_tie) * (-1)
        EV_banker = prob_banker * 0.95 + (prob_player + prob_tie) * (-1)
        EV_tie    = prob_tie * 8 + (prob_player + prob_banker) * (-1)

        # 6) Create user-facing info (not fed to LLM)
        user_friendly_state = self._create_user_state_string(
            game_state, probabilities, EV_player, EV_banker, EV_tie, third_card_info
        )

        # 7) Create minimal internal LLM prompt (with '###' stop marker)
        llm_prompt = self._create_prompt(EV_player, EV_banker, EV_tie)

        # 8) Log the user-facing info & LLM prompt
        logger.info("--- Current State for the user ---\n" + user_friendly_state)
        logger.info("--- LLM Prompt (internal) ---\n" + llm_prompt)

        try:
            # 9) Run inference
            llm_start_time = time.time()
            logger.info("Starting LLM prompt processing")

            inputs = self.model_loader.tokenizer(llm_prompt, return_tensors="pt").to(self.model_loader.device)
            output_ids = self.model_loader.model.generate(
                **inputs,
                max_new_tokens=self.config.get("max_new_tokens", 150)
            )

            raw_text = self.model_loader.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            llm_elapsed_time = time.time() - llm_start_time
            logger.info(f"LLM prompt processing completed in {llm_elapsed_time:.2f} seconds")

            # 10) Post-process to remove repeated prompt from the output
            #     We'll split on '###' and take whatever is AFTER it
            #     Then we parse the lines to keep only the final 2 lines we want.
            if "###" in raw_text:
                # everything after the last '###'
                raw_text = raw_text.split("###")[-1]

            # Now let's parse lines:
            lines = raw_text.strip().splitlines()
            final_lines = []
            for line in lines:
                if line.strip().startswith("(你的建议)") or line.strip().startswith("(你的解释)"):
                    final_lines.append(line.strip())
                # We only want 2 lines total
                if len(final_lines) == 2:
                    break

            # If the model didn't provide them properly, fallback to entire raw_text
            if len(final_lines) < 2:
                final_advice = raw_text.strip()
            else:
                final_advice = "\n".join(final_lines)

            logger.info("--- LLM output (post-processed) ---\n" + final_advice)

            return final_advice

        except Exception as e:
            logger.error(f"Error generating advice: {e}")
            return self._get_fallback_advice(resultlist)
