from CSVLoader import CSVLoader

def main():
    csv_loader = CSVLoader()
    csv_loader.loadCSV(r'C:\Users\Admin\PycharmProjects\Model\mass_case_description_test_set.csv')
    csv_loader.loadCSV(r'C:\Users\Admin\PycharmProjects\Model\mass_case_description_train_set.csv')
    csv_loader.loadCSV(r'C:\Users\Admin\PycharmProjects\Model\calc_case_description_train_set.csv')
    csv_loader.loadCSV(r'C:\Users\Admin\PycharmProjects\Model\calc_case_description_test_set.csv')

if __name__ == '__main__':
    main()

