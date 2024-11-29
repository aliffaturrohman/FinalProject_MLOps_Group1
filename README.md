# Final Project MLOps Group 1  
This project is part of the PSO course with the topic of MLOps. This project is developed by:  
- **Alif Faturrohman**  
- **Annisa Fadila Rahmawati**  
- **Anisa Fatin Idelia**  

## Introduction  
This application uses **Next.js** for the frontend and **Flask** for the backend to implement a machine learning model. The following guide explains the steps to run the application locally.  

## Setup  
### 1. Clone the Repository  
Clone this repository to your desired directory on your computer by running the following command:  
```bash  
git clone https://github.com/aliffaturrohman/FinalProject_MLOps_Group1.git  
```  

### 2. Project Structure  
The project structure includes:  
- **Frontend**: The `mlops-fp` folder uses Next.js.  
- **Backend**: The backend file is a Flask application located at `backend/app.py`.  
- **Dependencies**: There is a `requirements.txt` file for Flask and other dependencies.  

## Installation  

### A. Installing Frontend (Next.js)  
Follow the steps below to install Next.js:  

1. **Install Node.js and npm**  
   Ensure that Node.js and npm are installed. If not, download and install them from the [Node.js Official Website](https://nodejs.org/).  

2. **Navigate to the frontend directory**  
   Change to the frontend folder:  
   ```bash  
   cd mlops-fp  
   ```  

3. **Install dependencies**  
   Run the following command to install all required dependencies for Next.js:  
   ```bash  
   npm install  
   ```  

4. **Run Next.js**  
   After the installation is complete, start the Next.js application with:  
   ```bash  
   npm run dev  
   ```  

5. **Access the application**  
   Open your browser and go to [http://localhost:3000/](http://localhost:3000/) to view the frontend application.  

---

### B. Installing Backend (Flask)  
Follow these steps to set up the Flask backend:  

1. **Create a Virtual Environment**  
   In the root project folder, create a virtual environment by running:  
   ```bash  
   python -m venv .env  
   ```  

2. **Activate the Virtual Environment**  
   Activate the virtual environment:  
   - **Windows**:  
     ```bash  
     .env\Scripts\activate  
     ```  
   - **Mac/Linux**:  
     ```bash  
     source .env/bin/activate  
     ```  

3. **Install Dependencies**  
   Install all the necessary dependencies for Flask by running:  
   ```bash  
   pip install -r requirements/requirements.txt  
   ```  

4. **Run the Flask Server**  
   Run the Flask backend server by executing:  
   ```bash  
   python backend/app.py  
   ```  
   The Flask backend will run on [http://localhost:5000/](http://localhost:5000/).  

---

## Running the Application  
After both the backend and frontend are successfully set up, follow these steps:  

1. **Run the Backend**  
   Ensure the Flask server is running by executing:  
   ```bash  
   python backend/app.py  
   ```  

2. **Run the Frontend**  
   Open a new terminal, navigate to the frontend folder, and run:  
   ```bash  
   cd mlops-fp  
   npm run dev  
   ```  

3. **Access the Application**  
   Open your browser and go to [http://localhost:3000/](http://localhost:3000/).  

## Notes  
- Ensure that all dependencies are installed before running the application.  
- If errors occur, make sure that Node.js, npm, Python, and all dependencies are correctly installed.  

---  
By following these steps, the application will run as expected. Best of luck! 🚀  
