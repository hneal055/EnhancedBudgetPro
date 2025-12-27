import random
import statistics

class MonteCarloBudgetEngine:
    """
    Monte Carlo simulation engine for production budget forecasting.
    Supports volatility (%), simulation count, and clean statistical output.
    """

    def simulate_budget(self, simulations: int, base_cost: float, volatility: float = 10, risk_factor: float = None):
        """
        Run a Monte Carlo budget simulation.

        Args:
            simulations (int): Number of simulation runs.
            base_cost (float): Base talent or total budget to perturb.
            volatility (float): +/- % variation allowed in cost.
            risk_factor (float, optional): Alias for volatility. If provided, overrides volatility.

        Returns:
            dict: Simulation distribution, mean, percentiles.
        """
        
        # Allow risk_factor as an alias for volatility
        if risk_factor is not None:
            volatility = risk_factor * 100 if risk_factor < 1 else risk_factor

        if simulations <= 0:
            simulations = 100

        if volatility <= 0:
            volatility = 10

        volatility_fraction = volatility / 100.0

        results = []

        for _ in range(simulations):
            # random variation (e.g., +/- 10%)
            variation = random.uniform(-volatility_fraction, volatility_fraction)
            simulated_cost = base_cost * (1 + variation)
            results.append(simulated_cost)

        # Compute statistics
        mean_val = statistics.mean(results)
        p10 = sorted(results)[max(0, int(simulations * 0.10) - 1)]
        p90 = sorted(results)[min(simulations - 1, int(simulations * 0.90))]

        return {
            "simulations": results,
            "mean": mean_val,
            "p10": p10,
            "p90": p90
        }


