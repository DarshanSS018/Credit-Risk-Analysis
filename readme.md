
# Credit Risk Analysis
## Predicting Loan Defaults: A Comprehensive Machine Learning Approach

---

## Overview
This project employs advanced machine learning techniques to analyze credit risk in loan applications. The primary objective is to predict the likelihood of an applicant defaulting on a loan, thus enabling financial institutions to make informed and data-driven decisions.

---

## Data
The dataset comprises a plethora of variables, as outlined below:

- **ID**: Unique identifier for each loan applicant.
- **Age**: Age of the loan applicant.
- **Income**: The applicant's income.
- **Home**: Home ownership status (Own, Mortgage, Rent).
- **Emp_Length**: Employment length in years.
- **Intent**: Purpose of the loan (e.g., education, home improvement).
- **Amount**: Amount of loan applied for.
- **Rate**: Interest rate associated with the loan.
- **Status**: Loan approval status (Fully Paid, Charged Off, Current). **This is our target variable.**
- **Percent_Income**: Loan amount as a percentage of the applicant's income.
- **Default**: Past loan default history (Yes, No).
- **Cred_Length**: Length of the applicant's credit history.

---

## Objectives

- To develop a predictive model with high accuracy for identifying potential loan defaults.
- To pinpoint key variables that have a significant impact on the risk of default.
- To aid financial institutions in mitigating risks and making data-driven decisions.

---

## Methodology

1. **Data Exploration and Cleaning**: Thorough scrutiny and cleaning of the data, including handling missing values and outliers.
2. **Feature Engineering**: Creation and selection of features that improve model performance.
3. **Exploratory Data Analysis (EDA)**: In-depth visualization of data distributions, correlations, and other patterns.
4. **Model Selection**: Comparative analysis of machine learning models such as Random Forest, Gradient Boosting, and KNN.
5. **Hyperparameter Tuning**: Fine-tuning of model parameters to enhance performance.
6. **Model Evaluation**: Utilization of metrics like accuracy, precision, recall, F1 score, and AUC-ROC for comprehensive performance evaluation.
7. **Deployment**: Steps and methodologies for deploying the model into a live, production environment.

---

## Tools Employed

- Python 3.10
- Pandas for data manipulation
- Scikit-learn for machine learning algorithms
- Matplotlib and Seaborn for data visualization
- PyCaret for automated machine learning (model verification)

---

## Key Performance Indicators

- **Test Accuracy**: 93.22
- **Precision**: 93.96
- **Recall**: 73.65
- **F1 Score**: 82.58
- **AUC-ROC**: 96.14

## Conclusion

### Summary of Findings

This Credit Risk Analysis model has exhibited compelling performance in predicting loan defaults. The model achieved an impressive accuracy rate of 93.22%, suggesting that it correctly identifies whether a loan will default or not most of the time. It also scored high in other key metrics:

Interpretation of Metrics:

Precision: At nearly 94%, the model is highly precise in predicting the positive class, meaning it has a low rate of false positives. This is crucial for a financial institution, as mislabeling a defaulting loan as non-defaulting could be quite costly.

Recall: At 73.65%, the model captures a reasonable percentage of all actual defaults. While not as high as we'd ideally prefer, this still implies that the model is useful in a real-world setting for identifying high-risk loans.

F1 Score: The balance between Precision and Recall is represented by the F1 Score of 82.58%, indicating a well-rounded model.

AUC-ROC: The AUC-ROC score, a comprehensive metric that considers both the true positive rate and the false positive rate, is exceptionally high at 96.14%, further confirming the model's quality.

### Implications for Stakeholders

The model's strong performance provides a robust tool for financial institutions to assess the risk of loan default. It can significantly aid in decision-making processes, allowing for more prudent loan approvals and risk assessment. The model not only promises to reduce the rate of loan defaults but also to increase the efficiency of the loan approval process.

### Recommendations for Future Work

While the model performs well on multiple fronts, there is always room for improvement.

Further feature engineering could refine the model, as could exploring ensemble methods or more complex algorithms.
A more extensive dataset, possibly with more features, could improve the model's predictive power.
Regular updates to the model should be considered to adapt to evolving financial landscapes.

### Final Thoughts

The results of this project are promising, offering a practical and reliable resource for identifying loan default risk. This model stands to benefit both financial institutions and consumers by fostering more informed and responsible lending practices.
