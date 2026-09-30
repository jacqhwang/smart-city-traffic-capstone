Capstone Part 3: Machine Learning and AI

Smart City Traffic Intelligence: From Data Analytics to AI-Powered Mobility

Part 3 extends the traffic analysis and Python pipeline developed in Parts 1 and 2 into machine-learning and AI applications using the Metro Interstate Traffic Volume dataset. The dataset contains hourly westbound traffic observations for a section of I-94 in the Minneapolis–St Paul area.

This part covers supervised learning, unsupervised learning, deep learning and explainability, MLflow experiment tracking, a traffic recommendation system, deployment and monitoring simulation, and responsible and sustainable AI.

Task 1: Supervised Learning

Classification

Logistic Regression and Random Forest classification models were developed to predict a proxy accident-risk label.

Because the dataset does not contain actual accident records, the high-risk target was constructed using congestion and adverse weather conditions. This proxy should not be interpreted as actual accident probability.

Random Forest improved overall classification performance compared with Logistic Regression, particularly recall and ROC AUC. However, because weather information contributes to both the proxy target definition and the model predictors, the high classification performance may be affected by target leakage and should be interpreted cautiously.

Traffic Volume Regression

Linear Regression and Random Forest Regression models were developed to predict traffic volume.

Model

MAE

RMSE

R²

Linear Regression

812.7

1035.4

0.729

Random Forest Regression

225.4

378.8

0.964

Random Forest Regression achieved substantially lower prediction error and a higher R² than Linear Regression, indicating that the non-linear model better captured the relationships between traffic volume, time, weather and other engineered features.

Task 2: Unsupervised Learning

K-means clustering and association-rule mining were used to identify traffic patterns.

K-means identified interpretable groups based on combinations of time, weather severity and traffic volume.

Association-rule mining initially used a broad Night period of 00:00–05:59. Comparison with the hourly traffic patterns developed in Part 2 showed that weekday traffic begins increasing during the early morning. The time categories were therefore refined to separate:

Overnight: 00:00–03:59

Early Morning: 04:00–06:59

The refined analysis showed a particularly strong association between overnight travel and low congestion, while weekend early mornings also remained strongly associated with low traffic.

Task 3: Deep Learning and Explainability

A neural network was developed for traffic-volume prediction.

Model

MAE

RMSE

R²

Linear Regression

812.7

1035.4

0.729

Neural Network

343.8

510.6

0.934

Random Forest Regression

225.4

378.8

0.964

The Neural Network substantially outperformed the Linear Regression baseline, although Random Forest Regression achieved the strongest traffic-volume prediction performance.

SHAP was used for model explainability on a comparable regression model trained on the same traffic-volume prediction problem. The analysis showed that temporal features were the dominant predictors of traffic volume. Because variables such as hour, hour_sin and hour_cos represent related forms of the same underlying time information, their SHAP contributions should be interpreted collectively rather than as independent effects.

Task 4: MLflow Experiment Tracking

MLflow was used to provide structured experiment tracking for the traffic-volume models.

The experiment records include:

Model type and relevant parameters

MAE

RMSE

R²

Model versions

Experiment runs

Linear Regression, Random Forest Regression and the Neural Network were recorded and compared. Random Forest Regression was selected as version 1 (v1) for the deployment simulation based on its traffic-volume prediction performance.

A local SQLite database was used for MLflow tracking.

Task 5: Traffic Recommendation System

Because the dataset represents a single traffic corridor rather than a road network with alternative routes, the recommendation system focuses on travel timing rather than route selection.

A hybrid recommendation approach combines historical traffic patterns with predictions from the trained Random Forest Regression model.

Users can specify preferences including:

Day type

Day of week

Month

Earliest and latest travel start times

Rain

Snow

Low visibility

Holidays

The system evaluates matching historical observations and candidate travel times, then returns a recommended travel start time, predicted traffic volume, historical traffic information and alternative lower-traffic periods.

An interactive ipywidgets interface was also implemented. Because Jupyter widget state is session-dependent, interactive widgets may display a model not found message when the saved notebook is reopened in a different environment. Screenshots of the successfully tested interface and recommendation output are retained in the notebook.

Task 6: MLOps and Deployment Simulation

Model Versioning and Experiment Tracking

Model versions were documented for Linear Regression, Random Forest Regression and the Neural Network. MLflow records model parameters, metrics, experiment runs and version information.

Random Forest Regression v1 was selected for the deployment simulation.

Flask Deployment Mock-up

A Flask API mock-up was created with a /predict endpoint. The endpoint accepts input data, applies the trained Random Forest Regression model and returns a predicted traffic volume.

The API was tested using the Flask test client and successfully returned HTTP status code 200 together with a traffic-volume prediction.

Monitoring and Alerting

Prediction-error monitoring was simulated using RMSE.

Because no new post-deployment traffic data were available, a subset of the existing test data was used to demonstrate a normal monitoring scenario. The simulated monitoring RMSE was approximately 378.33 compared with the baseline RMSE of approximately 378.75, representing essentially no deterioration.

An artificial drift scenario was also created to demonstrate the alerting mechanism. A 20% increase in RMSE was used as the demonstration threshold:

PASS / Normal — RMSE increase is 20% or less

ALERT / Requires investigation — RMSE increase exceeds 20%

The artificial drift scenario increased RMSE by 30% and therefore triggered ALERT / Requires investigation.

The artificial scenario demonstrates the monitoring mechanism only and is not evidence of observed real-world model drift.

Task 7: Responsible and Sustainable AI

The responsible-AI assessment considers data coverage, proxy-label limitations, uneven model error, governance, human oversight and computational resources.

Important limitations include:

The dataset represents only westbound traffic on one section of I-94.

Temporal coverage is uneven, including partial coverage in 2012 and data-quality issues identified in 2014.

Some weather conditions contain relatively few observations.

The accident-risk target is a constructed proxy rather than an observed accident outcome.

Weather predictors overlap conceptually with variables used to construct the proxy risk label, creating potential target leakage.

Overall performance metrics may conceal poorer performance during uncommon traffic, weather or temporal conditions.

Models developed in this project should therefore be treated as decision-support tools rather than autonomous traffic-management or road-safety systems.

A real-world implementation would require current and representative data, independent validation, subgroup performance assessment, data-quality controls, model versioning, monitoring, human oversight and controlled retraining.

The modelling results also illustrate the importance of selecting complexity according to demonstrated value. In this project, Random Forest Regression achieved better traffic-volume prediction performance than the more computationally intensive Neural Network.

Feature Engineering

Part 3 reused and extended the data preparation developed in the earlier parts of the capstone. Engineered features include temporal variables, cyclical time encodings, weather variables and a holiday indicator.

The holiday indicator was refined so that all timestamps occurring on a holiday date are identified as holidays rather than only the single timestamp in the original dataset where the holiday name was recorded.

Key Outcome

The project demonstrates an end-to-end progression from traffic data analysis to machine-learning prediction and practical AI applications. Random Forest Regression provided the strongest traffic-volume prediction performance among the models compared and was subsequently used for the recommendation system and deployment simulation.

The project also demonstrates that predictive performance alone is insufficient for real-world mobility AI. Data coverage, proxy-target validity, explainability, experiment traceability, monitoring, governance, human oversight and resource use must also be considered.