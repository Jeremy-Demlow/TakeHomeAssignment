# Welcome to the companyname MLE Take-Home Assignment

In this project, we embark on a journey to transform a Jupyter Notebook, originally used for exploratory data analysis and preliminary modeling, into a robust, semi-production ready API process. The core of this project is a machine learning model developed to address some sort of business outcome that a customer will purchase or not purchase a product. This model, initially prototyped in a Jupyter Notebook, represents a critical step in our efforts to leverage data science.

This guide will outline the essential steps to transform the model from a static notebook into a dynamic, scalable API. This process includes but is not limited to adhering to production coding standards, ensuring code modularity and quality, rigorously testing the system, and thoroughly documenting each part of the workflow. Although the integration of continuous integration/continuous deployment (CI/CD) features like GitHub Actions and the use of an enterprise database or ADLS/S3 bucket for log storage are beyond the scope of this project, the approach taken lays the groundwork for these and other enhancements that are integral to a robust Data Science pipeline. The aim is not to just have a model but to add principles of software engineering and data science best practices to ensure effective but also maintainable, scalable processes to support our business.

# Objective
Ensure adherence to production standards in code, encompassing modularization, code quality, unit testing, and documentation.

### Rationale
The project aligns closely with the original Jupyter Notebook, focusing on rapid deployment, modularization, code quality, and robust unit testing, while minimizing extensive code rewrites and leveraging internal libraries for efficiency.

### Process Overview
This project emphasizes scalable architecture, using Docker Compose for service separation (API, Prometheus, Grafana), ensuring modularity and flexible scaling. FastAPI forms the core of the API service, chosen for its performance and ease of use. The setup supports both local development and rapid deployment, with a focus on environment configuration, resource utilization, and performance.

### Project Structure
- **Data Folder**: For data preparation and training dataset generation.
- **Modeling Folder**: Houses the model in a class structure, allowing for ease of modification and retraining.
- **Scripts**: Enable data scientists to retrain models with new data.
- **App Section**: Chose FastAPI simple yet powerful

### Key Decisions

- **Package Management with Poetry**: Chosen for its streamlined dependency management, Poetry ensures consistent environments across development and production. Its ability to lock dependencies and manage virtual environments simplifies the process of setting up the project on any machine, thereby reducing "it works on my machine" issues.

- **Model Serialization using Joblib**: Joblib is utilized for its efficiency in serializing Python objects, particularly those involving large NumPy arrays as typically found in machine learning models. This choice ensures a fast and reliable way to save and load the trained model, enabling quick start-up times and ease of model updates.

- **API and Backend with FastAPI**: FastAPI is selected for its high performance and ease of use, making it a fitting choice for building modern web APIs. Its ability to handle asynchronous requests enhances the throughput of the API, crucial for handling high-load scenarios. Additionally, its automatic generation of interactive API documentation (Swagger UI) significantly eases the process of testing and interacting with the API.

- **Containerization via Docker and Docker Compose**: Docker is used to containerize the application, ensuring that it runs consistently across different environments. Docker Compose further simplifies the orchestration of multi-container setups, like the one involving FastAPI, Prometheus, and Grafana in this project. This approach encapsulates the application and its dependencies, making it straightforward to deploy, scale, and manage.

- **Scalability Considerations with Asynchronous Threading**: The project leverages asynchronous programming in FastAPI, enhancing its ability to handle concurrent requests efficiently. This approach is pivotal for improving the speed and responsiveness of the prediction API, especially under heavy load. Asynchronous threading ensures that the API can manage multiple requests in a non-blocking manner, leading to better resource utilization and improved overall performance.


### Future Enhancements
- **Transition to Kubernetes**: For advanced orchestration and high-availability management.
- **CI/CD Pipeline**: Automating testing and deployment processes.
- **Auto-Scaling**: Dynamic resource adjustment for optimized performance.
- **Enhanced Security**: Regular vulnerability scans and secret management.
- **Performance Optimization**: Continuous improvement and cloud-native technology adoption.
- **Model Versioning with MLflow**: Effective management of machine learning models.
- **Feedback Loop for Continuous Learning**: Ensuring model evolution with new data and insights.
- **Container Management Processes**: Using actions and a private container registry
- **Serverless Architecture Considerations**: For specific components to reduce operational overhead.

### Conclusion

The project strikes a balance between adhering to production standards and maintaining the model's integrity for data scientists. The chosen structure, deployment strategy, and tools reflect a pragmatic approach to creating a deployable, maintainable, and scalable solution, keeping in mind the data scientists' working style and needs.


# How to Run the Project

### Step 0: Create a Virtual Environment

[Poetry Documentation](https://python-poetry.org/)

To start, ensure you have `poetry` installed on your computer. We use poetry as our package manager for this project. To train a new model yourself, poetry is crucial. If you prefer not to train the model and use the provided pickled model in the zipped folder, that's also an option. The Docker compose setup will handle the rest.

### Step 1: Decide To Train a Model

Run the following command to train your model. It automatically saves the model and preprocessor in the designated directories:

```python
python companyname/scripts/train_model.py --data_path 'companyname/files/data/exercise_26_train.csv' --model_save_path 'companyname/files/models/logistic_regression_model.pkl' --preprocessor_save_path 'companyname/files/models/preprocessor.pkl'
```

### Step 2: Poetry Dependent Run Test Locally

Execute the following commands to test the setup locally with poetry:

```bash
poetry run coverage run -m pytest && poetry run coverage report -m

Result:
======================================= 7 passed, 4 skipped, 8 warnings in 1.68s ========================================
Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
companyname/__init__.py                    1      0   100%
companyname/app/__init__.py                0      0   100%
companyname/data/__init__.py               0      0   100%
companyname/data/data_preparation.py      73      3    96%   178, 198, 236
companyname/modeling/__init__.py           0      0   100%
companyname/modeling/models.py            34      0   100%
test_api_script.py                      23     18    22%   6-12, 15-27
------------------------------------------------------------------
TOTAL
```

### Step 3: Run API

Use the following command to build Docker images and start the API:

```bash
bash run_api.sh
```

This script also handles port conflicts by suggesting alternative ports. Once the API is running, you can test it using `batch_predict_simple` and `batch_predict` endpoints.

> **Note:** Allow a moment for Granfa to catch up on the API calls for proper display.

### What Is Created

Here's what you'll find running on your local setup:

- **FastAPI Documentation**: Accessible at [API Home Page](http://localhost:1313/) or [API Docs](http://localhost:1313/doc).
- **Prometheus Monitoring**: View metrics at [Home Page](http://localhost:9090/).
- **Grafana Dashboard**: Accessible at [Home Page](http://localhost:3000/).
  - **Username**: companyname
  - **Password**: companyname
  - Navigate to the dashboards where you will see a simple dashboard showing how many API calls were called.


### Step 4: Optional Run Curl Commands

#### Single Prediction

```bash

curl -X 'POST' \
  'http://127.0.0.1:1313/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "data": { "x0": 0.042317, "x1": -3.344721, "x2": 4.6351242122, "x3": -0.5983959993, "x4": -0.6477715046, "x5": "monday", "x6": 0.184902, "x7": 46.690015, "x8": 3.034132, "x9": 0.364704, "x10": 14.260733, "x11": -1.559332, "x12": "$5,547.78", "x13": 0.520324, "x14": 31.212255, "x15": 4.891671, "x16": 0.357763, "x17": 14.766366, "x18": -17.467243, "x19": 0.224628, "x20": 0.096752, "x21": 1.305564, "x22": 0.353632, "x23": 3.909028, "x24": -91.273052, "x25": 1.396952, "x26": 4.401593, "x27": 0.443086, "x28": 14.048787, "x29": -0.932243, "x30": 5.255472, "x31": "germany", "x32": 0.54199153, "x33": 2.98948039, "x34": -1.78334189, "x35": 0.80127315, "x36": -2.60231221, "x37": 3.39682926, "x38": -1.22322646, "x39": -2.20977636, "x40": -68.69, "x41": 522.25, "x42": -428.69, "x43": 381.37, "x44": 0.0197503, "x45": 0.75116479, "x46": 0.8630479008, "x47": -1.0383166613, "x48": -0.2726187635, "x49": -0.3430207259, "x50": 0.3109008666, "x51": -0.797841974, "x52": -2.0390175153, "x53": 0.87182889, "x54": 0.14373012, "x55": -1.15212514, "x56": -2.1703139704, "x57": -0.267842962, "x58": 0.212110633, "x59": 1.6926559407, "x60": -0.9522767913, "x61": -0.8625864974, "x62": 0.0748487158, "x63": "36.29%", "x64": 3.47125327, "x65": -3.16656509, "x66": 0.65446814, "x67": 14.60067029, "x68": -20.57521013, "x69": 0.71083785, "x70": 0.16983767, "x71": 0.55082127, "x72": 0.62814576, "x73": 3.38608078, "x74": -112.45263714, "x75": 1.48370808, "x76": 1.77035368, "x77": 0.75702363, "x78": 14.75731742, "x79": -0.62550355, "x80": null, "x81": "October", "x82": "Female", "x83": -0.7116680715, "x84": -0.2653559892, "x85": 0.5175495907, "x86": -1.0881027092, "x87": -1.8188638198, "x88": -1.3584469527, "x89": -0.654995195, "x90": -0.4933042262, "x91": 0.373853, "x92": 0.94143481, "x93": 3.54679834, "x94": -99.8574882, "x95": 0.403926, "x96": 1.65378726, "x97": 0.00771459, "x98": -32.02164582, "x99": -60.3127828
    }
}'

```

#### Multi Through Predict Method

```bash
curl -X 'POST' \
  'http://localhost:1313/batch_predict_simple' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "data": [
        {
            "x0": 0.042317,
            "x1": -3.344721, "x2": 4.6351242122, "x3": -0.5983959993, "x4": -0.6477715046, "x5": "monday", "x6": 0.184902, "x7": 46.690015, "x8": 3.034132, "x9": 0.364704, "x10": 14.260733, "x11": -1.559332, "x12": "$5,547.78", "x13": 0.520324, "x14": 31.212255, "x15": 4.891671, "x16": 0.357763, "x17": 14.766366, "x18": -17.467243, "x19": 0.224628, "x20": 0.096752, "x21": 1.305564, "x22": 0.353632, "x23": 3.909028, "x24": -91.273052, "x25": 1.396952, "x26": 4.401593, "x27": 0.443086, "x28": 14.048787, "x29": -0.932243, "x30": 5.255472, "x31": "germany", "x32": 0.54199153, "x33": 2.98948039, "x34": -1.78334189, "x35": 0.80127315, "x36": -2.60231221, "x37": 3.39682926, "x38": -1.22322646, "x39": -2.20977636, "x40": -68.69, "x41": 522.25, "x42": -428.69, "x43": 381.37, "x44": 0.0197503, "x45": 0.75116479, "x46": 0.8630479008, "x47": -1.0383166613, "x48": -0.2726187635, "x49": -0.3430207259, "x50": 0.3109008666, "x51": -0.797841974, "x52": -2.0390175153, "x53": 0.87182889, "x54": 0.14373012, "x55": -1.15212514, "x56": -2.1703139704, "x57": -0.267842962, "x58": 0.212110633, "x59": 1.6926559407, "x60": -0.9522767913, "x61": -0.8625864974, "x62": 0.0748487158, "x63": "36.29%", "x64": 3.47125327, "x65": -3.16656509, "x66": 0.65446814, "x67": 14.60067029, "x68": -20.57521013, "x69": 0.71083785, "x70": 0.16983767, "x71": 0.55082127, "x72": 0.62814576, "x73": 3.38608078, "x74": -112.45263714, "x75": 1.48370808, "x76": 1.77035368, "x77": 0.75702363, "x78": 14.75731742, "x79": -0.62550355, "x80": null, "x81": "October", "x82": "Female", "x83": -0.7116680715, "x84": -0.2653559892, "x85": 0.5175495907, "x86": -1.0881027092, "x87": -1.8188638198, "x88": -1.3584469527, "x89": -0.654995195, "x90": -0.4933042262, "x91": 0.373853, "x92": 0.94143481, "x93": 3.54679834, "x94": -99.8574882, "x95": 0.403926, "x96": 1.65378726, "x97": 0.00771459, "x98": -32.02164582, "x99": -60.3127828
        },
        {
            "x0": 0.123456,
            "x1": -2.345678, "x2": 5.6789012345, "x3": -0.987654321, "x4": -1.2345678901, "x5": "tuesday", "x6": 0.567890, "x7": 12.345678, "x8": 6.789012, "x9": 0.123456, "x10": 23.456789, "x11": -3.456789, "x12": "$7,890.12", "x13": 0.234567, "x14": 45.678901, "x15": 7.890123, "x16": 0.456789, "x17": 23.456789, "x18": -12.345678, "x19": 0.345678, "x20": 0.567890, "x21": 2.345678, "x22": 1.234567, "x23": 4.567890, "x24": -67.890123, "x25": 2.345678, "x26": 5.678901, "x27": 0.678901, "x28": 12.345678, "x29": -1.234567, "x30": 7.890123, "x31": "usa", "x32": 0.67890123, "x33": 3.45678901, "x34": -2.3456789, "x35": 0.12345678, "x36": -1.23456789, "x37": 2.34567890, "x38": -0.12345678, "x39": -1.23456789, "x40": -45.67, "x41": 123.45, "x42": -34.56, "x43": 67.89, "x44": 0.05678901, "x45": 0.12345678, "x46": 0.2345678901, "x47": -0.3456789012, "x48": -0.4567890123, "x49": -0.5678901234, "x50": 0.6789012345, "x51": -0.7890123456, "x52": -0.8901234567, "x53": 0.9012345678, "x54": 0.0123456789, "x55": -1.1234567890, "x56": -2.2345678901, "x57": -0.3456789012, "x58": 0.4567890123, "x59": 2.3456789012, "x60": -1.2345678901, "x61": -0.3456789012, "x62": 0.1234567890, "x63": "45.67%", "x64": 4.567890123, "x65": -4.567890123, "x66": 0.567890123, "x67": 12.34567890, "x68": -23.45678901, "x69": 0.789012345, "x70": 0.890123456, "x71": 0.901234567, "x72": 0.012345678, "x73": 4.567890123, "x74": -123.4567890, "x75": 2.345678901, "x76": 2.345678901, "x77": 0.890123456, "x78": 12.34567890, "x79": -0.123456789, "x80": null, "x81": "November", "x82": "Male", "x83": -0.9876543210, "x84": -0.2345678901, "x85": 0.6789012345, "x86": -1.5678901234, "x87": -1.2345678901, "x88": -0.7890123456, "x89": -0.4567890123, "x90": -0.5678901234, "x91": 0.678901234, "x92": 0.9012345678, "x93": 4.567890123, "x94": -67.8901234, "x95": 0.234567890, "x96": 1.234567890, "x97": 0.123456789, "x98": -45.67890123, "x99": -12.34567890
        }
    ]
}'

```

### Many Predictions Batch Predict

```bash
curl -X 'POST' \
  'http://localhost:1313/batch_predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "data": [
        {
            "x0": 0.042317,
            "x1": -3.344721, "x2": 4.6351242122, "x3": -0.5983959993, "x4": -0.6477715046, "x5": "monday", "x6": 0.184902, "x7": 46.690015, "x8": 3.034132, "x9": 0.364704, "x10": 14.260733, "x11": -1.559332, "x12": "$5,547.78", "x13": 0.520324, "x14": 31.212255, "x15": 4.891671, "x16": 0.357763, "x17": 14.766366, "x18": -17.467243, "x19": 0.224628, "x20": 0.096752, "x21": 1.305564, "x22": 0.353632, "x23": 3.909028, "x24": -91.273052, "x25": 1.396952, "x26": 4.401593, "x27": 0.443086, "x28": 14.048787, "x29": -0.932243, "x30": 5.255472, "x31": "germany", "x32": 0.54199153, "x33": 2.98948039, "x34": -1.78334189, "x35": 0.80127315, "x36": -2.60231221, "x37": 3.39682926, "x38": -1.22322646, "x39": -2.20977636, "x40": -68.69, "x41": 522.25, "x42": -428.69, "x43": 381.37, "x44": 0.0197503, "x45": 0.75116479, "x46": 0.8630479008, "x47": -1.0383166613, "x48": -0.2726187635, "x49": -0.3430207259, "x50": 0.3109008666, "x51": -0.797841974, "x52": -2.0390175153, "x53": 0.87182889, "x54": 0.14373012, "x55": -1.15212514, "x56": -2.1703139704, "x57": -0.267842962, "x58": 0.212110633, "x59": 1.6926559407, "x60": -0.9522767913, "x61": -0.8625864974, "x62": 0.0748487158, "x63": "36.29%", "x64": 3.47125327, "x65": -3.16656509, "x66": 0.65446814, "x67": 14.60067029, "x68": -20.57521013, "x69": 0.71083785, "x70": 0.16983767, "x71": 0.55082127, "x72": 0.62814576, "x73": 3.38608078, "x74": -112.45263714, "x75": 1.48370808, "x76": 1.77035368, "x77": 0.75702363, "x78": 14.75731742, "x79": -0.62550355, "x80": null, "x81": "October", "x82": "Female", "x83": -0.7116680715, "x84": -0.2653559892, "x85": 0.5175495907, "x86": -1.0881027092, "x87": -1.8188638198, "x88": -1.3584469527, "x89": -0.654995195, "x90": -0.4933042262, "x91": 0.373853, "x92": 0.94143481, "x93": 3.54679834, "x94": -99.8574882, "x95": 0.403926, "x96": 1.65378726, "x97": 0.00771459, "x98": -32.02164582, "x99": -60.3127828
        },
        {
            "x0": 0.123456,
            "x1": -2.345678, "x2": 5.6789012345, "x3": -0.987654321, "x4": -1.2345678901, "x5": "tuesday", "x6": 0.567890, "x7": 12.345678, "x8": 6.789012, "x9": 0.123456, "x10": 23.456789, "x11": -3.456789, "x12": "$7,890.12", "x13": 0.234567, "x14": 45.678901, "x15": 7.890123, "x16": 0.456789, "x17": 23.456789, "x18": -12.345678, "x19": 0.345678, "x20": 0.567890, "x21": 2.345678, "x22": 1.234567, "x23": 4.567890, "x24": -67.890123, "x25": 2.345678, "x26": 5.678901, "x27": 0.678901, "x28": 12.345678, "x29": -1.234567, "x30": 7.890123, "x31": "usa", "x32": 0.67890123, "x33": 3.45678901, "x34": -2.3456789, "x35": 0.12345678, "x36": -1.23456789, "x37": 2.34567890, "x38": -0.12345678, "x39": -1.23456789, "x40": -45.67, "x41": 123.45, "x42": -34.56, "x43": 67.89, "x44": 0.05678901, "x45": 0.12345678, "x46": 0.2345678901, "x47": -0.3456789012, "x48": -0.4567890123, "x49": -0.5678901234, "x50": 0.6789012345, "x51": -0.7890123456, "x52": -0.8901234567, "x53": 0.9012345678, "x54": 0.0123456789, "x55": -1.1234567890, "x56": -2.2345678901, "x57": -0.3456789012, "x58": 0.4567890123, "x59": 2.3456789012, "x60": -1.2345678901, "x61": -0.3456789012, "x62": 0.1234567890, "x63": "45.67%", "x64": 4.567890123, "x65": -4.567890123, "x66": 0.567890123, "x67": 12.34567890, "x68": -23.45678901, "x69": 0.789012345, "x70": 0.890123456, "x71": 0.901234567, "x72": 0.012345678, "x73": 4.567890123, "x74": -123.4567890, "x75": 2.345678901, "x76": 2.345678901, "x77": 0.890123456, "x78": 12.34567890, "x79": -0.123456789, "x80": null, "x81": "November", "x82": "Male", "x83": -0.9876543210, "x84": -0.2345678901, "x85": 0.6789012345, "x86": -1.5678901234, "x87": -1.2345678901, "x88": -0.7890123456, "x89": -0.4567890123, "x90": -0.5678901234, "x91": 0.678901234, "x92": 0.9012345678, "x93": 4.567890123, "x94": -67.8901234, "x95": 0.234567890, "x96": 1.234567890, "x97": 0.123456789, "x98": -45.67890123, "x99": -12.34567890
        }
    ]
}'


```
