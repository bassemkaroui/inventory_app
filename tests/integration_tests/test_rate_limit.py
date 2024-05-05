def test_rate_limit(testing_app, rate_limit_value, valid_item_id):
    for _ in range(rate_limit_value + 1):
        response = testing_app.get(f'/item/{valid_item_id}')
        if response.status_code == 429:
            break
    assert response.status_code == 429