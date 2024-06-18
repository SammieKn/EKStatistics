import kaggle

api = kaggle.api
kaggle.api.dataset_download_files('martj42/international-football-results-from-1872-to-2017', path='./data_new', unzip=True)