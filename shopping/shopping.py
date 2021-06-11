import csv
import sys
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    label = []

    integerColumns  =   set()
    floatColumns    =   set()

    months = {"Jan":0, "Feb":1, "Mar":2, "Apr":3, "May":4, "June":5, "Jul":6, "Aug":7, "Sep":8, "Oct":9, "Nov":10, "Dec":11 }

    # To do: Después de crear el head, añadir los indexes de las columnas a los conjuntos de los diferentes tipos para luego poder discriminar

    # print(os.getcwd())
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:                                     # header line
                print(f'Column names are {", ".join(row)}')
                head = row

                for columnName in head:
                    i = head.index(columnName)
                    if i == head.index('Administrative') or i == head.index('Informational') or i == head.index('ProductRelated') or i == head.index('OperatingSystems') or i == head.index('Browser') or i == head.index('Region') or i == head.index('TrafficType'):
                        integerColumns.add(i)

                    if i == head.index('Administrative_Duration') or i == head.index('Informational_Duration') or i == head.index('ProductRelated_Duration') or i == head.index('BounceRates') or i == head.index('ExitRates') or i == head.index('PageValues') or i == head.index('SpecialDay'):
                        floatColumns.add(i)

                line_count += 1
            else:
                for data in row[0:-1]:
                    i = row.index(data)
                    if i == head.index('Month'):
                        row[i] = months[data]
                    
                    elif i == head.index('VisitorType'):
                        if data == 'Returning_Visitor':
                            row[i] = 1
                        else:
                            row[i] = 0

                    elif i == head.index('Weekend'):
                        if data.lower() == 'true':
                            row[i] = 1
                        else:
                            row[i] = 0

                    elif i in integerColumns:
                        row[ i ] = int( row[i] )

                    elif i in floatColumns:
                        row[ i ] = float( row[i] )

                evidence.append(row[0:-1])

                if row[-1].lower() == 'true':
                    row[-1] = 1
                else:
                    row[-1] = 0

                label.append(row[-1])
                
                line_count += 1
    return evidence, label#, head


    # raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors = 1)
    model.fit(evidence,labels)
    return model
    # raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    possitives = sum(labels)                    # 1 = possitive, 0 = negative
    negatives = len(labels) - possitives

    # correctlyPredicted = 0
    correctlyPredictedPossitives = 0
    # incorrectlyPredicted = 0
    correctlyPredictedNegatives = 0
    
    for i in range(len(labels)):
        if labels[i] == 1 and labels[i] == predictions[i]:
            correctlyPredictedPossitives  += 1
        if labels[i] == 0 and labels[i] == predictions[i]:
            correctlyPredictedNegatives += 1

    sensitivity = correctlyPredictedPossitives / possitives
    specificity = correctlyPredictedNegatives / negatives

    return sensitivity, specificity


    # raise NotImplementedError


if __name__ == "__main__":
    main()


############################ Testing #################
# Administrative,Administrative_Duration,Informational,Informational_Duration,ProductRelated,ProductRelated_Duration,BounceRates,ExitRates,PageValues,SpecialDay,Month,OperatingSystems,Browser,Region,TrafficType,VisitorType,Weekend,Revenue
# filename = 'shopping.csv'
# e,l,h = load_data(filename)
# e,l = load_data(filename)