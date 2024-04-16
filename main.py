import pandas as pd
from tkinter import *
import joblib
from sklearn.ensemble import RandomForestClassifier
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from io import StringIO
vishwa_root = Tk()
vishwa_root.geometry("1000x600")
vishwa_root.minsize(1000,600)
#vishwa_root.maxsize(1000,600)
vishwa_root.title("VISHWA")

def predict():
   csv_data = """age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,target
       66,1,0,160,228,0,0,138,0,2.3,2,1
       63,1,3,145,233,1,0,150,0,2.3,0,1
       59,1,2,150,212,1,1,157,0,1.6,2,1
       57,1,0,110,201,0,1,126,1,1.5,1,1
       51,1,0,140,261,0,0,186,1,0,2,1
       50,1,2,129,196,0,1,163,0,0,2,1
       45,1,0,104,208,0,0,148,1,3,1,1
       35,1,1,122,192,0,1,174,0,0,2,1
       67,0,2,115,564,0,0,160,0,1.6,1,1
       67,0,0,106,223,0,1,142,0,0.3,2,1
       60,0,3,150,240,0,1,171,0,0.9,2,1
       56,0,1,140,294,0,0,153,0,1.3,1,1
       51,0,2,140,308,0,0,142,0,1.5,2,1
       50,0,0,110,254,0,0,159,0,0,2,1
       69,1,2,140,254,0,0,146,0,2,1,0
       66,0,0,178,228,1,1,165,1,1,1,0
       64,1,0,145,212,0,0,132,0,2,1,0
       50,1,2,140,233,0,1,163,0,0.6,1,0
       """
   data = pd.read_csv(StringIO(csv_data))
   data = data.drop_duplicates()

   # Categorize variables
   cate_val = []
   cont_val = []
   for column in data.columns:
       if data[column].nunique() <= 10:
           cate_val.append(column)
       else:
           cont_val.append(column)

   # Remove 'sex' and 'target' from categorical variables
   cate_val.remove('sex')
   cate_val.remove('target')

   # One-hot encode categorical variables
   data = pd.get_dummies(data, columns=cate_val, drop_first=True)

   # Standardize continuous variables
   from sklearn.preprocessing import StandardScaler
   st = StandardScaler()
   data[cont_val] = st.fit_transform(data[cont_val])

   # Split data into features (X) and target variable (y)
   X = data.drop('target', axis=1)
   y = data['target']

   # Train a RandomForestClassifier on the entire dataset
   rf_full = RandomForestClassifier()
   rf_full.fit(X, y)

   # Save the trained model
   joblib.dump(rf_full, 'model_joblib_heart')

   # Load the trained model
   loaded_model = joblib.load('model_joblib_heart')

   # GUI for predicting heart disease
   def show_entry_fields():
       p1 = int(e1.get())

       p3 = int(e3.get())
       p4 = int(e4.get())
       p5 = int(e5.get())
       p6 = int(e6.get())
       p7 = int(e7.get())
       p8 = int(e8.get())
       p9 = int(e9.get())
       p10 = float(e10.get())
       p11 = int(e11.get())

       p2 = gender_var.get()


       # Create a DataFrame from user inputs
       new_data = pd.DataFrame({
           'age': p1,
           'sex': p2,
           'cp': p3,
           'trestbps': p4,
           'chol': p5,
           'fbs': p6,
           'restecg': p7,
           'thalach': p8,
           'exang': p9,
           'oldpeak': p10,
           'slope': p11
       }, index=[0])

       # One-hot encode categorical variables
       new_data_encoded = pd.get_dummies(new_data, columns=cate_val, drop_first=True)

       # Ensure that the columns in new_data_encoded match the columns used during training
       missing_cols = set(X.columns) - set(new_data_encoded.columns)
       for col in missing_cols:
           new_data_encoded[col] = 0

       # Reorder columns to match the order during training
       new_data_encoded = new_data_encoded[X.columns]

       # Predict using the loaded model
       prediction = loaded_model.predict(new_data_encoded)

       if prediction[0] == 0:
           Label(master, text="No Heart Disease",font="comicsansms 20 bold").grid(row=31)
       else:
           Label(master, text="Possibility of Heart Disease",font="comicsansms 20 bold").grid(row=31)

   from tkinter import Tk, Label, font

   master = Tk()
   master.title("Heart Disease Prediction System")

   # Set background color for the entire GUI
   master.configure(bg="lightgray")

   # Stylish title label
   title_font = font.Font(family='Helvetica', size=16, weight='bold')
   Label(master, text="Heart Disease Prediction System", bg="black", fg="white", font=title_font).grid(row=0,
                                                                                                       columnspan=2,
                                                                                                       pady=10)

   # Styled labels with increased spacing
   label_font = font.Font(family='Helvetica', size=12, weight='bold')
   labels = [
       "Age", "Male Or Female ",
       "Chest Pain Type [0: Typical , 1: Atypical , 2: Non-Anginal Pain, 3: Asymptomatic]",
       "Blood Pressure [94 to 200]",
       "Cholesterol [126 to 564]",
       "Fasting Blood Sugar [1: > 120 mg/dl, 0: Normal]",
       "Resting ECG [0 : Normal, 1: ST-T wave abnormality, 2: ventricular abnormality]",
       "Max Heart Rate [71 to 202]",
       "Exercise Angina [0 :No, 1:Yes]",
       "ST Depression [0 to 7]",
       "Slope of ST Segment [0:Up, 1:Flat, 2:Down]"
   ]

   for row, label_text in enumerate(labels, start=1):
       Label(master, text=label_text, font=label_font, bg="lightgray").grid(row=row, sticky="w", padx=10, pady=5)

   e1 = Entry(master)

   e3 = Entry(master)
   e4 = Entry(master)
   e5 = Entry(master)
   e6 = Entry(master)
   e7 = Entry(master)
   e8 = Entry(master)
   e9 = Entry(master)
   e10 = Entry(master)
   e11 = Entry(master)


   e1.grid(row=1, column=1)

   e3.grid(row=3, column=1)
   e4.grid(row=4, column=1)
   e5.grid(row=5, column=1)
   e6.grid(row=6, column=1)
   e7.grid(row=7, column=1)
   e8.grid(row=8, column=1)
   e9.grid(row=9, column=1)
   e10.grid(row=10, column=1)
   e11.grid(row=11, column=1)

   gender_var = IntVar()
   gender_label = Label(master, text="Male or Female", font=label_font, bg="lightgray")
   gender_label.grid(row=2, sticky="w", padx=10, pady=5)

   male_checkbox = Radiobutton(master, text="M",font="comicsansms 10 bold",  variable=gender_var, value=0, bg="lightgray")
   male_checkbox.grid(row=2, column=1, sticky="w", padx=10, pady=5)

   female_checkbox = Radiobutton(master, text="F",font="comicsansms 10 bold", variable=gender_var, value=1, bg="lightgray")
   female_checkbox.grid(row=2, column=1, sticky="e", padx=10, pady=5)

   Button(master, text='Predict', command=show_entry_fields, fg='white', bg='blue',font=('Arial', 12, 'bold')).grid()

#text label
# font = ("comicsansms",20,"Bold")
plogo = Label(text="Heart Disease Detection Software",bg="red",fg="white",
             font="comicsansms 20 bold",padx= 5,pady=5,borderwidth =3 ,relief=SUNKEN)
plogo.pack()


# Button


f2= Frame(vishwa_root,borderwidth =20,bg="gray",relief= SUNKEN)
f2.pack(side= RIGHT,anchor="se")
b2 = Button(f2,fg="red", text="PREDICT",font="comicsansms 20 bold",command=predict)
b2.pack(side=LEFT,padx=20,pady=20)

vishwa_root.mainloop()