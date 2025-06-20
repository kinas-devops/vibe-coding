# =============================================================================
# Generated with help from Microsoft AI Copilot (https://copilot.microsoft.com)
# =============================================================================
__author__ = "Kinas, Microsoft AI Copilot"
__copyright__ = "Copyright 2025, Vibe-Coding Project"
__credits__ = ["Kinas", "Microsoft AI Copilot"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Kinas"
__email__ = "kinas.devops@gmail.com"
__status__ = "Production"
# =============================================================================

from drl_solver import DRLMastermindAgent, feedback
from itertools import product

class HybridDRLCSPSolver:
    def __init__(self, code_length=4, colors="RGBYOP", model_path=None):
        self.code_length = code_length
        self.colors = colors
        self.history = []
        self.pool = self._generate_all_codes()
        self.agent = DRLMastermindAgent(colors=colors, code_length=code_length, epsilon=0.0)
        if model_path:
            import torch
            checkpoint = torch.load(model_path)
            self.agent.model.load_state_dict(checkpoint["state_dict"])

    def _generate_all_codes(self):
        return [''.join(p) for p in product(self.colors, repeat=self.code_length)]

    def _is_consistent(self, candidate):
        for past_guess, fb in self.history:
            if feedback(candidate, past_guess) != fb:
                return False
        return True

    def next_guess(self):
        legal_codes = [code for code in self.pool if self._is_consistent(code)]
        if not legal_codes:
            return None

        # Let DRL suggest a guess, pick it if consistent
        suggestion = self.agent.choose(self.history, training=False)
        if suggestion in legal_codes:
            return suggestion

        # Else pick the best legal guess by agent Q-values
        state = self.agent.state_vector(self.history)
        import torch
        state_t = torch.tensor([state], dtype=torch.float32)
        with torch.no_grad():
            qvals = self.agent.model(state_t).squeeze()

        scores = {code: qvals[self.agent.index[code]].item() for code in legal_codes}
        return max(scores, key=scores.get)

    def update(self, guess, fb):
        self.history.append((guess, fb))
        self.pool = [code for code in self.pool if feedback(code, guess) == fb]

