def pytest_configure(config):
    config.addinivalue_line(
        "markers", "custom_marker: custom marker for pytestPackages"
    )
