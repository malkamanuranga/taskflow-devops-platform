import pytest

import app as app_module

@pytest.fixture
def client():
    app_module.tasks.clear()
    app_module.next_id = 1
    return app_module.app.test_client()
