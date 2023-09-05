
Baby Monitoring System
Introduction
The Baby Monitoring System is a comprehensive project dedicated to ensuring the safety and well-being of infants in nursery environments. It combines advanced hardware and software components to continuously monitor infants and provide caregivers with timely notifications in critical situations. This README offers an overview of the project, its key features, setup instructions, and the technologies used.
Features
Face Recognition
Our system employs state-of-the-art face recognition algorithms to identify and track the positions of infants within the nursery, providing caregivers with real-time insights into their well-being.
Movement Detection
In addition to face recognition, our system now includes a movement detection feature. It can detect if an infant is not moving within a specified time frame and promptly notifies caregivers in such cases, ensuring their safety.
Danger Detection
Utilizing advanced image processing techniques, the system can identify potentially hazardous situations, such as the absence of recognized faces in an infant's crib, further enhancing safety measures.
Automated Notifications
Caregivers receive automated notifications via the Telegram messaging platform in the event of potential risks, including the absence of movement or unrecognized faces, enabling them to take immediate action.
Nursery Management
Our system supports the management of multiple nurseries, the addition of contacts, and the ability to enable or disable notifications for specific nurseries, providing flexibility and customization.
Embedded Development
This project also serves as a showcase for embedded development, as it efficiently implements the baby monitoring system on a Linux Virtual Machine (VM) with limited resources.
Technologies Used
Our system leverages the following technologies:
* Python
* OpenCV for advanced image processing
* Telegram Bot API for real-time notifications and user interaction
* Firebase for data storage, nursery, and user management
* YuNet for precise face detection
* Flask for the web application component
Project Components
The project comprises several essential components:
Face Detection and Recognition
We utilize the YuNet model and OpenCV to recognize and track infants' faces within the nursery, ensuring their safety and providing caregivers with peace of mind.
Image Processing
Our system employs advanced image processing techniques to identify potential dangers, such as the absence of recognized faces or lack of infant movement, adding an extra layer of security.
Telegram Bot
We integrate a Telegram Bot for real-time notifications and interaction with caregivers, ensuring prompt communication and action.
Firebase Database
Our system stores nursery and user data, manages contacts, and tracks notification preferences, providing a centralized and secure data management solution.
Web Application
We implement a user-friendly Flask-based web application to handle incoming messages, manage user interactions, and facilitate seamless notifications.
Embedded Development
Our project showcases embedded development by efficiently implementing the baby monitoring system on a resource-constrained Linux VM.

