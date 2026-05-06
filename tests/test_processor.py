import pytest

from src.data.processor import DataProcessor

from settings import POST_CAMPAIGN_FEATURES, TARGET_COLUMN


@pytest.fixture
def processor():
    processor = DataProcessor()
    processor.load_data()
    return processor

def test_load_data(processor):
    assert processor.df is not None, "Data should be loaded successfully."
    assert not processor.df.empty, "DataFrame should not be empty."

def test_preprocess_data(processor):
    X, y = processor.preprocess_data()
    assert X is not None, "Features (X) should not be None."
    assert y is not None, "Target variable (y) should not be None."

    assert X.shape[1] == 67, "Features (X) should have 67 columns."

def test_excluded_columns(processor):
    X, y = processor.preprocess_data()
    
    for col in POST_CAMPAIGN_FEATURES + [TARGET_COLUMN]:
        assert col not in X.columns

def test_preprocess_without_load_raises_error():
    p = DataProcessor()
    with pytest.raises(ValueError):
        p.preprocess_data()