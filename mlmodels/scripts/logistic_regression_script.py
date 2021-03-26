import argparse
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import os
import pandas as pd
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Get train test split ratio
    parser.add_argument("--test-ratio", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)

    # Parser environment variables by Amazon Sagemaker
    parser.add_argument('--output-data-dir', type=str, default=os.environ.get('SM_OUTPUT_DATA_DIR'))
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN'))

    # Parse all arguments
    args, _ = parser.parse_known_args()

    # Split into X and y
    input_files = [ os.path.join(args.train, file) for file in os.listdir(args.train) ]
    if len(input_files) == 0:
        raise ValueError(('There are no files in {}.\n' +
                          'This usually indicates that the channel ({}) was incorrectly specified,\n' +
                          'the data specification in S3 was incorrectly specified or the role specified\n' +
                          'does not have permission to access the data.').format(args.train, "train"))
    raw_data = [ pd.read_csv(file, header=None, engine="python", skiprows=1 ) for file in input_files ]
    train_data = pd.concat(raw_data)

    # Split into X and y
    train_data = train_data.values
    X = train_data[:, :-1]
    y = train_data[:, -1]

    # Split into train and test set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=args.test_ratio,
        random_state=args.random_state
    )

    # Create model and train using training set
    clf = LogisticRegression()
    clf.fit(X_train, y_train)

    # Make predictions
    y_train_prediction = clf.predict(X_train)
    y_test_prediction = clf.predict(X_test)

    # Calculate f1 score
    train_f1 = f1_score(y_train, y_train_prediction, average="micro")
    test_f1 = f1_score(y_test, y_test_prediction, average="micro")

    # Emit metrics
    sys.stdout.write(f"Train_accuracy={clf.score(X_train, y_train)};")
    sys.stdout.write(f"Test_accuracy={clf.score(X_test, y_test)};")
    sys.stdout.write(f"Train_f1={train_f1};")
    sys.stdout.write(f"Test_f1={test_f1};")

    # Save model to dir
    joblib.dump(clf, os.path.join(args.model_dir, "model.joblib"))


# Model function to load the model
def model_fn(model_dir):
    clf = joblib.load(os.path.join(model_dir, "model.joblib"))
    return clf