# AlgoGPT - CP/DSA Question Solver 
### Team Name: ML 35
Welcome to the CP/DSA Question Solver project, part of the IITI Summer of Code initiative! This repository contains the code and resources for building an automated solver for competitive programming and data structures & algorithms (CP/DSA) questions from various platforms.

## Overview

This project aims to create an automated solver for CP/DSA questions using state-of-the-art deep learning techniques. The solver is divided into three main workflows, each tailored to different platforms: Leetcode, Codeforces, and others.

### Common Workflow

1. **Question Simplification:**
   - **Tool Used:** Phi-3
   - Simplifies complex questions to make them more manageable for the model.

2. **Retrieval-Augmented Generation (RAG):**
   - **Retrieval:** Uses SentenceTransformer MiniLM and FAISS to retrieve relevant information.
   - **Model:** Specific models are used depending on the platform (detailed below).

3. **Fine-Tuning LLM:**
   - **Dataset:** Consists of 'prompt','accepted','rejected' columns for ORPO fine-tuning , made using base LLM and pandas.
   - **Method:** Reinforcement Learning based ORPO fine tuning, straying away from 'rejected' answers and running parallel to 'accepted' answers.
     
4. **Scraping Questions:**
   - **Tools Used:** BeautifulSoup and GitHub API
   - Collects questions from the respective platforms for training and testing the models.

5. **Deployment:**
   - **Tool Used:** Streamlit
   - Provides a user-friendly interface to interact with the question solver.

## Platform-Specific Workflows

### 1. Leetcode Workflow

For solving Leetcode questions:
- **Model:** Implements a RAG approach tailored for Leetcode questions.
- **Deployment:** Streamlit is used to deploy the Leetcode question solver.

### 2. Codeforces Workflow

For solving Codeforces questions:
- **Model:** Uses a DeepSeek-Coder-6.7B-base model, fine-tuned with RL-based ORPO techniques.
- **Deployment:** Streamlit is used to deploy the Codeforces question solver.

### 3. New Questions Workflow

For solving questions from other CP/DSA platforms:
- **Model:** Integrates RAG with DeepSeek-V2-Lite-Instruct (16B version) for a versatile solution.
- **Deployment:** Streamlit is used to deploy the solver for other platforms.

## Technologies Used

- **Deep Learning Models:**
  - DeepSeek-Coder-6.7B-base
  - DeepSeek-V2-Lite-Instruct (16B version)
  - Phi-3 for question simplification

- **Libraries and Tools:**
  - **RAG Implementation:** SentenceTransformer MiniLM, FAISS
  - **Scraping:** BeautifulSoup, GitHub API
  - **Deployment:** Streamlit
 
## Interface:
![image](https://github.com/user-attachments/assets/988b14be-07dd-49e0-a2f9-3361241862f5)

## Team Members:
- [Chanakya Cherukumalli](https://github.com/Chanakya2456)
- [Varad Pendse](https://github.com/)
- [Rishabh Anand](https://github.com/)
- [Kushagra Mishra](https://github.com/)
