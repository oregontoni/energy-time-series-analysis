# OVERVIEW 

## **UK National Energy Forecast**

Welcome to my kernel on time series forecasting to predict the UK's electricity generation capacity and energy mix in 2050 (ie, the year the UK is legally bound to have reached NetZero). 

This README file provides an overview and documentation for the datasets and Jupyter notebooks included in my capstone project on forecasting the UK's energy mix in 2050.

I will use historic electricity generation data from the <a href="Historic GB Generation Mix">UK National Grid ESO.</a>

(downloadable .csv available <a href="https://drive.google.com/file/d/1RkhiAB5u1XZzH3hCuNIjpY5-MmQtTod9/view?usp=drive_link">here</a>, with data dictionary for reference <a href="https://github.com/brainstation-datascience/capstone-oregontoni/blob/main/generation_dataset_glossary.ipynb">here</a> )


**Contents**
1. Data cleaning and initial EDA notebook
2. Advanced EDA notebook
3. Modelling notebook
4. requirements.yml
5. Dataset glossary


**1. Data cleaning and initial EDA notebook**
File Name: 1_Toni_Chan_capstone_generation_cleaning_eda.ipynb

Description: This notebook contains exploratoy data analysis (EDA) of 15 years' of electricity generation data from the UK National Grid ESO. It aims to provide insights into existing trends in energy consumption, with energy generation being a reflection of energy demand. Generation data is recorded every half hour across various renewable and non-renewable energy sources, as well as imports and energy storage.

Data Source: The analysis is based on publicly available data from the UK National Grid ESO. A Dataset glossary is also available for reference.

EDA initial findings: 
- The generation dataset shows half-hourly updates on electricity generation from 01 Jan 2009 to 27 Feb 2024.

- The generation dataset was quite clean, with no NULL values and only 8 rows of duplicate values. The only non-numerical column was the DATETIME column, which was changed to a datetime datatype.

- To make time series forecasting easier, Generation by Year, Month, Week, and Day columns were added.

- Wind energy composes the largest portion of renewable energy generation. Similarly, Gas is the largest portion of fossil fuel energy generation. This is contrasted by the sharp decline in Coal energy generation during the UK's transition away from an almost 100% reliance on fossil fuels in 2009.

- Battery storage is likely a vital component of the UK's path to net zero. However, the National Grid's recent efforts to fast-track growth of battery storage capacity while resolving the system's ability to use stored energy in its Balancing Mechanism are not reflected in historical data, and manual adjustments may need to be made post-initial modelling. 

- Total energy generation has shown a downward trend from 2009 to 2024. This is a mixed reflection of the UK's move away from fossil fuels against the steady growth of energy generation from renewable sources. There is also the added complexity of geopolitical effects on energy price volatility/rising cost of living resulting in dampening overall energy use. This will need to be balanced in the model forecasting against the UK's projected 11% growth in national population by and the subsequent increase in energy demand.

- Immediate next steps include advanced EDA, with preliminary modelling/forecasting to follow.


**2. Advanced EDA notebook**
File Name: 2_ Toni_Chan_capstone_advEDA_initial_modelling.ipynb

Description: This notebook is a continuation of the EDA in the first notebook outlining trends seen in the dataset, and includes results of a linear regression model.

Data Source: The .csv file following the data cleaning in the first EDA notebook

Advanced EDA findings and initial modelling results:
- Creating the monthly dataframe extract has helped remove some of the "noise" from the data during advanced EDA and modelling.

- Advanced EDA showed clear seasonality (eg, peak energy generation in winter months, and lower energy generation in summer months). Peak energy generation occurs in January, with August exhibiting the lowest energy usage per year.

- Overall, there is a clear downward trend in historical energy generation.

- The initial linear regression model showed an accuracy score of ~70%. While this leaves room for improvement, the closeness of the Train and Test accuracy scores indicates the model generalises well to unseen data.

- The .diff(), ACF, and PACF plots in Advanced EDA have helped us select hyperparameters for additional modelling.

- By exploring other models for increased accuracy (eg, SARIMA/SARIMAx and XGboost), we can finalise a model to expand the forecasting to other individual energy sources from the dataset. While it is good to model the future total energy generation in 2050, forecasting generation on a granular level (by individual energy source) may provide more useful insights for use by UK policy and decision makers with regards to opportunities and challenges during the energy transition, and  better reflect growth of renewable energy use without trends being skewed by the transition away from fossil fuels (and subsequent decline in energy generation).

**3. Modelling notebook**
File Name: 3_Toni_Chan_capstone_iterative_modelling.ipynb

Data Sources: The .csv file following the data cleaning in the first EDA notebook; UK population figures from OECD

Description: This notebook continues the initial modelling performed at the end of the Advanced EDA notebook, extending to use of XGBoost, SARIMA, and SARIMAX mdoels. 

Iterative modelling results and findings:
- XGBoost, while a better-performing model on the surface, has limitations for time series analysis, including requiring feature engineering to account for temporal dynamics, lacking the ability to account for exogenous factors, and greater risk of compounding errors when forecasting values. For these reasons, the SARIMA/SARIMAX model was chosen to predict future energy generation values to 2049.

- although it requires more effort, fitting the SARIMA model manually allows for optimising based on strength of predictors in the model, rather than using GridSearchCV and focusing on lowest AIC score (ie, there is not a direct connection between lowest AIC score and lower p-values).

- while the SARIMA model performed well on predicting overall energy generation, it had difficulty capturing the volatility of Wind values in the Test set. However, this could mean the model is more reliable in predicting stable, long-term generation values

- model reliability becomes weakther the farther into the future the values are predicted. During modelling of total energy generation, the models showed limitations due to existing trends in the data (ie, predicted values in 2049 equated to negative energy generation). One way of counterbalancing this is to model multiple  columns in the dataset (ie, modelling individual energy sources), to incorporate multiple trends and seasonality patterns into forecasted values

- based on the results of the predicted values for Wind generation, there is the potential for the UK to fulfill its energy demand needs via renewable energy sources and achieve net zero by 2050

- forecasting total energy generation for the UK (or any country) is a hugely complex, gargantuan task. These notebooks are single person's attempt to replicate some of the many year's of work completed by  thousands of experts carried on throughout the UK. It is a vast and fascinating topic worth many more hours of additional work and exploration.


**Usage Guidelines**
- Ensure that you have Jupyter Notebook or JupyterLab installed to open .ipynb files.
- CSV data can be viewed and manipulated using standard data analysis tools such as pandas in Python.
- Instructions are included in the .yml file to download the required libraries


**BACKGROUND**

**UK Net Zero 2050:**

In 2019, the UK became the first country in the world to legally bind itself to a Net Zero target. By 2050, the UK would no longer add more greenhouse gases to the atmosphere than it removes.

At the end of 2023, fossil fuels made up one-third of the UK's energy mix. How will that proportion change as the UK moves toward NetZero? What is the UK's current generation capacity, and how much can/should each of the renewable energy sources grow in order to help the UK achieve NetZero?


**The Data Science solution:**

Statistical modelling and historical data can be used to predict future energy output. National Grid ESO has a dashboard showing the UK’s historic energy generation. Energy generated is an inherent reflection of energy demand. 

<a href="https://www.bbc.co.uk/bitesize/guides/z3qd7p3/revision/11">As noted by the BBC</a>, the demand for electricity in the UK varies throughout the day. When the demand for electricity is greater than the base load (ie, the minimum amount of energy needed to be supplied to the grid at any given point in time), the National Grid reacts by providing additional electricity. National Grid ESO data for both generation and demand is recorded in half-hour increments.

As such, it makes sense to use only one of the datasets, as both contain records with the same time increments (ie, if there is a change in demand, it should be reflected in the subsequent row of generation data). We will use the energy generation dataset as a reflection of energy use in the UK.

Forecasting models can map current energy production capacities and extrapolate to the future energy production capacities required in 2050 and help determine the manufacturing capabilities required to fulfil that demand. Through feature engineering, time series modelling, and data visualisation, the half-hour increments of data can be aggregated and summarised into actionable insights (eg, taking the current annual production of wind energy, forecasting the total estimated wind energy production in 2050, and using that number to calculate total required windfarm construction requirements over the next three decades).

Ultimately, these insights could become the tools for policy makers to make decisions on how the UK can fulfil its Net Zero obligations. 


**The Dataset:**

The UK National Grid ESO's historic generation dataset includes half-hourly historical updates on electricity generation from 01 Jan 2009 00:00:00 to 27 Feb 2024 11:00:00. This equates to more than a quarter million rows (265,703 to be exact) of data on which to run predictive models. The dataset includes the total number of megawatts of energy generated, as well as the generation breakdown across various energy sources (eg, gas, coal, nuclear, wind, solar, biomass, etc) and each energy sources' percent of the total. 


**What is the potential impact, and who are the beneficiaries?**

Who are the parties most vested in understanding the UK's future energy mix?

  - **The UK government and policy makers:**
  Having a reliably modelled energy generation forecast could help the UK government ie, policy makers, be better-informed when making decisions on where investments should be made for growing energy generation capacity. The energy generation forecast could also impact foreign affairs, depending on the UK's future need for energy imports. Additionally, since renewable energy sources are largely stationary (eg, hydro power plants, windmills, etc.) and the energy produced is mostly used locally rather than stored or transported, the future "onshoring" of a larger portion of the UK's energy mix could potentially lessen the impact of geopolitical events and energy market volatility. Moreover, as the UK's current infrastructure was designed for use of fossil fuels (eg, transportable energy), having a forecasted energy generation mix that reflects future renewable energy generation needs can help the UK government can better understand the associated costs with changes to infrastructure.

  - **Energy Producers:**
  Change in policy could provide additional growth opportunities for energy producers. Those opportunities could also mean changes in infrastructure required for growth, as well as incenstives or subsidies to promote energy generation capacity growth.
  
  - **Consumers/Citizens:**
  Energy is one of the backbones of society, and thus everyone in the UK will be affected by changes in the UK’s energy       mix. Large consumers such as heavy industry and ocean shipping will be affected, as they rely on a certain level of energy power (eg, steelmaking) and mobility that can be more difficult to achieve with renewable energy sources. Household consumers will also be affected by potential changes in pricing and energy availability. 


In summary, an energy generation forecast could help inform key players (ie, government decision makers) where and whether more investment is needed in various renewable energy sectors. This could lead to additional subsidies and power purchase agreements as needed, growth opportunities for renewable energy producers, and, ultimately, contribute to greater market stability for consumers and UK citizens.
