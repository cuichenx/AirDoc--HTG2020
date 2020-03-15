import pandas as pd
import numpy as np


def shorten_name(long_name):
	if type(long_name) != str:
		print(long_name)
		raise Exception
	if '^' in long_name:
		# e.g. UMLS:C0011570_depression mental^UMLS:C0011581_depressive disorder -> depression mental/depressive disorder
		return '/'.join([x.split('_')[1] for x in long_name.split('^')])  
	else:
		# e.g. UMLS:C0011847_diabetes -> diabetes
		return long_name.split('_')[1]



df = pd.read_csv(R".\in\disease-symptom.csv")
diseases = [shorten_name(x) for x in df[df['Disease'].notnull()]['Disease'].to_numpy()] + ['TOTAL'] # 134 diseases -> rows (samples)


symptoms = [shorten_name(x) for x in df[df['Symptom'].notnull()]['Symptom'].unique()]  # 402 symptoms -> columns (features)

	


# num_diseases = sum(df['Disease'].notnull())
# num_symptoms = len(df['Symptom'].unique())

df_data = pd.DataFrame(np.zeros((len(diseases), len(symptoms))), index=diseases, columns=symptoms)

cur_disease = None
for i, row in df.iterrows():
    if pd.isnull(row['Symptom']):
        continue

    if not pd.isnull(row['Disease']):
        cur_disease = shorten_name(row['Disease'])

    df_data.loc[cur_disease, shorten_name(row['Symptom'])] = 1

df_data.loc["TOTAL"] = df_data.sum(numeric_only=True, axis=0)
symptoms.sort(key=lambda x: df_data.loc['TOTAL', x], reverse=True)
df_data.to_csv(R".\in\disease-symptom_preprocessed2.csv", columns=symptoms)  # display most common symptom first

