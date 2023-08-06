
import pandas as pd
import json
import os
import pkg_resources

# df = pd.read_csv("E:\\Inde_Abbre\\List_of_Abbrevations_Main.csv")


# # you can simply use the dataframe (df) to read the columns and covert them as a dict and save it as a jSON file
# # below is the part
# abb_dict = {}
# for i, j in df.iterrows():
#     abb_dict[j['Unnamed: 0']] = j['List of Abbreviations ']

# now save your dict to JSON
# with open("output_2.json", 'w') as fp:
#     json.dump(abb_dict, fp)

# now sload the same json as use it

try:
    
    def Abbreviation(arr):
        """The passing argument should be given in string characters within quotes
        Abbreviation: "lic"
        will give an output of list Life Insurance of corporation
        """
        # package_dir = os.path.dirname(os.path.abspath('Inde_Abbre\\'))
        # file_path = os.path.join(package_dir, "output_2.json")
        file_path = pkg_resources.resource_filename(__name__, 'output_2.json')
        with open(file_path) as jfile:
            loaded_dict = json.load(jfile)
            arr1=arr.lower().strip()
            emty_list=[]
            for i,j in loaded_dict.items():
                if i==arr1:
                    emty_list.append(j)
                    print(emty_list)
                    break
            else:
                print(" The data is not available")
                
except Exception as e:
    print(e)




