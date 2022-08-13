from CSVLoader import CSVLoader
from ProcessedData import ProcessedData


def main():

    csv_loader = CSVLoader(r'D:\Adam\manifest-ZkhPvrLo5216730872708713142\CBIS-DDSM\\')
    csv_loader.loadCSV(r'C:\Users\Admin\PycharmProjects\Model\mass_case_description_test_set.csv')
    csv_loader.loadCSV(r'C:\Users\Admin\PycharmProjects\Model\mass_case_description_train_set.csv')
    csv_loader.loadCSV(r'C:\Users\Admin\PycharmProjects\Model\calc_case_description_train_set.csv')
    csv_loader.loadCSV(r'C:\Users\Admin\PycharmProjects\Model\calc_case_description_test_set.csv')

    data_processor = ProcessedData(r'calc_case_description_test_set_for_training.csv', verbose=True)

if __name__ == '__main__':
    main()

