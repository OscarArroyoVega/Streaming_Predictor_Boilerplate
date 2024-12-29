import socket

import requests
from loguru import logger


def test_connection():  # TODO: remove this once we are done debugging or move to testing folder
    try:
        # Test raw socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('host.docker.internal', 11434))
        logger.info('Socket connection successful')
        sock.close()
    except Exception as e:
        logger.error(f'Socket connection failed: {e}')

    try:
        # Test HTTP connection
        response = requests.get(
            'http://host.docker.internal:11434/api/tags', timeout=30
        )
        logger.info(f'HTTP connection successful: {response.json()}')

        # Test actual LLM endpoint
        data = {
            'model': 'claude-3-opus-20240620',
            'prompt': 'Hello, how are you?',
            'stream': False,
        }

        response = requests.post(
            'http://host.docker.internal:11434/api/generate',
            json=data,
            timeout=30,  # Add timeout
        )
        logger.info(f'LLM generation successful: {response.json()}')
    except Exception as e:
        logger.error(f'HTTP connection failed: {e}')
