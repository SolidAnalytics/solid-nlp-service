from typing import Any
from datetime import datetime


def get_error_message(service_name: str, input_data: dict[str, Any], err: Exception, trace: str) -> dict[str, Any]:
    return {
        'service': service_name,
        'type': 'error',
        'priority': 'high',
        'date': datetime.now().isoformat(),
        'input_data': input_data,
        'message': {
            'error': f"Error during getting input data: {err}",
            'trace': trace
        }
    }