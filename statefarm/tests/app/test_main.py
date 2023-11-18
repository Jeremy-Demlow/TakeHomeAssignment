import pytest


@pytest.mark.asyncio
async def test_predict(client, sample_data):
    response = await client.post("/predict", json=sample_data[0])
    assert response.status_code == 200
    assert "business_outcome" in response.json()


@pytest.mark.asyncio
async def test_batch_predict(client, sample_data):
    response = await client.post("/batch_predict", json=sample_data)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_business_logic(client, sample_data):
    response = await client.post("/predict", json=sample_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "phat" in response_data
    assert "business_outcome" in response_data
    input_variables = [
        key for key in response_data.keys() if key not in ["phat", "business_outcome"]
    ]
    assert input_variables == sorted(input_variables)
