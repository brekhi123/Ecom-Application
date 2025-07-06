# Ecommerce Application 

This repository contains the code for a full-featured e-commerce application, designed to provide a seamless shopping experience.

-----

## Getting Started 

Follow these steps to set up and run the application locally:

1.  **Clone/Pull/Download** this repository to your local machine.
2.  **Create a virtual environment** using `virtualenv env` and install all necessary dependencies with `pip install -r requirements.txt`.
3.  **Configure your environment variables** by setting up your `.env` file. This includes sensitive information and API keys for services like payment gateways.
4.  **Rename your project** to a custom name using the Django command: `python manage.py rename <yourprojectname> <newprojectname>`.

-----

### Key Features 

This e-commerce project comes packed with robust functionalities:

1.  **Product Catalog & Browse:** Explore products categorized into "All," "Shirts," "Sportswear," and "Outwears."
2.  **Shopping Cart Management:** Easily add items to your cart, view selected products, and manage quantities.
3.  **Secure Checkout Process:** A multi-step checkout flow ensures a smooth and secure transaction, including:
      * **Shipping Address Input:** Collects detailed shipping information.
      * **Multiple Payment Gateways:** Supports popular payment methods like **Stripe** and **PayPal** for flexible and secure transactions.
4.  **Order Confirmation:** Provides immediate confirmation upon successful order placement.
5.  **Refund Request System:** Includes a dedicated system for handling customer refund requests.
6.  **User Authentication:** Features robust login and logout functionalities for user management.
7.  **Deployment Ready:** Includes settings modules specifically configured for easy deployment with **Azure**.
8.  **Developer Utilities:** Comes with convenient Django commands for renaming your project and creating a superuser, along with a CLI tool for setting environment variables for deployment.

-----
