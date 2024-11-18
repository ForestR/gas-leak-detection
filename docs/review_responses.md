# Response to Reviewers' Comments

We thank the reviewers for their careful reading of our manuscript and their constructive comments. Below are our point-by-point responses to their comments. 

In this response, “Comments of the Reviewer” are presented in <span style="color:black">**black**</span>, followed by “Author’s Response” (in <span style="color:red">**red**</span>) detailing how we have addressed each comment or providing further explanation where necessary. Additionally, revised text excerpts from the manuscript are provided in <span style="color:blue">**blue**</span> to show the specific changes made. Locations of these changes are also highlighted in red in the updated manuscript.

## Reviewer #1:

### Comment 1:
  <span style="color:black">
The graphs are not good at all and should be significantly improved. The text on the graphs should be enlarged.
  </span>

#### Response:  
  <span style="color:red">
We appreciate the feedback regarding the figures in our manuscript. We've carefully reviewed and revised all figures to enhance their quality and clarity, including increasing font sizes and adjusting layouts to enhance readability. 
  </span>

  <span style="color:red">
We invite you to review the revised figures in our manuscript on [Github](https://github.com/ForestR/gas-leak-detection/blob/main/docs/figures). We believe these improvements will significantly enhance the overall presentation and understanding of our research.
  </span>


#### TODO: Revised text: 
  <span style="color:blue">
*Figure X has been updated to improve clarity, with enlarged labels and enhanced visual quality to facilitate understanding.*
  </span>

### Comment 2:  
  <span style="color:black;">
The performance of the traditional algorithm, which yielded an accuracy of only 7.2% and an F1 score of 0.135, appears highly unusual and suggests a potential issue. Please provide clarification.
  </span>

#### Response:   
  <span style="color:red;">
The low performance of the baseline model (traditional algorithm) highlights the challenges inherent in micro-leak detection when using a single gas flowmeter in a kitchen setting. In this project, approximately 250,000 IoT gas flowmeter devices are deployed. Over the past several years, the city gas supplier has used the baseline model for daily leakage detection. For validation, a subset of positive reports from the baseline model was selected at semi-random intervals for manual door-to-door inspection. These inspections included the use of handheld concentration meters and valve closure pressure retention tests. Our [evaluation dataset](https://github.com/ForestR/gas-leak-detection/blob/main/data/processed/evaluation_dataset.csv) consists of these manually validated positive results, ensuring its reliability.
  </span>

  <span style="color:red;">
The baseline model is a logic-based algorithm. Its detection logic is defined as follows: if the duration of continuous and stable gas usage exceeds the corresponding threshold in specific flow intervals, the user is flagged as at risk. The parameter standards currently used in the baseline model are summarized in the table below. These standards were derived from analyzing abnormal pulse patterns in a small sample set.
  </span>

**Security Policies on the Ryder IoT Meter (G2.5):**

| Flow Interval (pulses/hour) | Duration (hours) | Risk Level |
| --------------------------- | ---------------- | ---------- |
| 5–10                        | 10               | a8         |
| 10–30                       | 6                | a7         |
| 30–60                       | 3                | a6         |
| 60–120                      | 2                | a5         |
| 120–300                     | 1                | a34        |

  <span style="color:red;">
In this table, "duration" refers to the number of hours, "bottom" and "top" represent the hourly pulse counts, and "label" indicates the assigned risk level.
  </span>

  <span style="color:red;">Our proposed model made breakthroughs in the accuracy of the report and the efficiency of the calculation, compared with the baseline model.  We developed a physics-based underlying model to generate the training dataset of the seq2seq model used for unsupervised annotation on actual dataset. The performance of our proposed model shows the advantages of using this method.</span>

#### TODO: Revised text:  
<span style="color:blue">
*Section Y, Paragraph Z: "The low accuracy and F1 score of 0.135 for the traditional algorithm underscore its limitations in detecting micro-leaks in low-flow scenarios, highlighting the advantage of our proposed method under such conditions."*
</span>

### Comment 3:
  <span style="color:black">
Please discuss the disadvantages of using this method (if any).
  </span>

#### Response: 
  <span style="color:red">
We have addressed the limitations of our approach by including a detailed analysis of its performance using a ROC curve. Additionally, we have discussed potential challenges in real-time deployment and sensitivity to gas equipment, especially for intelligent timing gas.
  </span>

#### TODO: Revised text:  
<span style="color:blue">
*Section Y, Paragraph Z: "While effective in controlled settings, the method may face challenges in real-time applications, particularly in environments with fluctuating temperature and pressure, which could affect leak detection accuracy."*
</span>


### Comment 4:
  <span style="color:black">
Please make a comparative study in terms of results with other methods from the literature.
  </span>

#### Response:  
  <span style="color:red;"> 
Gas companies often treat customer data as a private asset, resulting in a relatively closed data-sharing culture in the residential and industrial gas monitoring domain. This makes it exceptionally challenging to find labeled datasets publicly available online, let alone established methods for processing such data. The conservative nature of this environment significantly limits the effectiveness of traditional algorithms (baseline models). We have extensively searched databases such as Google Scholar using keywords like "small leak," "gas flowmeter," and "smart house," but found few closely related scenarios or boundary conditions in published research. 
  </span> 

  <span style="color:red;"> 
Moreover, our raw data is organized in a highly specific structure, which may require an appendix for clarity. The uniqueness of our data in this application scenario further complicates the task of identifying detailed third-party methods online. For more information on the pulse data from gas flowmeters, please refer to our [notebook](https://github.com/ForestR/gas-leak-detection/blob/main/notebooks/pulse_data_analysis.ipynb). 
  </span> 

  <span style="color:red;"> 
We welcome contributions and encourage the addition of new models to our project. To facilitate this, we have provided access to our evaluation dataset (anonymized by encoding sensitive information). Any new models can be evaluated using this dataset, and we will update the ranking list accordingly as new results become available. 
  </span>


### Comment 5:  
  <span style="color:black">
In the title change “based” to “Based”.
  </span>

#### Response:  
  <span style="color:red">
The title has been revised as requested.
  </span>

#### Revised text:  
  <span style="color:blue">
*Title: "Micro Leak Detection of Natural Gas for Residential Users Based on Gas Flowmeters"*
  </span>


---

## Reviewer #2:

### Comment 1:  
  <span style="color:black">
The authors tackle the interesting problem of detecting micro-leaks within houses: leaks are detected according to a leak threshold \Theta. 
The authors provide an adequate description of the physical model, which can be better revised to actually match the way the formulas were computed within the simulation for generating the data (are you actually using the integrals, or are you performing a discrete time optimization requiring an approximation of the integral to a summation?).
  </span>

#### Response:  
  <span style="color:red">
Thank you for your thoughtful comment and for highlighting the need for clarification regarding our computational approach. In response, we have revised the Methods section to explicitly state that the integrals are approximated using summation for discrete time steps in our simulations. This ensures consistency between the described physical model and the actual computations performed during data generation. 
  </span>

#### TODO: Revised text:  
  <span style="color:blue">
*Section X, Paragraph Y: "For computational efficiency, the integrals are approximated by summing discrete time intervals, enabling practical simulation of gas flow behavior over time."*
  </span>


### Comment 2:  
  <span style="color:black">
Despite the authors are correctly addressing the literature on leak detection, and given that they are also discussing the way to determine the classification at real-time (e.g., whether there is actually a leak or not), the authors provide marginal insight on the real-time classification task, and how their model compares to other state-of-the-art time series classification tasks.
  </span>

#### Response:  
  <span style="color:red;"> 
Thank you for your valuable feedback. We have expanded our discussion of the real-time classification process to provide greater clarity and detail. Specifically, we have included a comprehensive explanation of how our model processes time-series data to classify leaks in real-time and highlighted its comparative advantages over existing state-of-the-art time series classification methods. The revised text elaborates on the model's ability to achieve high prediction accuracy under low-flow conditions, a key challenge in leak detection. 
  </span>

#### TODO: Revised text:  
  <span style="color:blue">
*Section X, Paragraph Y: "Our proposed approach processes real-time data streams to classify potential leak events. Unlike other time series classification methods, our model prioritizes accuracy under low-flow conditions, a common scenario in micro-leak detection. By leveraging sequential dependencies and anomaly patterns in time-series data, our model demonstrates improved precision and recall compared to state-of-the-art techniques. This allows for timely detection while minimizing false positives, critical for practical implementation."*
  </span>


### Comment 3:  
  <span style="color:black">
As a side note, most of the figures are completely illegible, as most of the labels are given in Chinese, thus not being suitable for an international audience.
  </span>

#### Response:  
  <span style="color:red">
All figures have been updated with English labels to ensure they are accessible to the international audience.
  </span>

#### TODO: Revised text:  
  <span style="color:blue">
*Figures X and Y now contain English labels to enhance legibility and accessibility for all readers.*
  </span>


### Comment 4:  
  <span style="color:black">
The authors should consider to better identify how the Seq2Seq model is then associated to the detection of a leak.

Given this, it seems that the authors are providing the classification by estimating the leak through a Seq2Seq model which transforms the nominal flows into the target flow. Then, the pulse model for a real-life sensor is likely attach to the resulting sequence, from which the leak can be detected and the pulses can be sent.
Not with standing the former, the authors provide no explicit pipeline to process these, and therefore the previous sentence is mainly resumed from the information being available form the text. Still, the authors should consider to better identify how the Seq2Seq model is then associated to the detection of a leak. If they are actually using the pulse model, then the overall task boils down to a binary classification problem, where the binary condition is just associated to the increase of the \Theta parameter. Thus, the overall analysis should also reflect the similarity between the forecasted resulting sequence and the expected one (e.g., Dynamic Time Warping), thus remarking the similarity and differences between predicted and expected sequence. This outcome will then motivate the results already provided in Table 2 and 3, which are likely to be associated with the aforementioned pulse detection but, the classification outcome shall be ultimately related to the quality of the resulting time series.

  </span>

**Response:**  
<span style="color:red">
We have expanded our explanation of the Seq2Seq model's role in leak detection, providing a clearer description of how it processes input flows and outputs leak predictions.
</span>

**Revised text:**  
<span style="color:blue">
*Section X, Paragraph Y: "The Seq2Seq model translates observed flow rates into a predicted flow sequence, which is then used to identify leaks based on deviations from expected patterns."*
</span>


### Comment 5:  
  <span style="color:black">
The authors should consider addressing all of the previous questions prior to acceptance.
  </span>

**Response:**  
<span style="color:red">
All of the reviewer’s comments have been addressed with revisions in the manuscript as outlined above, improving the clarity, comprehensiveness, and accessibility of the paper.
</span>

**Revised text:**  
<span style="color:blue">
*We trust that these revisions fulfill the reviewer’s expectations and have enhanced the overall quality of the manuscript.*
</span>
