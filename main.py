from pathlib import Path
import os
import data
import PCA
import predictor
import plots
import scraper
import normality_test
import keras_bucket
import pdb

def setup_data():
    # parameters
    wd = Path(os.getcwd())
    pwd = str(wd.parent.absolute())
    all_data = {}
    all_data['pwd'] = pwd
    all_data['google_drive_path'] = '/Volumes/GoogleDrive/My Drive/Projects_sync/Wind_prediction_update'

    all_data['task'] = 'get_data' # pca | predict | plot | get_data | normality_test | keras_bucket
    all_data['days'] = 20
    all_data['ml_algo'] = 'RF' # RF CLA
    all_data['random_state_val'] = 42
    # all_data['suppress_tf_warnings'] = True

    # read in data
    all_data = data.read_data(all_data)

    # pdb.set_trace()

    return all_data


if __name__ == '__main__':
    all_data = setup_data()

    if all_data['task'] == 'pca':
        PCA.PCA(all_data)
    elif all_data['task'] == 'predict':
        X, y = predictor.train_regressor(all_data)
        predictor.evaluate_regressor(all_data, X, y)
    elif all_data['task'] == 'plot':
        # plots.density_plot(all_data)
        plots.histo_plot(all_data)
    elif all_data['task'] == 'get_data':
        scraper.historical_data(all_data)
    elif all_data['task'] == 'normality_test':
        normality_test.run_test(all_data)
        # plots.density_plot_newNREL(all_data)
    elif all_data['task'] == 'keras_bucket':
        # pdb.set_trace()
        history = keras_bucket.predict(all_data)
        keras_bucket.plotting(history, all_data)

