from config import config
from loguru import logger
from quixstreams import State

max_candles_in_state = config.num_candles_in_state


def update_candles(candle: dict, state: State) -> dict:
    """
    Updates the list of candles we have in the state using the new candle,
    if the latest candle corresponds to a new window of candles, we append it to the list
    if it corresponds to the last candle of the current window, we replace the last candle in the list with the new candle

    Args:
        candle: The new candle
        state: The current state

    Returns:
        None
    """
    # Get the list of candles in the state
    candles = state.get(key='candles', default=[])
    if len(candles) == 0:
        candles.append(candle)
    # If the latest candle corresponds to a new window of candles, we append it to the list
    elif same_window(candles[-1], candle):
        candles[-1] = candle
    else:
        candles.append(candle)
    # If the number of candles in the state is greater than the maximum number of candles in the state, we remove the oldest candle
    if len(candles) > max_candles_in_state:
        candles.pop(0)

    # TODO: Check the candles have no missing windows. this can happen if the stream has small trade rates
    logger.debug(f'Number of candles in state for {candle["pair"]}: {len(candles)}')

    # Update the state with the new list of candles
    state.set('candles', candles)

    # Return the latest candle
    return candle


def count_candles(value: dict, state: State) -> int:
    """ "
    Updates the count of messages we have in the state using the new message,
    if the latest message corresponds to a new window of messages, we append it to the list
    if it corresponds to the last message of the current window, we replace the last message in the list with the new message

    Args:
        candle: The new candle
        state: The current state

    Returns:
        The updated state
    """
    total = state.get('total', default=0)
    total += 1
    state.set('total', total)
    return {**value, 'total': total}


def same_window(candle: dict, previous_candle: dict) -> bool:
    """
    Checks if two candles correspond to the same window
    """
    return (
        (candle['window_start'] == previous_candle['window_start'])
        and (candle['window_end'] == previous_candle['window_end'])
        and (candle['pair'] == previous_candle['pair'])
    )
