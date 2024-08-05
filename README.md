User Registration and Medical Requisition System

Project Overview

This project aims to streamline user registration and medical requisition processing using optical character recognition (OCR) technology. The system allows users to register by uploading official documents, which are then processed to extract relevant information such as name, birth date, and CPF (Brazilian individual taxpayer registry). After registration, users can submit medical requisitions, and the system will automatically extract and display the relevant exam information in a user report.

Key Features

Document Upload and OCR Extraction: Users can upload documents (PDFs or images), and the system uses EasyOCR to extract text. Key information such as name, birth date, and CPF is extracted and stored.
Medical Requisition Submission: After registration, users can submit medical requisitions and associated images. The system processes and saves this information for further use.
User Report Generation: A detailed report is generated for each user, showcasing the extracted information and any submitted exams.
Technologies Used

Python: The primary programming language used for the project.
EasyOCR: For optical character recognition to extract text from documents.
OpenCV: For image preprocessing and manipulation.
Matplotlib: For visualizing data and generating plots.
NumPy: For numerical operations and image processing.
Django: The web framework used to build the application.
