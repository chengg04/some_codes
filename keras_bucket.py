def predict(all_data):
    preprocessing(all_data)
    da_df = all_data['da_df']
    # 60% train, 20% validation, 20% test.
    train, test = train_test_split(da_df, test_size=0.2)
    train, val = train_test_split(train, test_size=0.25)

    batch_size = 32
    train_ds = df_to_dataset(train, batch_size = batch_size)
    val_ds = df_to_dataset(val, shuffle=False, batch_size = batch_size)
    test_ds = df_to_dataset(test, shuffle=False, batch_size = batch_size)
    # for feature_batch, label_batch in train_ds.take(1):
    #     print('Every feature:', list(feature_batch.keys()))
    #     print('A batch of zones:', feature_batch['zone'])
    #     print('A batch of targets:', label_batch)

    # numarical features
    da_df_keys = da_df.keys().tolist()
    num_c = [item for item in da_df_keys if item not in ['zone','rt_wind']]
    # categorical features
    cat = ['zone']  # indicator categorical columns

    # Creating feature columns.
    feature_columns = []
    for header in num_c:
        scal_input_fn = get_scal(train, header)
        feature_columns.append(feature_column.numeric_column(header, normalizer_fn=scal_input_fn))
    for feature_name in cat:
        vocabulary = da_df[feature_name].unique()
        cat_c = tf.feature_column.categorical_column_with_vocabulary_list(feature_name, vocabulary)
        one_hot = feature_column.indicator_column(cat_c)
        feature_columns.append(one_hot)

    pdb.set_trace()

    # Create a feature layer from feature columns.
    feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

    # Setup the NN.
    model = tf.keras.Sequential([
        feature_layer,
        layers.Dense(1024, activation='relu'),
        layers.Dense(1024, activation='relu'),
        layers.Dense(512, activation='relu'),
        layers.Dense(512, activation='relu'),
        layers.Dense(256, activation='relu'),
        # layers.Dense(128, activation='relu'),
        # layers.Dense(16, kernel_regularizer=tf.keras.regularizers.l2(0.01), activation='relu'),
        # layers.Dense(64, kernel_regularizer=tf.keras.regularizers.l2(0.01), activation='relu'),
        # layers.Dropout(0.2),

        layers.Dense(5)
        # layers.Dense(10, activation = 'softmax')
    ])
    model.compile(optimizer='adam',
                  # loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  loss = 'binary_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(train_ds,
                        validation_data=val_ds,
                        epochs = 10)


    # Evaluation.
    loss, accuracy = model.evaluate(test_ds)
    print('Accuracy: ', accuracy)

    # Predicting the probability.
    probability_model = tf.keras.Sequential([model,
                                             tf.keras.layers.Softmax()])
    predictions = probability_model.predict(test_ds)

    pdb.set_trace()
    # test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
    #
    # print('\nTest accuracy:', test_acc)
    #
    # # Turn the raw output to probablity.
    # probability_model = tf.keras.Sequential([model,
    #                                          tf.keras.layers.Softmax()])
    # predictions = probability_model.predict(test_images)
    # print("First prediction:", predictions[0])

    return history
