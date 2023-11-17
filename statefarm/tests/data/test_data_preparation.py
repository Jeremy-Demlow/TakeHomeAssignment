def test_data_splitting(data_splitter):
    data_splitter.split_data(
        test_size=0.2, val_size=0.1, random_state=42, create_test_set=True
    )
    assert data_splitter.X_train is not None
    assert data_splitter.X_valid is not None
    assert data_splitter.X_test is not None
    assert len(data_splitter.X_train) + len(data_splitter.X_valid) + len(
        data_splitter.X_test
    ) == len(data_splitter.df)


def test_no_test_set(data_splitter):
    data_splitter.split_data(create_test_set=False)
    assert data_splitter.X_test is None


def test_fit_transform(data_preprocessor, data_splitter):
    data_splitter.split_data(create_test_set=True)
    transformed_train = data_preprocessor.fit_transform(data_splitter.X_train)
    assert transformed_train is not None
    assert (
        "x12" not in transformed_train.columns
    )  # Assuming x12 was a column to convert


def test_transform(data_preprocessor, data_splitter):
    data_splitter.split_data(create_test_set=True)
    transformed_valid = data_preprocessor.transform(data_splitter.X_valid)
    assert transformed_valid is not None
    assert (
        "x63" not in transformed_valid.columns
    )  # Assuming x63 was a column to convert
