# structure
.
* [Tc_uc4]
 * [config](./config) folder with the configuration file in toml format 
 * [data](./data) folder containing the input data
 * [docs](./docs)
 * [experiments](./experiments) folder with the module to run the experiments
 * [jobs](./jobs) folder with the module to run the jobs
 * [logs](./logs) folder where the log files will be saved
 * [tc_uc4](./tc_uc4) folder with codebase
   * [algorithms](./tc_uc4/algorithms) folder with modules with algorithms and utils to run the models
   * [analytics](./tc_uc4/analytics) folder with modules with evaluation metrics
   * [datahandler](./tc_uc4/datahandler) folder with moduls for reading and writing files
   * [datapreparation](./tc_uc4/datapreparation) folder with moduls for preprocessing 
   * [utility](./tc_uc4/utility) folder with utility files
 * [tests](./tests) folder with modules to run unitary tests
 * [README.md](./README.md)
 * [requirements.txt](./requirements.txt)
 * [setup.py](./setup.py)


# in order to install the codebase run 
```bash
python pip install TEST-TC
```
# after this it can be imported in notebooks. 

# From the folder "Tc_uc4", 
- to execute the experiments to train and tune models, run:
    ```bash
    python experiments/train_and_tune_prophet.py
    ```
- After the experiments, to excute the job for forecasting with best models, run:
    ```bash
    python jobs/job_predict.py
    ```

# Note that in order for the execution to be successful:
- in confing file, update the section "data_paths" 
- in config file, edit the other sections with parameters and configurations to be tested
- in train_and_tune_prophet.py and job_predict.py edit the variables config_paths (path to the folder containing the config file, e.g: '/Tc_uc4/config') and config_file (name of the config file, e.g: "train_and_tune_prophet.toml")
