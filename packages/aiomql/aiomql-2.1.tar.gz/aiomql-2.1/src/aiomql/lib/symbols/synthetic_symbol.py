from math import ceil, log10

from ...symbol import Symbol


class SyntheticSymbol(Symbol):
    """Subclass of Symbol for Synthetic Symbols. Handles the computation of stop loss, take profit and volume.
    """

    async def get_sl_tp_volume(self, *, amount: float, risk_to_reward: float, points: float) -> tuple[float, float, float]:
        """Calculate the required stop_loss, take_profit and volume given an amount, a risk to reward factor and the
        desired points to capture.

        Keyword Args:
            amount (float): amount to risk.
            risk_to_reward: ratio of risk to reward.
            points: points to capture.

        Returns:
            tuple[float, float, float]: stop loss, take profit and volume

        Raises:
            ValueError: If the computed volume is less than the minimum volume or greater than the maximum volume.
        """
        volume = (points * self.point) / amount
        step = ceil(abs(log10(self.volume_step)))
        volume = round(volume, step)

        if (volume < self.volume_min) or (volume > self.volume_max):
            raise ValueError(f'Incorrect Volume. Computed Volume: {volume}; Symbol Max Volume: {self.volume_max}; '
                             f'Symbol Min Volume: {self.volume_min}')

        return (sl := amount / volume), sl * risk_to_reward, volume
