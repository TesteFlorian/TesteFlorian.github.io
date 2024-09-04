---
title: "Forecasting crop yield and price variations with machine learning from satellite-derived gross primary production maps"
collection: publications
permalink: /publication/2024-03-04-leveraging-satellite-data
excerpt: "This study presents a novel approach for forecasting corn yield and price variations using satellite-derived Gross Primary Production (GPP) data. It compares Empirical Orthogonal Functions (EOF), Autoencoders (AE), and Variational Autoencoders (β-VAEs) for dimensionality reduction and employs machine learning models, including ElasticNet and Random Forest, to predict yield and price variations in the US, Malawi, and South Africa. We also compare the effect of single vs. double-nested cross-validation on model performance."
date: 2024-03-04
venue: 'Preprint'
paperurl: 'https://doi.org/10.13140/RG.2.2.31718.23362'
citation: 'Teste, F., Ciais, P., Makowski, D. (2024). &quot;Forecasting crop yield and price variations with machine learning from satellite-derived gross primary production maps.&quot; <i>Preprint</i>.'

---
**Abstract**  
This study presents a novel approach for forecasting corn yield and price variations on a large scale, using exclusively satellite-derived Gross Primary Production (GPP) data with a native resolution of 0.05°. Dimensionality reduction techniques are implemented to extract relevant latent features from the high-dimensional GPP datasets. These features are then used as predictors in machine learning models forecasting yield and price variations (i.e., increase vs. decrease compared to the previous year). We compared the predictive performance of the proposed approach across three contrasted regions: the US (the world’s leading corn producer), South Africa, and Malawi, using monthly data covering their respective corn-growing seasons. Three dimension-reduction techniques - Empirical Orthogonal Functions (EOF), Autoencoders (AE), and Variational Autoencoders (β-VAEs) - and two machine learning models - ElasticNet and Random Forest - were evaluated.

Crucially, we compared the model performances using single and double-nested cross-validation to avoid any risk of overfitting. The results demonstrated that AE and β-VAE outperformed other techniques in identifying relevant predictors, while ElasticNet achieved the best predictive performance. A notable trend emerged, indicating that the accuracy of yield and price predictions improves when satellite-derived GPP data are collected around the peak month of corn growth, several months before harvest.

In addition, our model assessment revealed that the single cross-validation gave an overly optimistic view of model performances compared to double-nested cross-validation since tuning of hyperparameters and model evaluation are not performed independently. This suggests that it would be useful to use double cross-validation more systematically when evaluating predictive models. Our approach supports strategic planning and decision-making thanks to its good performance in early forecasting.
