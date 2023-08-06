# import random
# import time as T
# import requests
# import json
# import numpy as np
# import warnings
# import re
# import pandas as pd
# import urllib.request
# import math as m
# import matplotlib.pyplot as plt
# import numpy as np
# from time import sleep
# from tqdm import tqdm
# import time
# from typing import List, Tuple
# from sqlalchemy import create_engine,inspect
# import pandas as pd
# pd.options.display.max_rows = 10000
# pd.options.display.max_columns = 10000
# import matplotlib.pyplot as plt
# import numpy as np 
# import seaborn as sns
# import math 
# import difflib
# from fuzzywuzzy import fuzz
# import logging
    
# import bisect

# warnings.filterwarnings('ignore')
import pandas as pd
import re
import warnings
import math 
from fuzzywuzzy import fuzz
import difflib

warnings.filterwarnings('ignore')

class DataProcessor:
    @staticmethod
    def clean_column_values(data_frame, column):
        data_frame[column] = data_frame[column].str.strip().str.lower().fillna('Nan')

    @staticmethod
    def get_unique_values(data_frame, column):
        column_values = list(data_frame[column])
        unique_values = set(column_values)
        return unique_values

    
    @staticmethod
    def convert_column_to_list(data_frame, column):
        column_values = list(data_frame[column])
        return column_values
    
    def covert_list_lower_case(original_list):
        
        lowercase_list = [item.lower() for item in original_list]

        return lowercase_list

    @staticmethod
    def get_unique_from_lists(original_list):
        unique_values = set(original_list)
        return unique_values
    
    
    
    def convert_to_DF(list_input,columns):
        return (pd.DataFrame(list_input,columns=columns))
    
    def covert_list_strip_case(original_list):
        
        lowercase_list = [item.strip() for item in original_list]

        return lowercase_list
    
    def fill_nan(original_list):
        
        my_list = list(map(lambda x: 'nan' if isinstance(x, float) and math.isnan(x) else x, original_list))

        return my_list    
    
    def split(original_list):
        separators = set()

        # Detecting separators
        for item in original_list:
            for char in item:
                if not char.isalnum():
                    separators.add(char)

        detected_separators = list(separators)

        # Selecting separator
        selected_separator = None
        if detected_separators:
            print("Detected separators:", detected_separators)
            random_number = random.randint(0, len(original_list))

            sample = original_list[random_number]
            print("Sample:", sample)
            selected_separator = input("Enter the desired separator: ")

        # Splitting using selected separator
        my_list = [item.split(selected_separator) if selected_separator else [item] for item in original_list]

        return my_list

    def replacer(original_list):
        separators = set()

        # Detecting separators
        for item in original_list:
            for char in item:
                if not char.isalnum():
                    separators.add(char)

        detected_separators = list(separators)

        # Selecting separator for replacement
        selected_separator = None
        if detected_separators:
            print("Detected separators:", detected_separators)
            random_number = random.randint(0, len(original_list))
            sample = original_list[random_number]
            print("Sample==>", sample)
            selected_separator = input("Enter the separator to replace: ")

        # Replacing selected separator
        replaced_list = []
        if selected_separator:
            replace_char = input("Enter the replacement character: ")
            for item in original_list:
                replaced_item = item.replace(selected_separator, replace_char)
                replaced_list.append(replaced_item)
        else:
            replaced_list = original_list

        return replaced_list

    

    def extract_External_ID_from_URL(url):
        parts = url.split('/')
        return parts[4]


    def filter_data_by_pattern(dataframe, company_column_name, testing_companies):
        index = []

        for i in range(len(dataframe)):
            for testing in testing_companies:
                pattern = testing.lower() + r'\d+'
                finder = re.findall(pattern, dataframe[company_column_name].iloc[i].lower().strip())

                if len(finder) > 0:
                    index.append(i)

        filtered_data = dataframe.drop(index)
        filtered_data = filtered_data.reset_index(drop=True)

        return filtered_data


    
class Getting_Details_from_table:
    
    @staticmethod
    def find_matching_data(data_frame, subset, base_column, selected_columns):
        Final_data = []
#         data_dict = {row[base_column]: [row[column] for column in selected_columns] for row in data_frame.to_dict('records')}
#         data_dict = {row[base_column]: [row[column].lower().strip() for column in selected_columns] for row in data_frame.to_dict('records')}
        data_dict = {row[base_column].lower().strip(): [str(row[column]).lower().strip() for column in selected_columns] for row in data_frame.to_dict('records')}
        for item in subset:
            if item in data_dict:
                matched_item = data_dict[item]
                Final_data.append(matched_item)

        Final_data_DF = pd.DataFrame(Final_data, columns=selected_columns)
        return Final_data_DF


class MyAlert(Exception):
    pass

class ExistenceChecker:
    
    def union_method(first_set,second_set):
        return list(first_set - second_set)
    
    
    def intersection_method(first_set,second_set):
        return list(first_set & second_set)   

    def convert_from_list_to_DF(list_data,columns_names):
        return pd.DataFrame(list_data,columns=columns_names)
    
    def intersection(first_data_frame, second_dataframe, column_1, column_2, out_column):
        
        
        first_set =DataProcessor.get_unique_from_lists(DataProcessor.covert_list_strip_case(DataProcessor.covert_list_lower_case((DataProcessor.fill_nan(DataProcessor.convert_column_to_list (first_data_frame,column_1))))))
        second_set = DataProcessor.get_unique_from_lists(DataProcessor.covert_list_strip_case(DataProcessor.covert_list_lower_case((DataProcessor.fill_nan(DataProcessor.convert_column_to_list (second_dataframe,column_2))))))

        in_First_not_Second_second_method_unique    = ExistenceChecker.union_method(first_set,second_set)
        in_First_and_in_Second_second_method_unique = ExistenceChecker.intersection_method(first_set,second_set)

        return (pd.DataFrame({out_column: in_First_not_Second_second_method_unique}),
                pd.DataFrame({out_column: in_First_and_in_Second_second_method_unique}))


    
    

class DataFrameExtractor:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.extracted_data = {}

    def extract_duplicate_records(self, column):
        return self.dataframe[self.dataframe.duplicated(subset=column)].copy()

    def extract_null_records(self, column):
        return self.dataframe[self.dataframe[column].isnull()].copy()

    def extract_multiple_value_records(self, column):
        return self.dataframe[self.dataframe[column].apply(type) == list].copy()

    def extract_data_from_dataframe(self):
        for column in self.dataframe.columns:
            column_data = self.dataframe[column]
            column_name = column

            duplicate_records = self.extract_duplicate_records(column)
            null_records = self.extract_null_records(column)
            multiple_value_records = self.extract_multiple_value_records(column)

            self.extracted_data[f'Duplicate_{column_name}'] = duplicate_records
            self.extracted_data[f'Null_{column_name}'] = null_records
            self.extracted_data[f'Multiple_Values_{column_name}'] = multiple_value_records

        return self.extracted_data



# # Usage:
# df = pd.DataFrame(...)  # Provide your dataframe here
# extractor = DataExtractor(df)
# extracted_data = extractor.extract_data_from_dataframe()
    


class JaccardSimilarityCalculator:
    
    @staticmethod
    def jaccard_similarity(a, b):
        a = set(a.split())
        b = set(b.split())
        intersection = a.intersection(b)
        union = a.union(b)
        return len(intersection) / len(union)    

    @staticmethod
    def find_matches_difflib(str1, str2, TH=0.60):
        match = difflib.get_close_matches(str1, [str2], n=1, cutoff=TH)
        if match:
            return True
        else:
            return False

    @staticmethod
    def find_matches_fuzz_token_set_ratio(str1, str2, TH=80):
        score = fuzz.token_set_ratio(str1, str2)
        if score >= TH:
            return True
        else:
            return False
    
    @staticmethod
    def name_similarity(list_1, list_2):
        in_First_and_in_Second = []
        in_First_not_Second = []

        preprocessed_list_1 = DataProcessor.covert_list_lower_case(DataProcessor.covert_list_strip_case(DataProcessor.fill_nan(list_1)))
        preprocessed_list_2 = DataProcessor.covert_list_lower_case(DataProcessor.covert_list_strip_case(DataProcessor.fill_nan(list_2)))

        set_list_2 = set(preprocessed_list_2)  # Convert list_2 to a set for faster membership testing

        for item in preprocessed_list_1:
            for other_item in set_list_2:
                similarity = JaccardSimilarityCalculator.jaccard_similarity(item, other_item)
                fuzz_sim = JaccardSimilarityCalculator.find_matches_fuzz_token_set_ratio(item, other_item)
                difflib_sim = JaccardSimilarityCalculator.find_matches_difflib(item, other_item)

                if similarity > 0.99 or fuzz_sim or difflib_sim:
                    in_First_and_in_Second.append(item)
                    break  # Found a match, no need to continue iterating over list_2

            if item not in in_First_and_in_Second:
                in_First_not_Second.append(item)

        return (in_First_and_in_Second, in_First_not_Second)
    
class Fast_stats:
    def Group_by_column(dataframe,column_name):
        return dataframe.groupby(column_name).size().reset_index(name='count')

class Miss_match:
            
    
    def Role_missmatch(first_data_frame,column_role_1,second_data_frame,column_role_2,):
        
        list_1=DataProcessor.split(DataProcessor.replacer(DataProcessor.covert_list_lower_case(DataProcessor.covert_list_strip_case(DataProcessor.fill_nan(first_data_frame,column_role_1)))))
        list_2=DataProcessor.split(DataProcessor.replacer(DataProcessor.covert_list_lower_case(DataProcessor.covert_list_strip_case(DataProcessor.fill_nan(second_data_frame,column_role_2)))))
    
    
    def intersection(first_data_frame, second_dataframe, column_1, column_2, out_column):
        
        
        first_set =DataProcessor.get_unique_from_lists(DataProcessor.covert_list_strip_case(DataProcessor.covert_list_lower_case((DataProcessor.fill_nan(DataProcessor.convert_column_to_list (first_data_frame,column_1))))))
        second_set = DataProcessor.get_unique_from_lists(DataProcessor.covert_list_strip_case(DataProcessor.covert_list_lower_case((DataProcessor.fill_nan(DataProcessor.convert_column_to_list (second_dataframe,column_2))))))

        in_First_not_Second_second_method_unique    = ExistenceChecker.union_method(first_set,second_set)
        in_First_and_in_Second_second_method_unique = ExistenceChecker.intersection_method(first_set,second_set)

        return (pd.DataFrame({out_column: in_First_not_Second_second_method_unique}),
                pd.DataFrame({out_column: in_First_and_in_Second_second_method_unique}))

 
        
class Exists_NonExists:
    def Smart_Finder(first_data_frame, second_dataframe, column_Email_1, column_Email_2, column_ID_1, column_ID_2,
                     column_category_1, column_category_2, out_Email, out_ID,column_Name_1='Name_1',column_Name_2='Name_2', Integration_category='visitors_integration',
                     selected_columns = ['Email', 'Visitor_Code','Company'],ID_comparison='ID_Email'): 

        in_First_not_Second_ID_details=[]
        in_First_and_in_Second_ID_details=[]
        ID_match_Email_match=[]
        ID_match_Email_miss_match=[]
        in_First_not_Second_Email_details=[]
        in_First_and_in_Second_Email_details=[]
        in_first_and_in_second_Name=[]
        in_first_not_second_Name=[]

        if (Integration_category == 'visitors_integration' or Integration_category == 'Exhibitor_integration') and ID_comparison == 'ID_Email':


            in_first_not_in_second_ID, in_first_and_in_second_ID = ExistenceChecker.intersection(first_data_frame, second_dataframe,
                                                                                column_ID_1, column_ID_2, out_ID)

            in_First_not_Second_ID_details = Getting_Details_from_table.find_matching_data(first_data_frame,
                                                                              list(in_first_not_in_second_ID[out_ID]),
                                                                              column_ID_1, selected_columns)
            in_First_and_in_Second_ID_details = Getting_Details_from_table.find_matching_data(first_data_frame,
                                                                                 list(in_first_and_in_second_ID[out_ID]),
                                                                                 column_ID_1, selected_columns)



            in_First_not_Second_Email, in_First_and_in_Second_Email = ExistenceChecker.intersection(in_First_and_in_Second_ID_details,
                                                                                   second_dataframe, column_Email_1,
                                                                                   column_Email_2, out_Email)



            ID_match_Email_miss_match = Getting_Details_from_table.find_matching_data(first_data_frame,
                                                                         list(in_First_not_Second_Email[out_Email]),
                                                                         column_Email_1, selected_columns)
            ID_match_Email_match      = Getting_Details_from_table.find_matching_data(first_data_frame,
                                                                    list(in_First_and_in_Second_Email[out_Email]),
                                                                    column_Email_1, selected_columns)

    #         return in_First_not_Second_ID_details, in_First_and_in_Second_ID_details, ID_match_Email_match, ID_match_Email_miss_match
            return in_First_not_Second_ID_details, in_First_and_in_Second_ID_details, ID_match_Email_match, ID_match_Email_miss_match,in_First_not_Second_Email_details,in_First_and_in_Second_Email_details,in_first_and_in_second_Name,in_first_not_second_Name

        elif (Integration_category == 'visitors_integration' or Integration_category == 'Exhibitor_integration') and ID_comparison == 'ID':


            in_first_not_in_second_ID, in_first_and_in_second_ID = ExistenceChecker.intersection(first_data_frame, second_dataframe,
                                                                                column_ID_1, column_ID_2, out_ID)


            in_First_not_Second_ID_details = Getting_Details_from_table.find_matching_data(first_data_frame,
                                                                              list(in_first_not_in_second_ID[out_ID]),
                                                                             column_ID_1, selected_columns)

            in_First_and_in_Second_ID_details = Getting_Details_from_table.find_matching_data(first_data_frame,
                                                                                 list(in_first_and_in_second_ID[out_ID]),
                                                                                 column_ID_1, selected_columns)

    #         return in_First_not_Second_ID_details, in_First_and_in_Second_ID_details
            return in_First_not_Second_ID_details, in_First_and_in_Second_ID_details, ID_match_Email_match, ID_match_Email_miss_match,in_First_not_Second_Email_details,in_First_and_in_Second_Email_details,in_first_and_in_second_Name,in_first_not_second_Name

        elif (Integration_category == 'visitors_integration' or Integration_category == 'Exhibitor_integration') and ID_comparison == 'Email':


            in_first_not_in_second_Email, in_first_and_in_second_Email = ExistenceChecker.intersection(first_data_frame, second_dataframe,
                                                                                      column_Email_1, column_Email_2,
                                                                                      out_Email)



            in_First_not_Second_Email_details = Getting_Details_from_table.find_matching_data(first_data_frame,
                                                                                 list(in_first_not_in_second_Email[
                                                                                          out_Email]),
                                                                                 column_Email_1, selected_columns)

            in_First_and_in_Second_Email_details = Getting_Details_from_table.find_matching_data(first_data_frame,
                                                                                    list(in_first_and_in_second_Email[
                                                                                             out_Email]),
                                                                                    column_Email_1, selected_columns)

    #         return in_First_not_Second_Email_details, in_First_and_in_Second_Email_details

            return in_First_not_Second_ID_details, in_First_and_in_Second_ID_details, ID_match_Email_match, ID_match_Email_miss_match,in_First_not_Second_Email_details,in_First_and_in_Second_Email_details,in_first_and_in_second_Name,in_first_not_second_Name

        elif (Integration_category == 'visitors_integration' or Integration_category == 'Exhibitor_integration') and ID_comparison == 'Name':


    #         raise MyAlert("This method will take longer time.")


            list_1=DataProcessor.convert_column_to_list(first_data_frame,column_Name_1)

            list_2=DataProcessor.convert_column_to_list(second_dataframe,column_Name_2)



            in_first_and_in_second_Name, in_first_not_second_Name = JaccardSimilarityCalculator.name_similarity(list_1, list_2)

            in_First_not_in_Second_Name_details = Getting_Details_from_table.find_matching_data(first_data_frame,in_first_not_second_Name,
                                                                                     column_Name_1, selected_columns)


    #         return (in_first_and_in_second,in_first_not_second)
            return in_First_not_Second_ID_details, in_First_and_in_Second_ID_details, ID_match_Email_match, ID_match_Email_miss_match,in_First_not_Second_Email_details,in_First_and_in_Second_Email_details,in_first_and_in_second_Name,in_First_not_in_Second_Name_details

    

class DataFrameExtractor:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.extracted_data = {}

    def extract_duplicate_records(self, column):
        duplicate_records = self.dataframe[self.dataframe.duplicated(subset=column)].copy()
        return duplicate_records

    def extract_null_records(self, column):
        null_records = self.dataframe[self.dataframe[column].isnull()].copy()
        return null_records

    def extract_multiple_value_records(self, column):
        multiple_value_records = self.dataframe[self.dataframe[column].apply(type) == list].copy()
        return multiple_value_records

    def extract_data_from_dataframe(self):
        for col in self.dataframe.columns:
            col_data = self.dataframe[col]
            col_name = col

            duplicate_records = self.extract_duplicate_records(col)
            null_records = self.extract_null_records(col)
            multiple_value_records = self.extract_multiple_value_records(col)

            self.extracted_data[f'Duplicate_{col_name}'] = duplicate_records
            self.extracted_data[f'Null_{col_name}'] = null_records
            self.extracted_data[f'Multiple_Values_{col_name}'] = multiple_value_records

        return self.extracted_data

    
    
    

class RegistrationTypeComparator:
    def __init__(self, dataframe, form_column, registration_type_column, exhibitor_roles_types,
                 exhibitor_forms, non_exhibitors_forms):
        self.dataframe = dataframe
        self.form_column = form_column
        self.registration_type_column = registration_type_column
        self.exhibitor_roles_types = exhibitor_roles_types
        self.exhibitor_forms = exhibitor_forms
        self.non_exhibitors_forms = non_exhibitors_forms

    def get_non_exhibitors(self):
        non_exhibitors = self.dataframe[~self.dataframe[self.registration_type_column].isin(self.exhibitor_roles_types)]
        return non_exhibitors

    def get_exhibitors(self):
        exhibitors = self.dataframe[self.dataframe[self.registration_type_column].isin(self.exhibitor_roles_types)]
        return exhibitors

    def get_wrong_exhibitor_registration(self):
        exhibitors = self.get_exhibitors()
        wrong_exhibitor_registration = exhibitors[exhibitors[self.form_column].isin(self.non_exhibitors_forms)]
        return wrong_exhibitor_registration

    def get_wrong_non_exhibitor_registration(self):
        non_exhibitors = self.get_non_exhibitors()
        wrong_non_exhibitor_registration = non_exhibitors[non_exhibitors[self.form_column].isin(self.exhibitor_forms)]
        return wrong_non_exhibitor_registration

    def get_wrong_exhibitor_registration_stats(self):
        wrong_exhibitor_registration = self.get_wrong_exhibitor_registration()
        stats = wrong_exhibitor_registration.groupby([self.registration_type_column, self.form_column]) \
            .size().reset_index(name='count')
        return stats

    def get_wrong_non_exhibitor_registration_stats(self):
        wrong_non_exhibitor_registration = self.get_wrong_non_exhibitor_registration()
        stats = wrong_non_exhibitor_registration.groupby([self.registration_type_column, self.form_column]) \
            .size().reset_index(name='count')
        return stats