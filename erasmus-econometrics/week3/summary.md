# Econometrics Week 3 Test
All results are from the python library statsmodels. The code can be found [here](https://github.com/cheriot/data-analysis/blob/master/erasmus-econometrics/week3/test_exer_3.py).

#### (a)  Use general-to-specific to come to a model.  Start by regressing the federal funds rate on the other 7 variables and eliminate 1 variable at a time.
1. The highest p-value and lowest t statistic is for UNEMPL (t-value 1.059, p-value 0.290) so remove it from the model.
2. The highest p-value and lowest t statistic is now PROD (t-value -0.989, p-value 0.323) so remove it from the model.
3. Now everything is significant while the R^2, AIC, and BIC have only changed slightly from the original. Result is INTRATE ~ INFL + COMMPRI + PCE + PERSINC + HOUST

Formula | R^2 | AIC | BIC
---     | --: | --: | --:
INTRATE ~ INFL + PROD + UNEMPL + COMMPRI + PCE + PERSINC + HOUST | 0.639 | 2914 | 2950
INTRATE ~ INFL + PROD + COMMPRI + PCE + PERSINC + HOUST | 0.638 | 2913 | 2945
INTRATE ~ INFL + COMMPRI + PCE + PERSINC + HOUST | 0.637 | 2912 | 2939

#### (b)  Use specific-to-general to come to a model.  Start by regressing the federal funds rate on only a constant and add 1 variable at a time.  Is the model the same as in (a)?
1. Each individual explanatory variable was examined on its own. Starting with INFL with t-value = 28.924506, p-value = 2.472635e-119.
2. Next add PERSINC with t-value = 9.478074, p-value = 4.616637e-20.
3. Next add PCE with t-value = 3.412051, p-value = 6.843747e-04.
4. Next add HOUST with t-value = -4.893253, p-value = 1.249935e-06.
5. Next add COMMPRI with t-value = -2.841100, p-values 4.635778e-03.
6. The remaining PROD (t-value -0.988680, p-value 3.231857e-01) and UNEMPL (-0.071740, p-value 9.428308e-01) are not significant when added to the model. Stop.

Formula | R^2 | AIC | BIC
---     | --: | --: | --:
INTRATE ~ INFL | 0.560 | 3032 | 3041
INTRATE ~ INFL + PERSINC | 0.613 | 2950 | 2963
INTRATE ~ INFL + PERSINC + PCE | 0.619 | 2940 | 2958
INTRATE ~ INFL + PERSINC + PCE + HOUST | 0.633 | 2919 | 2941
INTRATE ~ INFL + PERSINC + PCE + HOUST + COMMPRI | 0.637 | 2912 | 2939

Yes, the model is the same as in (a).

#### (c)  Compare  your  model  from  (a)  and  the  Taylor  rule  of  equation  (1).  Consider R 2 ,  AIC  and  BIC.  Which  of  the models do you prefer?

Source | Formula | R^2 | AIC | BIC
---    | ---     | --: | --: | --:
(a) | INTRATE ~ INFL + PERSINC + PCE + HOUST + COMMPRI | 0.637 | 2912 | 2939
Taylor Rule | INTRATE ~ INFL + PROD | 0.575 | 3012 | 3025
simplest | INTRATE ~ INFL | 0.560 | 3032 | 3041

The Taylor rule's use of PROD would not be my choice given the results above. Leaving it out only slightly lowers the R^2 from 0.575 to 0.560 while including all significan explanatory variables raises R^2 to 0.637. The AIC and BIC for all models in the table are similar. For my own choice, of course it depends on the application, but I lean toward the simplest model based only on INFL.

#### d)  Test the Taylor rule of equation (1) using the RESET test, Chow break and forecast test (with in both tests as break date January 1980) and a Jarque-Bera test.  What do you conclude?
* The Ramsey RESET tests has the null hypothesis that additional higher order terms have coefficients of 0. I configured the test to use 2nd and 3rd order parameters. The resulting F-statistic is 2.2 with p-value 0.1. We cannot reject the null hypothesis at the desired 95% confidence interval.
* The Jarque-Bera test produces a value of 12.444 and p-value 0.002 suggesting the residual is not normally distributed. The results are similar for all regressions tested except the simplest one using only INFL.
* Testing for a break in January 1980 does produce signficant results such that we can reject the null hypothesis that there is no break.
