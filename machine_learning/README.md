# Machine Learning Microservice

This microservice implements the machine learning aspect of the SmellInspector Companion software.

> On start, the "backend" sends this microservice all existing database data, that is
> then used to train all available machine learning models.
>
> Note that restarting the container, without restarting the "backend" will mean
> that the container doesnt have any existing training data.

After the microservice reads initial data from the backend, it receives packets
every time data is read and cached from connected SmellInspector devices. This
happens when tests are ran with "data acquisition" enabled (checkbox in frontend when starting
new tests).

> Every 100 samples, the machine learning models are re-trained using all available data.
> This can be controlled through the `RE_TRAINING_RATE` environment variable.

## API Documentation

Available endpoints (with nginx prefix `/ml`):

- `/`
    - Method: **GET**
    - Returns an overview of available endpoints.
- `/ml/initial-data`
    - Method: **POST**
    - Called on start to pass data from "backend" to this microservice.
    - Body:
  ```json
  {
    "data": "base64 data of database.db file."
  }
  ```
- `/ml/healthcheck`
  - Method: **GET**
  - Simple healthcheck to ensure service is running.
- `/ml/new`
  - Method: **POST**
  - Persist new data to the machine learning database.
  - Body:
  ```json
  {
    "data": {
      "data": ["Array of 64 values read from sensor."],
      "substance": "Measured substance name (Label).",
      "quantity": "Measured substance quantity (Appended to label)"
    }
  }
  ```
- `/ml/predict`
  - Method: **POST**
  - Predict the label for the given data.
  - Response:
  ```json
  {
    "predictions": [
      # For each available model
      {
        "ML Model Name (String)": "Predicted Label + Quantity (String)"
      }
    ]
  }
  ```
  - Body:
  ```json
  {
    "data": ["Array of 64 values read from sensor."]
  }
  ```
