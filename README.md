# Sales Team Performance Analysis Using LLM

This project involves analyzing sales data for team performance using an open-source model (Flan-T5 in this case) to provide feedback on individual and team performance. The FastAPI app provides API endpoints for performance analysis and forecasting.

## Overview

The system is designed to:

- Provide insights on individual sales representatives' performance.
- Analyze overall team performance.
- Offer sales trends and performance forecasts for monthly or quarterly data.

It uses **FastAPI** for the backend API, **Pandas** for data processing, and **Hugging Face's open-source models** for generating insights.

## Architecture

The system consists of the following components:

- **FastAPI**: A web framework to create API endpoints for querying sales performance.
- **Pandas**: For loading and processing the sales data from the CSV file.
- **Transformers**: Hugging Face's pipeline to load pre-trained models like Flan-T5 to generate insights based on data.
- **CSV**: The sales data is stored in a CSV file with columns like `rep_id`, `sales_amount`, and other performance metrics for each representative.

## Technologies Used

- **FastAPI**: For building the RESTful API.
- **Pandas**: For data handling and analysis.
- **Transformers (Hugging Face)**: For leveraging pre-trained models to generate performance insights.
- **Python 3.x**: Programming language used for the implementation.

## Setup Instructions

Follow these steps to set up and run the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/JM-JamalMustafa/Analysis-Using-LLM.git
cd Analysis-Using-LLM
