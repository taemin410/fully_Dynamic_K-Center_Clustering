# Stabilization of Fully Dynamic K-Center Clustering

This project was motivated by Fully Dynamic k-Center Clustering (Chan et al. 2018). It aims to provide the enhancement of fully dynamic k-center clustering. 

The stability is defined as the degree of similarities between different clusterings. Stability is measured by different metrics including Consistency, ARI, and NMI.
The consistency is defined as the number of changes in centers of clusterings. ARI and NMI is defined by Pair-counting measures and contingency table measures. 


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

What things you need to install the software and how to install them

- Python3 

### Installing

A step by step series of examples that tell you how to get a development env running

```
pip install -e . 
```

## Running the Source Code

To run the program (in fully adversarial model)
```

python fdkcc/ -f 

```

#### Flags that can be specified:

- -f , --fullyadv = Run Fully Adversarial model
- -s , --sliding = Run sliding window model



If you see the following console screen, 
the program is running successfully.

![](images/samplerun.png)

```
average of center changes : 7.686274509803922 
average of center changes for Selective : 1.2938931297709924 
average of NMI:  0.9817545560091205
average of Selective NMI:  0.9994655512106769
average of ARI:  0.5134579491675249
average of Selective ARI:  0.8591171769543855
average of contingency_ARI:  0.9720373134523597
average of contingency_Selective ARI:  0.9988657316177523

```

You will see the following graphical images when fully_adv model successfully runs,

![](images/1.png)
![](images/2.png)
![](images/3.png)

*For sliding window model, you can specify the window length.

When the program terminates, `cluster_information.log` file will be created. This log file contains the solution for the optimal radius for the clustering.

### Break down into end to end tests

To run a full test,

```
pytest
```

You will see the result as follows
```
test/test_algo_fully_adv.py ....... [ 26%]
test/test_data_fully_adv.py .       [ 30%]
test/test_point.py ....             [ 50%]
test/test_set.py .........          [ 88%]
test/test_util.py ..                [100%]
```



## Contributing

This project is motivated by [fully dynamic k-center algorithm](https://github.com/fe6Bc5R4JvLkFkSeExHM/k-center) project. Note that this project is a translation of the existing C code base. 

### References

[1]José E. Chacón and Ana I. Rastrojo. 2020. Minimum adjusted Rand index for twoclusterings of a given size.  arXiv:2002.03677 [stat.ML]

[2]T-H. Hubert Chan, Arnaud Guerquin, and Mauro Sozio. 2018.  Fully Dynamick-Center Clustering.WWW 2018(April 2018), 579–587.   https://doi.org/10.1145/3178876.3186124

[3]Vincent Cohen-Addad, Niklas Hjuler, Nikos Parotsidis, David Saulpic, and ChrisSchwiegelshohn. 2019. Fully Dynamic Consistent Facility Location.33rd Confer-ence on Neural Information Processing Systems (NeurIPS 2019)(2019).

[4]Jasmine Irani, Nitin Pise, and Nitin Pise. 2016. Clustering Techniques and the Sim-ilarity Measures used in Clustering: A Survey.International Journal of ComputerApplications134 (Jan. 2016).

[5]Alexander Kraskov, Harald Stögbauer, and Peter Grassberger. 2004. Estimatingmutual information.Phys. Rev. E69 (Jun 2004), 066138. Issue 6.  https://doi.org/10.1103/PhysRevE.69.066138

[6]Silvio Lattanzi and Sergei Vassilvitskii. 2017. Consistent k-Clustering.Proceedingsof the 34th International Conference on Machine Learning, PMLR 70(2017).

[7]David McAllester and Karl Stratos. 2018. Formal Limitations on the Measurementof Mutual Information.CoRRabs/1811.04251 (2018).  arXiv:1811.04251   http://arxiv.org/abs/1811.04251

[8]A. Meyerson. 2001. Online facility location. InProceedings 42nd IEEE Symposiumon Foundations of Computer Science. 426–431.

[9]Ben Poole, Sherjil Ozair, Aäron van den Oord, Alexander A. Alemi, and GeorgeTucker. 2019. On Variational Bounds of Mutual Information.CoRRabs/1905.06922(2019). arXiv:1905.06922  http://arxiv.org/abs/1905.06922

[10]Simone Romano, Nguyen Xuan Vinh, James Bailey, and Karin Verspoor. 2016.Adjusting for Chance Clustering Comparison Measures.Journal of MachineLearning Research 17(2016), 1–32.

[11]Nguyen Vinh, Julien Epps, and James Bailey. 2009. Information theoretic measuresfor clusterings comparison: Is a correction for chance necessary?ICML, 135.https://doi.org/10.1145/1553374.1553511

[12]Nguyen Xuan Vinh, Julien Epps, and James Bailey. 2010. Information TheoreticMeasures for Clusterings Comparison: Variants, Properties, Normalization andCorrection for Chance.Journal of Machine Learning Research, Article 11 (2010),2837–2854 pages

## Authors

* **Choi Jae Won** - *Initial work* - [github](https://github.com/choijaewon959)
* **Ha Tae Min** - *Initial work* - [github](https://github.com/taemin410)


## License

This project is licensed under the MIT License

## Acknowledgments

* Dr. Hubert Chan - hubert@cs.hku.hk 
* Shuguang Hu  - sghu@cs.hku.hk

