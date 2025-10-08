# Data Science with Multiple Agents

## Overview

This project is based on the [Google ADK Samples Data Science Agent](https://github.com/google/adk-samples/tree/main/python/agents/data-science) and demonstrates a multi-agent system designed for sophisticated data analysis. It integrates several specialized agents to handle different aspects of the data pipeline, from data retrieval to advanced analytics and machine learning. The system is built to interact with BigQuery, perform complex data manipulations, generate data visualizations and execute machine learning tasks using BigQuery ML (BQML). The agent can generate text response as well as visuals, including plots and graphs for data analysis and exploration.

> **Note:** This project is derived from the official Google ADK samples repository. For the original implementation and latest updates, please refer to the [Google ADK Samples](https://github.com/google/adk-samples/tree/main/python/agents/data-science).

▶️ **Watch the Video Walkthrough:** [How to build a Data Science agent with ADK](https://www.youtube.com/watch?v=efcUXoMX818)

## Modifications from Original Sample

This implementation includes several improvements over the original Google ADK sample:

*   **Centralized Configuration Management:** Enhanced environment variable handling with proper validation and error messages
*   **Improved Error Handling:** Custom exception classes and better error reporting throughout the codebase
*   **Code Quality Improvements:** Better type hints, logging, and code organization
*   **Enhanced Documentation:** Updated setup instructions and troubleshooting guides

## Agent Details
The key features of the Data Science Multi-Agent include:

| Feature | Description |
| --- | --- |
| **Interaction Type:** | Conversational |
| **Complexity:**  | Advanced |
| **Agent Type:**  | Multi Agent |
| **Components:**  | Tools, AgentTools, Session Memory, RAG |
| **Vertical:**  | All (Applicable across industries needing advanced data analysis) |


### Architecture
![Data Science Architecture](data-science-architecture.png)

### Key Features

*   **Multi-Agent Architecture:** Utilizes a top-level agent that orchestrates sub-agents, each specialized in a specific task.
*   **Database Interaction (NL2SQL):** Employs a Database Agent to interact with BigQuery using natural language queries, translating them into SQL.
*   **Data Science Analysis (NL2Py):** Includes a Data Science Agent that performs data analysis and visualization using Python, based on natural language instructions.
*   **Machine Learning (BQML):** Features a BQML Agent that leverages BigQuery ML for training and evaluating machine learning models.
*   **Code Interpreter Integration:** Supports the use of a Code Interpreter extension in Vertex AI for executing Python code, enabling complex data analysis and manipulation.
*   **ADK Web GUI:** Offers a user-friendly GUI interface for interacting with the agents.
*   **Testability:** Includes a comprehensive test suite for ensuring the reliability of the agents.



## Setup and Installation

### Prerequisites

*   **Google Cloud Account:** You need a Google Cloud account with BigQuery enabled.
*   **Python 3.12+:** Ensure you have Python 3.12 or a later version installed.
*   **uv:** Install uv by following the instructions on the official uv website: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)
*   **Git:** Ensure you have git installed. If not, you can download it from [https://git-scm.com/](https://git-scm.com/) and follow the [installation guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).



### Project Setup with uv

1.  **Clone the Repository:**

    **Option A: Use this modified version:**
    ```bash
    git clone <your-repository-url>
    cd aiAgent/data-science
    ```

    **Option B: Use the original Google ADK sample:**
    ```bash
    git clone https://github.com/google/adk-samples.git
    cd adk-samples/python/agents/data-science
    ```

2.  **Install Dependencies with uv:**

    ```bash
    uv sync
    ```

    This command reads the `pyproject.toml` file and installs all the necessary
    dependencies into a virtual environment managed by uv. On the first run,
    this command will also create a new virtual environment. By default, the
    virtual environment will be created in a `.venv` directory inside
    `adk-samples/python/agents/data-science`. If you already have a virtual
    environment created, or you want to use a different location, you can use
    the `--active` flag for `uv` commands, and/or change the
    `UV_PROJECT_ENVIRONMENT` environment variable. See
    [How to customize uv's virtual environment location](https://pydevtools.com/handbook/how-to/how-to-customize-uvs-virtual-environment-location/)
    for more details.

2.  **Activate the uv Shell:**

    If you are using the `uv` default virtual environment, you now need
    to activate the environment.

    ```bash
    source .venv/bin/activate
    ```

4.  **Set up Environment Variables:**
    Rename the file ".env.example" to ".env"
    Fill the below values:

    ```bash
    # Choose Model Backend: 0 -> ML Dev, 1 -> Vertex
    GOOGLE_GENAI_USE_VERTEXAI=1

    # ML Dev backend config. Fill if using Ml Dev backend.
    GOOGLE_API_KEY='YOUR_VALUE_HERE'

    # Vertex backend config
    GOOGLE_CLOUD_PROJECT='YOUR_VALUE_HERE'
    GOOGLE_CLOUD_LOCATION='YOUR_VALUE_HERE'
    ```

    Follow the following steps to set up the remaining environment variables.

5.  **BigQuery Setup:**
    These steps will load the sample data provided in this repository to BigQuery.
    For our sample use case, we are working on the House Prices dataset from Kaggle:

    _House Prices: Advanced Regression Techniques. https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques, Kaggle._

    *   First, set the BigQuery project IDs in the `.env` file. This can be the
        same GCP Project you use for `GOOGLE_CLOUD_PROJECT`, but you can use
        other BigQuery projects as well, as long as you have access permissions
        to that project.
        *   In some cases you may want to separate the BigQuery compute consumption from
            BigQuery data storage. You can set `BQ_DATA_PROJECT_ID` to the project you use
            for data storage, and `BQ_COMPUTE_PROJECT_ID` to the project you want
            to use for compute.
        *   Otherwise, you can set both `BQ_DATA_PROJECT_ID` and
            `BQ_COMPUTE_PROJECT_ID` to the same project id.

        If you have an existing BigQuery table you wish to
        connect, specify the `BQ_DATASET_ID` in the `.env` file as well.
        Make sure you leave `BQ_DATASET_ID='house_prices'` if you
        wish to use the sample data.

        Alternatively, you can set the variables from your terminal:

        ```bash
        export BQ_DATA_PROJECT_ID='YOUR-BQ-DATA-PROJECT-ID'
        export BQ_COMPUTE_PROJECT_ID='YOUR-BQ-COMPUTE-PROJECT-ID'
        export BQ_DATASET_ID='YOUR-DATASET-ID' # leave as 'house_prices' if using sample data
        ```

        You can skip the upload steps if you are using your own data. We recommend not adding any production critical datasets to this sample agent.
        If you wish to use the sample data, continue with the next step.

    *   You will find the datasets inside 'data-science/data_science/utils/data/'.
        Make sure you are still in the working directory (`agents/data-science`). To load the test and train tables into BigQuery, run the following commands:
        ```bash
        python3 data_science/utils/create_bq_table.py
        ```


6.  **BQML Setup:**
    The BQML Agent uses the Vertex AI RAG Engine to query the full BigQuery ML Reference Guide.

    Before running the setup, ensure your project ID is added in .env file: `"GOOGLE_CLOUD_PROJECT"`.
    Leave the corpus name empty in the .env file: `BQML_RAG_CORPUS_NAME = ''`. The corpus name will be added automatically once it's created.

    To set up the RAG Corpus for your project, run the methods `create_RAG_corpus()` and `ingest_files()` in
    `data-science/data_science/utils/reference_guide_RAG.py` by running the below command from the working directory:

    ```bash
    python3 data_science/utils/reference_guide_RAG.py
    ```


7.  **Other Environment Variables:**

    *   `NL2SQL_METHOD`: (Optional) Either `BASELINE` or `CHASE`. Sets the method for SQL Generation. Baseline uses Gemini off-the-shelf, whereas CHASE uses [CHASE-SQL](https://arxiv.org/abs/2410.01943)
    *   `CODE_INTERPRETER_EXTENSION_NAME`: (Optional) The full resource name of
        a pre-existing Code Interpreter extension in Vertex AI. If not provided,
        a new extension will be created. (e.g.,
        `projects/<YOUR_PROJECT_ID>/locations/<YOUR_LOCATION>/extensions/<YOUR_EXTENSION_ID>`).
        Check the logs/terminal for the ID of the newly created Code Interpreter
        Extension and provide the value in your environment variables to avoid
        creating multiple extensions.

    From the terminal:

    ```bash
    export CODE_INTERPRETER_EXTENSION_NAME='projects/<YOUR_PROJECT_ID>/locations/us-central1/extensions/<YOUR_EXTENSION_ID>'
    ```

## Running the Agent

You can run the agent using the ADK command in your terminal.
from the working directory:

1.  Run agent in CLI:

    ```bash
    uv run adk run data_science
    ```

2.  Run agent with ADK Web UI:
    ```bash
    uv run adk web
    ```
    Select the data_science from the dropdown



### Example Agent Interaction

Here's a quick example of how a user might interact with the Data Science Multi-Agent System:

> **User:** Hi, What data do you have access to?

> **Agent:**  I have access to two tables: `train` and `test`. Both tables contain house price data with the following columns: `Id`, `MSSubClass`, `MSZoning`, `LotFrontage`, `LotArea`, `Street`, `Alley`, `LotShape`, `LandContour`, `Utilities`, `LotConfig`, `LandSlope`, `Neighborhood`, `Condition1`, `Condition2`, `BldgType`, `HouseStyle`, `OverallQual`, `OverallCond`, `YearBuilt`, `YearRemodAdd`, `RoofStyle`, `RoofMatl`, `Exterior1st`, `Exterior2nd`, `MasVnrType`, `MasVnrArea`, `ExterQual`, `ExterCond`, `Foundation`, `BsmtQual`, `BsmtCond`, `BsmtExposure`, `BsmtFinType1`, `BsmtFinSF1`, `BsmtFinType2`, `BsmtFinSF2`, `BsmtUnfSF`, `TotalBsmtSF`, `Heating`, `HeatingQC`, `CentralAir`, `Electrical`, `1stFlrSF`, `2ndFlrSF`, `LowQualFinSF`, `GrLivArea`, `BsmtFullBath`, `BsmtHalfBath`, `FullBath`, `HalfBath`, `BedroomAbvGr`, `KitchenAbvGr`, `KitchenQual`, `TotRmsAbvGrd`, `Functional`, `Fireplaces`, `FireplaceQu`, `GarageType`, `GarageYrBlt`, `GarageFinish`, `GarageCars`, `GarageArea`, `GarageQual`, `GarageCond`, `PavedDrive`, `WoodDeckSF`, `OpenPorchSF`, `EnclosedPorch`, `3SsnPorch`, `ScreenPorch`, `PoolArea`, `PoolQC`, `Fence`, `MiscFeature`, `MiscVal`, `MoSold`, `YrSold`, `SaleType`, `SaleCondition`, and `SalePrice` (target variable in train table only).

> **User:** I need more details on the train table. What neighborhoods exist? How many houses are there?

> **Agent:** Result: The train table contains data from various neighborhoods including North Ames, College Creek, Old Town, Edwards, Somerset, Northridge Heights, Gilbert, Sawyer, Northwest Ames, Sawyer West, Meadow Village, Briardale, Brookside, Crawford, Iowa DOT and Rail Road, Timberland, Northridge, Stone Brook, South and West of Iowa State University, Clear Creek, Bloomington Heights, Veenker, Northpark Villa, Blueste, and Mitchell. There are 1460 houses in the training dataset.

>Explanation: The database agent executed a SQL query against the train table to find the distinct neighborhoods and count the total number of houses. The query grouped the results by neighborhood and counted the distinct house IDs.

> **User:** Please generate a plot with average house prices by neighborhood.

> **Agent:**  Result: A bar plot has been generated showing the average house prices by neighborhood. The x-axis represents the neighborhood, and the y-axis represents the average sale price.

> Explanation:
> 1. The database agent was first called to retrieve the average sale prices by neighborhood from the train table.
> 2. The data science agent was then called to generate a bar plot visualizing the results. The plot displays each neighborhood on the x-axis and its corresponding average sale price on the y-axis.

> **User:** What kinds of machine learning models can I train in BQML?

> **Agent:** You can train several types of machine learning models in BQML, including Linear Regression, Logistic Regression, K-means Clustering, and Neural Networks. For house price prediction, I recommend starting with Linear Regression. Would you like to proceed with training a model?

> **User:** Yes

> **Agent:** Okay, before proceeding, let's confirm the project and dataset ID for BQML. We'll be using the `PROJECT_ID` project and the `house_prices` dataset. Does that sound right?

> **User:** Yes

> **Agent:** For house price prediction, BQML supports several model types including `linear_reg`, `logistic_reg`, and `dnn_regressor`.

>To proceed, I need to know which model you'd like to use. I also need to know the following:

>*   The name of the target column (e.g., 'SalePrice').
>*   Which features you'd like to use for prediction (e.g., 'GrLivArea', 'OverallQual', 'YearBuilt').
>*   Do you want to use all available features or select specific ones?


## Testing and Evaluation

To run the test and evaluation code, you need a few additional dependencies. Run
the following uv command from the `agents/data-science` directory to install them:
```bash
uv sync
```

### Running Evaluations


Evaluation tests assess the overall performance and capabilities of the agent in a holistic manner.

**Run Evaluation Tests:**

```bash
uv run pytest eval
```


- This command executes all test files within the `eval/` directory.
- `uv run` ensures that pytest runs within the project's virtual environment.



### Running Tests

Tests assess the overall executability of the agents.

**Test Categories:**

*   **Integration Tests:** These tests verify that the agents can interact correctly with each other and with external services like BigQuery. They ensure that the root agent can delegate tasks to the appropriate sub-agents and that the sub-agents can perform their intended tasks.
*   **Sub-Agent Functionality Tests:** These tests focus on the specific capabilities of each sub-agent (e.g., Database Agent, BQML Agent). They ensure that each sub-agent can perform its intended tasks, such as executing SQL queries or training BQML models.
*   **Environment Query Tests:** These tests verify that the agent can handle queries that are based on the environment.

**Run Tests:**

```bash
uv run pytest tests
```

- This command executes all test files within the `tests/` directory.
- `uv run` ensures that pytest runs within the project's virtual environment.



## Deployment on Vertex AI Agent Engine

To deploy the agent to Google Agent Engine, first follow
[these steps](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/set-up)
to set up your Google Cloud project for Agent Engine.

You also need to give BigQuery User, BigQuery Data Viewer, and Vertex AI User
permissions to the Reasoning Engine Service Agent. Run the following commands to
grant the required permissions:

```bash
export RE_SA="service-${GOOGLE_CLOUD_PROJECT_NUMBER}@gcp-sa-aiplatform-re.iam.gserviceaccount.com"
gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
    --member="serviceAccount:${RE_SA}" \
    --condition=None \
    --role="roles/bigquery.user"
gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
    --member="serviceAccount:${RE_SA}" \
    --condition=None \
    --role="roles/bigquery.dataViewer"
gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
    --member="serviceAccount:${RE_SA}" \
    --condition=None \
    --role="roles/aiplatform.user"
```

Next, you need to create a `.whl` file for your agent. From the `data-science`
directory, run this command:

```bash
uv build --wheel --out-dir deployment
```

This will create a file named `data_science-0.1.0-py3-none-any.whl` in the
`deployment` directory.

Then run the below command. This will create a staging bucket in your GCP project and deploy the agent to Vertex AI Agent Engine:

```bash
cd deployment/
python3 deploy.py --create
```

When this command returns, if it succeeds it will print an AgentEngine resource
name that looks something like this:
```
projects/************/locations/europe-west4/reasoningEngines/7737333693403889664
```
The last sequence of digits is the AgentEngine resource ID.

Once you have successfully deployed your agent, you can interact with it
using the `test_deployment.py` script in the `deployment` directory. Store the
agent's resource ID in an environment variable and run the following command:

```bash
export RESOURCE_ID=...
export USER_ID=<any string>
python test_deployment.py --resource_id=$RESOURCE_ID --user_id=$USER_ID
```

The session will look something like this:
```
Found agent with resource ID: ...
Created session for user ID: ...
Type 'quit' to exit.
Input: Hello. What data do you have?
Response: I have access to the train and test tables inside the  dataset.
...
```

Note that this is *not* a full-featured, production-ready CLI; it is just intended to
show how to use the Agent Engine API to interact with a deployed agent.

The main part of the `test_deployment.py` script is approximately this code:

```python
from vertexai import agent_engines
remote_agent = vertexai.agent_engines.get(RESOURCE_ID)
session = remote_agent.create_session(user_id=USER_ID)
while True:
    user_input = input("Input: ")
    if user_input == "quit":
      break

    for event in remote_agent.stream_query(
        user_id=USER_ID,
        session_id=session["id"],
        message=user_input,
    ):
        parts = event["content"]["parts"]
        for part in parts:
            if "text" in part:
                text_part = part["text"]
                print(f"Response: {text_part}")
```

To delete the agent, run the following command (using the resource ID returned previously):
```bash
python3 deployment/deploy.py --delete --resource_id=RESOURCE_ID
```



## Optimizing and Adjustment Tips

*   **Prompt Engineering:** Refine the prompts for `root_agent`, `bqml_agent`, `db_agent`
    and `ds_agent` to improve accuracy and guide the agents more effectively.
    Experiment with different phrasing and levels of detail.
*   **Extension:** Extend the multi-agent system with your own AgentTools or sub_agents.
    You can do so by adding additional tools and sub_agents to the root agent inside
    `agents/data-science/data_science/agent.py`.
*   **Partial imports:** If you only need certain capabilities inside the multi-agent system,
    e.g. just the data agent, you can import the data_agent as an AgentTool into your own root agent.
*   **Model Selection:** Try different language models for both the top-level
    agent and the sub-agents to find the best performance for your data and
    queries.


## Troubleshooting

*   If you face `500 Internal Server Errors` when running the agent, simply re-run your last command.
    That should fix the issue.
*   If you encounter issues with the code interpreter, review the logs to
    understand the errors. Make sure you're using base-64 encoding for
    files/images if interacting directly with a code interpreter extension
    instead of through the agent's helper functions.
*   If you see errors in the SQL generated, try the following:
    - including clear descriptions in your tables and columns help boost performance
    - if your database is large, try setting up a RAG pipeline for schema linking by storing your table schema details in a vector store

## Deployment on Google Cloud Run

These instructions walk through the process of deploying the Data Science agent to Google Cloud Run, including Cloud SQL for session storage.

### Before you begin

Deploying to Google Cloud Run requires:

- A [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) with billing enabled.
- `gcloud` CLI ([Installation instructions](https://cloud.google.com/sdk/docs/install))

### 1 - Authenticate the Google Cloud CLI, and enable Google Cloud APIs.

```
gcloud auth login
gcloud auth application-default login 

export PROJECT_ID="<YOUR_PROJECT_ID>"
gcloud config set project $PROJECT_ID

gcloud services enable sqladmin.googleapis.com \
   compute.googleapis.com \
   cloudresourcemanager.googleapis.com \
   servicenetworking.googleapis.com \
   aiplatform.googleapis.com
```

### 2 - Create a Cloud SQL instance for the agent sessions service.

```bash
gcloud sql instances create ds-agent-session-service \
   --database-version=POSTGRES_17 \
   --tier=db-g1-small \
   --region=europe-west4 \
   --edition=ENTERPRISE \
   --root-password=ds-agent-demo
```

Once created, you can view your instance in the Cloud Console [here](https://console.cloud.google.com/sql/instances/ds-agent-session-service/overview).

### 3 - Deploy the agent to Cloud Run
Now we are ready to deploy the Data Science agent to Cloud Run! :rocket:

```bash
gcloud run deploy data-science-agent \
  --source . \
  --port 8080 \
  --memory 2G \
  --project $PROJECT_ID \
  --allow-unauthenticated \
  --add-cloudsql-instances $PROJECT_ID:europe-west4:ds-agent-session-service \
  --update-env-vars SERVE_WEB_INTERFACE=True,SESSION_SERVICE_URI="postgresql+pg8000://postgres:ds-agent-demo@postgres/?unix_sock=/cloudsql/$PROJECT_ID:europe-west4:ds-agent-session-service/.s.PGSQL.5432",GOOGLE_CLOUD_PROJECT=$PROJECT_ID \
  --region europe-west4 
```

When this runs successfully, you should see:

```bash
Service [data-science-agent] revision [data-science-agent-00001-aaa] has been deployed and is serving 100 percent of traffic.
```

### 4 - Test the Cloud Run Deployment

Open the Cloud Run Service URL outputted by the previous step.
You should see the ADK Web UI for the Data Science Agent.

### Clean up

You can clean up this agent sample by:
- Deleting the [Cloud Run Services](https://console.cloud.google.com/run).
- Deleting the [Cloud SQL instance](https://console.cloud.google.com/sql/instances).


## Improvements Over Original Sample

This modified version addresses several issues identified in the original Google ADK sample:

### Configuration Management
- **Centralized environment variable handling** with proper validation
- **Clear error messages** for missing required variables
- **Type-safe configuration** with better defaults

### Error Handling
- **Custom exception classes** for different error types
- **Proper exception propagation** instead of returning error strings
- **Better debugging information** with structured logging

### Code Quality
- **Improved type hints** throughout the codebase
- **Better code organization** and separation of concerns
- **Enhanced documentation** and inline comments

### Testing & Reliability
- **Better error handling** in critical functions
- **Improved validation** of inputs and configurations
- **More robust deployment** process

## Disclaimer

This agent sample is based on the [Google ADK Samples](https://github.com/google/adk-samples/tree/main/python/agents/data-science) and is provided for illustrative purposes only. While this modified version includes improvements over the original sample, it is not intended for production use without further testing and security hardening.

The original Google ADK sample has not been rigorously tested, may contain bugs or limitations, and does not include features or optimizations typically required for a production environment (e.g., robust error handling, security measures, scalability, performance considerations, comprehensive logging, or advanced configuration options).

Users are solely responsible for any further development, testing, security hardening, and deployment of agents based on this sample. We recommend thorough review, testing, and the implementation of appropriate safeguards before using any derived agent in a live or critical system.
